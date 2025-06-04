#!/usr/bin/env python3
"""
Script tạo icon chất lượng cao cho phần mềm từ ảnh gốc
"""
import sys
import os
from pathlib import Path
from PIL import Image, ImageEnhance
import shutil

def create_high_quality_icons():
    """Tạo các icon chất lượng cao từ ảnh gốc"""
    
    # Đường dẫn ảnh gốc
    source_image = Path("C:/Users/Admin/Downloads/image 488.png")
    
    if not source_image.exists():
        print(f"❌ Không tìm thấy ảnh gốc: {source_image}")
        return False
    
    print(f"📱 Đang tạo icon từ ảnh gốc: {source_image}")
    
    try:
        # Mở ảnh gốc
        original_img = Image.open(source_image)
        print(f"🖼️ Kích thước ảnh gốc: {original_img.size}")
        
        # Convert sang RGBA để đảm bảo tính tương thích
        if original_img.mode != 'RGBA':
            original_img = original_img.convert('RGBA')
        
        # Enhance chất lượng
        enhancer = ImageEnhance.Sharpness(original_img)
        original_img = enhancer.enhance(1.2)  # Tăng độ sắc nét
        
        # Tạo thư mục icons nếu chưa có
        icons_dir = Path("icons")
        icons_dir.mkdir(exist_ok=True)
        
        # Các kích thước icon cần tạo (quan trọng cho Windows)
        icon_sizes = [
            16,   # Taskbar small
            20,   # System tray
            24,   # Small toolbar
            32,   # Standard icon
            40,   # Medium icon  
            48,   # Large icon
            64,   # Extra large
            96,   # Jumbo icon
            128,  # Very large
            256,  # Ultra large
            512   # Maximum quality
        ]
        
        created_files = []
        
        for size in icon_sizes:
            # Resize với chất lượng cao nhất
            resized_img = original_img.resize(
                (size, size), 
                Image.Resampling.LANCZOS  # Chất lượng cao nhất
            )
            
            # Lưu vào thư mục icons
            icon_path = icons_dir / f"icon_{size}x{size}.png"
            resized_img.save(icon_path, 'PNG', optimize=True, quality=100)
            created_files.append(icon_path)
            print(f"✅ Tạo icon {size}x{size}: {icon_path}")
        
        # Tạo icon.png chính (256x256 cho chất lượng cao)
        main_icon = original_img.resize((256, 256), Image.Resampling.LANCZOS)
        main_icon_path = Path("icon.png")
        main_icon.save(main_icon_path, 'PNG', optimize=True, quality=100)
        created_files.append(main_icon_path)
        print(f"✅ Tạo icon chính: {main_icon_path}")
        
        # Tạo app.ico cho Windows (multi-size ICO)
        ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        ico_images = []
        
        for size_tuple in ico_sizes:
            ico_img = original_img.resize(size_tuple, Image.Resampling.LANCZOS)
            ico_images.append(ico_img)
        
        # Lưu file .ico
        ico_path = Path("app.ico")
        ico_images[0].save(
            ico_path, 
            format='ICO', 
            sizes=ico_sizes,
            append_images=ico_images[1:]
        )
        created_files.append(ico_path)
        print(f"✅ Tạo file ICO: {ico_path}")
        
        # Tạo các logo trong thư mục logos
        logos_dir = Path("logos")
        logos_dir.mkdir(exist_ok=True)
        
        logo_sizes = [64, 128, 256, 512]
        for size in logo_sizes:
            logo_img = original_img.resize((size, size), Image.Resampling.LANCZOS)
            logo_path = logos_dir / f"logo_{size}x{size}.png"
            logo_img.save(logo_path, 'PNG', optimize=True, quality=100)
            created_files.append(logo_path)
            print(f"✅ Tạo logo {size}x{size}: {logo_path}")
        
        # Tạo logo.png chính
        main_logo = original_img.resize((512, 512), Image.Resampling.LANCZOS)
        main_logo_path = logos_dir / "logo.png"
        main_logo.save(main_logo_path, 'PNG', optimize=True, quality=100)
        created_files.append(main_logo_path)
        print(f"✅ Tạo logo chính: {main_logo_path}")
        
        print(f"\n🎉 Tạo thành công {len(created_files)} file icon & logo!")
        print("📋 Danh sách file đã tạo:")
        for file in created_files:
            file_size = file.stat().st_size / 1024  # KB
            print(f"  • {file} ({file_size:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo icon: {e}")
        return False

