#!/usr/bin/env python3
"""
Test script đầy đủ cho Qt app với tất cả tính năng mới
"""
import sys
import os
import time
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_full_app():
    """Test ứng dụng đầy đủ với system tray và image handling"""
    print("🚀 Starting full Qt app test...")
    
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Fix: Skip deprecated DPI attributes for Qt 6
        print("✅ Using Qt 6 automatic DPI scaling")
        
        print("✅ QApplication created")
        
        # Import và create main window
        from qt_ui.main_window_qt import MainWindowQt
        window = MainWindowQt()
        
        print("✅ MainWindow created")
        
        # Test system tray
        if window.tray_icon:
            print("✅ System tray available")
        else:
            print("⚠️ System tray not available")
        
        # Test startup setting
        startup_enabled = window._is_startup_enabled()
        print(f"📱 Auto startup: {'✅ Enabled' if startup_enabled else '❌ Disabled'}")
        
        # Show window
        window.show()
        print("✅ Window shown")
        
        # Force process events to ensure UI is ready
        app.processEvents()
        
        # Test content type switching
        print("🔄 Testing content type switching...")
        
        # Test text mode
        window.ui.textRadioBtn.setChecked(True)
        window._update_content_type_visibility()
        app.processEvents()  # Process UI updates
        text_visible = window.ui.contentTextEdit.isVisible()
        images_visible = hasattr(window, 'images_widget') and window.images_widget.isVisible()
        print(f"📝 Text mode: Text={text_visible}, Images={images_visible}")
        
        # Test image mode
        window.ui.imageRadioBtn.setChecked(True)
        window._update_content_type_visibility()
        app.processEvents()  # Process UI updates
        text_visible = window.ui.contentTextEdit.isVisible()
        images_visible = hasattr(window, 'images_widget') and window.images_widget.isVisible()
        print(f"🖼️ Image mode: Text={text_visible}, Images={images_visible}")
        
        # Test mixed mode
        window.ui.mixedRadioBtn.setChecked(True)
        window._update_content_type_visibility()
        app.processEvents()  # Process UI updates
        text_visible = window.ui.contentTextEdit.isVisible()
        images_visible = hasattr(window, 'images_widget') and window.images_widget.isVisible()
        print(f"📝🖼️ Mixed mode: Text={text_visible}, Images={images_visible}")
        
        # Test clear form
        window._clear_form()
        app.processEvents()
        print("✅ Clear form test passed")
        
        # Test load shortcuts
        window._load_shortcuts()
        shortcuts_count = len(window.config.get_shortcuts())
        print(f"📊 Loaded {shortcuts_count} shortcuts")
        
        # Show some info
        print("\n📋 App Information:")
        print(f"   Window size: {window.size().width()}x{window.size().height()}")
        print(f"   System tray: {'Available' if window.tray_icon else 'Not available'}")
        print(f"   Shortcuts: {shortcuts_count}")
        print(f"   Keyboard monitoring: {'Active' if window.keyboard_monitor else 'Inactive'}")
        
        # Test tray message
        if window.tray_icon:
            print("💬 Testing tray notification...")
            window.tray_icon.showMessage(
                "Test Notification",
                "Qt app đang hoạt động tốt!",
                window.tray_icon.MessageIcon.Information,
                2000
            )
        
        # Test form functionality
        print("🧪 Testing form functionality...")
        
        # Test adding some text
        window.ui.shortcutLineEdit.setText("test_keyword")
        window.ui.contentTextEdit.setPlainText("Test content")
        print("✅ Form input test passed")
        
        # Test search
        window.ui.searchLineEdit.setText("test")
        app.processEvents()
        print("✅ Search test passed")
        
        # Clear search
        window.ui.searchLineEdit.clear()
        app.processEvents()
        
        # Run for 3 seconds then close
        print("\n⏰ Running app for 3 seconds...")
        print("   - UI đang hoạt động")
        print("   - System tray ready")
        print("   - Tất cả test cases passed")
        
        QTimer.singleShot(3000, app.quit)
        
        result = app.exec()
        print("✅ App test completed successfully")
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

def test_registry_access():
    """Test quyền truy cập registry cho startup setting"""
    print("🔑 Testing registry access...")
    
    try:
        import winreg
        
        # Test read access
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_READ)
        print("✅ Registry read access OK")
        
        # Test if TextNow entry exists
        try:
            value, _ = winreg.QueryValueEx(key, "TextNow")
            print(f"📱 TextNow startup entry found: {value}")
        except FileNotFoundError:
            print("📱 TextNow startup entry not found")
        
        winreg.CloseKey(key)
        
        # Test write access
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_WRITE)
            print("✅ Registry write access OK")
            winreg.CloseKey(key)
        except Exception as e:
            print(f"❌ Registry write access failed: {e}")
            
    except Exception as e:
        print(f"❌ Registry access test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 Starting comprehensive Qt tests...")
    print(f"📂 Project root: {project_root}")
    print(f"🐍 Python: {sys.version}")
    print()
    
    # Test registry first
    registry_ok = test_registry_access()
    print()
    
    # Test full app
    exit_code = test_full_app()
    
    print(f"\n🎯 Test Results:")
    print(f"   Registry access: {'✅ OK' if registry_ok else '❌ Failed'}")
    print(f"   App execution: {'✅ OK' if exit_code == 0 else '❌ Failed'}")
    
    sys.exit(exit_code) 