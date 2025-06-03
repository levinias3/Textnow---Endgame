#!/usr/bin/env python3
"""
Minimal test để tìm exact crash point
"""
import sys
import traceback
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt, QTimer

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_qt():
    """Test basic Qt window"""
    print("🧪 Testing basic Qt...")
    try:
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        window = QMainWindow()
        window.setWindowTitle("Basic Test")
        window.setFixedSize(400, 300)
        
        label = QLabel("Basic Qt Test")
        label.setAlignment(Qt.AlignCenter)
        window.setCentralWidget(label)
        
        print("✅ Basic window created")
        
        window.show()
        print("✅ Basic window shown")
        
        QTimer.singleShot(1000, app.quit)
        result = app.exec()
        print(f"✅ Basic test completed: {result}")
        return result == 0
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        traceback.print_exc()
        return False

def test_ui_file_only():
    """Test chỉ load UI file"""
    print("🧪 Testing UI file loading...")
    try:
        from PySide6.QtUiTools import QUiLoader
        
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        ui_file = Path(__file__).parent / "qt_ui" / "forms" / "main_window.ui"
        print(f"📝 Loading UI: {ui_file}")
        
        loader = QUiLoader()
        ui_widget = loader.load(str(ui_file))
        print("✅ UI widget loaded")
        
        window = QMainWindow()
        window.setCentralWidget(ui_widget)
        window.setWindowTitle("UI Test")
        print("✅ UI window created")
        
        window.show()
        print("✅ UI window shown")
        
        QTimer.singleShot(1000, app.quit)
        result = app.exec()
        print(f"✅ UI test completed: {result}")
        return result == 0
        
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        traceback.print_exc()
        return False

def test_step_by_step():
    """Test từng bước một"""
    print("🧪 Testing step by step...")
    try:
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Import MainWindow class
        from qt_ui.main_window_qt import MainWindowQt
        print("✅ MainWindowQt imported")
        
        # Create instance
        print("📝 Creating MainWindow instance...")
        window = MainWindowQt()
        print("✅ MainWindow instance created")
        
        # Test properties before show
        print(f"📋 Window size: {window.size().width()}x{window.size().height()}")
        print(f"📋 Window title: {window.windowTitle()}")
        
        # Try to show
        print("📝 Attempting to show window...")
        window.show()
        print("✅ Window.show() called successfully")
        
        # Process events
        app.processEvents()
        print("✅ Events processed")
        
        # Check if visible
        print(f"📋 Window visible: {window.isVisible()}")
        
        QTimer.singleShot(1000, app.quit)
        result = app.exec()
        print(f"✅ Step-by-step test completed: {result}")
        return result == 0
        
    except Exception as e:
        print(f"❌ Step-by-step test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Minimal debug tests...")
    print()
    
    # Test 1: Basic Qt
    basic_ok = test_basic_qt()
    print()
    
    # Test 2: UI file only
    ui_ok = test_ui_file_only()
    print()
    
    # Test 3: Step by step
    step_ok = test_step_by_step()
    print()
    
    print("🎯 Results:")
    print(f"   Basic Qt: {'✅ OK' if basic_ok else '❌ Failed'}")
    print(f"   UI file: {'✅ OK' if ui_ok else '❌ Failed'}")
    print(f"   Step-by-step: {'✅ OK' if step_ok else '❌ Failed'}")
    
    if basic_ok and ui_ok and step_ok:
        print("✅ All minimal tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1) 