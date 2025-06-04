"""
Module xử lý cấu hình cho ứng dụng Auto Text & Image
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any

class Config:
    def __init__(self, config_file: str = "shortcuts.json"):
        # Always use absolute path relative to script location
        if not os.path.isabs(config_file):
            # Get the directory where the main script is located
            script_dir = Path(__file__).parent.parent
            self.config_file = str(script_dir / config_file)
        else:
        self.config_file = config_file
            
        self.shortcuts = []
        print(f"📁 Config file path: {self.config_file}")
        self.load()
    
    def load(self) -> bool:
        """Tải cấu hình từ file JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.shortcuts = data.get('shortcuts', [])
                return True
            else:
                # Tạo file cấu hình mặc định nếu không tồn tại
                self.save()
                return True
        except Exception as e:
            print(f"Lỗi khi tải cấu hình: {e}")
            return False
    
    def save(self) -> bool:
        """Lưu cấu hình xuống file JSON"""
        try:
            data = {
                'shortcuts': self.shortcuts
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu cấu hình: {e}")
            return False
    
    def get_shortcuts(self) -> List[Dict[str, Any]]:
        """Lấy danh sách shortcuts"""
        return self.shortcuts
    
    def add_shortcut(self, keyword: str, content: str, type: str = "text", enabled: bool = True) -> bool:
        """Thêm shortcut mới"""
        # Kiểm tra xem keyword đã tồn tại chưa
        for shortcut in self.shortcuts:
            if shortcut['keyword'] == keyword:
                return False
        
        self.shortcuts.append({
            'keyword': keyword,
            'type': type,
            'content': content,
            'enabled': enabled
        })
        return self.save()
    
    def update_shortcut(self, index: int, keyword: str, content: str, type: str = "text", enabled: bool = True) -> bool:
        """Cập nhật shortcut"""
        if 0 <= index < len(self.shortcuts):
            self.shortcuts[index] = {
                'keyword': keyword,
                'type': type,
                'content': content,
                'enabled': enabled
            }
            return self.save()
        return False
    
    def delete_shortcut(self, index: int) -> bool:
        """Xóa shortcut"""
        if 0 <= index < len(self.shortcuts):
            del self.shortcuts[index]
            return self.save()
        return False
    
    def import_config(self, file_path: str) -> bool:
        """Import cấu hình từ file khác"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.shortcuts = data.get('shortcuts', [])
            return self.save()
        except Exception as e:
            print(f"Lỗi khi import cấu hình: {e}")
            return False
    
    def export_config(self, file_path: str) -> bool:
        """Export cấu hình ra file khác"""
        try:
            data = {
                'shortcuts': self.shortcuts
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Lỗi khi export cấu hình: {e}")
            return False 