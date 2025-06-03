"""
Module quản lý single instance cho ứng dụng Auto Text & Image
"""
import os
import sys
import time
import tempfile
import socket
from typing import Optional

# Import fcntl chỉ trên Unix/Linux
if os.name != 'nt':
    import fcntl

class SingleInstance:
    """Class quản lý single instance của ứng dụng"""
    
    def __init__(self, app_name: str = "AutoTextImage"):
        self.app_name = app_name
        self.lock_file_path = os.path.join(tempfile.gettempdir(), f"{app_name}.lock")
        self.socket_path = os.path.join(tempfile.gettempdir(), f"{app_name}.sock")
        self.lock_file = None
        self.socket_server = None
        self.is_locked = False
        
    def __enter__(self):
        """Context manager entry"""
        return self.acquire_lock()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.release_lock()
        
    def acquire_lock(self) -> bool:
        """
        Thử acquire lock. 
        Returns True nếu thành công (là instance duy nhất)
        Returns False nếu đã có instance khác đang chạy
        """
        try:
            # Tạo file lock
            self.lock_file = open(self.lock_file_path, 'w')
            
            # Thử lock file (non-blocking)
            if os.name == 'nt':  # Windows
                import msvcrt
                try:
                    msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                    self.is_locked = True
                except IOError:
                    self.lock_file.close()
                    return False
            else:  # Unix/Linux
                try:
                    fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    self.is_locked = True
                except IOError:
                    self.lock_file.close()
                    return False
            
            # Ghi PID vào file
            self.lock_file.write(str(os.getpid()))
            self.lock_file.flush()
            
            # Tạo socket server để nhận signal từ instance khác
            self._create_socket_server()
            
            print(f"🔒 Acquired single instance lock: {self.lock_file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error acquiring lock: {e}")
            return False
    
    def release_lock(self):
        """Giải phóng lock"""
        try:
            if self.socket_server:
                self.socket_server.close()
                self.socket_server = None
                
            if self.lock_file and self.is_locked:
                if os.name == 'nt':  # Windows
                    import msvcrt
                    try:
                        msvcrt.locking(self.lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                    except:
                        pass
                else:  # Unix/Linux
                    try:
                        fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                    except:
                        pass
                
                self.lock_file.close()
                self.is_locked = False
                
            # Xóa file lock
            if os.path.exists(self.lock_file_path):
                try:
                    os.remove(self.lock_file_path)
                    print(f"🔓 Released single instance lock")
                except:
                    pass
                    
            # Xóa socket file nếu có
            if os.path.exists(self.socket_path):
                try:
                    os.remove(self.socket_path)
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Error releasing lock: {e}")
    
    def _create_socket_server(self):
        """Tạo socket server để nhận signal từ instance khác"""
        try:
            # Xóa socket file cũ nếu có
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)
            
            if os.name == 'nt':  # Windows - sử dụng TCP socket
                self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_server.bind(('localhost', 0))  # Port ngẫu nhiên
                port = self.socket_server.getsockname()[1]
                
                # Ghi port vào file để instance khác biết
                with open(self.socket_path, 'w') as f:
                    f.write(str(port))
            else:  # Unix/Linux - sử dụng Unix socket
                self.socket_server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.socket_server.bind(self.socket_path)
            
            self.socket_server.listen(1)
            self.socket_server.settimeout(0.1)  # Non-blocking
            
        except Exception as e:
            print(f"❌ Error creating socket server: {e}")
            self.socket_server = None
    
    def check_for_show_signal(self) -> bool:
        """
        Kiểm tra xem có signal từ instance khác không
        Returns True nếu cần hiện cửa sổ
        """
        if not self.socket_server:
            return False
            
        try:
            conn, addr = self.socket_server.accept()
            data = conn.recv(1024).decode('utf-8')
            conn.close()
            
            if data == "SHOW_WINDOW":
                print("📢 Received show window signal from another instance")
                return True
                
        except socket.timeout:
            pass  # No connection, that's fine
        except Exception as e:
            print(f"❌ Error checking signal: {e}")
            
        return False
    
    def send_show_signal(self) -> bool:
        """
        Gửi signal để hiện cửa sổ của instance đang chạy
        Returns True nếu gửi thành công
        """
        try:
            if os.name == 'nt':  # Windows
                if not os.path.exists(self.socket_path):
                    return False
                    
                with open(self.socket_path, 'r') as f:
                    port = int(f.read().strip())
                
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('localhost', port))
            else:  # Unix/Linux
                if not os.path.exists(self.socket_path):
                    return False
                    
                client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client_socket.connect(self.socket_path)
            
            client_socket.send("SHOW_WINDOW".encode('utf-8'))
            client_socket.close()
            
            print("📢 Sent show window signal to running instance")
            return True
            
        except Exception as e:
            print(f"❌ Error sending signal: {e}")
            return False
    
    def is_another_instance_running(self) -> bool:
        """Kiểm tra xem có instance khác đang chạy không"""
        return os.path.exists(self.lock_file_path)

def ensure_single_instance(app_name: str = "AutoTextImage") -> Optional[SingleInstance]:
    """
    Đảm bảo chỉ có 1 instance chạy
    Returns SingleInstance object nếu là instance duy nhất
    Returns None nếu đã có instance khác chạy
    """
    instance = SingleInstance(app_name)
    
    if instance.acquire_lock():
        return instance
    else:
        # Thử gửi signal để hiện cửa sổ instance đang chạy
        if instance.send_show_signal():
            print("✅ Signaled existing instance to show window")
        else:
            print("⚠️ Another instance is running but couldn't signal it")
        
        return None 