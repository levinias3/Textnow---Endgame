#!/usr/bin/env python3
"""
TextNow - Auto Text & Image v2.0.1
PySide6 UI Migration

Entry point cho ứng dụng PySide6 - Optimized for EXE deployment
"""
import sys
import os
from pathlib import Path
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

# ✅ EXE-optimized path handling
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Development mode - use script directory
        base_path = Path(__file__).parent.absolute()
    
    return os.path.join(base_path, relative_path)

def get_data_path(relative_path):
    """Get absolute path for user data files (always in app directory)"""
    # For user data, always use the directory where exe/script is located
    if getattr(sys, 'frozen', False):
        # Running as exe
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent
    
    return app_dir / relative_path

# Setup paths
project_root = get_data_path("")  # Use data path for config files
sys.path.insert(0, str(project_root))

# Add resource path for bundled resources
if hasattr(sys, '_MEIPASS'):
    # In exe mode, also add MEIPASS to path for imports
    sys.path.insert(0, sys._MEIPASS)

try:
    from qt_ui.main_window_qt import MainWindowQt
    from utils.single_instance import SingleInstance
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Traceback:")
    traceback.print_exc()
    
    # Try to show error in message box for exe mode
    if getattr(sys, 'frozen', False):
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(
                None,
                "Lỗi khởi động",
                f"Không thể tải modules:\n\n{e}\n\n"
                "Vui lòng báo cáo lỗi này cho developer."
            )
        except:
            pass
    
    sys.exit(1)


class TextNowQtApp:
    """Main application class - EXE optimized"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.single_instance = None
        self.startup_mode = False  # Flag for silent startup
        self.is_exe_mode = getattr(sys, 'frozen', False)
        
    def setup_application(self):
        """Setup QApplication with properties"""
        # Create application
        self.app = QApplication(sys.argv)
        
        # ✅ Optimized for exe - no console output in exe mode
        if not self.is_exe_mode:
            print("✅ DPI scaling: Using Qt 6 automatic scaling")
        
        # Set application properties
        self.app.setApplicationName("TextNow")
        self.app.setApplicationDisplayName("TextNow - Auto Text & Image")
        self.app.setApplicationVersion("2.0.1")
        self.app.setOrganizationName("TextNow Team")
        self.app.setOrganizationDomain("textnow.app")
        
        # Set application icon
        self._set_app_icon()
        
        if not self.is_exe_mode:
            print("✅ QApplication setup completed")
        
    def _set_app_icon(self):
        """Set application icon - EXE optimized"""
        try:
            # Try bundled icon first (for exe)
            icon_path = get_resource_path("icon.png")
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                self.app.setWindowIcon(icon)
                if not self.is_exe_mode:
                    print(f"✅ App icon set: {icon_path}")
                return
            
            # Fallback to data directory
            icon_path = get_data_path("icon.png")
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self.app.setWindowIcon(icon)
                if not self.is_exe_mode:
                    print(f"✅ App icon set: {icon_path}")
                return
                
            if not self.is_exe_mode:
                print("⚠️ App icon not found")
                
        except Exception as e:
            if not self.is_exe_mode:
                print(f"❌ App icon error: {e}")
    
    def check_single_instance(self):
        """Check if another instance is running"""
        try:
            self.single_instance = SingleInstance("TextNow_Qt")
            
            if not self.single_instance.acquire_lock():
                if not self.is_exe_mode:
                    print("📱 Another instance is already running")
                
                # Try to show existing window
                if self.single_instance.send_show_signal():
                    if not self.is_exe_mode:
                        print("✅ Sent show signal to existing instance")
                else:
                    if not self.is_exe_mode:
                        print("⚠️ Could not communicate with existing instance")
                
                # Exit silently
                return False
            
            if not self.is_exe_mode:
                print("✅ Single instance check passed")
            return True
            
        except Exception as e:
            if not self.is_exe_mode:
                print(f"⚠️ Single instance check failed: {e}")
            # Continue anyway
            return True
    
    def create_main_window(self):
        """Create main window"""
        try:
            self.main_window = MainWindowQt()
            
            # Setup signal checking for other instances
            if self.single_instance:
                self._setup_signal_checking()
            
            if not self.is_exe_mode:
                print("✅ Main window created")
            return True
            
        except Exception as e:
            error_msg = f"Không thể khởi tạo cửa sổ chính:\n\n{e}"
            
            if not self.is_exe_mode:
                print(f"❌ Main window creation failed: {e}")
                traceback.print_exc()
            
            # Always show message box for critical errors
            QMessageBox.critical(
                None,
                "Lỗi khởi động", 
                error_msg + "\n\nVui lòng báo cáo lỗi này."
            )
            return False
    
    def _setup_signal_checking(self):
        """Setup timer để check signals từ instances khác"""
        def check_signals():
            if self.single_instance:
                if self.single_instance.check_for_show_signal():
                    if self.main_window:
                        if not self.is_exe_mode:
                            print("📱 Received SHOW_WINDOW signal")
                        self.main_window.show()
                        self.main_window.raise_()
                        self.main_window.activateWindow()
        
        # Check every 500ms
        signal_timer = QTimer()
        signal_timer.timeout.connect(check_signals)
        signal_timer.start(500)
        self.signal_timer = signal_timer  # Keep reference
    
    def run(self):
        """Run the application"""
        try:
            # Setup application
            self.setup_application()
            
            # Check single instance
            if not self.check_single_instance():
                return 0
            
            # Create main window
            if not self.create_main_window():
                return 1
            
            # Show main window (or hide if startup mode)
            if self.startup_mode:
                # Start minimized to tray for silent startup
                if not self.is_exe_mode:
                    print("🔇 Starting in silent mode (minimized to tray)")
                
                # Đảm bảo window được tạo nhưng không hiển thị
                # Window sẽ ẩn và chỉ hiển thị qua system tray
                self.main_window.hide()
                
                # Không hiển thị notification khi khởi động ẩn để giữ im lặng hoàn toàn
                # Ứng dụng sẽ chạy ngầm mà không làm phiền người dùng
                
            else:
                self.main_window.show()
                if not self.is_exe_mode:
                    print("🚀 TextNow Qt started successfully!")
            
            # Run event loop
            return self.app.exec()
            
        except KeyboardInterrupt:
            if not self.is_exe_mode:
                print("\n⚠️ Interrupted by user")
            return 0
        except Exception as e:
            if not self.is_exe_mode:
                print(f"❌ Application error: {e}")
                traceback.print_exc()
            return 1
        finally:
            # Cleanup
            if self.single_instance:
                self.single_instance.release_lock()
                if not self.is_exe_mode:
                    print("🧹 Cleanup completed")


def main():
    """Main entry point - EXE optimized"""
    is_exe = getattr(sys, 'frozen', False)
    
    if not is_exe:
        print("🚀 Starting TextNow Qt v2.0.1...")
        print(f"📂 Project root: {project_root}")
        print(f"🐍 Python: {sys.version}")
    
    try:
        app = TextNowQtApp()
        
        # Kiểm tra command line arguments để xác định startup mode
        # Hỗ trợ: --hidden, --silent, --minimized, --tray
        if len(sys.argv) > 1:
            args = [arg.lower() for arg in sys.argv[1:]]
            if any(arg in ['--hidden', '--silent', '--minimized', '--tray', '-h', '-s'] for arg in args):
                app.startup_mode = True
                if not is_exe:
                    print("🔇 Silent startup mode enabled via command line")
        
        exit_code = app.run()
        
        if not is_exe:
            print(f"✅ Application exited with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        if not is_exe:
            print(f"❌ Fatal error: {e}")
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 