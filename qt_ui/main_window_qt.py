"""
MainWindow controller cho PySide6 - Migration từ Tkinter
"""
import os
import sys
import winreg
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                               QFileDialog, QHeaderView, QSystemTrayIcon, 
                               QMenu, QListWidget, QListWidgetItem, QVBoxLayout, 
                               QHBoxLayout, QWidget, QPushButton, QLabel)
from PySide6.QtCore import Qt, QTimer, Signal, QModelIndex
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon, QFont, QFontDatabase, QAction, QPixmap

# Import existing modules
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import Config
from core.shortcut_manager import ShortcutManager
from core.keyboard_monitor import KeyboardMonitor
from qt_ui.models.shortcut_table_model import ShortcutTableModel


class MainWindowQt(QMainWindow):
    """Main Window cho TextNow với PySide6"""
    
    # Signals
    shortcut_added = Signal(str)  # keyword
    shortcut_updated = Signal(str)  # keyword
    shortcut_deleted = Signal(str)  # keyword
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.config = Config()
        self.shortcut_manager = ShortcutManager(self.config)
        self.keyboard_monitor = None  # Initialize later
        
        # UI components
        self.ui = None
        self.table_model = None
        self.current_shortcuts = []
        self.selected_index = None
        
        # Image handling
        self.selected_images = []  # List of image paths
        self.images_listbox = None  # Will be created dynamically
        
        # System tray
        self.tray_icon = None
        
        # Setup
        self._load_fonts()
        self._load_ui()
        self._setup_ui()
        self._setup_table()
        self._setup_connections()
        self._load_shortcuts()
        
        # Delay system tray setup to avoid conflicts
        QTimer.singleShot(500, self._setup_system_tray)
        
        # Initialize keyboard monitoring (delayed further)
        QTimer.singleShot(1000, self._init_keyboard_monitoring)
        
    def _init_keyboard_monitoring(self):
        """Initialize keyboard monitoring safely"""
        try:
            print("📝 Initializing keyboard monitoring...")
            self.keyboard_monitor = KeyboardMonitor(self.shortcut_manager)
            
            # Setup callbacks
            self.keyboard_monitor.set_on_status_changed(self._on_monitoring_status_changed)
            self.shortcut_manager.set_on_shortcut_triggered(self._on_shortcut_triggered)
            
            # Start monitoring in a timer to avoid blocking (longer delay for safety)
            QTimer.singleShot(2000, self._start_monitoring)
            
            print("✅ Keyboard monitoring initialized")
        except Exception as e:
            print(f"⚠️ Keyboard monitoring init failed: {e}")
            # Continue without keyboard monitoring
            self.keyboard_monitor = None
            
    def _start_monitoring(self):
        """Start keyboard monitoring"""
        try:
            if self.keyboard_monitor:
                print("📝 Starting keyboard monitoring...")
                self.keyboard_monitor.start_monitoring()
                print("✅ Keyboard monitoring started")
        except Exception as e:
            print(f"⚠️ Failed to start monitoring: {e}")
            self.keyboard_monitor = None
        
    def _load_fonts(self):
        """Load SVN Poppins fonts"""
        try:
            fonts_dir = Path(__file__).parent.parent / "fonts"
            if fonts_dir.exists():
                for font_file in fonts_dir.glob("*.ttf"):
                    font_id = QFontDatabase.addApplicationFont(str(font_file))
                    if font_id != -1:
                        font_families = QFontDatabase.applicationFontFamilies(font_id)
                        print(f"✅ Font loaded: {font_families}")
                    else:
                        print(f"❌ Failed to load font: {font_file}")
        except Exception as e:
            print(f"⚠️ Font loading error: {e}")
    
    def _load_ui(self):
        """Load UI file"""
        try:
            ui_file = Path(__file__).parent / "forms" / "main_window.ui"
            if not ui_file.exists():
                raise FileNotFoundError(f"UI file not found: {ui_file}")
                
            loader = QUiLoader()
            ui_widget = loader.load(str(ui_file))
            self.setCentralWidget(ui_widget)
            self.ui = ui_widget
            
            print("✅ UI loaded successfully")
        except Exception as e:
            print(f"❌ UI loading error: {e}")
            QMessageBox.critical(None, "Error", f"Failed to load UI: {e}")
            sys.exit(1)
    
    def _setup_ui(self):
        """Setup UI properties"""
        # Window properties
        self.setWindowTitle("TextNow - Auto Text & Image")
        self.setFixedSize(1440, 1080)
        self._center_window()
        
        # Load and apply stylesheet
        self._load_stylesheet()
        
        # Set window icon
        self._set_window_icon()
        
        # Setup dynamic image list widget
        self._setup_dynamic_widgets()
        
        print("✅ UI setup completed")
    
    def _setup_dynamic_widgets(self):
        """Setup dynamic widgets for image handling trong panel riêng"""
        try:
            print("📝 Setting up image management panel...")
            
            # Get references to UI elements trong imageManagerCard
            if not hasattr(self.ui, 'imageManagerCard'):
                print("⚠️ imageManagerCard not found in UI")
                return
                
            # Get UI elements
            self.images_count_label = self.ui.imageCountLabel
            self.choose_images_btn = self.ui.chooseImagesBtn
            self.move_up_btn = self.ui.moveUpBtn
            self.move_down_btn = self.ui.moveDownBtn
            self.remove_image_btn = self.ui.removeImageBtn
            self.clear_images_btn = self.ui.clearImagesBtn
            self.images_listbox = self.ui.imagesListWidget
            
            # Setup connections
            self.choose_images_btn.clicked.connect(self._choose_images)
            self.move_up_btn.clicked.connect(self._move_image_up)
            self.move_down_btn.clicked.connect(self._move_image_down)
            self.remove_image_btn.clicked.connect(self._remove_selected_image)
            self.clear_images_btn.clicked.connect(self._clear_all_images)
            self.images_listbox.itemSelectionChanged.connect(self._on_image_selection_changed)
            
            # Enable drag and drop trên dropZoneWidget
            if hasattr(self.ui, 'dropZoneWidget'):
                self._setup_drag_drop_on_zone(self.ui.dropZoneWidget)
            
            # Store reference
            self.images_widget = self.ui.imageManagerCard
            
            # Initially hide panel (will show when needed)
            self._update_image_panel_visibility()
            
            # Setup initial image info text
            self._update_image_info_text()
            
            print("✅ Image management panel setup completed")
            
        except Exception as e:
            print(f"❌ Image panel setup error: {e}")
            # Continue without image panel
            self.images_widget = None
    
    def _center_window(self):
        """Center window on screen"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def _load_stylesheet(self):
        """Load and apply QSS stylesheet"""
        try:
            style_file = Path(__file__).parent / "resources" / "style.qss"
            if style_file.exists():
                with open(style_file, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                self.setStyleSheet(stylesheet)
                print("✅ Stylesheet loaded")
            else:
                print("⚠️ Stylesheet not found")
        except Exception as e:
            print(f"❌ Stylesheet error: {e}")
    
    def _set_window_icon(self):
        """Set window icon"""
        try:
            icon_path = Path(__file__).parent.parent / "icon.png"
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
        except Exception as e:
            print(f"⚠️ Icon error: {e}")
    
    def _setup_system_tray(self):
        """Setup system tray icon and menu"""
        try:
            print("📝 Setting up system tray...")
            
            if not QSystemTrayIcon.isSystemTrayAvailable():
                print("⚠️ System tray not available")
                return
            
            # Create tray icon
            self.tray_icon = QSystemTrayIcon(self)
            
            # Set icon
            icon_path = Path(__file__).parent.parent / "icon.png"
            if icon_path.exists():
                self.tray_icon.setIcon(QIcon(str(icon_path)))
                print(f"✅ Tray icon set: {icon_path}")
            else:
                # Fallback to default icon
                self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
                print("✅ Tray icon set: default")
            
            # Create context menu
            tray_menu = QMenu()
            
            # Show action
            show_action = QAction("Hiển thị cửa sổ", self)
            show_action.triggered.connect(self._show_from_tray)
            tray_menu.addAction(show_action)
            
            tray_menu.addSeparator()
            
            # Shortcuts count
            count_action = QAction(f"Shortcuts: {len(self.config.get_shortcuts())}", self)
            count_action.setEnabled(False)
            tray_menu.addAction(count_action)
            self.tray_count_action = count_action
            
            # Monitoring status
            status_action = QAction("Đang theo dõi bàn phím", self)
            status_action.setEnabled(False)
            tray_menu.addAction(status_action)
            self.tray_status_action = status_action
            
            tray_menu.addSeparator()
            
            # Settings action
            settings_action = QAction("⚙️ Cài đặt", self)
            settings_action.triggered.connect(self._show_settings)
            tray_menu.addAction(settings_action)
            
            # Auto startup toggle
            self.startup_action = QAction("🚀 Khởi động cùng Windows", self)
            self.startup_action.setCheckable(True)
            self.startup_action.setChecked(self._is_startup_enabled())
            self.startup_action.triggered.connect(self._toggle_startup)
            tray_menu.addAction(self.startup_action)
            
            tray_menu.addSeparator()
            
            # Exit action
            exit_action = QAction("Thoát", self)
            exit_action.triggered.connect(self._exit_app)
            tray_menu.addAction(exit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            
            # Connect double click to show
            self.tray_icon.activated.connect(self._tray_activated)
            
            # Set tooltip
            self.tray_icon.setToolTip("TextNow - Auto Text & Image")
            
            # Show tray icon
            self.tray_icon.show()
            
            print("✅ System tray setup completed")
        except Exception as e:
            print(f"❌ System tray setup error: {e}")
            self.tray_icon = None
    
    def _tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._show_from_tray()
    
    def _show_from_tray(self):
        """Show window from system tray"""
        self.show()
        self.raise_()
        self.activateWindow()
    
    def _is_startup_enabled(self):
        """Check if auto startup is enabled"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, "TextNow")
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    def _toggle_startup(self):
        """Toggle auto startup with Windows"""
        try:
            if self.startup_action.isChecked():
                # Enable startup
                self._enable_startup()
            else:
                # Disable startup
                self._disable_startup()
        except Exception as e:
            print(f"❌ Toggle startup error: {e}")
            QMessageBox.warning(self, "Lỗi", f"Không thể thay đổi cài đặt khởi động: {e}")
    
    def _enable_startup(self):
        """Enable auto startup"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_WRITE)
            
            # Get current executable path
            if getattr(sys, 'frozen', False):
                # Running as exe - use exe path directly
                app_path = f'"{sys.executable}"'
            else:
                # Running as script - use pythonw.exe with silent startup script
                python_exe = sys.executable
                
                # Use pythonw.exe instead of python.exe to avoid terminal
                if python_exe.endswith('python.exe'):
                    pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
                else:
                    pythonw_exe = python_exe  # Fallback
                
                # Use silent startup script
                script_path = Path(__file__).parent.parent / "main_qt_silent.py"
                app_path = f'"{pythonw_exe}" "{script_path}"'
            
            print(f"🔧 Setting startup command: {app_path}")
            winreg.SetValueEx(key, "TextNow", 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            
            print("✅ Auto startup enabled")
            QMessageBox.information(self, "Thành công", 
                                  "Đã bật khởi động cùng Windows!\n\n"
                                  "🔇 Phần mềm sẽ chạy im lặng khi khởi động\n"
                                  "📱 Kiểm tra system tray để mở cửa sổ")
        except Exception as e:
            print(f"❌ Enable startup error: {e}")
            raise e
    
    def _disable_startup(self):
        """Disable auto startup"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_WRITE)
            try:
                winreg.DeleteValue(key, "TextNow")
                print("✅ Auto startup disabled")
                QMessageBox.information(self, "Thành công", "Đã tắt khởi động cùng Windows")
            except FileNotFoundError:
                pass  # Already disabled
            winreg.CloseKey(key)
        except Exception as e:
            print(f"❌ Disable startup error: {e}")
            raise e
    
    def _exit_app(self):
        """Exit application completely"""
        if self.keyboard_monitor:
            self.keyboard_monitor.stop_monitoring()
        QApplication.quit()
    
    def _setup_table(self):
        """Setup shortcuts table"""
        try:
            # Create model
            self.table_model = ShortcutTableModel()
            
            # Set model to table view
            table_view = self.ui.shortcutTableView
            table_view.setModel(self.table_model)
            
            # Configure table
            header = table_view.horizontalHeader()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Shortcut column
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type column
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Content column (stretch)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Status column
            
            # Hide vertical header
            table_view.verticalHeader().setVisible(False)
            
            # Row selection
            table_view.setSelectionBehavior(table_view.SelectionBehavior.SelectRows)
            
            print("✅ Table setup completed")
        except Exception as e:
            print(f"❌ Table setup error: {e}")
    
    def _setup_connections(self):
        """Setup signal connections"""
        try:
            # Search functionality
            self.ui.searchLineEdit.textChanged.connect(self._on_search_changed)
            
            # Table selection
            self.ui.shortcutTableView.selectionModel().currentRowChanged.connect(self._on_table_selection_changed)
            
            # Form buttons
            self.ui.addBtn.clicked.connect(self._add_shortcut)
            self.ui.updateBtn.clicked.connect(self._update_shortcut)
            self.ui.deleteBtn.clicked.connect(self._delete_shortcut)
            self.ui.createShortcutBtn.clicked.connect(self._create_shortcut)
            
            # Footer buttons
            self.ui.importBtn.clicked.connect(self._import_config)
            self.ui.exportBtn.clicked.connect(self._export_config)
            self.ui.settingsBtn.clicked.connect(self._show_settings)
            
            # Content type radio buttons
            self.ui.textRadioBtn.toggled.connect(self._on_content_type_changed)
            self.ui.imageRadioBtn.toggled.connect(self._on_content_type_changed)
            self.ui.mixedRadioBtn.toggled.connect(self._on_content_type_changed)
            
            print("✅ Connections setup completed")
        except Exception as e:
            print(f"❌ Connections setup error: {e}")
    
    def _load_shortcuts(self):
        """Load shortcuts vào table"""
        try:
            # Get shortcuts from config
            all_shortcuts = self.config.get_shortcuts()
            
            # Filter if search is active
            search_text = self.ui.searchLineEdit.text().strip()
            if search_text:
                filtered_shortcuts = self._filter_shortcuts(all_shortcuts, search_text)
            else:
                filtered_shortcuts = all_shortcuts
            
            # Update table model
            self.table_model.setShortcuts(filtered_shortcuts)
            self.current_shortcuts = filtered_shortcuts
            
            # Update count label
            count = len(filtered_shortcuts)
            total_count = len(all_shortcuts)
            if search_text:
                self.ui.countLabel.setText(f"SHORTCUT HIỆN CÓ: {count}/{total_count}")
            else:
                self.ui.countLabel.setText(f"SHORTCUT HIỆN CÓ: {count}")
            
            # Update tray menu
            if hasattr(self, 'tray_count_action'):
                self.tray_count_action.setText(f"Shortcuts: {total_count}")
            
            # Reload shortcuts trong manager
            self.shortcut_manager.reload_shortcuts()
            if self.keyboard_monitor:
                self.keyboard_monitor.refresh_keywords_cache()
            
            print(f"✅ Loaded {count} shortcuts")
        except Exception as e:
            print(f"❌ Load shortcuts error: {e}")
    
    def _filter_shortcuts(self, shortcuts_list, search_text):
        """Filter shortcuts by keyword only"""
        if not search_text:
            return shortcuts_list
        
        search_text = search_text.lower()
        filtered = []
        
        for shortcut in shortcuts_list:
            keyword = shortcut.get('keyword', '').lower()
            if search_text in keyword:
                filtered.append(shortcut)
        
        return filtered
    
    def _on_search_changed(self, text):
        """Handle search text change"""
        self._load_shortcuts()
    
    def _on_table_selection_changed(self, current: QModelIndex, previous: QModelIndex):
        """Handle table selection change"""
        if current.isValid():
            row = current.row()
            if row < len(self.current_shortcuts):
                shortcut = self.current_shortcuts[row]
                self._load_shortcut_to_form(shortcut)
                
                # Find index in original list
                all_shortcuts = self.config.get_shortcuts()
                for i, original_shortcut in enumerate(all_shortcuts):
                    if original_shortcut['keyword'] == shortcut['keyword']:
                        self.selected_index = i
                        break
                else:
                    self.selected_index = None
    
    def _load_shortcut_to_form(self, shortcut):
        """Load shortcut data to form với improved UI system"""
        try:
            # Clear selection first
            self.ui.shortcutLineEdit.setText(shortcut.get('keyword', ''))
            
            # Set content type
            shortcut_type = shortcut.get('type', 'text')
            if shortcut_type == 'mixed':
                self.ui.mixedRadioBtn.setChecked(True)
            elif shortcut_type == 'image':
                self.ui.imageRadioBtn.setChecked(True)
            else:
                self.ui.textRadioBtn.setChecked(True)
            
            # Clear images first
            self.selected_images.clear()
            
            # Set content based on type
            content = shortcut.get('content', '')
            if shortcut_type == 'mixed' and isinstance(content, dict):
                # Mixed content
                text_content = content.get('text', '')
                self.ui.contentTextEdit.setPlainText(text_content)
                
                # Load images
                images = content.get('images', [])
                self.selected_images.extend(images)
                    
            elif shortcut_type == 'image':
                # Single image content
                self.ui.contentTextEdit.setPlainText(str(content))
                if content:
                    self.selected_images.append(content)
            else:
                # Text content
                self.ui.contentTextEdit.setPlainText(str(content))
            
            # Refresh images display với new system
            self._refresh_images_list()
            
            # Set enabled state
            self.ui.activateCheckBox.setChecked(shortcut.get('enabled', True))
            
            # Update visibility
            self._update_content_type_visibility()
            
        except Exception as e:
            print(f"❌ Load to form error: {e}")
    
    def _on_content_type_changed(self):
        """Handle content type radio button change"""
        self._update_image_panel_visibility()
        self._update_content_type_visibility()
        self._update_image_info_text()
    
    def _update_content_type_visibility(self):
        """Update visibility of content fields based on type"""
        try:
            if self.ui.textRadioBtn.isChecked():
                # Text only: show text area, image panel tự động ẩn
                self.ui.contentTextEdit.setVisible(True)
                    
            elif self.ui.imageRadioBtn.isChecked():
                # Image only: hide text area, image panel tự động hiện
                self.ui.contentTextEdit.setVisible(False)
                    
            elif self.ui.mixedRadioBtn.isChecked():
                # Mixed: show both text area and image panel
                self.ui.contentTextEdit.setVisible(True)
            
        except Exception as e:
            print(f"❌ Update visibility error: {e}")
    
    def _update_image_info_text(self):
        """Update image info text based on shortcut type"""
        try:
            if hasattr(self.ui, 'imageInfoLabel'):
                if self.ui.imageRadioBtn.isChecked():
                    # Image only: tối đa 1 ảnh
                    self.ui.imageInfoLabel.setText("Tối đa 1 ảnh • Hỗ trợ kéo thả")
                elif self.ui.mixedRadioBtn.isChecked():
                    # Mixed: tối đa 20 ảnh
                    self.ui.imageInfoLabel.setText("Thứ tự từ 1-20, tối đa 20 ảnh • Hỗ trợ kéo thả")
                else:
                    # Default fallback
                    self.ui.imageInfoLabel.setText("Hỗ trợ kéo thả")
        except Exception as e:
            print(f"❌ Update image info text error: {e}")
    
    def _setup_drag_drop_on_zone(self, drop_zone_widget):
        """Setup drag and drop cho drop zone widget"""
        try:
            from PySide6.QtCore import QMimeData
            from PySide6.QtGui import QDragEnterEvent, QDropEvent
            
            # Enable drag drop
            drop_zone_widget.setAcceptDrops(True)
            
            # Override drag and drop events
            def dragEnterEvent(event: QDragEnterEvent):
                if event.mimeData().hasUrls():
                    # Check if có file ảnh
                    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
                    urls = event.mimeData().urls()
                    has_images = any(url.toLocalFile().lower().endswith(tuple(image_extensions)) for url in urls)
                    
                    if has_images:
                        event.acceptProposedAction()
                        print("📥 Drag enter: Image files detected")
                    else:
                        event.ignore()
                else:
                    event.ignore()
            
            def dropEvent(event: QDropEvent):
                if event.mimeData().hasUrls():
                    urls = event.mimeData().urls()
                    image_paths = []
                    
                    for url in urls:
                        file_path = url.toLocalFile()
                        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
                            image_paths.append(file_path)
                    
                    if image_paths:
                        self._add_images_from_paths(image_paths)
                        event.acceptProposedAction()
                        print(f"📥 Dropped {len(image_paths)} images")
                    else:
                        event.ignore()
                else:
                    event.ignore()
            
            # Attach events
            drop_zone_widget.dragEnterEvent = dragEnterEvent
            drop_zone_widget.dropEvent = dropEvent
            
            print("✅ Drag & drop setup completed on drop zone")
            
        except Exception as e:
            print(f"⚠️ Drag & drop setup failed: {e}")
    
    def _update_image_panel_visibility(self):
        """Update visibility của image management panel"""
        try:
            if not hasattr(self, 'images_widget') or not self.images_widget:
                return
                
            # Hiển thị panel khi content type là image hoặc mixed
            if hasattr(self.ui, 'imageRadioBtn') and hasattr(self.ui, 'mixedRadioBtn'):
                show_panel = (self.ui.imageRadioBtn.isChecked() or 
                             self.ui.mixedRadioBtn.isChecked())
                self.images_widget.setVisible(show_panel)
                
                if show_panel:
                    print("👁️ Image panel visible")
                else:
                    print("👁️ Image panel hidden")
            else:
                # Fallback: always show
                self.images_widget.setVisible(True)
                
        except Exception as e:
            print(f"❌ Update panel visibility error: {e}")
    
    def _add_images_from_paths(self, paths):
        """Add images from paths (for drag & drop) với giới hạn theo loại shortcut"""
        try:
            # Determine max images based on shortcut type
            if self.ui.imageRadioBtn.isChecked():
                max_images = 1
                type_name = "Ảnh"
            elif self.ui.mixedRadioBtn.isChecked():
                max_images = 20
                type_name = "Văn bản + Ảnh"
            else:
                # Text mode shouldn't show image panel, but just in case
                return
            
            added_count = 0
            for path in paths:
                if len(self.selected_images) >= max_images:
                    if max_images == 1:
                        QMessageBox.warning(
                            self, "Giới hạn", 
                            f"Shortcut loại '{type_name}' chỉ cho phép tối đa {max_images} ảnh!\n\n"
                            f"Vui lòng xóa ảnh hiện tại trước khi thêm ảnh mới."
                        )
                    else:
                        QMessageBox.warning(
                            self, "Giới hạn", 
                            f"Shortcut loại '{type_name}' chỉ cho phép tối đa {max_images} ảnh!\n\n"
                            f"Đã thêm {added_count} ảnh."
                        )
                    break
                
                # Add to list
                self.selected_images.append(path)
                added_count += 1
            
            # Refresh list display
            self._refresh_images_list()
            
            if added_count > 0:
                print(f"✅ Added {added_count} images via drag & drop")
                
        except Exception as e:
            print(f"❌ Add images from paths error: {e}")
    
    def _refresh_images_list(self):
        """Refresh images list display với thumbnails và info"""
        try:
            # Clear current list
            self.images_listbox.clear()
            
            # Update count
            count = len(self.selected_images)
            self.images_count_label.setText(f"📋 {count} ảnh")
            
            # Add items với enhanced display
            for i, image_path in enumerate(self.selected_images):
                try:
                    # Create item với thumbnail info
                    item_widget = self._create_image_list_item(i + 1, image_path)
                    
                    # Add to list
                    item = QListWidgetItem()
                    item.setSizeHint(item_widget.sizeHint())
                    self.images_listbox.addItem(item)
                    self.images_listbox.setItemWidget(item, item_widget)
                    
                except Exception as e:
                    print(f"⚠️ Error creating item for {image_path}: {e}")
                    # Fallback to simple text
                    simple_text = f"{i+1}. {Path(image_path).name}"
                    self.images_listbox.addItem(simple_text)
            
            # Update button states
            self._update_image_button_states()
            
        except Exception as e:
            print(f"❌ Refresh images list error: {e}")
    
    def _create_image_list_item(self, index, image_path):
        """Create enhanced image list item với thumbnail và info"""
        try:
            from PySide6.QtCore import QSize
            
            # Container widget
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(4, 4, 4, 4)
            item_layout.setSpacing(8)
            
            # Index label
            index_label = QLabel(f"{index}")
            index_label.setFixedSize(24, 24)
            index_label.setAlignment(Qt.AlignCenter)
            index_label.setStyleSheet(
                "background-color: #3B82F6; color: #FFFFFF; "
                "border-radius: 12px; font-size: 10px; font-weight: bold;"
            )
            item_layout.addWidget(index_label)
            
            # Thumbnail placeholder (tạm thời dùng icon)
            thumb_label = QLabel("🖼️")
            thumb_label.setFixedSize(32, 32)
            thumb_label.setAlignment(Qt.AlignCenter)
            thumb_label.setStyleSheet(
                "background-color: #F3F4F6; border: 1px solid #D1D5DB; "
                "border-radius: 4px; font-size: 16px;"
            )
            
            # Try to load actual thumbnail (basic version)
            try:
                from PySide6.QtGui import QPixmap
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    # Scale to thumbnail size
                    thumb_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    thumb_label.setPixmap(thumb_pixmap)
                    thumb_label.setText("")  # Clear icon text
            except:
                pass  # Keep icon fallback
            
            item_layout.addWidget(thumb_label)
            
            # File info
            info_layout = QVBoxLayout()
            info_layout.setSpacing(2)
            
            # File name
            file_name = Path(image_path).name
            if len(file_name) > 25:
                file_name = file_name[:22] + "..."
            name_label = QLabel(file_name)
            name_label.setStyleSheet("color: #374151; font-size: 11px; font-weight: bold;")
            info_layout.addWidget(name_label)
            
            # File size và type
            try:
                file_size = Path(image_path).stat().st_size
                if file_size < 1024:
                    size_text = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_text = f"{file_size // 1024} KB"
                else:
                    size_text = f"{file_size // (1024 * 1024)} MB"
                
                file_ext = Path(image_path).suffix.upper()
                detail_label = QLabel(f"{file_ext} • {size_text}")
                detail_label.setStyleSheet("color: #6B7280; font-size: 10px;")
                info_layout.addWidget(detail_label)
            except:
                detail_label = QLabel(Path(image_path).suffix.upper())
                detail_label.setStyleSheet("color: #6B7280; font-size: 10px;")
                info_layout.addWidget(detail_label)
            
            item_layout.addLayout(info_layout)
            item_layout.addStretch()
            
            # Status icon
            status_label = QLabel("✅")
            status_label.setStyleSheet("font-size: 12px;")
            item_layout.addWidget(status_label)
            
            item_widget.setMinimumHeight(48)
            return item_widget
            
        except Exception as e:
            print(f"❌ Create image item error: {e}")
            # Fallback widget
            fallback_widget = QWidget()
            fallback_layout = QHBoxLayout(fallback_widget)
            fallback_layout.addWidget(QLabel(f"{index}. {Path(image_path).name}"))
            return fallback_widget
    
    def _on_image_selection_changed(self):
        """Handle image selection change"""
        self._update_image_button_states()
    
    def _update_image_button_states(self):
        """Update button states based on selection và list"""
        try:
            current_row = self.images_listbox.currentRow()
            count = len(self.selected_images)
            
            # Move buttons
            self.move_up_btn.setEnabled(current_row > 0)
            self.move_down_btn.setEnabled(current_row >= 0 and current_row < count - 1)
            
            # Remove button
            self.remove_image_btn.setEnabled(current_row >= 0)
            
            # Clear button
            self.clear_images_btn.setEnabled(count > 0)
            
        except Exception as e:
            print(f"❌ Update button states error: {e}")
    
    def _move_image_up(self):
        """Move selected image up"""
        try:
            current_row = self.images_listbox.currentRow()
            if current_row > 0:
                # Swap in list
                self.selected_images[current_row], self.selected_images[current_row - 1] = \
                    self.selected_images[current_row - 1], self.selected_images[current_row]
                
                # Refresh display
                self._refresh_images_list()
                
                # Restore selection
                self.images_listbox.setCurrentRow(current_row - 1)
                
                print(f"✅ Moved image up: {current_row} -> {current_row - 1}")
                
        except Exception as e:
            print(f"❌ Move image up error: {e}")
    
    def _move_image_down(self):
        """Move selected image down"""
        try:
            current_row = self.images_listbox.currentRow()
            if current_row >= 0 and current_row < len(self.selected_images) - 1:
                # Swap in list
                self.selected_images[current_row], self.selected_images[current_row + 1] = \
                    self.selected_images[current_row + 1], self.selected_images[current_row]
                
                # Refresh display
                self._refresh_images_list()
                
                # Restore selection
                self.images_listbox.setCurrentRow(current_row + 1)
                
                print(f"✅ Moved image down: {current_row} -> {current_row + 1}")
                
        except Exception as e:
            print(f"❌ Move image down error: {e}")
    
    def _choose_images(self):
        """Choose image files với giới hạn theo loại shortcut"""
        try:
            # Determine max images based on shortcut type
            if self.ui.imageRadioBtn.isChecked():
                max_images = 1
                type_name = "Ảnh"
            elif self.ui.mixedRadioBtn.isChecked():
                max_images = 20
                type_name = "Văn bản + Ảnh"
            else:
                # Text mode shouldn't show image panel, but just in case
                return
            
            file_paths, _ = QFileDialog.getOpenFileNames(
                self, "Chọn ảnh", "", 
                "Image files (*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.webp);;All files (*.*)"
            )
            
            if file_paths:
                added_count = 0
                for file_path in file_paths:
                    if len(self.selected_images) >= max_images:
                        if max_images == 1:
                            QMessageBox.warning(
                                self, "Giới hạn", 
                                f"Shortcut loại '{type_name}' chỉ cho phép tối đa {max_images} ảnh!\n\n"
                                f"Vui lòng xóa ảnh hiện tại trước khi thêm ảnh mới."
                            )
                        else:
                            QMessageBox.warning(
                                self, "Giới hạn", 
                                f"Shortcut loại '{type_name}' chỉ cho phép tối đa {max_images} ảnh!\n\n"
                                f"Đã thêm {added_count} ảnh."
                            )
                        break
                    
                    # Add to list
                    self.selected_images.append(file_path)
                    added_count += 1
                
                # Refresh display
                self._refresh_images_list()
                
                print(f"✅ Added {added_count} images via file dialog")
                
        except Exception as e:
            print(f"❌ Choose images error: {e}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chọn ảnh: {e}")
    
    def _remove_selected_image(self):
        """Remove selected image from list"""
        try:
            current_row = self.images_listbox.currentRow()
            if current_row >= 0 and current_row < len(self.selected_images):
                # Get file name for confirmation
                image_path = self.selected_images[current_row]
                file_name = Path(image_path).name
                
                # Confirm removal
                reply = QMessageBox.question(
                    self, "Xác nhận xóa", 
                    f"Bạn có chắc muốn xóa ảnh này?\n\n📄 {file_name}",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Remove from list
                    removed_file = self.selected_images.pop(current_row)
                    
                    # Refresh display
                    self._refresh_images_list()
                    
                    # Select next item or previous if at end
                    if self.selected_images:
                        new_row = min(current_row, len(self.selected_images) - 1)
                        self.images_listbox.setCurrentRow(new_row)
                    
                    print(f"✅ Removed image: {Path(removed_file).name}")
                
        except Exception as e:
            print(f"❌ Remove image error: {e}")
            QMessageBox.warning(self, "Lỗi", f"Không thể xóa ảnh: {e}")
    
    def _clear_all_images(self):
        """Clear all images với confirmation"""
        try:
            if not self.selected_images:
                QMessageBox.information(self, "Thông báo", "Không có ảnh nào để xóa!")
                return
            
            count = len(self.selected_images)
            reply = QMessageBox.question(
                self, "Xác nhận xóa tất cả", 
                f"Bạn có chắc muốn xóa tất cả {count} ảnh?\n\n"
                "Hành động này không thể hoàn tác.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.selected_images.clear()
                self._refresh_images_list()
                
                print(f"✅ Cleared all {count} images")
                QMessageBox.information(self, "Thành công", f"Đã xóa tất cả {count} ảnh!")
                
        except Exception as e:
            print(f"❌ Clear images error: {e}")
            QMessageBox.warning(self, "Lỗi", f"Không thể xóa ảnh: {e}")
    
    def _create_shortcut(self):
        """Clear form for creating new shortcut"""
        self._clear_form()
        self.ui.shortcutLineEdit.setFocus()
    
    def _add_shortcut(self):
        """Add new shortcut"""
        try:
            keyword = self.ui.shortcutLineEdit.text().strip()
            enabled = self.ui.activateCheckBox.isChecked()
            
            # Determine type and content
            if self.ui.mixedRadioBtn.isChecked():
                shortcut_type = "mixed"
                text_content = self.ui.contentTextEdit.toPlainText().strip()
                
                # Validate: phải có ít nhất text hoặc images
                if not text_content and not self.selected_images:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản hoặc chọn ít nhất 1 ảnh")
                    return
                
                # Create mixed content
                content = {
                    'text': text_content,
                    'images': self.selected_images.copy()
                }
                
            elif self.ui.imageRadioBtn.isChecked():
                shortcut_type = "image"
                if not self.selected_images:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất 1 ảnh")
                    return
                
                # For single image type, use first image path as content
                content = self.selected_images[0]
                
            else:
                shortcut_type = "text"
                content = self.ui.contentTextEdit.toPlainText().strip()
                if not content:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung")
                    return
            
            if not keyword:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập từ khóa")
                return
            
            # Add shortcut
            success = self.config.add_shortcut(keyword, content, shortcut_type, enabled)
            
            if success:
                self._load_shortcuts()
                self._clear_form()
                
                if shortcut_type == "mixed":
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã thêm shortcut '{keyword}' thành công!\n\n"
                                          f"📝 Văn bản + {len(self.selected_images)} ảnh")
                elif shortcut_type == "image":
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã thêm shortcut '{keyword}' thành công!\n\n"
                                          f"🖼️ Ảnh: {Path(content).name}")
                else:
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã thêm shortcut '{keyword}' thành công!")
                
                self.shortcut_added.emit(keyword)
            else:
                QMessageBox.warning(self, "Lỗi", f"Từ khóa '{keyword}' đã tồn tại!")
                
        except Exception as e:
            print(f"❌ Add shortcut error: {e}")
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm shortcut: {e}")
    
    def _update_shortcut(self):
        """Update selected shortcut"""
        try:
            if self.selected_index is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn shortcut cần cập nhật")
                return
            
            keyword = self.ui.shortcutLineEdit.text().strip()
            enabled = self.ui.activateCheckBox.isChecked()
            
            # Determine type and content
            if self.ui.mixedRadioBtn.isChecked():
                shortcut_type = "mixed"
                text_content = self.ui.contentTextEdit.toPlainText().strip()
                
                # Validate: phải có ít nhất text hoặc images
                if not text_content and not self.selected_images:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng nhập văn bản hoặc chọn ít nhất 1 ảnh")
                    return
                
                # Create mixed content
                content = {
                    'text': text_content,
                    'images': self.selected_images.copy()
                }
                
            elif self.ui.imageRadioBtn.isChecked():
                shortcut_type = "image"
                if not self.selected_images:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất 1 ảnh")
                    return
                
                # For single image type, use first image path as content
                content = self.selected_images[0]
                
            else:
                shortcut_type = "text"
                content = self.ui.contentTextEdit.toPlainText().strip()
                if not content:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng nhập nội dung")
                    return
            
            if not keyword:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập từ khóa")
                return
            
            # Update shortcut
            success = self.config.update_shortcut(self.selected_index, keyword, content, 
                                                shortcut_type, enabled)
            
            if success:
                self._load_shortcuts()
                self._clear_form()
                
                if shortcut_type == "mixed":
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã cập nhật shortcut '{keyword}' thành công!\n\n"
                                          f"📝 Văn bản + {len(self.selected_images)} ảnh")
                elif shortcut_type == "image":
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã cập nhật shortcut '{keyword}' thành công!\n\n"
                                          f"🖼️ Ảnh: {Path(content).name}")
                else:
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã cập nhật shortcut '{keyword}' thành công!")
                
                self.shortcut_updated.emit(keyword)
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể cập nhật shortcut!")
                
        except Exception as e:
            print(f"❌ Update shortcut error: {e}")
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật shortcut: {e}")
    
    def _delete_shortcut(self):
        """Delete selected shortcut"""
        try:
            if self.selected_index is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn shortcut cần xóa")
                return
            
            shortcut = self.config.get_shortcuts()[self.selected_index]
            keyword = shortcut['keyword']
            
            reply = QMessageBox.question(self, "Xác nhận xóa", 
                                       f"Bạn có chắc muốn xóa shortcut '{keyword}'?\n\n"
                                       "Hành động này không thể hoàn tác.",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.config.delete_shortcut(self.selected_index)
                if success:
                    self._load_shortcuts()
                    self._clear_form()
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã xóa shortcut '{keyword}' thành công!")
                    self.shortcut_deleted.emit(keyword)
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể xóa shortcut!")
                    
        except Exception as e:
            print(f"❌ Delete shortcut error: {e}")
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa shortcut: {e}")
    
    def _clear_form(self):
        """Clear form fields"""
        try:
            self.ui.shortcutLineEdit.clear()
            self.ui.contentTextEdit.clear()
            self.ui.textRadioBtn.setChecked(True)
            self.ui.activateCheckBox.setChecked(True)
            self.selected_index = None
            
            # Clear images without confirmation
            self.selected_images.clear()
            self._refresh_images_list()
            
            # Clear table selection
            self.ui.shortcutTableView.clearSelection()
            
            # Update visibility
            self._update_content_type_visibility()
            
        except Exception as e:
            print(f"❌ Clear form error: {e}")
    
    def _import_config(self):
        """Import configuration"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Chọn file cấu hình để import", 
                "", "JSON files (*.json);;All files (*.*)")
            
            if file_path:
                if self.config.import_config(file_path):
                    self._load_shortcuts()
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã import cấu hình thành công!\n\n"
                                          f"Số shortcuts: {len(self.config.get_shortcuts())}")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể import cấu hình!")
        except Exception as e:
            print(f"❌ Import error: {e}")
            QMessageBox.critical(self, "Lỗi", f"Import failed: {e}")
    
    def _export_config(self):
        """Export configuration"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Lưu file cấu hình", 
                "shortcuts_config.json", "JSON files (*.json);;All files (*.*)")
            
            if file_path:
                if self.config.export_config(file_path):
                    QMessageBox.information(self, "Thành công", 
                                          f"Đã export cấu hình thành công!\n\n"
                                          f"File: {file_path}\n"
                                          f"Số shortcuts: {len(self.config.get_shortcuts())}")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể export cấu hình!")
        except Exception as e:
            print(f"❌ Export error: {e}")
            QMessageBox.critical(self, "Lỗi", f"Export failed: {e}")
    
    def _show_settings(self):
        """Show settings dialog"""
        try:
            from qt_ui.dialogs.settings_dialog import SettingsDialog
            dialog = SettingsDialog(self)
            dialog.exec()
        except ImportError:
            QMessageBox.information(self, "Cài đặt", "Settings dialog sẽ được implement sau!")
    
    def _on_monitoring_status_changed(self, is_active: bool):
        """Handle monitoring status change"""
        try:
            if is_active:
                self.ui.statusLabel.setText("Đang theo dõi bàn phím")
                self.ui.statusIndicator.setStyleSheet("background-color: #34B369; border-radius: 6px;")
                if hasattr(self, 'tray_status_action'):
                    self.tray_status_action.setText("Đang theo dõi bàn phím")
            else:
                self.ui.statusLabel.setText("Đã dừng theo dõi")
                self.ui.statusIndicator.setStyleSheet("background-color: #FC6157; border-radius: 6px;")
                if hasattr(self, 'tray_status_action'):
                    self.tray_status_action.setText("Đã dừng theo dõi")
        except Exception as e:
            print(f"❌ Status change error: {e}")
    
    def _on_shortcut_triggered(self, keyword: str, type: str, content: str):
        """Handle shortcut triggered"""
        print(f"🔥 Triggered: {keyword} ({type})")
        
        # Show tray notification
        if self.tray_icon:
            self.tray_icon.showMessage(
                "TextNow - Shortcut Triggered",
                f"Đã sử dụng shortcut: {keyword}",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.tray_icon and self.tray_icon.isVisible():
            # Hide to tray instead of closing
            self.hide()
            if not hasattr(self, '_tray_message_shown'):
                self.tray_icon.showMessage(
                    "TextNow",
                    "Ứng dụng đã thu nhỏ xuống khay hệ thống.\n"
                    "Nhấp đúp vào icon để hiển thị lại.",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )
                self._tray_message_shown = True
            event.ignore()
        else:
            # No tray icon, close normally
            if self.keyboard_monitor:
                self.keyboard_monitor.stop_monitoring()
            event.accept()


def main():
    """Main function for testing"""
    app = QApplication(sys.argv)
    
    # Fix: Skip deprecated DPI attributes for Qt 6
    # Qt 6 has automatic high DPI scaling by default
    print("✅ Using Qt 6 automatic DPI scaling")
    
    # Set application properties
    app.setApplicationName("TextNow")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("TextNow Team")
    
    # Create and show main window
    window = MainWindowQt()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 