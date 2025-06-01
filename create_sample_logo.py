"""
Script tạo logo mẫu cho ứng dụng
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_sample_logo():
    # Tạo ảnh 256x256
    img = Image.new('RGB', (256, 256), color='white')
    draw = ImageDraw.Draw(img)
    
    # Vẽ background gradient
    for y in range(256):
        color = int(255 - (y / 256) * 100)
        draw.rectangle([(0, y), (256, y+1)], fill=(color, color, 255))
    
    # Vẽ chữ A lớn
    try:
        # Thử dùng font hệ thống
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        # Dùng font mặc định nếu không tìm thấy
        font = ImageFont.load_default()
    
    # Vẽ chữ A với shadow
    draw.text((90, 50), "A", fill='darkblue', font=font)
    draw.text((85, 45), "A", fill='white', font=font)
    
    # Vẽ text nhỏ
    try:
        small_font = ImageFont.truetype("arial.ttf", 24)
    except:
        small_font = ImageFont.load_default()
    
    draw.text((70, 180), "Text", fill='white', font=small_font)
    draw.text((68, 178), "Text", fill='navy', font=small_font)
    
    # Lưu file
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    img.save('assets/logo.png', 'PNG')
    
    # Tạo icon 32x32
    icon_img = img.resize((32, 32), Image.Resampling.LANCZOS)
    icon_img.save('icon.ico', 'ICO')
    
    print("Đã tạo logo mẫu tại assets/logo.png và icon.ico")

if __name__ == "__main__":
    create_sample_logo() 