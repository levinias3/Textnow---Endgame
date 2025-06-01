"""
Module xử lý việc tự khởi động cùng Windows
"""
import os
import sys
import win32com.client

def get_startup_folder():
    """Lấy đường dẫn thư mục Startup của Windows"""
    return os.path.join(os.environ['APPDATA'], 
                       'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

def get_shortcut_path():
    """Lấy đường dẫn file shortcut trong thư mục Startup"""
    return os.path.join(get_startup_folder(), 'AutoTextImage.lnk')

def is_autostart_enabled():
    """Kiểm tra xem ứng dụng có được cài đặt tự khởi động không"""
    return os.path.exists(get_shortcut_path())

def enable_autostart():
    """Bật tự khởi động cùng Windows"""
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(get_shortcut_path())
        
        # Lấy đường dẫn đến file exe hoặc python script
        if getattr(sys, 'frozen', False):
            # Đang chạy từ file exe được build bởi PyInstaller
            target_path = sys.executable
        else:
            # Đang chạy từ Python script
            target_path = sys.executable
            shortcut.Arguments = f'"{os.path.abspath("main.py")}"'
        
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))
        shortcut.IconLocation = target_path
        shortcut.Description = "Auto Text & Image - Ứng dụng gõ tắt thông minh"
        shortcut.save()
        
        return True
    except Exception as e:
        print(f"Lỗi khi bật tự khởi động: {e}")
        return False

def disable_autostart():
    """Tắt tự khởi động cùng Windows"""
    try:
        shortcut_path = get_shortcut_path()
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
        return True
    except Exception as e:
        print(f"Lỗi khi tắt tự khởi động: {e}")
        return False

def toggle_autostart():
    """Bật/tắt tự khởi động"""
    if is_autostart_enabled():
        return disable_autostart()
    else:
        return enable_autostart() 