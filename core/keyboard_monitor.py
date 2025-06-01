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
        """Lên lịch auto trigger với delay tối ưu"""
        self._cancel_pending_trigger()
        
        # Nếu instant trigger được bật, trigger ngay lập tức
        if self.instant_trigger or self.auto_trigger_delay <= 0.05:
            self._trigger_shortcut_immediate(keyword)
            return
        
        def auto_trigger():
            if (self.is_monitoring and 
                self.typed_buffer.endswith(keyword) and 
                keyword != self.last_triggered_keyword):
                
                self._trigger_shortcut_immediate(keyword)
        
        self.pending_trigger_timer = threading.Timer(self.auto_trigger_delay, auto_trigger)
        self.pending_trigger_timer.start()
    
    def _trigger_shortcut_immediate(self, keyword: str):
        """Trigger shortcut ngay lập tức với tốc độ tối ưu và sửa lỗi timing"""
        try:
            print(f"🚀 Bắt đầu trigger shortcut '{keyword}'")
            print(f"📝 Buffer hiện tại: '{self.typed_buffer}'")
            
            # Đánh dấu đã trigger để tránh lặp lại
            self.last_triggered_keyword = keyword
            original_buffer = self.typed_buffer
            self.typed_buffer = ""
            
            print(f"🧹 Đã reset buffer và đánh dấu keyword: '{keyword}'")
            
            # BƯỚC 1: Xóa keyword đã gõ trước tiên
            print(f"🔙 BƯỚC 1: Xóa keyword '{keyword}' ({len(keyword)} ký tự)")
            self._fast_backspace(len(keyword))
            
            # Thêm delay nhỏ để đảm bảo backspace hoàn tất
            time.sleep(0.010)  # 10ms delay sau backspace
            
            # BƯỚC 2: Xử lý shortcut (copy vào clipboard)
            print(f"📋 BƯỚC 2: Xử lý shortcut '{keyword}'")
            success = self.shortcut_manager.process_shortcut(keyword)
            
            if success:
                # BƯỚC 3: Đợi một chút để đảm bảo clipboard đã sẵn sàng - tối ưu cho mixed content
                print(f"⏱️ BƯỚC 3: Đợi clipboard sẵn sàng")
                if self.instant_trigger or self.auto_trigger_delay <= 0.05:
                    time.sleep(0.010)  # Giảm từ 15ms xuống 10ms cho instant mode
                else:
                    time.sleep(0.015)  # Giảm từ 25ms xuống 15ms cho chế độ khác
                
                # BƯỚC 4: Paste nội dung từ clipboard
                print(f"📥 BƯỚC 4: Paste nội dung")
                keyboard.send('ctrl+v')
                
                # Delay cuối để đảm bảo paste hoàn tất - tối ưu tốc độ
                time.sleep(0.003)  # Giảm từ 5ms xuống 3ms
                
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
        """Thực hiện backspace nhanh với cải tiến cho tốc độ cao và debugging"""
        try:
            if count <= 0:
                return
            
            print(f"🔙 Đang xóa {count} ký tự...")
            
            # Sử dụng phương pháp đơn giản và đáng tin cậy nhất cho keywords mới
            if count <= 5:
                # Với 5 ký tự trở xuống: backspace tuần tự (đáng tin cậy nhất)
                for i in range(count):
                    keyboard.send('backspace')
                    if count > 1:
                        time.sleep(0.002)  # 2ms delay để đảm bảo ổn định
                print(f"✅ Đã xóa {count} ký tự bằng backspace tuần tự")
            else:
                # Với keywords dài hơn: thử selection trước, fallback về backspace
                selection_success = False
                try:
                    # Thử phương pháp selection
                    # Ctrl+Shift+Left để select word
                    keyboard.send('ctrl+shift+left')
                    time.sleep(0.005)  # 5ms để đảm bảo selection
                    keyboard.send('delete')
                    selection_success = True
                    print(f"✅ Đã xóa {count} ký tự bằng selection")
                except Exception as sel_error:
                    print(f"⚠️ Selection method thất bại: {sel_error}")
                    selection_success = False
                
                # Fallback: nếu selection không thành công
                if not selection_success:
                    print(f"🔄 Fallback: sử dụng backspace tuần tự cho {count} ký tự")
                    for i in range(count):
                        keyboard.send('backspace')
                        time.sleep(0.002)  # 2ms delay
                    print(f"✅ Đã xóa {count} ký tự bằng backspace fallback")
                        
        except Exception as e:
            print(f"❌ Lỗi trong _fast_backspace: {e}")
            # Fallback cuối cùng: backspace đơn giản
            print(f"🆘 Emergency fallback: xóa {count} ký tự")
            try:
                for i in range(count):
                    keyboard.send('backspace')
                    time.sleep(0.005)  # Delay lớn hơn cho emergency
            except Exception as final_error:
                print(f"💥 Emergency fallback cũng thất bại: {final_error}")
    
    def _on_key_press(self, event):
        """Xử lý sự kiện phím bấm với tốc độ tối ưu"""
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
            
        elif event.name in ['space', 'enter', 'tab']:
            # Reset trigger state khi có phím kết thúc từ
            self.last_triggered_keyword = ""
            self._cancel_pending_trigger()
            
            # Thêm ký tự vào buffer
            if event.name == 'space':
                self.typed_buffer += ' '
            elif event.name == 'tab':
                self.typed_buffer += '\t'
            elif event.name == 'enter':
                self.typed_buffer = ""
                
        elif len(event.name) == 1:
            # Xử lý tất cả ký tự có thể gõ được (bao gồm cả ký tự đặc biệt)
            char = event.name
            if char.isprintable():  # Chỉ xử lý ký tự có thể in được
                self.typed_buffer += char
                
                # Giới hạn độ dài buffer
                if len(self.typed_buffer) > 30:
                    self.typed_buffer = self.typed_buffer[-30:]
                
                # Kiểm tra keywords với thuật toán tối ưu
                self._fast_check_for_shortcuts()
        
        # Reset trigger state cho các phím đặc biệt khác
        elif event.name in ['ctrl', 'alt', 'shift', 'up', 'down', 'left', 'right', 
                           'home', 'end', 'page_up', 'page_down', 'delete', 'insert']:
            self.last_triggered_keyword = ""
            self._cancel_pending_trigger()
    
    def _fast_check_for_shortcuts(self):
        """Kiểm tra shortcuts với thuật toán tối ưu tốc độ"""
        if not self.typed_buffer:
            return
        
        buffer_len = len(self.typed_buffer)
        
        # Kiểm tra từ keywords dài nhất trước (tối ưu cache)
        for keyword_len in sorted(self._keyword_cache.keys(), reverse=True):
            if keyword_len > buffer_len:
                continue  # Skip keywords dài hơn buffer
            
            if keyword_len <= buffer_len:
                # Kiểm tra các keywords có độ dài phù hợp
                for keyword in self._keyword_cache[keyword_len]:
                    if (self.typed_buffer.endswith(keyword) and 
                        keyword != self.last_triggered_keyword and
                        self._is_complete_word_fast(keyword)):
                        
                        self._schedule_auto_trigger(keyword)
                        return  # Tìm thấy rồi thì dừng luôn
    
    def _is_complete_word_fast(self, keyword: str) -> bool:
        """Kiểm tra từ hoàn chỉnh với thuật toán nhanh"""
        buffer_len = len(self.typed_buffer)
        keyword_len = len(keyword)
        
        if buffer_len == keyword_len:
            return True  # Keyword chiếm toàn bộ buffer
        
        # Kiểm tra ký tự trước keyword
        start_pos = buffer_len - keyword_len
        if start_pos > 0:
            char_before = self.typed_buffer[start_pos - 1]
            # Dùng set lookup thay vì list để tăng tốc
            return char_before in {' ', '\t', '\n', '\r'}
        
        return True  # Keyword ở đầu buffer
    
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