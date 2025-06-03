"""
Auto Text & Image - Ứng dụng gõ tắt thông minh cho Windows
Main entry point
"""
import sys
import os
from ui.main_window import MainWindow
from system_tray import SystemTray
from utils.single_instance import ensure_single_instance

class AutoTextImageApp:
    def __init__(self):
        self.main_window = MainWindow()
        self.system_tray = SystemTray()
        self.single_instance = None
        
        # Kết nối các callback
        self.main_window.set_on_minimize_to_tray(self._on_minimize_to_tray)
        self.system_tray.set_callbacks(
            on_show_window=self._on_show_window,
            on_exit=self._on_exit
        )
        
        # Callback để cập nhật icon tray khi trạng thái monitoring thay đổi
        original_callback = self.main_window.keyboard_monitor.on_status_changed
        def new_callback(is_active):
            if original_callback:
                original_callback(is_active)
            self.system_tray.update_icon(is_active)
        self.main_window.keyboard_monitor.set_on_status_changed(new_callback)
        
    def set_single_instance(self, single_instance):
        """Đặt single instance object"""
        self.single_instance = single_instance
        
    def _on_minimize_to_tray(self):
        """Xử lý khi minimize to tray"""
        self.system_tray.show_notification(
            "Auto Text & Image",
            "Ứng dụng đã được thu nhỏ xuống khay hệ thống"
        )
    
    def _on_show_window(self):
        """Xử lý khi click mở cửa sổ từ tray"""
        self.main_window.show()
    
    def _on_exit(self):
        """Xử lý khi click thoát từ tray"""
        try:
            self.main_window.stop()
            self.system_tray.stop()
            
            # Giải phóng single instance lock
            if self.single_instance:
                self.single_instance.release_lock()
                
            self.main_window.root.quit()
            self.main_window.root.destroy()
        except:
            pass
        finally:
            os._exit(0)  # Force exit để tránh SystemExit exception
    
    def check_signals_periodically(self):
        """Kiểm tra signals từ instance khác định kỳ"""
        if self.single_instance and self.single_instance.check_for_show_signal():
            # Có signal từ instance khác, hiện cửa sổ
            self.main_window.show()
            
        # Lên lịch kiểm tra lại sau 500ms
        self.main_window.root.after(500, self.check_signals_periodically)
    
    def run(self):
        """Chạy ứng dụng"""
        # Khởi động system tray
        self.system_tray.start()
        
        # Bắt đầu kiểm tra signals
        if self.single_instance:
            self.check_signals_periodically()
        
        # Khởi động main window
        self.main_window.start()

def main():
    """Entry point"""
    try:
        # Kiểm tra single instance trước
        single_instance = ensure_single_instance("AutoTextImage")
        if not single_instance:
            print("⚠️ Ứng dụng đã được chạy. Hiện cửa sổ của phiên bản đang chạy...")
            sys.exit(0)
            
        print("🔒 Single instance lock acquired successfully")
        
        # Kiểm tra quyền administrator (khuyến nghị cho keyboard hook)
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Cảnh báo: Ứng dụng hoạt động tốt nhất khi chạy với quyền Administrator")
            print("Một số tính năng có thể bị giới hạn trong một số ứng dụng")
        
        # Khởi động ứng dụng
        app = AutoTextImageApp()
        app.set_single_instance(single_instance)
        
        try:
            app.run()
        finally:
            # Đảm bảo giải phóng lock khi thoát
            single_instance.release_lock()
        
    except KeyboardInterrupt:
        print("\nỨng dụng đã được dừng bởi người dùng")
    except Exception as e:
        print(f"Lỗi khi khởi động ứng dụng: {e}")
        import traceback
        traceback.print_exc()
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main() 