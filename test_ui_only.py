#!/usr/bin/env python3
"""
Test UI only - không keyboard monitoring
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_ui_simple():
    """Test UI đơn giản"""
    print("🚀 Starting UI test...")
    
    try:
        # Create application
        app = QApplication(sys.argv)
        
        # Fix: Skip deprecated DPI attributes for Qt 6
        print("✅ Using Qt 6 automatic DPI scaling")
        
        print("✅ QApplication created")
        
        # Load UI file
        ui_file = Path(__file__).parent / "qt_ui" / "forms" / "main_window.ui"
        print(f"UI file: {ui_file}")
        print(f"Exists: {ui_file.exists()}")
        
        if not ui_file.exists():
            QMessageBox.critical(None, "Error", f"UI file not found: {ui_file}")
            return 1
        
        loader = QUiLoader()
        ui_widget = loader.load(str(ui_file))
        print("✅ UI loaded")
        
        # Create main window
        window = QMainWindow()
        window.setCentralWidget(ui_widget)
        window.setWindowTitle("TextNow - Qt Test")
        window.setFixedSize(1440, 1080)
        
        # Center window
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - window.width()) // 2
        y = (screen_geometry.height() - window.height()) // 2
        window.move(x, y)
        
        print("✅ Window setup completed")
        
        # Load stylesheet
        style_file = Path(__file__).parent / "qt_ui" / "resources" / "style.qss"
        if style_file.exists():
            with open(style_file, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
            window.setStyleSheet(stylesheet)
            print("✅ Stylesheet loaded")
        else:
            print("⚠️ Stylesheet not found")
        
        # Show window
        window.show()
        print("✅ Window shown")
        
        # Run for 3 seconds then quit
        from PySide6.QtCore import QTimer
        QTimer.singleShot(3000, app.quit)
        
        print("🚀 Running app for 3 seconds...")
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_ui_simple()) 