#!/usr/bin/env python3
"""
Script test kiểm tra icon chất lượng cao cho TextNow
"""
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap, QAction

class IconTestWindow(QMainWindow):
    """Window test icon"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextNow - Icon Quality Test")
        self.setFixedSize(600, 500)
        
        # Test icon cho window
        self._test_window_icon()
        
        # Setup UI
        self._setup_ui()
        
        # Test system tray sau 1 giây
        QTimer.singleShot(1000, self._test_system_tray)
    
    def _test_window_icon(self):
        """Test window icon"""
        print("🪟 Testing window icons...")
        
        base_path = Path(__file__).parent
        icon_candidates = [
            base_path / "icons" / "icon_256x256.png",  # Chất lượng cao nhất
            base_path / "icons" / "icon_128x128.png",  # Chất lượng cao
            base_path / "icons" / "icon_64x64.png",    # Chất lượng trung bình
            base_path / "icon.png",                    # Fallback
            base_path / "app.ico"                      # ICO fallback
        ]
        
        for icon_path in icon_candidates:
            if icon_path.exists():
                try:
                    icon = QIcon(str(icon_path))
                    if not icon.isNull():
                        self.setWindowIcon(icon)
                        print(f"✅ Window icon set: {icon_path.name}")
                        return
                    else:
                        print(f"⚠️ Icon null: {icon_path.name}")
                except Exception as e:
                    print(f"❌ Error loading {icon_path.name}: {e}")
        
        print("❌ No valid window icon found!")
    
    def _setup_ui(self):
        """Setup test UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🔍 ICON QUALITY TEST")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #3B82F6; padding: 20px;")
        layout.addWidget(title)
        
        # Test window icon
        self._test_icon_display(layout, "Window Icon Test", "icons/icon_256x256.png")
        self._test_icon_display(layout, "Logo Test", "logos/logo_128x128.png") 
        self._test_icon_display(layout, "Small Icon Test", "icons/icon_32x32.png")
        
        # ICO test
        ico_path = Path("app.ico")
        if ico_path.exists():
            ico_label = QLabel("✅ app.ico file exists")
            ico_label.setStyleSheet("color: green; padding: 5px;")
            layout.addWidget(ico_label)
        else:
            ico_label = QLabel("❌ app.ico file missing!")
            ico_label.setStyleSheet("color: red; padding: 5px;")
            layout.addWidget(ico_label)
        
        # Test tray button
        tray_btn = QPushButton("Test System Tray Icon")
        tray_btn.clicked.connect(self._test_system_tray)
        layout.addWidget(tray_btn)
        
        # Close button
        close_btn = QPushButton("Close Test")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
    
    def _test_icon_display(self, layout, title, icon_path):
        """Test hiển thị một icon"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; margin: 10px 0 5px 0;")
        container_layout.addWidget(title_label)
        
        # Icon display
        icon_widget = QWidget()
        icon_layout = QVBoxLayout(icon_widget)
        
        full_path = Path(icon_path)
        if full_path.exists():
            try:
                # Load và hiển thị icon
                pixmap = QPixmap(str(full_path))
                if not pixmap.isNull():
                    # Scale to display size (64x64)
                    scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    icon_label = QLabel()
                    icon_label.setPixmap(scaled_pixmap)
                    icon_label.setAlignment(Qt.AlignCenter)
                    icon_layout.addWidget(icon_label)
                    
                    # Info
                    info_text = f"✅ {full_path.name} ({pixmap.width()}x{pixmap.height()}) - {full_path.stat().st_size/1024:.1f}KB"
                    info_label = QLabel(info_text)
                    info_label.setStyleSheet("color: green; font-size: 11px;")
                    icon_layout.addWidget(info_label)
                else:
                    error_label = QLabel(f"❌ Cannot load pixmap: {full_path.name}")
                    error_label.setStyleSheet("color: red;")
                    icon_layout.addWidget(error_label)
            except Exception as e:
                error_label = QLabel(f"❌ Error: {e}")
                error_label.setStyleSheet("color: red;")
                icon_layout.addWidget(error_label)
        else:
            missing_label = QLabel(f"❌ File not found: {icon_path}")
            missing_label.setStyleSheet("color: red;")
            icon_layout.addWidget(missing_label)
        
        container_layout.addWidget(icon_widget)
        layout.addWidget(container)
    
    def _test_system_tray(self):
        """Test system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("⚠️ System tray not available")
            return
        
        print("📱 Testing system tray icons...")
        
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self)
        
        # Test various icon sizes
        base_path = Path(__file__).parent
        tray_icon_candidates = [
            base_path / "icons" / "icon_32x32.png",    # Tối ưu cho system tray
            base_path / "icons" / "icon_20x20.png",    # Kích thước chuẩn tray
            base_path / "icons" / "icon_24x24.png",    # Alternative tray size
            base_path / "icon.png",                    # Fallback
            base_path / "app.ico"                      # ICO fallback
        ]
        
        tray_icon_set = False
        for icon_path in tray_icon_candidates:
            if icon_path.exists():
                try:
                    icon = QIcon(str(icon_path))
                    if not icon.isNull():
                        self.tray_icon.setIcon(icon)
                        print(f"✅ Tray icon set: {icon_path.name}")
                        tray_icon_set = True
                        break
                    else:
                        print(f"⚠️ Tray icon null: {icon_path.name}")
                except Exception as e:
                    print(f"❌ Tray icon error {icon_path.name}: {e}")
        
        if not tray_icon_set:
            # Fallback to default icon
            self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
            print("✅ Tray icon set: default fallback")
        
        # Create context menu
        tray_menu = QMenu()
        
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        test_action = QAction("Icon Test Successful!", self)
        test_action.setEnabled(False)
        tray_menu.addAction(test_action)
        
        tray_menu.addSeparator()
        
        exit_action = QAction("Exit Test", self)
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("TextNow - Icon Quality Test")
        
        # Show tray icon
        self.tray_icon.show()
        
        # Show notification
        self.tray_icon.showMessage(
            "Icon Test",
            "System tray icon displayed! Right-click to test menu.",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )
        
        print("✅ System tray icon test completed")

def main():
    """Main test function"""
    print("🚀 Testing TextNow high-quality icons...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("TextNow Icon Test")
    app.setQuitOnLastWindowClosed(False)  # Keep running for tray test
    
    # Create test window
    window = IconTestWindow()
    window.show()
    
    print("\n📋 Icon Test Checklist:")
    print("  1. ✅ Window icon in taskbar (high quality)")
    print("  2. ✅ System tray icon (optimized size)")  
    print("  3. ✅ Icon display in window")
    print("  4. ✅ Multi-size support")
    print("  5. ✅ Fallback mechanism")
    
    print("\n🔍 Check results:")
    print("  • Taskbar: Window should show high-quality icon")
    print("  • System tray: Icon should appear crisp and clear")
    print("  • Window: Icons should display without pixelation")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 