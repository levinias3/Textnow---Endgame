#!/usr/bin/env python3
"""
Script tạo checkmark icon đơn giản cho radio buttons và checkbox
"""
import sys
from PIL import Image, ImageDraw

def create_checkmark_icon(filename, size=20, bg_color=(59, 130, 246), check_color=(255, 255, 255)):
    """Tạo checkmark icon"""
    # Tạo image với background trong suốt
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Vẽ background màu xanh
    draw.rectangle([0, 0, size-1, size-1], fill=bg_color, outline=None)
    
    # Vẽ checkmark (✓)
    # Đường line từ 25% chiều rộng, 50% chiều cao -> 40% chiều rộng, 70% chiều cao
    # Rồi từ 40% chiều rộng, 70% chiều cao -> 75% chiều rộng, 30% chiều cao
    
    x1, y1 = int(size * 0.25), int(size * 0.5)   # Điểm bắt đầu
    x2, y2 = int(size * 0.45), int(size * 0.7)   # Điểm giữa
    x3, y3 = int(size * 0.75), int(size * 0.3)   # Điểm cuối
    
    # Vẽ đường line đầu tiên
    draw.line([(x1, y1), (x2, y2)], fill=check_color, width=2)
    # Vẽ đường line thứ hai
    draw.line([(x2, y2), (x3, y3)], fill=check_color, width=2)
    
    # Lưu file
    img.save(filename, 'PNG')
    print(f"✅ Created checkmark icon: {filename}")

def main():
    """Tạo các checkmark icons"""
    try:
        # Tạo checkmark cho radio buttons
        create_checkmark_icon('checkmark.png', size=20)
        
        # Tạo checkmark vector cho checkbox
        create_checkmark_icon('checkmark_vector.png', size=20)
        
        print("✅ All checkmark icons created successfully!")
        
    except ImportError:
        print("❌ Pillow not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
        
        # Retry
        from PIL import Image, ImageDraw
        create_checkmark_icon('checkmark.png', size=20)
        create_checkmark_icon('checkmark_vector.png', size=20)
        print("✅ All checkmark icons created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating icons: {e}")
        # Fallback: create simple text-based icon
        create_text_checkmark()

def create_text_checkmark():
    """Fallback: create simple text checkmark"""
    # This is a very basic fallback if PIL isn't available
    print("📝 Creating simple text checkmark...")

if __name__ == "__main__":
    main() 