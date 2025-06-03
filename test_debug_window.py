#!/usr/bin/env python3
"""
Debug window.show() crash
"""
import sys
import traceback
from pathlib import Path
from PySide6.QtWidgets import QApplication

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_debug_show():
    """Debug window.show() với từng step"""
    print("🐛 Debugging window.show() crash...")
    
    try:
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Import với monkey patch để disable risky features
        import qt_ui.main_window_qt as main_module
        
        # Temporarily disable system tray and keyboard monitoring
        original_setup_tray = main_module.MainWindowQt._setup_system_tray
        original_init_keyboard = main_module.MainWindowQt._init_keyboard_monitoring
        
        def dummy_setup_tray(self):
            print("⚠️ System tray setup disabled for debug")
            
        def dummy_init_keyboard(self):
            print("⚠️ Keyboard monitoring disabled for debug")
            
        main_module.MainWindowQt._setup_system_tray = dummy_setup_tray
        main_module.MainWindowQt._init_keyboard_monitoring = dummy_init_keyboard
        
        print("📝 Creating MainWindow with disabled features...")
        window = main_module.MainWindowQt()
        print("✅ MainWindow created")
        
        # Try to show now
        print("📝 Attempting window.show()...")
        window.show()
        print("✅ window.show() success!")
        
        app.processEvents()
        print("✅ Events processed")
        
        print(f"📋 Window visible: {window.isVisible()}")
        print(f"📋 Window size: {window.size().width()}x{window.size().height()}")
        
        # Restore original methods
        main_module.MainWindowQt._setup_system_tray = original_setup_tray
        main_module.MainWindowQt._init_keyboard_monitoring = original_init_keyboard
        
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, app.quit)
        
        result = app.exec()
        print(f"✅ Debug test completed: {result}")
        return result == 0
        
    except Exception as e:
        print(f"❌ Debug test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🐛 Debug test for window.show() crash...")
    print()
    
    success = test_debug_show()
    
    print(f"\n🎯 Debug Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1) 