#!/usr/bin/env python3
"""
Script test font SVN Poppins
"""
import tkinter as tk
from tkinter import ttk
from utils.font_manager import get_font_manager

def test_font():
    """Test font SVN Poppins"""
    print("🧪 Testing SVN Poppins Font...")
    
    # Khởi tạo font manager
    font_manager = get_font_manager()
    
    # Kiểm tra trạng thái
    print(f"📁 Font directory: {font_manager.font_dir}")
    print(f"✅ Font loaded: {font_manager.is_loaded()}")
    print(f"🔤 Font family: {font_manager.get_font_family()}")
    print(f"⚖️ Available weights: {font_manager.get_available_weights()}")
    
    # Tạo cửa sổ test
    root = tk.Tk()
    root.title("SVN Poppins Font Test")
    root.geometry("600x500")
    
    # Test các font weights
    frame = tk.Frame(root, bg='white', padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    title = tk.Label(frame, text="SVN Poppins Font Test", 
                    font=font_manager.get_font(18, 'bold'), 
                    bg='white', fg='#1f2937')
    title.pack(pady=(0, 20))
    
    # Test các weights
    weights = ['thin', 'light', 'regular', 'medium', 'semibold', 'bold', 'black']
    
    for weight in weights:
        try:
            label = tk.Label(frame, 
                           text=f"Weight: {weight.title()} - Tiếng Việt: Xin chào, ăn cơm chưa?",
                           font=font_manager.get_font(12, weight),
                           bg='white', fg='#374151', anchor='w')
            label.pack(fill=tk.X, pady=2)
            print(f"✅ {weight}: OK")
        except Exception as e:
            print(f"❌ {weight}: {e}")
    
    # Test italic
    try:
        italic_label = tk.Label(frame,
                              text="Italic: SVN Poppins Italic Font - Tiếng Việt nghiêng",
                              font=font_manager.get_font(12, 'regular', italic=True),
                              bg='white', fg='#6b7280', anchor='w')
        italic_label.pack(fill=tk.X, pady=2)
        print("✅ Italic: OK")
    except Exception as e:
        print(f"❌ Italic: {e}")
    
    # Test TTK widgets
    ttk_frame = ttk.LabelFrame(frame, text="TTK Widgets Test", padding=10)
    ttk_frame.pack(fill=tk.X, pady=10)
    
    style = ttk.Style()
    style.configure('Test.TLabel', font=font_manager.get_font(10, 'medium'))
    style.configure('Test.TButton', font=font_manager.get_font(10, 'semibold'))
    style.configure('Test.TEntry', font=font_manager.get_font(10))
    
    ttk.Label(ttk_frame, text="TTK Label với SVN Poppins", style='Test.TLabel').pack(anchor='w')
    ttk.Button(ttk_frame, text="TTK Button với SVN Poppins", style='Test.TButton').pack(anchor='w', pady=5)
    ttk.Entry(ttk_frame, font=font_manager.get_font(10)).pack(fill=tk.X, pady=5)
    
    # Thông tin chi tiết
    info_text = tk.Text(frame, height=6, width=70, 
                       font=font_manager.get_font(9),
                       bg='#f9fafb', fg='#374151')
    info_text.pack(fill=tk.X, pady=10)
    
    info_content = f"""Font Manager Info:
Font Directory: {font_manager.font_dir}
Font Loaded: {font_manager.is_loaded()}
Font Family: {font_manager.get_font_family()}
Available Weights: {', '.join(font_manager.get_available_weights())}
Cache Size: {len(font_manager.font_cache)} fonts cached

Nếu bạn thấy text này hiển thị với font SVN Poppins đẹp mắt, 
tức là font đã được load thành công! 🎉"""
    
    info_text.insert(1.0, info_content)
    info_text.config(state=tk.DISABLED)
    
    print("🖥️ Font test window opened. Close window to exit.")
    root.mainloop()

if __name__ == "__main__":
    test_font() 