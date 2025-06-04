#!/usr/bin/env python3
"""
Test script để verify config functionality và shortcuts.json
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit
from PySide6.QtCore import Qt

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.config import Config

class ConfigTestWindow(QMainWindow):
    """Test window cho config functionality"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Config & Shortcuts.json Test")
        self.setFixedSize(600, 400)
        
        # Initialize config
        self.config = Config()
        
        self._setup_ui()
        self._refresh_display()
    
    def _setup_ui(self):
        """Setup test UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🧪 CONFIG & SHORTCUTS.JSON TEST")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #3B82F6; padding: 10px;")
        layout.addWidget(title)
        
        # Config file path
        self.path_label = QLabel()
        self.path_label.setStyleSheet("color: #6B7280; padding: 5px;")
        layout.addWidget(self.path_label)
        
        # Shortcuts display
        self.shortcuts_display = QTextEdit()
        self.shortcuts_display.setReadOnly(True)
        self.shortcuts_display.setMaximumHeight(150)
        layout.addWidget(self.shortcuts_display)
        
        # Add new shortcut form
        form_layout = QVBoxLayout()
        
        form_title = QLabel("📝 Add New Shortcut:")
        form_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form_layout.addWidget(form_title)
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Enter keyword (e.g., 'test')")
        form_layout.addWidget(self.keyword_input)
        
        self.content_input = QLineEdit()
        self.content_input.setPlaceholderText("Enter content (e.g., 'This is a test shortcut')")
        form_layout.addWidget(self.content_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QVBoxLayout()
        
        self.add_btn = QPushButton("➕ Add Shortcut")
        self.add_btn.clicked.connect(self._add_shortcut)
        self.add_btn.setStyleSheet("background-color: #10B981; color: white; padding: 8px; font-weight: bold;")
        buttons_layout.addWidget(self.add_btn)
        
        self.refresh_btn = QPushButton("🔄 Refresh Display")
        self.refresh_btn.clicked.connect(self._refresh_display)
        buttons_layout.addWidget(self.refresh_btn)
        
        self.delete_last_btn = QPushButton("🗑️ Delete Last Shortcut")
        self.delete_last_btn.clicked.connect(self._delete_last)
        self.delete_last_btn.setStyleSheet("background-color: #EF4444; color: white; padding: 8px; font-weight: bold;")
        buttons_layout.addWidget(self.delete_last_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: #6B7280; padding: 5px;")
        layout.addWidget(self.status_label)
    
    def _refresh_display(self):
        """Refresh shortcuts display"""
        try:
            # Update path
            self.path_label.setText(f"📁 Config file: {self.config.config_file}")
            
            # Check if file exists
            file_exists = Path(self.config.config_file).exists()
            self.path_label.setText(
                self.path_label.text() + f" {'✅' if file_exists else '❌'}"
            )
            
            # Get shortcuts
            shortcuts = self.config.get_shortcuts()
            count = len(shortcuts)
            
            # Display shortcuts
            display_text = f"📋 Found {count} shortcuts:\n\n"
            
            if shortcuts:
                for i, shortcut in enumerate(shortcuts):
                    keyword = shortcut.get('keyword', 'N/A')
                    type_str = shortcut.get('type', 'text')
                    content = shortcut.get('content', '')
                    enabled = shortcut.get('enabled', True)
                    
                    # Truncate long content
                    if len(content) > 50:
                        content = content[:47] + "..."
                    
                    status = "🟢" if enabled else "🔴"
                    display_text += f"{i+1}. {status} '{keyword}' ({type_str})\n"
                    display_text += f"   → {content}\n\n"
            else:
                display_text += "No shortcuts found."
            
            self.shortcuts_display.setPlainText(display_text)
            
            # Update status
            self.status_label.setText(f"✅ Loaded {count} shortcuts • File: {'exists' if file_exists else 'missing'}")
            
        except Exception as e:
            self.status_label.setText(f"❌ Error: {e}")
            print(f"❌ Refresh error: {e}")
    
    def _add_shortcut(self):
        """Add new shortcut"""
        try:
            keyword = self.keyword_input.text().strip()
            content = self.content_input.text().strip()
            
            if not keyword or not content:
                self.status_label.setText("⚠️ Please enter both keyword and content")
                return
            
            success = self.config.add_shortcut(keyword, content, "text", True)
            
            if success:
                self.status_label.setText(f"✅ Added shortcut: '{keyword}'")
                self.keyword_input.clear()
                self.content_input.clear()
                self._refresh_display()
            else:
                self.status_label.setText(f"❌ Failed to add shortcut (may already exist)")
                
        except Exception as e:
            self.status_label.setText(f"❌ Add error: {e}")
            print(f"❌ Add shortcut error: {e}")
    
    def _delete_last(self):
        """Delete last shortcut"""
        try:
            shortcuts = self.config.get_shortcuts()
            if not shortcuts:
                self.status_label.setText("⚠️ No shortcuts to delete")
                return
            
            last_index = len(shortcuts) - 1
            last_keyword = shortcuts[last_index].get('keyword', 'N/A')
            
            success = self.config.delete_shortcut(last_index)
            
            if success:
                self.status_label.setText(f"✅ Deleted shortcut: '{last_keyword}'")
                self._refresh_display()
            else:
                self.status_label.setText(f"❌ Failed to delete shortcut")
                
        except Exception as e:
            self.status_label.setText(f"❌ Delete error: {e}")
            print(f"❌ Delete shortcut error: {e}")

def main():
    """Main test function"""
    print("🧪 Testing Config & Shortcuts.json functionality...")
    
    app = QApplication(sys.argv)
    
    window = ConfigTestWindow()
    window.show()
    
    print("✅ Test window opened")
    print("📋 Test checklist:")
    print("  1. Check config file path is correct")
    print("  2. Verify shortcuts.json is loaded/created")
    print("  3. Add new shortcut and verify it saves")
    print("  4. Delete shortcut and verify it's removed")
    print("  5. Refresh to verify persistence")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 