def update_icon_references():
    """Cập nhật các tham chiếu icon trong mã để sử dụng icon chất lượng cao"""
    
    print("\n🔧 Cập nhật tham chiếu icon trong mã...")
    
    # Cập nhật main_window_qt.py để sử dụng icon chất lượng cao
    qt_main_file = Path("qt_ui/main_window_qt.py")
    if qt_main_file.exists():
        try:
            content = qt_main_file.read_text(encoding='utf-8')
            
            # Tìm và thay thế đoạn _set_window_icon
            old_method = '''def _set_window_icon(self):
        """Set window icon"""
        try:
            icon_path = Path(__file__).parent.parent / "icon.png"
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"⚠️ Icon error: {e}")'''
            
            new_method = '''def _set_window_icon(self):
        """Set window icon với chất lượng cao"""
        try:
            # Sử dụng icon chất lượng cao nhất có sẵn
            base_path = Path(__file__).parent.parent
            
            # Thử các icon theo thứ tự ưu tiên (chất lượng cao -> thấp)
            icon_candidates = [
                base_path / "icons" / "icon_256x256.png",  # Chất lượng cao nhất
                base_path / "icons" / "icon_128x128.png",  # Chất lượng cao
                base_path / "icons" / "icon_64x64.png",    # Chất lượng trung bình
                base_path / "icon.png",                    # Fallback
                base_path / "app.ico"                      # ICO fallback
            ]
            
            for icon_path in icon_candidates:
                if icon_path.exists():
                    self.setWindowIcon(QIcon(str(icon_path)))
                    print(f"✅ Window icon set: {icon_path.name}")
                    return
                    
            print("⚠️ No window icon found")
        except Exception as e:
            print(f"⚠️ Window icon error: {e}")'''
            
            if old_method in content:
                content = content.replace(old_method, new_method)
                print("✅ Cập nhật _set_window_icon() method")
            
            # Tìm và thay thế đoạn system tray icon
            old_tray = '''# Set icon
            icon_path = Path(__file__).parent.parent / "icon.png"
            if icon_path.exists():
                self.tray_icon.setIcon(QIcon(str(icon_path)))
                print(f"✅ Tray icon set: {icon_path}")
            else:
                # Fallback to default icon
                self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
                print("✅ Tray icon set: default")'''
            
            new_tray = '''# Set icon với chất lượng cao
            base_path = Path(__file__).parent.parent
            tray_icon_candidates = [
                base_path / "icons" / "icon_32x32.png",    # Tối ưu cho system tray
                base_path / "icons" / "icon_20x20.png",    # Kích thước chuẩn tray
                base_path / "icons" / "icon_24x24.png",    # Alternative tray size
                base_path / "icon.png",                    # Fallback
                base_path / "app.ico"                      # ICO fallback
            ]
            
            tray_icon_set = False
            for icon_path in tray_icon_candidates:
                if icon_path.exists():
                    self.tray_icon.setIcon(QIcon(str(icon_path)))
                    print(f"✅ Tray icon set: {icon_path.name}")
                    tray_icon_set = True
                    break
            
            if not tray_icon_set:
                # Fallback to default icon
                self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
                print("✅ Tray icon set: default fallback")'''
            
            if old_tray in content:
                content = content.replace(old_tray, new_tray)
                print("✅ Cập nhật system tray icon")
            
            # Lưu file
            qt_main_file.write_text(content, encoding='utf-8')
            print(f"✅ Cập nhật file: {qt_main_file}")
            
        except Exception as e:
            print(f"❌ Lỗi cập nhật {qt_main_file}: {e}")
    
    # Cập nhật main_qt.py
    main_qt_file = Path("main_qt.py")
    if main_qt_file.exists():
        try:
            content = main_qt_file.read_text(encoding='utf-8')
            
            # Cập nhật icon paths để ưu tiên icon chất lượng cao
            old_icon = 'icon_path = get_resource_path("icon.png")'
            new_icon = '''# Sử dụng icon chất lượng cao nhất có sẵn
        high_quality_icons = [
            "icons/icon_256x256.png",
            "icons/icon_128x128.png", 
            "icons/icon_64x64.png",
            "icon.png",
            "app.ico"
        ]
        
        icon_path = None
        for icon_file in high_quality_icons:
            candidate_path = get_resource_path(icon_file)
            if candidate_path and os.path.exists(candidate_path):
                icon_path = candidate_path
                break
        
        if not icon_path:
            icon_path = get_resource_path("icon.png")'''
            
            if old_icon in content:
                content = content.replace(old_icon, new_icon)
                print("✅ Cập nhật main_qt.py icon handling")
                
                main_qt_file.write_text(content, encoding='utf-8')
                print(f"✅ Cập nhật file: {main_qt_file}")
            
        except Exception as e:
            print(f"❌ Lỗi cập nhật {main_qt_file}: {e}")

def main():
    """Main function"""
    print("🚀 Bắt đầu tạo icon chất lượng cao cho TextNow...")
    
    # Kiểm tra Pillow
    try:
        from PIL import Image, ImageEnhance
    except ImportError:
        print("📦 Cài đặt Pillow...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
        from PIL import Image, ImageEnhance
        
    # Tạo icon
    if create_high_quality_icons():
        print("\n✅ Tạo icon thành công!")
        
        # Cập nhật mã
        update_icon_references()
        
        print("\n🎯 Hoàn tất! Các cải tiến:")
        print("  • Icon taskbar & system tray chất lượng cao")
        print("  • Hỗ trợ nhiều kích thước (16x16 -> 512x512)")
        print("  • File .ico multi-size cho Windows")
        print("  • Logo chất lượng cao cho UI")
        print("  • Tối ưu cho việc build exe")
        
        print("\n📁 Kiểm tra các file đã tạo:")
        print("  • icons/ - Các icon kích thước khác nhau")
        print("  • logos/ - Các logo kích thước khác nhau") 
        print("  • icon.png - Icon chính 256x256")
        print("  • app.ico - Icon Windows multi-size")
        
    else:
        print("❌ Tạo icon thất bại!")

if __name__ == "__main__":
    main() 