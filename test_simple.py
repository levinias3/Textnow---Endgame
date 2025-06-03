#!/usr/bin/env python3
"""
Simple test để debug issues
"""
import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test import"""
    print("🧪 Testing imports...")
    try:
        from PySide6.QtWidgets import QApplication
        print("✅ PySide6 import OK")
        
        from qt_ui.main_window_qt import MainWindowQt
        print("✅ MainWindowQt import OK")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """Test app creation"""
    print("🧪 Testing app creation...")
    try:
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        from qt_ui.main_window_qt import MainWindowQt
        print("📝 Creating MainWindow...")
        
        window = MainWindowQt()
        print("✅ MainWindow created")
        
        print("📝 Testing window properties...")
        print(f"   Size: {window.size().width()}x{window.size().height()}")
        print(f"   Title: {window.windowTitle()}")
        print(f"   Visible: {window.isVisible()}")
        
        # Test show
        window.show()
        print("✅ Window shown")
        
        # Process events
        app.processEvents()
        print("✅ Events processed")
        
        # Quick test and close
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, app.quit)
        
        print("⏰ Running for 1 second...")
        result = app.exec()
        print(f"✅ App exec completed with result: {result}")
        
        return result == 0
        
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Simple debug test...")
    print(f"📂 Project root: {project_root}")
    print()
    
    # Test imports
    import_ok = test_imports()
    print()
    
    if import_ok:
        # Test app creation
        app_ok = test_app_creation()
        print()
        
        print("🎯 Results:")
        print(f"   Imports: {'✅ OK' if import_ok else '❌ Failed'}")
        print(f"   App: {'✅ OK' if app_ok else '❌ Failed'}")
        
        if import_ok and app_ok:
            print("✅ All tests passed!")
            sys.exit(0)
        else:
            print("❌ Some tests failed!")
            sys.exit(1)
    else:
        print("❌ Import test failed!")
        sys.exit(1) 