"""
Module quản lý shortcuts và xử lý logic thay thế
"""
from typing import Dict, List, Optional, Callable
from utils.config import Config
from core.clipboard_handler import ClipboardHandler
import time
import os
import threading

class ShortcutManager:
    def __init__(self, config: Config):
        self.config = config
        self.shortcuts_dict = {}
        self.update_shortcuts_dict()
        self.on_shortcut_triggered = None  # Callback khi shortcut được trigger
        self.pending_images = []  # Queue cho các ảnh cần xử lý sau
        self.processing_mixed = False  # Flag để tránh conflict
    
    def update_shortcuts_dict(self):
        """Cập nhật dictionary shortcuts từ config"""
        self.shortcuts_dict = {}
        for shortcut in self.config.get_shortcuts():
            if shortcut.get('enabled', True):
                self.shortcuts_dict[shortcut['keyword']] = shortcut
    
    def set_on_shortcut_triggered(self, callback: Callable):
        """Đặt callback khi shortcut được trigger"""
        self.on_shortcut_triggered = callback
    
    def get_shortcut(self, keyword: str) -> Optional[Dict]:
        """Lấy thông tin shortcut theo keyword"""
        return self.shortcuts_dict.get(keyword)
    
    def process_shortcut(self, keyword: str) -> bool:
        """Xử lý shortcut khi được trigger với tốc độ tối ưu và logging chi tiết"""
        shortcut = self.get_shortcut(keyword)
        if not shortcut:
            print(f"❌ Không tìm thấy shortcut cho keyword: '{keyword}'")
            return False
        
        shortcut_type = shortcut.get('type', 'text')
        content = shortcut.get('content', '')
        
        print(f"🔄 Đang xử lý shortcut '{keyword}' - Loại: {shortcut_type}")
        
        success = False
        start_time = time.time()
        
        try:
            if shortcut_type in ['text', 'richtext']:
                # Xử lý văn bản với logic tối ưu
                print(f"📝 Xử lý văn bản cho '{keyword}' - {len(content)} ký tự...")
                
                content_length = len(content)
                has_html_tags = '<' in content and '>' in content
                
                # Quyết định phương pháp copy dựa trên nội dung
                if content_length > 20000:
                    # Văn bản rất dài -> dùng copy_text (nhanh nhất)
                    print(f"📄 Văn bản dài ({content_length} ký tự) -> dùng copy_text")
                    success = ClipboardHandler.copy_text(content)
                elif not has_html_tags:
                    # Text thuần -> copy_text
                    print(f"📝 Text thuần -> dùng copy_text")
                    success = ClipboardHandler.copy_text(content)
                else:
                    # Có HTML tags -> thử copy_html trước
                    print(f"🌐 Có HTML tags -> thử copy_html")
                    success = ClipboardHandler.copy_html(content)
                    if not success:
                        print(f"⚠️ copy_html thất bại, fallback sang copy_text")
                        success = ClipboardHandler.copy_text(content)
                        
            elif shortcut_type == 'image':
                # Xử lý ảnh
                print(f"🖼️ Xử lý ảnh cho '{keyword}': {content}")
                
                # Kiểm tra file path trước khi xử lý
                if not content.strip():
                    print(f"❌ Đường dẫn ảnh trống cho shortcut '{keyword}'")
                    success = False
                elif not os.path.exists(content):
                    print(f"❌ File ảnh không tồn tại: {content}")
                    success = False
                else:
                    success = ClipboardHandler.copy_image(content)
            
            elif shortcut_type == 'mixed':
                # Xử lý mixed content: text + images
                print(f"📄🖼️ Xử lý mixed content cho '{keyword}'...")
                
                if isinstance(content, dict):
                    text_content = content.get('text', '')
                    images = content.get('images', [])
                    
                    print(f"📝 Text: {len(text_content)} ký tự, 🖼️ Images: {len(images)} ảnh")
                    
                    # Clear clipboard trước khi bắt đầu - tối ưu tốc độ
                    ClipboardHandler.clear_clipboard()
                    time.sleep(0.02)  # Giảm từ 0.05s xuống 0.02s
                    
                    success = True
                    
                    # Xử lý ưu tiên: text trước, nếu không có text thì ảnh đầu tiên
                    if text_content:
                        # Copy text để paste ngay
                        print(f"🔄 Copy text ({len(text_content)} ký tự) để paste trước...")
                        text_success = ClipboardHandler.copy_text(text_content)
                        if text_success:
                            print(f"✅ Text đã sẵn sàng cho paste")
                            # Schedule xử lý tất cả ảnh sau khi text được paste
                            if images:
                                print(f"📋 Lên lịch xử lý {len(images)} ảnh sau khi paste text")
                                self.pending_images = images.copy()
                        else:
                            print(f"❌ Copy text thất bại")
                            success = False
                    elif images:
                        # Không có text, copy ảnh đầu tiên để paste ngay
                        first_image = images[0]
                        print(f"🔄 Copy ảnh đầu tiên: {first_image}")
                        
                        if not os.path.exists(first_image):
                            print(f"❌ Ảnh đầu tiên không tồn tại: {first_image}")
                            success = False
                        else:
                            image_success = ClipboardHandler.copy_image(first_image)
                            if image_success:
                                print(f"✅ Ảnh 1 đã sẵn sàng cho paste")
                                # Schedule xử lý các ảnh còn lại (từ ảnh 2)
                                if len(images) > 1:
                                    print(f"📋 Lên lịch xử lý {len(images)-1} ảnh còn lại")
                                    self.pending_images = images.copy()
                            else:
                                print(f"❌ Copy ảnh đầu tiên thất bại")
                                success = False
                    else:
                        print(f"❌ Mixed content rỗng")
                        success = False
                    
                    if success:
                        if text_content and images:
                            print(f"🎉 Mixed content sẵn sàng: Text (paste ngay) + {len(images)} ảnh (paste sau)")
                        elif text_content:
                            print(f"🎉 Text content sẵn sàng cho paste")
                        elif images:
                            print(f"🎉 Image content sẵn sàng: Ảnh 1 (paste ngay) + {len(images)-1} ảnh (paste sau)")
                    
                else:
                    print(f"❌ Mixed content format không hợp lệ cho '{keyword}'")
                    success = False
                    
            else:
                print(f"❌ Loại shortcut không được hỗ trợ: {shortcut_type}")
                success = False
                
        except Exception as e:
            print(f"❌ Exception khi xử lý shortcut '{keyword}': {e}")
            success = False
        
        # Tính thời gian xử lý
        processing_time = (time.time() - start_time) * 1000
        
        # Logging kết quả với thời gian
        if success:
            print(f"✅ Shortcut '{keyword}' đã được xử lý thành công trong {processing_time:.1f}ms")
            
            # Gọi callback nếu có (không block)
            if self.on_shortcut_triggered:
                try:
                    if shortcut_type == 'mixed':
                        display_type = "văn bản + ảnh"
                        display_content = f"Text + {len(content.get('images', []))} ảnh" if isinstance(content, dict) else str(content)
                    else:
                        display_type = "văn bản" if shortcut_type in ['text', 'richtext'] else "ảnh"
                        display_content = content
                    self.on_shortcut_triggered(keyword, display_type, display_content)
                except Exception as callback_error:
                    print(f"⚠️ Lỗi trong callback: {callback_error}")
        else:
            print(f"❌ Shortcut '{keyword}' xử lý thất bại sau {processing_time:.1f}ms")
        
        return success
    
    def get_all_keywords(self) -> List[str]:
        """Lấy danh sách tất cả keywords đang active"""
        return list(self.shortcuts_dict.keys())
    
    def reload_shortcuts(self):
        """Tải lại shortcuts từ config"""
        self.config.load()
        self.update_shortcuts_dict()
    
    def is_valid_keyword(self, keyword: str) -> bool:
        """Kiểm tra keyword có hợp lệ không"""
        # Keyword phải có ít nhất 2 ký tự
        if len(keyword) < 2:
            return False
        
        # Không được chứa các ký tự điều khiển và khoảng trắng
        invalid_chars = {' ', '\t', '\n', '\r', '\b', '\f', '\v'}
        return not any(char in invalid_chars for char in keyword)
    
    def get_shortcuts_count(self) -> int:
        """Đếm số lượng shortcuts đang active"""
        return len(self.shortcuts_dict)
    
    def get_shortcuts_by_type(self, shortcut_type: str) -> List[Dict]:
        """Lấy danh sách shortcuts theo loại"""
        result = []
        for shortcut in self.shortcuts_dict.values():
            if shortcut_type == 'text':
                # Với "text", bao gồm cả text và richtext
                if shortcut.get('type', 'text') in ['text', 'richtext']:
                    result.append(shortcut)
            elif shortcut_type == 'mixed':
                # Mixed content: text + images
                if shortcut.get('type', 'text') == 'mixed':
                    result.append(shortcut)
            else:
                # Với các loại khác (image), so sánh exact
                if shortcut.get('type', 'text') == shortcut_type:
                    result.append(shortcut)
        return result
    
    def process_remaining_images(self, images: List[str], start_index: int = 1):
        """Xử lý các ảnh còn lại sau khi paste đầu tiên hoàn thành"""
        if self.processing_mixed:
            print("⚠️ Đang xử lý mixed content khác, bỏ qua...")
            return
            
        self.processing_mixed = True
        
        def process_images_delayed():
            try:
                for i in range(start_index, len(images)):
                    image_path = images[i]
                    order = i + 1
                    
                    print(f"🔄 Xử lý ảnh {order}: {image_path}")
                    
                    if not os.path.exists(image_path):
                        print(f"❌ Ảnh {order} không tồn tại: {image_path}")
                        continue
                    
                    # Copy ảnh với tối ưu tốc độ
                    success = ClipboardHandler.copy_image(image_path)
                    if success:
                        print(f"✅ Ảnh {order} đã copy thành công")
                        # Paste ảnh ngay lập tức
                        ClipboardHandler.paste()
                        print(f"📋 Ảnh {order} đã paste")
                        
                        # Delay tối thiểu chỉ để đảm bảo paste hoàn thành
                        if i < len(images) - 1:  # Không delay cho ảnh cuối
                            time.sleep(0.05)  # Tối ưu: giảm từ 0.08s xuống 0.05s
                    else:
                        print(f"❌ Copy ảnh {order} thất bại")
                        
                print(f"🎉 Hoàn thành xử lý {len(images)} ảnh")
            except Exception as e:
                print(f"❌ Lỗi khi xử lý ảnh: {e}")
            finally:
                self.processing_mixed = False
        
        # Delay tối thiểu trước khi xử lý ảnh tiếp theo
        timer = threading.Timer(0.08, process_images_delayed)  # Giảm từ 0.15s xuống 0.08s
        timer.start() 