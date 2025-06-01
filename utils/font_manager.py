"""
Module quản lý font SVN Poppins cho ứng dụng
"""
import os
import tkinter as tk
from tkinter import font as tkFont
import platform

class FontManager:
    """Quản lý font SVN Poppins"""
    
    def __init__(self):
        self.fonts_loaded = False
        self.font_cache = {}
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.font_dir = os.path.join(self.base_path, "fonts", "SVN-Poppins (18 fonts) + webfonts", "TTF")
        
        # Font weights mapping
        self.font_weights = {
            'thin': 'SVN-Poppins-Thin.ttf',
            'extralight': 'SVN-Poppins-ExtraLight.ttf', 
            'light': 'SVN-Poppins-Light.ttf',
            'regular': 'SVN-Poppins-Regular.ttf',
            'medium': 'SVN-Poppins-Medium.ttf',
            'semibold': 'SVN-Poppins-SemiBold.ttf',
            'bold': 'SVN-Poppins-Bold.ttf',
            'extrabold': 'SVN-Poppins-ExtraBold.ttf',
            'black': 'SVN-Poppins-Black.ttf'
        }
        
        self._load_fonts()
    
    def _load_fonts(self):
        """Load font SVN Poppins vào hệ thống"""
        try:
            if not os.path.exists(self.font_dir):
                print(f"⚠️ Thư mục font không tồn tại: {self.font_dir}")
                return False
            
            # Kiểm tra OS để load font phù hợp
            if platform.system() == "Windows":
                self._load_fonts_windows()
            else:
                self._load_fonts_unix()
            
            self.fonts_loaded = True
            print("✅ Đã load font SVN Poppins thành công!")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi load font SVN Poppins: {e}")
            return False
    
    def _load_fonts_windows(self):
        """Load fonts trên Windows"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Load AddFontResourceEx API
            gdi32 = ctypes.windll.gdi32
            gdi32.AddFontResourceExW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
            gdi32.AddFontResourceExW.restype = ctypes.c_int
            
            FR_PRIVATE = 0x10
            
            # Load từng font file
            loaded_count = 0
            for weight, filename in self.font_weights.items():
                font_path = os.path.join(self.font_dir, filename)
                if os.path.exists(font_path):
                    result = gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
                    if result > 0:
                        loaded_count += 1
                        print(f"🔤 Loaded font: {filename}")
                    else:
                        print(f"⚠️ Không thể load font: {filename}")
            
            print(f"✅ Đã load {loaded_count}/{len(self.font_weights)} font SVN Poppins")
            
        except Exception as e:
            print(f"❌ Lỗi khi load font Windows: {e}")
    
    def _load_fonts_unix(self):
        """Load fonts trên Unix/Linux (fallback)"""
        # Với Unix, font sẽ được load thông qua tkinter font
        print("💡 Đang chạy trên Unix/Linux - sử dụng fallback method")
    
    def get_font(self, size=10, weight='regular', italic=False):
        """
        Lấy font SVN Poppins với size và weight chỉ định
        
        Args:
            size: Kích thước font (default: 10)
            weight: Trọng lượng font (thin, light, regular, medium, semibold, bold, black)
            italic: Có sử dụng italic không (default: False)
        
        Returns:
            tuple: (font_family, size, style)
        """
        cache_key = f"{size}_{weight}_{italic}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        # Tạo font tuple cho tkinter
        family = "SVN-Poppins"
        
        # Mapping weight to tkinter weight
        weight_map = {
            'thin': 'normal',
            'extralight': 'normal', 
            'light': 'normal',
            'regular': 'normal',
            'medium': 'normal',
            'semibold': 'bold',
            'bold': 'bold',
            'extrabold': 'bold',
            'black': 'bold'
        }
        
        tk_weight = weight_map.get(weight, 'normal')
        style = []
        
        if tk_weight == 'bold':
            style.append('bold')
        if italic:
            style.append('italic')
        
        if not style:
            style = ['normal']
        
        # Tạo font tuple
        font_tuple = (family, size, ' '.join(style))
        
        # Cache để tăng tốc
        self.font_cache[cache_key] = font_tuple
        
        return font_tuple
    
    def get_font_family(self):
        """Lấy tên font family"""
        return "SVN-Poppins" if self.fonts_loaded else "Segoe UI"
    
    def is_loaded(self):
        """Kiểm tra font đã được load chưa"""
        return self.fonts_loaded
    
    def get_available_weights(self):
        """Lấy danh sách weights có sẵn"""
        return list(self.font_weights.keys())
    
    def create_font_object(self, size=10, weight='regular', italic=False):
        """
        Tạo font object cho tkinter
        
        Returns:
            tkinter.font.Font object
        """
        font_tuple = self.get_font(size, weight, italic)
        return tkFont.Font(family=font_tuple[0], size=font_tuple[1], weight=font_tuple[2])

# Singleton instance
_font_manager = None

def get_font_manager():
    """Lấy instance của FontManager (Singleton pattern)"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager

def get_font(size=10, weight='regular', italic=False):
    """Shortcut để lấy font tuple"""
    return get_font_manager().get_font(size, weight, italic)

def get_font_family():
    """Shortcut để lấy font family"""
    return get_font_manager().get_font_family() 