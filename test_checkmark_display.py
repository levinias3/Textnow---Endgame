#!/usr/bin/env python3
"""
Test script để kiểm tra hiển thị checkmark trong radio buttons và checkbox
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QRadioButton, QCheckBox, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

def test_checkmark_display():
    """Test hiển thị checkmark với đường dẫn tuyệt đối"""
    
    app = QApplication(sys.argv)
    
    # Get absolute paths
    project_root = Path(__file__).parent
    checkmark_path = project_root / "checkmark.png"
    checkmark_vector_path = project_root / "checkmark_vector.png"
    
    print(f"🧪 Testing checkmark display:")
    print(f"  Project root: {project_root}")
    print(f"  Checkmark radio: {checkmark_path} {'✅' if checkmark_path.exists() else '❌'}")
    print(f"  Checkmark checkbox: {checkmark_vector_path} {'✅' if checkmark_vector_path.exists() else '❌'}")
    
    # Convert to simple absolute paths for CSS
    checkmark_path_str = str(checkmark_path).replace('\\', '/') if checkmark_path.exists() else ""
    checkmark_vector_path_str = str(checkmark_vector_path).replace('\\', '/') if checkmark_vector_path.exists() else ""
    
    print(f"  Radio path: {checkmark_path_str}")
    print(f"  Checkbox path: {checkmark_vector_path_str}")
    
    # Create main window
    window = QMainWindow()
    window.setWindowTitle("Checkmark Display Test")
    window.setFixedSize(400, 300)
    
    # Central widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    
    # Radio buttons với checkmark
    if checkmark_path_str:
        radio_style = f"""
        QRadioButton {{
          font-size: 16px;
          font-weight: 500;
          color: #374151;
          spacing: 12px;
          padding: 8px 16px;
          min-height: 40px;
        }}
        QRadioButton::indicator {{
          width: 20px;
          height: 20px;
          border-radius: 4px;
          border: 2px solid #D1D5DB;
          background-color: #FFFFFF;
        }}
        QRadioButton::indicator:checked {{
          background-color: #3B82F6;
          border-color: #3B82F6;
          image: url("{checkmark_path_str}");
        }}
        QRadioButton::indicator:hover {{
          border-color: #9CA3AF;
        }}
        QRadioButton:checked {{
          color: #3B82F6;
          font-weight: 600;
        }}
        """
        
        radio1 = QRadioButton("Radio 1 (Văn bản)")
        radio1.setStyleSheet(radio_style)
        radio1.setChecked(True)
        layout.addWidget(radio1)
        
        radio2 = QRadioButton("Radio 2 (Hình ảnh)")
        radio2.setStyleSheet(radio_style)
        layout.addWidget(radio2)
        
        radio3 = QRadioButton("Radio 3 (Văn bản + Ảnh)")
        radio3.setStyleSheet(radio_style)
        layout.addWidget(radio3)
    
    # Checkbox với checkmark_vector
    if checkmark_vector_path_str:
        checkbox_style = f"""
        QCheckBox {{
          font-size: 16px;
          font-weight: 500;
          color: #374151;
          spacing: 12px;
          padding: 8px 16px;
          min-height: 40px;
        }}
        QCheckBox::indicator {{
          width: 20px;
          height: 20px;
          border-radius: 4px;
          border: 2px solid #D1D5DB;
          background-color: #FFFFFF;
        }}
        QCheckBox::indicator:checked {{
          background-color: #3B82F6;
          border-color: #3B82F6;
          image: url("{checkmark_vector_path_str}");
        }}
        QCheckBox::indicator:hover {{
          border-color: #9CA3AF;
        }}
        QCheckBox:checked {{
          color: #3B82F6;
          font-weight: 600;
        }}
        """
        
        checkbox = QCheckBox("Kích hoạt shortcut")
        checkbox.setStyleSheet(checkbox_style)
        checkbox.setChecked(True)
        layout.addWidget(checkbox)
    
    # Exit button
    exit_btn = QPushButton("Đóng Test")
    exit_btn.clicked.connect(app.quit)
    layout.addWidget(exit_btn)
    
    # Show window
    window.show()
    
    print("\n✅ Test window opened - Check if checkmarks are visible!")
    print("  • Radio buttons should show checkmark when selected")
    print("  • Checkbox should show checkmark when checked")
    print("  • Both should have blue background when active")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_checkmark_display()) 