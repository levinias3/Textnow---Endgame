"""
Module theo dõi bàn phím và xử lý shortcuts - Phiên bản tối ưu tốc độ
"""
import keyboard
import threading
import time
from typing import Set, Callable, Dict
from core.shortcut_manager import ShortcutManager

class KeyboardMonitor:
    def __init__(self, shortcut_manager: ShortcutManager):
        self.shortcut_manager = shortcut_manager
        self.is_monitoring = False
        self.monitor_thread = None
        self.typed_buffer = ""
        self.last_key_time = 0
        self.buffer_timeout = 2.0  # Reset buffer sau 2 giây không gõ
        self.auto_trigger_delay = 0.1  # Delay tối thiểu cho tốc độ tối đa
        self.instant_trigger = False  # Tùy chọn trigger ngay lập tức
        self.on_status_changed = None  # Callback khi trạng thái thay đổi
        self.pending_trigger_timer = None  # Timer cho auto trigger
        self.last_triggered_keyword = ""  # Tránh trigger liên tục
        self._keyword_cache = {}  # Cache để tăng tốc kiểm tra
        self._update_keyword_cache()
        
    def set_on_status_changed(self, callback: Callable):
        """Đặt callback khi trạng thái monitoring thay đổi"""
        self.on_status_changed = callback
    
    def _update_keyword_cache(self):
        """Cập nhật cache keywords để tăng tốc"""
        self._keyword_cache = {}
        keywords = self.shortcut_manager.get_all_keywords()
        # Tạo dictionary theo độ dài keyword để tìm kiếm nhanh hơn
        for keyword in keywords:
            length = len(keyword)
            if length not in self._keyword_cache:
                self._keyword_cache[length] = []
            self._keyword_cache[length].append(keyword)
        
        # Sắp xếp theo độ dài giảm dần trong mỗi nhóm
        for length in self._keyword_cache:
            self._keyword_cache[length].sort(key=len, reverse=True)
    
    def start_monitoring(self):
        """Bắt đầu theo dõi bàn phím"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.typed_buffer = ""
        self._update_keyword_cache()  # Cập nhật cache khi bắt đầu
        
        # Hook keyboard events
        keyboard.on_press(self._on_key_press)
        
        # Notify status changed
        if self.on_status_changed:
            self.on_status_changed(True)
        
        print("Đã bắt đầu theo dõi bàn phím (Chế độ tốc độ cao)")
    
    def stop_monitoring(self):
        """Dừng theo dõi bàn phím"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        
        # Cancel pending timer
        if self.pending_trigger_timer:
            self.pending_trigger_timer.cancel()
            self.pending_trigger_timer = None
        
        # Unhook keyboard events
        keyboard.unhook_all()
        
        # Notify status changed
        if self.on_status_changed:
            self.on_status_changed(False)
        
        print("Đã dừng theo dõi bàn phím")
    
    def _cancel_pending_trigger(self):
        """Hủy trigger đang chờ"""
        if self.pending_trigger_timer:
            self.pending_trigger_timer.cancel()
            self.pending_trigger_timer = None
    
    def _schedule_auto_trigger(self, keyword: str):
        """Lên lịch auto trigger với delay tối ưu và kiểm tra chính xác"""
        self._cancel_pending_trigger()
        
        # Kiểm tra lại để đảm bảo keyword vẫn đúng
        if not self.typed_buffer.endswith(keyword):
            print(f"⚠️ Keyword '{keyword}' không còn ở cuối buffer '{self.typed_buffer}', bỏ qua")
            return
        
        # Tránh trigger cùng keyword liên tục
        if keyword == self.last_triggered_keyword:
            print(f"⚠️ Keyword '{keyword}' đã được trigger, bỏ qua để tránh lặp")
            return
        
        # Nếu instant trigger được bật, trigger ngay lập tức
        if self.instant_trigger or self.auto_trigger_delay <= 0.05:
            print(f"⚡ Instant trigger cho '{keyword}'")
            self._trigger_shortcut_immediate(keyword)
            return
        
        def auto_trigger():
            if (self.is_monitoring and 
                self.typed_buffer.endswith(keyword) and 
                keyword != self.last_triggered_keyword):
                
                print(f"⏰ Auto trigger cho '{keyword}' sau delay {self.auto_trigger_delay}s")
                self._trigger_shortcut_immediate(keyword)
        
        print(f"⏲️ Lên lịch trigger '{keyword}' sau {self.auto_trigger_delay}s")
        self.pending_trigger_timer = threading.Timer(self.auto_trigger_delay, auto_trigger)
        self.pending_trigger_timer.start()
    
    def _trigger_shortcut_immediate(self, keyword: str):
        """Trigger shortcut ngay lập tức với tốc độ tối ưu và xóa đúng keyword"""
        try:
            print(f"🚀 Bắt đầu trigger shortcut '{keyword}' (độ dài: {len(keyword)} ký tự)")
            print(f"📝 Buffer hiện tại: '{self.typed_buffer}'")
            
            # Kiểm tra xem keyword có thực sự ở cuối buffer không
            if not self.typed_buffer.endswith(keyword):
                print(f"❌ Keyword '{keyword}' không ở cuối buffer '{self.typed_buffer}', bỏ qua trigger")
                return
            
            # Đánh dấu đã trigger để tránh lặp lại
            self.last_triggered_keyword = keyword
            original_buffer = self.typed_buffer
            self.typed_buffer = ""
            
            print(f"🧹 Đã reset buffer và đánh dấu keyword: '{keyword}'")
            
            # BƯỚC 1: Xóa keyword đã gõ trước tiên - XÓA ĐÚNG SỐ KÝ TỰ CỦA KEYWORD
            keyword_length = len(keyword)
            print(f"🔙 BƯỚC 1: Xóa keyword '{keyword}' ({keyword_length} ký tự)")
            self._fast_backspace(keyword_length)
            
            # Thêm delay nhỏ để đảm bảo backspace hoàn tất
            time.sleep(0.015)  # Tăng từ 10ms lên 15ms để đảm bảo ổn định
            
            # BƯỚC 2: Xử lý shortcut (copy vào clipboard)
            print(f"📋 BƯỚC 2: Xử lý shortcut '{keyword}'")
            success = self.shortcut_manager.process_shortcut(keyword)
            
            if success:
                # BƯỚC 3: Đợi một chút để đảm bảo clipboard đã sẵn sàng
                print(f"⏱️ BƯỚC 3: Đợi clipboard sẵn sàng")
                if self.instant_trigger or self.auto_trigger_delay <= 0.05:
                    time.sleep(0.015)  # Tăng từ 10ms lên 15ms cho instant mode
                else:
                    time.sleep(0.020)  # Tăng từ 15ms lên 20ms cho chế độ khác
                
                # BƯỚC 4: Paste nội dung từ clipboard
                print(f"📥 BƯỚC 4: Paste nội dung")
                keyboard.send('ctrl+v')
                
                # Delay cuối để đảm bảo paste hoàn tất
                time.sleep(0.005)  # Tăng từ 3ms lên 5ms
                
                # BƯỚC 5: Xử lý mixed content nếu có ảnh còn lại
                if hasattr(self.shortcut_manager, 'pending_images') and self.shortcut_manager.pending_images:
                    print(f"📷 BƯỚC 5: Xử lý {len(self.shortcut_manager.pending_images)} ảnh còn lại")
                    
                    # Lấy shortcut info để xác định logic
                    shortcut = self.shortcut_manager.get_shortcut(keyword)
                    if shortcut and shortcut.get('type') == 'mixed':
                        content = shortcut.get('content', {})
                        if isinstance(content, dict):
                            text_content = content.get('text', '')
                            images = self.shortcut_manager.pending_images
                            
                            if text_content:
                                # Có text: xử lý tất cả ảnh (từ ảnh 1)
                                print(f"📝➡️🖼️ Text đã paste, xử lý {len(images)} ảnh...")
                                self.shortcut_manager.process_remaining_images(images, 0)
                            else:
                                # Không có text: ảnh đầu tiên đã paste, xử lý từ ảnh 2
                                if len(images) > 1:
                                    print(f"🖼️➡️🖼️ Ảnh 1 đã paste, xử lý {len(images)-1} ảnh còn lại...")
                                    self.shortcut_manager.process_remaining_images(images, 1)
                                else:
                                    print(f"✅ Chỉ có 1 ảnh, đã hoàn thành")
                    
                    # Clear pending images
                    self.shortcut_manager.pending_images = []
                
                print(f"✅ Đã trigger shortcut '{keyword}' thành công")
            else:
                print(f"❌ Lỗi khi xử lý shortcut '{keyword}' - không thể copy vào clipboard")
                
        except Exception as e:
            print(f"❌ Exception trong trigger shortcut '{keyword}': {e}")
            # Reset state nếu có lỗi
            self.typed_buffer = ""
            self.last_triggered_keyword = ""
    
    def _fast_backspace(self, count: int):
        """Thực hiện backspace chính xác và đáng tin cậy"""
        try:
            if count <= 0:
                return
            
            print(f"🔙 Đang xóa {count} ký tự...")
            
            # Sử dụng phương pháp backspace tuần tự cho tất cả trường hợp để đảm bảo chính xác
            # Đây là phương pháp đáng tin cậy nhất cho mọi loại shortcut
            for i in range(count):
                keyboard.send('backspace')
                # Delay nhỏ giữa các backspace để đảm bảo ổn định
                if i < count - 1:  # Không delay cho backspace cuối cùng
                    time.sleep(0.003)  # 3ms delay để đảm bảo từng ký tự được xóa hoàn toàn
            
            print(f"✅ Đã xóa {count} ký tự bằng backspace tuần tự")
                        
        except Exception as e:
            print(f"❌ Lỗi trong _fast_backspace: {e}")
            # Emergency fallback: thử lại với delay lớn hơn
            print(f"🆘 Emergency fallback: xóa {count} ký tự với delay lớn")
            try:
                for i in range(count):
                    keyboard.send('backspace')
                    time.sleep(0.010)  # Delay lớn hơn cho emergency
                print(f"✅ Emergency fallback thành công")
            except Exception as final_error:
                print(f"💥 Emergency fallback cũng thất bại: {final_error}")
    
    def _on_key_press(self, event):
        """Xử lý sự kiện phím bấm với tốc độ tối ưu - Hỗ trợ mọi định dạng shortcut"""
        if not self.is_monitoring:
            return
        
        current_time = time.time()
        
        # Reset buffer nếu quá lâu không gõ
        if current_time - self.last_key_time > self.buffer_timeout:
            self.typed_buffer = ""
            self.last_triggered_keyword = ""
        
        self.last_key_time = current_time
        
        # Debug: In ra tên phím để hiểu cách xử lý
        # print(f"Key pressed: '{event.name}' (length: {len(event.name)})")
        
        # Xử lý phím với logic tối ưu
        if event.name == 'backspace':
            # Xóa ký tự cuối trong buffer
            if self.typed_buffer:
                self.typed_buffer = self.typed_buffer[:-1]
                self.last_triggered_keyword = ""
            self._cancel_pending_trigger()
            
        elif event.name in ['enter', 'tab']:
            # Chỉ reset với enter và tab, không reset với space để hỗ trợ shortcut có dấu cách
            self.last_triggered_keyword = ""
            self._cancel_pending_trigger()
            
            # Thêm ký tự vào buffer
            if event.name == 'tab':
                self.typed_buffer += '\t'
            elif event.name == 'enter':
                self.typed_buffer = ""
                
        elif event.name == 'space':
            # Thêm dấu cách vào buffer nhưng không reset trigger state
            self.typed_buffer += ' '
            
            # Giới hạn độ dài buffer
            if len(self.typed_buffer) > 50:  # Tăng từ 30 lên 50 để hỗ trợ shortcut dài hơn
                self.typed_buffer = self.typed_buffer[-50:]
            
            # Kiểm tra shortcuts ngay sau khi thêm dấu cách
            self._fast_check_for_shortcuts()
                
        elif len(event.name) == 1:
            # Xử lý tất cả ký tự có thể gõ được (bao gồm cả ký tự đặc biệt)
            char = event.name
            if char.isprintable():  # Chỉ xử lý ký tự có thể in được
                self.typed_buffer += char
                
                # Giới hạn độ dài buffer
                if len(self.typed_buffer) > 50:  # Tăng từ 30 lên 50 để hỗ trợ shortcut dài hơn
                    self.typed_buffer = self.typed_buffer[-50:]
                
                # Kiểm tra keywords với thuật toán tối ưu
                self._fast_check_for_shortcuts()
        
        # Reset trigger state cho các phím đặc biệt khác
        elif event.name in ['ctrl', 'alt', 'shift', 'up', 'down', 'left', 'right', 
                           'home', 'end', 'page_up', 'page_down', 'delete', 'insert']:
            self.last_triggered_keyword = ""
            self._cancel_pending_trigger()
    
    def _fast_check_for_shortcuts(self):
        """Kiểm tra shortcuts với thuật toán tối ưu tốc độ - Ưu tiên exact match và shortcut ngắn"""
        if not self.typed_buffer:
            return
        
        buffer_len = len(self.typed_buffer)
        found_keywords = []
        
        # Thu thập tất cả keywords phù hợp
        for keyword_len in self._keyword_cache.keys():
            if keyword_len > buffer_len:
                continue  # Skip keywords dài hơn buffer
            
            for keyword in self._keyword_cache[keyword_len]:
                if (self.typed_buffer.endswith(keyword) and 
                    keyword != self.last_triggered_keyword):
                    found_keywords.append(keyword)
        
        if not found_keywords:
            return
        
        # Ưu tiên shortcut theo thứ tự:
        # 1. Exact match (keyword = buffer)
        # 2. Shortcut ngắn nhất (tránh conflict)
        exact_matches = [kw for kw in found_keywords if kw == self.typed_buffer]
        if exact_matches:
            # Nếu có exact match, ưu tiên shortcut ngắn nhất
            selected_keyword = min(exact_matches, key=len)
        else:
            # Nếu không có exact match, chọn shortcut ngắn nhất
            selected_keyword = min(found_keywords, key=len)
        
        self._schedule_auto_trigger(selected_keyword)
    
    def _is_complete_word_fast(self, keyword: str) -> bool:
        """Kiểm tra từ hoàn chỉnh - Luôn trả về True để hỗ trợ mọi định dạng shortcut"""
        # Để hỗ trợ mọi loại shortcut (có dấu cách, ký tự đặc biệt), 
        # chúng ta không cần kiểm tra từ hoàn chỉnh nữa
        return True
    
    def set_instant_trigger(self, enabled: bool):
        """Bật/tắt chế độ trigger ngay lập tức"""
        self.instant_trigger = enabled
        if enabled:
            print("Đã bật chế độ trigger ngay lập tức (không delay)")
        else:
            print(f"Đã tắt chế độ instant, delay: {self.auto_trigger_delay}s")
    
    def set_auto_trigger_delay(self, delay: float):
        """Đặt thời gian delay cho auto trigger"""
        self.auto_trigger_delay = max(0.01, min(2.0, delay))  # Tối thiểu 10ms, tối đa 2s
        print(f"Đã đặt delay: {self.auto_trigger_delay}s")
    
    def pause(self):
        """Tạm dừng monitoring"""
        self.stop_monitoring()
    
    def resume(self):
        """Tiếp tục monitoring"""
        self.start_monitoring()
    
    def is_active(self) -> bool:
        """Kiểm tra xem đang monitoring hay không"""
        return self.is_monitoring 
    
    def refresh_keywords_cache(self):
        """Cập nhật lại cache keywords khi có shortcuts mới (gọi từ bên ngoài)"""
        if self.is_monitoring:
            # Reset tất cả state để tránh conflict với keywords mới
            self.typed_buffer = ""
            self.last_triggered_keyword = ""
            self._cancel_pending_trigger()
            
            # Cập nhật cache với keywords mới
            self._update_keyword_cache()
            
            print("🔄 Đã cập nhật cache keywords và reset state để nhận diện shortcuts mới")
        else:
            # Nếu không monitoring, chỉ cập nhật cache thôi
            self._update_keyword_cache()
            print("🔄 Đã cập nhật cache keywords (chưa monitoring)")
    
    def _update_keyword_cache(self):
        """Cập nhật cache keywords để tăng tốc"""
        self._keyword_cache = {}
        keywords = self.shortcut_manager.get_all_keywords()
        # Tạo dictionary theo độ dài keyword để tìm kiếm nhanh hơn
        for keyword in keywords:
            length = len(keyword)
            if length not in self._keyword_cache:
                self._keyword_cache[length] = []
            self._keyword_cache[length].append(keyword)
        
        # Sắp xếp theo độ dài giảm dần trong mỗi nhóm
        for length in self._keyword_cache:
            self._keyword_cache[length].sort(key=len, reverse=True) 