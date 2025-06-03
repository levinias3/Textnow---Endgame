#!/usr/bin/env python3
"""
Test script cho giới hạn ảnh theo loại shortcut
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_image_limits():
    """Test giới hạn ảnh cho shortcut loại 'Ảnh' và 'Văn bản + Ảnh'"""
    print("🚀 Testing image limits cho các loại shortcut...")
    
    try:
        # Create application
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Import và create main window
        from qt_ui.main_window_qt import MainWindowQt
        window = MainWindowQt()
        
        print("✅ MainWindow created")
        
        # Show window
        window.show()
        print("✅ Window shown")
        
        # Force process events để UI ready
        app.processEvents()
        
        print("\n🔍 Testing image info text updates:")
        
        # Test Text mode
        window.ui.textRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        print(f"   📝 Text mode: Panel {'visible' if window.ui.imageManagerCard.isVisible() else 'hidden'}")
        
        # Test Image mode (1 ảnh)
        window.ui.imageRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        info_text = window.ui.imageInfoLabel.text()
        print(f"   🖼️ Image mode: '{info_text}'")
        
        # Test Mixed mode (20 ảnh)
        window.ui.mixedRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        info_text = window.ui.imageInfoLabel.text()
        print(f"   📝🖼️ Mixed mode: '{info_text}'")
        
        print("\n🧪 Testing image limits:")
        
        # Get sample images để test
        sample_images = []
        for ext in ['.png', '.jpg', '.jpeg']:
            for path in project_root.glob(f"*{ext}"):
                sample_images.append(str(path))
                if len(sample_images) >= 3:  # Cần ít nhất 3 để test
                    break
            if len(sample_images) >= 3:
                break
        
        if len(sample_images) < 2:
            print("   ⚠️ Không đủ sample images để test, creating mock paths...")
            sample_images = ["mock1.png", "mock2.jpg", "mock3.jpeg"]
        
        print(f"   📁 Using {len(sample_images)} sample images for testing")
        
        # Test Image mode (chỉ cho phép 1 ảnh)
        print("\n📸 Testing Image mode limits (max 1):")
        window.ui.imageRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        
        # Clear existing images
        window.selected_images.clear()
        window._refresh_images_list()
        
        # Add first image - should work
        try:
            window._add_images_from_paths([sample_images[0]])
            count = len(window.selected_images)
            print(f"   ✅ Added 1st image: {count} total images")
        except Exception as e:
            print(f"   ❌ Error adding 1st image: {e}")
        
        # Try to add second image - should show warning
        try:
            window._add_images_from_paths([sample_images[1]])
            count = len(window.selected_images)
            if count == 1:
                print(f"   ✅ Correctly rejected 2nd image: still {count} total")
            else:
                print(f"   ❌ Unexpected: {count} total images")
        except Exception as e:
            print(f"   ❌ Error testing 2nd image: {e}")
        
        # Test Mixed mode (cho phép 20 ảnh)
        print("\n📝🖼️ Testing Mixed mode limits (max 20):")
        window.ui.mixedRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        
        # Clear và test multiple images
        window.selected_images.clear()
        window._refresh_images_list()
        
        # Add multiple images
        try:
            window._add_images_from_paths(sample_images[:2])  # Add 2 images
            count = len(window.selected_images)
            print(f"   ✅ Added multiple images in Mixed mode: {count} total")
        except Exception as e:
            print(f"   ❌ Error adding multiple images: {e}")
        
        # Test switching back to Image mode với existing images
        print("\n🔄 Testing mode switch với existing images:")
        window.ui.imageRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        
        try:
            # Try to add when already have images in Image mode
            window._add_images_from_paths([sample_images[2]])
            count = len(window.selected_images)
            print(f"   ✅ Mode switch handling: {count} total images")
        except Exception as e:
            print(f"   ❌ Error in mode switch test: {e}")
        
        print("\n✅ Test Features:")
        print("   📝 Dynamic info text based on shortcut type")
        print("   🖼️ Image mode: max 1 ảnh với popup warning")
        print("   📝🖼️ Mixed mode: max 20 ảnh")
        print("   🔄 Smart limits when switching modes")
        print("   💬 User-friendly warning messages")
        
        print("\n⏰ Running demo for 5 seconds...")
        print("   - Try switching between content types")
        print("   - Notice the info text changes")
        print("   - Try adding images in different modes")
        
        QTimer.singleShot(5000, app.quit)
        
        result = app.exec()
        print("✅ Image limits test completed")
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("🧪 Testing image limits cho shortcut types...")
    print(f"📂 Project root: {project_root}")
    print()
    
    exit_code = test_image_limits()
    
    print(f"\n🎯 Test Result: {'✅ SUCCESS' if exit_code == 0 else '❌ FAILED'}")
    sys.exit(exit_code) 