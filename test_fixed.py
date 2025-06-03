#!/usr/bin/env python3
"""
Fixed test với single QApplication
"""
import sys
import traceback
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt, QTimer

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_all_with_single_app():
    """Test tất cả với single QApplication"""
    print("🚀 Testing with single QApplication...")
    
    try:
        # Create single app instance
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Test 1: Basic Qt window
        print("\n🧪 Test 1: Basic Qt...")
        window1 = QMainWindow()
        window1.setWindowTitle("Basic Test")
        window1.setFixedSize(400, 300)
        
        label = QLabel("Basic Qt Test")
        label.setAlignment(Qt.AlignCenter)
        window1.setCentralWidget(label)
        
        window1.show()
        app.processEvents()
        print("✅ Basic window shown")
        window1.hide()
        
        # Test 2: UI file loading
        print("\n🧪 Test 2: UI file loading...")
        from PySide6.QtUiTools import QUiLoader
        
        ui_file = Path(__file__).parent / "qt_ui" / "forms" / "main_window.ui"
        print(f"📝 Loading UI: {ui_file}")
        
        loader = QUiLoader()
        ui_widget = loader.load(str(ui_file))
        print("✅ UI widget loaded")
        
        window2 = QMainWindow()
        window2.setCentralWidget(ui_widget)
        window2.setWindowTitle("UI Test")
        window2.show()
        app.processEvents()
        print("✅ UI window shown")
        window2.hide()
        
        # Test 3: MainWindow class
        print("\n🧪 Test 3: MainWindow class...")
        from qt_ui.main_window_qt import MainWindowQt
        print("✅ MainWindowQt imported")
        
        print("📝 Creating MainWindow instance...")
        window3 = MainWindowQt()
        print("✅ MainWindow instance created")
        
        print(f"📋 Window size: {window3.size().width()}x{window3.size().height()}")
        print(f"📋 Window title: {window3.windowTitle()}")
        
        print("📝 Showing MainWindow...")
        window3.show()
        app.processEvents()
        print("✅ MainWindow shown successfully")
        
        print(f"📋 Window visible: {window3.isVisible()}")
        
        # Keep window open for 2 seconds
        print("⏰ Keeping window open for 2 seconds...")
        
        # Setup timer to close
        def close_app():
            print("📝 Closing application...")
            window3.close()
            app.quit()
        
        QTimer.singleShot(2000, close_app)
        
        # Run event loop
        result = app.exec()
        print(f"✅ Application completed with result: {result}")
        
        return result == 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Fixed test with single QApplication...")
    print(f"📂 Project root: {project_root}")
    print()
    
    success = test_all_with_single_app()
    
    print(f"\n🎯 Final Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1) 