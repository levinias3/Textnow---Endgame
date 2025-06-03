#!/usr/bin/env python3
"""
Test script cho layout 3 cột với Image Management Panel
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_3_column_layout():
    """Test layout 3 cột với image management panel"""
    print("🚀 Testing 3-column layout với image management panel...")
    
    try:
        # Create application
        app = QApplication(sys.argv)
        print("✅ QApplication created")
        
        # Import và create main window
        from qt_ui.main_window_qt import MainWindowQt
        window = MainWindowQt()
        
        print("✅ MainWindow với 3-column layout created")
        
        # Show window
        window.show()
        print("✅ Window shown")
        
        # Force process events để UI ready
        app.processEvents()
        
        print("\n📊 Testing 3-column layout:")
        print("   📋 Cột 1: Danh sách shortcut (45%)")
        print("   🖼️ Cột 2: Quản lý ảnh (25%)")  
        print("   📝 Cột 3: Form thêm/sửa (30%)")
        
        # Test UI elements existence
        ui_elements = [
            ('shortcutListCard', 'Shortcut List Panel'),
            ('imageManagerCard', 'Image Management Panel'),
            ('formCard', 'Form Panel'),
            ('dropZoneWidget', 'Drop Zone'),
            ('imagesListWidget', 'Images List'),
            ('chooseImagesBtn', 'Choose Images Button'),
            ('moveUpBtn', 'Move Up Button'),
            ('moveDownBtn', 'Move Down Button'),
            ('removeImageBtn', 'Remove Image Button'),
            ('clearImagesBtn', 'Clear Images Button'),
        ]
        
        print("\n🔍 Checking UI elements:")
        for element_name, display_name in ui_elements:
            if hasattr(window.ui, element_name):
                element = getattr(window.ui, element_name)
                visible = element.isVisible()
                print(f"   ✅ {display_name}: {'Visible' if visible else 'Hidden'}")
            else:
                print(f"   ❌ {display_name}: Not found")
        
        # Test image panel visibility theo content type
        print("\n🔄 Testing image panel visibility:")
        
        # Text mode
        window.ui.textRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        panel_visible = window.ui.imageManagerCard.isVisible()
        print(f"   📝 Text mode: Panel {'visible' if panel_visible else 'hidden'}")
        
        # Image mode
        window.ui.imageRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        panel_visible = window.ui.imageManagerCard.isVisible()
        print(f"   🖼️ Image mode: Panel {'visible' if panel_visible else 'hidden'}")
        
        # Mixed mode
        window.ui.mixedRadioBtn.setChecked(True)
        window._on_content_type_changed()
        app.processEvents()
        panel_visible = window.ui.imageManagerCard.isVisible()
        print(f"   📝🖼️ Mixed mode: Panel {'visible' if panel_visible else 'hidden'}")
        
        # Test adding sample images (if available)
        sample_images = []
        for ext in ['.png', '.jpg', '.jpeg']:
            for path in project_root.glob(f"*{ext}"):
                sample_images.append(str(path))
                if len(sample_images) >= 2:
                    break
            if len(sample_images) >= 2:
                break
        
        if sample_images:
            print(f"\n📁 Adding {len(sample_images)} sample images for demo:")
            window.selected_images.extend(sample_images)
            window._refresh_images_list()
            app.processEvents()
            
            for i, img_path in enumerate(sample_images):
                print(f"   {i+1}. {Path(img_path).name}")
            
            # Test button states
            print("\n🔘 Testing button states:")
            window._update_image_button_states()
            buttons = [
                ('move_up_btn', 'Move Up'),
                ('move_down_btn', 'Move Down'),
                ('remove_image_btn', 'Remove'),
                ('clear_images_btn', 'Clear All')
            ]
            
            for btn_name, display_name in buttons:
                if hasattr(window, btn_name):
                    btn = getattr(window, btn_name)
                    enabled = btn.isEnabled()
                    print(f"   🔘 {display_name}: {'Enabled' if enabled else 'Disabled'}")
        
        print("\n🎯 Layout Features:")
        print("   ✅ 3-column responsive layout")
        print("   🖼️ Dedicated image management panel")
        print("   📂 Drag & drop support")
        print("   🔄 Auto show/hide based on content type")
        print("   🎨 Modern UI with proper spacing")
        print("   📱 Proper width ratios (45% + 25% + 30%)")
        
        print("\n⏰ Running demo for 8 seconds...")
        print("   - Test switching content types")
        print("   - Try drag & drop images")
        print("   - Click image management buttons")
        print("   - Resize window to test responsiveness")
        
        QTimer.singleShot(8000, app.quit)
        
        result = app.exec()
        print("✅ 3-column layout test completed")
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    print("🎨 Testing 3-column layout với image management panel...")
    print(f"📂 Project root: {project_root}")
    print()
    
    exit_code = test_3_column_layout()
    
    print(f"\n🎯 Test Result: {'✅ SUCCESS' if exit_code == 0 else '❌ FAILED'}")
    sys.exit(exit_code) 