#!/usr/bin/env python3
"""
TextNow - Auto Text & Image v2.0.0
PySide6 UI Migration

Entry point cho ứng dụng PySide6
"""
import sys
import os
from pathlib import Path
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from qt_ui.main_window_qt import MainWindowQt
    from utils.single_instance import SingleInstance
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)


class TextNowQtApp:
    """Main application class"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.single_instance = None
        self.startup_mode = False  # Flag for silent startup
        
    def setup_application(self):
        """Setup QApplication with properties"""
        # Create application
        self.app = QApplication(sys.argv)
        
        # Fix: Remove deprecated DPI attributes for Qt 6
        # Qt 6 has automatic high DPI scaling enabled by default
        # Only set these if needed for older Qt versions
        try:
            # These are deprecated in Qt 6, but kept for compatibility
            if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
                # Only for Qt < 6.0
                pass  # Skip deprecated attributes
            
            print("✅ DPI scaling: Using Qt 6 automatic scaling")
        except Exception as e:
            print(f"⚠️ DPI setup warning: {e}")
        
        # Set application properties
        self.app.setApplicationName("TextNow")
        self.app.setApplicationDisplayName("TextNow - Auto Text & Image")
        self.app.setApplicationVersion("2.0.0")
        self.app.setOrganizationName("TextNow Team")
        self.app.setOrganizationDomain("textnow.app")
        
        # Set application icon
        self._set_app_icon()
        
        print("✅ QApplication setup completed")
        
    def _set_app_icon(self):
        """Set application icon"""
        try:
            icon_path = project_root / "icon.png"
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self.app.setWindowIcon(icon)
                print(f"✅ App icon set: {icon_path}")
            else:
                print("⚠️ App icon not found")
        except Exception as e:
            print(f"❌ App icon error: {e}")
    
    def check_single_instance(self):
        """Check if another instance is running"""
        try:
            self.single_instance = SingleInstance("TextNow_Qt")
            
            if not self.single_instance.acquire_lock():
                print("📱 Another instance is already running")
                
                # Try to show existing window
                if self.single_instance.send_show_signal():
                    print("✅ Sent show signal to existing instance")
                else:
                    print("⚠️ Could not communicate with existing instance")
                
                # Exit silently without showing popup message
                return False
            
            print("✅ Single instance check passed")
            return True
            
        except Exception as e:
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
            
            print("✅ Main window created")
            return True
            
        except Exception as e:
            print(f"❌ Main window creation failed: {e}")
            traceback.print_exc()
            
            QMessageBox.critical(
                None,
                "Lỗi khởi động",
                f"Không thể khởi tạo cửa sổ chính:\n\n{e}\n\n"
                "Vui lòng kiểm tra console để biết chi tiết."
            )
            return False
    
    def _setup_signal_checking(self):
        """Setup timer để check signals từ instances khác"""
        def check_signals():
            if self.single_instance:
                if self.single_instance.check_for_show_signal():
                    if self.main_window:
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
                print("🔇 Starting in silent mode (minimized to tray)")
                # Don't call show(), window will be hidden by default
                # System tray will be available for user to open
            else:
                self.main_window.show()
                print("🚀 TextNow Qt started successfully!")
            
            # Run event loop
            return self.app.exec()
            
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user")
            return 0
        except Exception as e:
            print(f"❌ Application error: {e}")
            traceback.print_exc()
            return 1
        finally:
            # Cleanup
            if self.single_instance:
                self.single_instance.release_lock()
                print("🧹 Cleanup completed")


def main():
    """Main entry point"""
    print("🚀 Starting TextNow Qt v2.0.0...")
    print(f"📂 Project root: {project_root}")
    print(f"🐍 Python: {sys.version}")
    
    try:
        app = TextNowQtApp()
        exit_code = app.run()
        print(f"✅ Application exited with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 