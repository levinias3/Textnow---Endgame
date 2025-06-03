#!/usr/bin/env python3
"""
Test script để debug Qt app
"""
import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test import modules"""
    print("🧪 Testing imports...")
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow
        print("✅ PySide6 imported successfully")
    except Exception as e:
        print(f"❌ PySide6 import failed: {e}")
        return False
    
    try:
        from utils.config import Config
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from core.shortcut_manager import ShortcutManager
        print("✅ ShortcutManager imported successfully")
    except Exception as e:
        print(f"❌ ShortcutManager import failed: {e}")
        return False
    
    try:
        from core.keyboard_monitor import KeyboardMonitor
        print("✅ KeyboardMonitor imported successfully")
    except Exception as e:
        print(f"❌ KeyboardMonitor import failed: {e}")
        return False
    
    return True

def test_qt_basic():
    """Test basic Qt functionality"""
    print("🧪 Testing Qt basic functionality...")
    
    try:
        from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
        from PySide6.QtCore import Qt
        
        app = QApplication(sys.argv)
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        
        window = QMainWindow()
        window.setWindowTitle("Test Qt Window")
        window.setFixedSize(400, 300)
        
        label = QLabel("Qt App is working!")
        label.setAlignment(Qt.AlignCenter)
        window.setCentralWidget(label)
        
        print("✅ Qt basic functionality test passed")
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ Qt basic test failed: {e}")
        traceback.print_exc()
        return False

def test_ui_file():
    """Test UI file loading"""
    print("🧪 Testing UI file loading...")
    
    try:
        from PySide6.QtUiTools import QUiLoader
        from PySide6.QtWidgets import QApplication
        
        ui_file = Path(__file__).parent / "qt_ui" / "forms" / "main_window.ui"
        print(f"UI file path: {ui_file}")
        print(f"UI file exists: {ui_file.exists()}")
        
        if not ui_file.exists():
            print("❌ UI file not found")
            return False
        
        app = QApplication(sys.argv)
        loader = QUiLoader()
        ui_widget = loader.load(str(ui_file))
        
        print("✅ UI file loaded successfully")
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ UI file loading failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Starting Qt tests...")
    print(f"📂 Project root: {project_root}")
    print(f"🐍 Python: {sys.version}")
    print()
    
    tests = [
        test_imports,
        test_qt_basic,
        test_ui_file,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            traceback.print_exc()
            results.append(False)
            print()
    
    print("📊 Test Results:")
    for i, result in enumerate(results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  Test {i+1}: {status}")
    
    all_passed = all(results)
    print(f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 