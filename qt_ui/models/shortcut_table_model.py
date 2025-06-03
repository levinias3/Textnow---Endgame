"""
Model cho bảng hiển thị shortcuts với tô màu trạng thái
"""
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide6.QtGui import QColor
from typing import List, Dict, Any


class ShortcutTableModel(QAbstractTableModel):
    """Model cho bảng shortcuts với tô màu trạng thái"""
    
    def __init__(self, shortcuts: List[Dict[str, Any]] = None):
        super().__init__()
        self._shortcuts = shortcuts or []
        self._headers = ["Shortcut", "Loại", "Nội dung", "Trạng thái"]
        
        # Màu sắc trạng thái
        self.COLOR_ACTIVE = QColor("#34B369")  # Xanh lá
        self.COLOR_INACTIVE = QColor("#FC6157")  # Đỏ
        
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Số dòng trong bảng"""
        return len(self._shortcuts)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Số cột trong bảng"""
        return len(self._headers)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """Dữ liệu cho từng cell"""
        if not index.isValid() or index.row() >= len(self._shortcuts):
            return None
            
        shortcut = self._shortcuts[index.row()]
        column = index.column()
        
        if role == Qt.DisplayRole:
            if column == 0:  # Shortcut
                return shortcut.get('keyword', '')
            elif column == 1:  # Loại
                shortcut_type = shortcut.get('type', 'text')
                if shortcut_type == 'mixed':
                    return "Văn bản + Ảnh"
                elif shortcut_type in ['text', 'richtext']:
                    return "Văn bản"
                else:
                    return "Hình ảnh"
            elif column == 2:  # Nội dung
                content = shortcut.get('content', '')
                if isinstance(content, dict):
                    # Mixed content
                    text_part = content.get('text', '')
                    images_count = len(content.get('images', []))
                    if text_part and len(text_part) > 30:
                        text_part = text_part[:27] + "..."
                    return f"{text_part} + {images_count} ảnh" if images_count > 0 else text_part
                elif isinstance(content, str) and len(content) > 40:
                    return content[:37] + "..."
                return content
            elif column == 3:  # Trạng thái
                return "Bật" if shortcut.get('enabled', True) else "Tắt"
                
        elif role == Qt.ForegroundRole:
            if column == 3:  # Tô màu cột trạng thái
                is_active = shortcut.get('enabled', True)
                return self.COLOR_ACTIVE if is_active else self.COLOR_INACTIVE
                
        elif role == Qt.FontRole:
            if column == 3:  # Bold cho cột trạng thái
                from PySide6.QtGui import QFont
                font = QFont()
                font.setBold(True)
                return font
                
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        """Header của bảng"""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section < len(self._headers):
                return self._headers[section]
        return None
    
    def setShortcuts(self, shortcuts: List[Dict[str, Any]]):
        """Cập nhật danh sách shortcuts"""
        self.beginResetModel()
        self._shortcuts = shortcuts
        self.endResetModel()
    
    def getShortcut(self, index: int) -> Dict[str, Any]:
        """Lấy shortcut theo index"""
        if 0 <= index < len(self._shortcuts):
            return self._shortcuts[index]
        return {}
    
    def getAllShortcuts(self) -> List[Dict[str, Any]]:
        """Lấy tất cả shortcuts"""
        return self._shortcuts.copy() 