"""
Module xử lý cấu hình cho ứng dụng Auto Text & Image
"""
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

class Config:
    def __init__(self, config_file: str = "shortcuts.json"):
        # EXE-optimized path handling
        if not os.path.isabs(config_file):
            # Determine the correct directory for config files
            if getattr(sys, 'frozen', False):
                # Running as exe - use exe directory for user data
                app_dir = Path(sys.executable).parent
            else:
                # Running as script - use script directory
                app_dir = Path(__file__).parent.parent
            
            self.config_file = str(app_dir / config_file)
        else:
            self.config_file = config_file
            
        self.shortcuts = []
        print(f"📁 Config file path: {self.config_file}")
        
        # Ensure directory exists
        config_dir = Path(self.config_file).parent
        config_dir.mkdir(parents=True, exist_ok=True)
        
        self.load()
    
    def load(self) -> bool:
        """Tải cấu hình từ file JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.shortcuts = data.get('shortcuts', [])
                print(f"✅ Loaded {len(self.shortcuts)} shortcuts from config")
                return True
            else:
                # Tạo file cấu hình mặc định nếu không tồn tại
                print("📝 Creating default config file")
                self._create_default_config()
                self.save()
                return True
        except Exception as e:
            print(f"❌ Lỗi khi tải cấu hình: {e}")
            # Create default config on error
            self._create_default_config()
            return False
    
    def _create_default_config(self):
        """Tạo cấu hình mặc định với một số shortcuts demo"""
        self.shortcuts = [
            {
                "keyword": "tên",
                "type": "text",
                "content": "Nguyễn Văn A",
                "enabled": True
            },
            {
                "keyword": "mail",
                "type": "text", 
                "content": "nguyenvana@email.com",
                "enabled": True
            },
            {
                "keyword": "sdt",
                "type": "text",
                "content": "0123456789",
                "enabled": True
            },
            {
                "keyword": "địa chỉ",
                "type": "text",
                "content": "123 Đường ABC, Quận XYZ, TP.HCM",
                "enabled": True
            }
        ]
    
    def save(self) -> bool:
        """Lưu cấu hình xuống file JSON"""
        try:
            data = {
                'shortcuts': self.shortcuts
            }
            # Ensure directory exists before saving
            config_dir = Path(self.config_file).parent
            config_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"💾 Saved {len(self.shortcuts)} shortcuts to config")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi lưu cấu hình: {e}")
            return False
    
    def get_shortcuts(self) -> List[Dict[str, Any]]:
        """Lấy danh sách shortcuts"""
        return self.shortcuts
    
    def add_shortcut(self, keyword: str, content: str, type: str = "text", enabled: bool = True) -> bool:
        """Thêm shortcut mới"""
        # Kiểm tra xem keyword đã tồn tại chưa
        for shortcut in self.shortcuts:
            if shortcut['keyword'] == keyword:
                print(f"⚠️ Keyword '{keyword}' already exists")
                return False
        
        new_shortcut = {
            'keyword': keyword,
            'type': type,
            'content': content,
            'enabled': enabled
        }
        
        self.shortcuts.append(new_shortcut)
        success = self.save()
        if success:
            print(f"✅ Added shortcut: {keyword}")
        return success
    
    def update_shortcut(self, index: int, keyword: str, content: str, type: str = "text", enabled: bool = True) -> bool:
        """Cập nhật shortcut"""
        if 0 <= index < len(self.shortcuts):
            old_keyword = self.shortcuts[index]['keyword']
            self.shortcuts[index] = {
                'keyword': keyword,
                'type': type,
                'content': content,
                'enabled': enabled
            }
            success = self.save()
            if success:
                print(f"✅ Updated shortcut: {old_keyword} -> {keyword}")
            return success
        else:
            print(f"❌ Invalid index: {index}")
            return False
    
    def delete_shortcut(self, index: int) -> bool:
        """Xóa shortcut"""
        if 0 <= index < len(self.shortcuts):
            deleted_keyword = self.shortcuts[index]['keyword']
            del self.shortcuts[index]
            success = self.save()
            if success:
                print(f"✅ Deleted shortcut: {deleted_keyword}")
            return success
        else:
            print(f"❌ Invalid index: {index}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Import cấu hình từ file khác"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                imported_shortcuts = data.get('shortcuts', [])
                self.shortcuts = imported_shortcuts
            success = self.save()
            if success:
                print(f"✅ Imported {len(imported_shortcuts)} shortcuts")
            return success
        except Exception as e:
            print(f"❌ Lỗi khi import cấu hình: {e}")
            return False
    
    def export_config(self, file_path: str) -> bool:
        """Export cấu hình ra file khác"""
        try:
            data = {
                'shortcuts': self.shortcuts
            }
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ Exported {len(self.shortcuts)} shortcuts to {file_path}")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi export cấu hình: {e}")
            return False 