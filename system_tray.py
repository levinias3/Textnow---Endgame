"""
Module xử lý System Tray cho ứng dụng
"""
import pystray
from PIL import Image, ImageDraw
import threading
from typing import Callable, Optional
import os

class SystemTray:
    def __init__(self):
        self.app_name = "Auto Text & Image - Fullscreen"
        self.icon = None
        self.thread = None
        self.on_show_window = None
        self.on_exit = None
    
    def set_callbacks(self, on_show_window: Callable = None, on_exit: Callable = None):
        """Đặt các callback functions"""
        self.on_show_window = on_show_window
        self.on_exit = on_exit
    
    def create_icon(self, is_monitoring: bool = True) -> Image.Image:
        """Tạo icon cho system tray từ file ảnh"""
        try:
            # Đường dẫn đến file icon trong thư mục dự án
            icon_path = "icon.png"
            
            # Kiểm tra file tồn tại
            if os.path.exists(icon_path):
                # Load ảnh từ file
                image = Image.open(icon_path)
                
                # Resize về 64x64 cho system tray
                image = image.resize((64, 64), Image.Resampling.LANCZOS)
                
                # Convert sang RGBA để đảm bảo tương thích
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                # Nếu không monitoring, làm mờ icon một chút
                if not is_monitoring:
                    # Tạo overlay mờ
                    overlay = Image.new('RGBA', (64, 64), (128, 128, 128, 128))
                    image = Image.alpha_composite(image, overlay)
                
                return image
            else:
                print(f"Không tìm thấy file icon: {icon_path}")
                # Fallback về icon mặc định
                return self._create_default_icon(is_monitoring)
                
        except Exception as e:
            print(f"Lỗi khi load icon: {e}")
            # Fallback về icon mặc định
            return self._create_default_icon(is_monitoring)
    
    def _create_default_icon(self, is_monitoring: bool = True) -> Image.Image:
        """Tạo icon mặc định nếu không load được file ảnh"""
        # Tạo icon 64x64
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # Vẽ icon đơn giản (có thể thay bằng icon file sau)
        if is_monitoring:
            # Icon màu xanh khi đang hoạt động
            draw.rectangle([16, 16, 48, 48], fill='green', outline='darkgreen', width=2)
            draw.text((26, 26), "A", fill='white')
        else:
            # Icon màu đỏ khi tạm dừng
            draw.rectangle([16, 16, 48, 48], fill='red', outline='darkred', width=2)
            draw.text((26, 26), "A", fill='white')
        
        return image
    
    def update_icon(self, is_monitoring: bool):
        """Cập nhật icon theo trạng thái monitoring"""
        if self.icon:
            self.icon.icon = self.create_icon(is_monitoring)
    
    def _create_menu(self):
        """Tạo context menu cho system tray"""
        return pystray.Menu(
            pystray.MenuItem("📺 Hiển thị (Toàn màn hình)", self._on_show_window, default=True),
            pystray.MenuItem("ℹ️ Thông tin", self._show_info),
            pystray.MenuItem("🚪 Thoát", self._on_exit)
        )
    
    def _on_show_window(self, icon, item):
        """Xử lý khi click Mở cửa sổ"""
        if self.on_show_window:
            self.on_show_window()
    
    def _on_exit(self, icon, item):
        """Xử lý khi click Thoát"""
        if self.on_exit:
            self.on_exit()
        self.stop()
    
    def _show_info(self, icon, item):
        """Hiển thị thông tin về chế độ fullscreen"""
        self.show_notification(
            "📺 Chế độ Toàn màn hình", 
            "Ứng dụng chạy fullscreen\nKhông thể minimize\nCtrl+Alt+Q để thoát khẩn cấp"
        )
    
    def start(self):
        """Bắt đầu system tray trong thread riêng"""
        def run():
            self.icon = pystray.Icon(
                self.app_name,
                self.create_icon(True),
                self.app_name,
                menu=self._create_menu()
            )
            self.icon.run()
        
        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Dừng system tray"""
        if self.icon:
            self.icon.stop()
    
    def show_notification(self, title: str, message: str):
        """Hiển thị notification từ system tray"""
        if self.icon:
            try:
                self.icon.notify(message, title)
                print(f"📢 Notification: {title} - {message}")
            except Exception as e:
                # Một số hệ thống không hỗ trợ notification
                print(f"⚠️ Không thể hiện notification: {e}")
                pass 