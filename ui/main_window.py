"""
Giao diện chính của ứng dụng Auto Text & Image - Modern UI with SVN Poppins Font & Modern Icons
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Optional
from utils.config import Config
from utils.startup import is_autostart_enabled, toggle_autostart
from utils.font_manager import get_font_manager, get_font_family
from utils.icon_manager import ModernIcons, ModernColors, TypographyScale
from core.shortcut_manager import ShortcutManager
from core.keyboard_monitor import KeyboardMonitor

class ModernStyle:
    """Định nghĩa theme hiện đại cho ứng dụng với font SVN Poppins và icons"""
    
    # Color Palette - Updated with ModernColors
    PRIMARY = ModernColors.PRIMARY
    PRIMARY_LIGHT = ModernColors.PRIMARY_LIGHT  
    PRIMARY_DARK = ModernColors.PRIMARY_DARK
    
    SECONDARY = ModernColors.SUCCESS
    SECONDARY_LIGHT = ModernColors.SUCCESS_LIGHT
    
    ACCENT = ModernColors.WARNING
    DANGER = ModernColors.DANGER
    
    # Neutral colors - Using ModernColors
    WHITE = ModernColors.BACKGROUND
    GRAY_50 = ModernColors.SURFACE
    GRAY_100 = "#f3f4f6"
    GRAY_200 = ModernColors.BORDER
    GRAY_300 = "#d1d5db"
    GRAY_400 = ModernColors.TEXT_MUTED
    GRAY_500 = ModernColors.TEXT_SECONDARY
    GRAY_600 = "#4b5563"
    GRAY_700 = "#374151"
    GRAY_800 = ModernColors.TEXT_PRIMARY
    GRAY_900 = "#111827"
    
    # Typography with SVN Poppins - Using TypographyScale
    FONT_FAMILY = get_font_family()
    
    # Font sizes from TypographyScale
    FONT_SIZE_DISPLAY = TypographyScale.DISPLAY
    FONT_SIZE_H1 = TypographyScale.H1
    FONT_SIZE_H2 = TypographyScale.H2
    FONT_SIZE_H3 = TypographyScale.H3
    FONT_SIZE_LARGE = TypographyScale.BODY_LARGE
    FONT_SIZE_NORMAL = TypographyScale.BODY
    FONT_SIZE_SMALL = TypographyScale.CAPTION
    FONT_SIZE_MICRO = TypographyScale.MICRO
    
    # Spacing
    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 12
    SPACE_LG = 16
    SPACE_XL = 24
    SPACE_2XL = 32
    
    @staticmethod
    def get_font(size=12, weight='regular', italic=False):
        """Lấy font SVN Poppins với weight và size chỉ định"""
        return get_font_manager().get_font(size, weight, italic)

    @staticmethod
    def get_heading_font(level=1):
        """Lấy font cho heading theo level"""
        size, weight = TypographyScale.get_heading_style(level)
        return ModernStyle.get_font(size, weight)

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Text & Image - SVN Poppins")
        
        # ✨ Thiết lập kích thước cửa sổ 1440x1080
        window_width = 1440
        window_height = 1080
        
        # Tính toán vị trí để cửa sổ hiển thị ở giữa màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Thiết lập geometry cho cửa sổ
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)  # Cho phép resize
        
        # Thiết lập kích thước tối thiểu
        self.root.minsize(1200, 800)
        
        # Ngăn không cho minimize bằng cách xử lý window state event
        # self.root.bind('<Unmap>', self._on_window_state_change)  # Tạm thời disable để tránh loop
        
        # Sử dụng cách khác: override window manager protocol
        self.root.protocol("WM_WINDOW_DELETE", self._on_closing)
        
        # Thiết lập window attributes
        try:
            # Trên Windows: Enable window controls
            import tkinter.messagebox
            self.root.attributes('-disabled', 0)  # Enable window
            # self.root.attributes('-topmost', True)  # Always on top (optional)
        except:
            pass
        
        # Thêm hotkey thoát khẩn cấp (Ctrl+Alt+Q)
        self.root.bind('<Control-Alt-q>', self._emergency_exit)
        self.root.bind('<Control-Alt-Q>', self._emergency_exit)
        
        # Initialize font manager first
        self.font_manager = get_font_manager()
        print(f"🔤 Font hiện tại: {self.font_manager.get_font_family()}")
        print(f"✨ Font SVN Poppins loaded: {self.font_manager.is_loaded()}")
        print(f"📺 Kích thước cửa sổ: {window_width}x{window_height}")
        
        # Configure modern style
        self._configure_style()
        self._set_window_icon()
        
        # Biến trạng thái
        self.config = Config()
        self.shortcut_manager = ShortcutManager(self.config)
        self.keyboard_monitor = KeyboardMonitor(self.shortcut_manager)
        self.selected_index = None
        self.on_minimize_to_tray = None
        self.current_shortcuts = []  # Danh sách shortcuts hiện tại (có thể đã lọc)
        
        # Setup callbacks
        self.keyboard_monitor.set_on_status_changed(self._on_monitoring_status_changed)
        self.shortcut_manager.set_on_shortcut_triggered(self._on_shortcut_triggered)
        
        # Tạo giao diện hiện đại
        self._create_modern_ui()
        self._load_shortcuts()
        
        # Xử lý sự kiện
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
    def _configure_style(self):
        """Cấu hình style hiện đại với font SVN Poppins cho ttk widgets"""
        self.style = ttk.Style()
        
        # Configure modern theme
        self.style.theme_use('clam')
        
        # Configure Notebook style với SVN Poppins
        self.style.configure('Modern.TNotebook', 
                           background=ModernStyle.GRAY_50,
                           borderwidth=0)
        self.style.configure('Modern.TNotebook.Tab', 
                           padding=[24, 12],
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'medium'),
                           background=ModernStyle.GRAY_200,
                           focuscolor='none')
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', ModernStyle.WHITE),
                                ('active', ModernStyle.GRAY_100)])
        
        # Configure Button styles với SVN Poppins
        self.style.configure('Primary.TButton',
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'semibold'),
                           background=ModernStyle.PRIMARY,
                           foreground=ModernStyle.WHITE,
                           borderwidth=0,
                           focuscolor='none',
                           padding=[16, 8])
        self.style.map('Primary.TButton',
                      background=[('active', ModernStyle.PRIMARY_LIGHT),
                                ('pressed', ModernStyle.PRIMARY_DARK)])
        
        self.style.configure('Secondary.TButton',
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'medium'),
                           background=ModernStyle.GRAY_200,
                           foreground=ModernStyle.GRAY_700,
                           borderwidth=0,
                           focuscolor='none',
                           padding=[16, 8])
        self.style.map('Secondary.TButton',
                      background=[('active', ModernStyle.GRAY_300),
                                ('pressed', ModernStyle.GRAY_400)])
        
        self.style.configure('Success.TButton',
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'semibold'),
                           background=ModernStyle.SECONDARY,
                           foreground=ModernStyle.WHITE,
                           borderwidth=0,
                           focuscolor='none',
                           padding=[16, 8])
        self.style.map('Success.TButton',
                      background=[('active', ModernStyle.SECONDARY_LIGHT)])
        
        self.style.configure('Danger.TButton',
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'semibold'),
                           background=ModernStyle.DANGER,
                           foreground=ModernStyle.WHITE,
                           borderwidth=0,
                           focuscolor='none',
                           padding=[16, 8])
        
        # Configure Treeview với SVN Poppins
        self.style.configure('Modern.Treeview',
                           background=ModernStyle.WHITE,
                           foreground=ModernStyle.GRAY_800,
                           fieldbackground=ModernStyle.WHITE,
                           borderwidth=0,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL))
        self.style.configure('Modern.Treeview.Heading',
                           background=ModernStyle.GRAY_100,
                           foreground=ModernStyle.GRAY_700,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'semibold'),
                           borderwidth=0)
        self.style.map('Modern.Treeview',
                      background=[('selected', ModernStyle.PRIMARY_LIGHT)],
                      foreground=[('selected', ModernStyle.WHITE)])
        
        # Configure LabelFrame với SVN Poppins
        self.style.configure('Modern.TLabelframe',
                           background=ModernStyle.WHITE,
                           borderwidth=1,
                           relief='solid',
                           bordercolor=ModernStyle.GRAY_200)
        self.style.configure('Modern.TLabelframe.Label',
                           background=ModernStyle.WHITE,
                           foreground=ModernStyle.GRAY_700,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, 'semibold'))
        
        # Configure Entry với SVN Poppins
        self.style.configure('Modern.TEntry',
                           fieldbackground=ModernStyle.WHITE,
                           borderwidth=1,
                           relief='solid',
                           bordercolor=ModernStyle.GRAY_300,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL))
        self.style.map('Modern.TEntry',
                      bordercolor=[('focus', ModernStyle.PRIMARY)])
        
        # Configure Checkbutton với SVN Poppins
        self.style.configure('Modern.TCheckbutton',
                           background=ModernStyle.WHITE,
                           foreground=ModernStyle.GRAY_700,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL),
                           focuscolor='none')
        
        # Configure Radiobutton với SVN Poppins
        self.style.configure('Modern.TRadiobutton',
                           background=ModernStyle.WHITE,
                           foreground=ModernStyle.GRAY_700,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL),
                           focuscolor='none')
    
    def _set_window_icon(self):
        """Thiết lập icon cho cửa sổ chính"""
        try:
            import os
            from PIL import Image, ImageTk
            
            icon_path = "icon.png"
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                image = image.resize((32, 32), Image.Resampling.LANCZOS)
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                self.window_icon = ImageTk.PhotoImage(image)
                self.root.iconphoto(True, self.window_icon)
        except Exception as e:
            print(f"Lỗi khi thiết lập icon cửa sổ: {e}")
    
    def _create_modern_ui(self):
        """Tạo giao diện hiện đại"""
        # Configure root background
        self.root.configure(bg=ModernStyle.GRAY_50)
        
        # Main container với padding
        self.main_container = tk.Frame(self.root, bg=ModernStyle.GRAY_50)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_LG, pady=ModernStyle.SPACE_LG)
        
        # Header section
        self._create_header()
        
        # Content section với tabs
        self._create_content()
        
        # Footer section
        self._create_footer()
    
    def _create_header(self):
        """Tạo header với thông tin trạng thái sử dụng icons hiện đại"""
        header_frame = tk.Frame(self.main_container, bg=ModernStyle.WHITE, relief='solid', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, ModernStyle.SPACE_LG))
        
        # Header content với padding
        header_content = tk.Frame(header_frame, bg=ModernStyle.WHITE)
        header_content.pack(fill=tk.X, padx=ModernStyle.SPACE_LG, pady=ModernStyle.SPACE_MD)
        
        # Left side - App title và status
        left_frame = tk.Frame(header_content, bg=ModernStyle.WHITE)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # App title với icon hiện đại
        title_label = tk.Label(left_frame, 
                              text=f"✨ Auto Text & Image {ModernIcons.WINDOW}",
                              font=ModernStyle.get_heading_font(1),
                              bg=ModernStyle.WHITE,
                              fg=ModernStyle.GRAY_800)
        title_label.pack(anchor=tk.W)
        
        # Status indicator với icons động
        status_frame = tk.Frame(left_frame, bg=ModernStyle.WHITE)
        status_frame.pack(anchor=tk.W, pady=(ModernStyle.SPACE_XS, 0))
        
        self.status_indicator = tk.Label(status_frame,
                                       text=ModernIcons.ACTIVE,
                                       font=ModernStyle.get_font(14, TypographyScale.SEMIBOLD),
                                       bg=ModernStyle.WHITE,
                                       fg=ModernColors.SUCCESS)
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(status_frame,
                                   text=f"{ModernIcons.HOTKEY} Đang theo dõi bàn phím",
                                   font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.MEDIUM),
                                   bg=ModernStyle.WHITE,
                                   fg=ModernStyle.GRAY_600)
        self.status_label.pack(side=tk.LEFT, padx=(ModernStyle.SPACE_XS, 0))
        
        # Right side - Count info với icons
        right_frame = tk.Frame(header_content, bg=ModernStyle.WHITE)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.count_label = tk.Label(right_frame,
                                  text=f"{ModernIcons.SHORTCUTS} 0 shortcuts",
                                  font=ModernStyle.get_font(ModernStyle.FONT_SIZE_LARGE, TypographyScale.BOLD),
                                  bg=ModernStyle.WHITE,
                                  fg=ModernStyle.PRIMARY)
        self.count_label.pack(anchor=tk.E)
        
        # Performance info với icon
        self.perf_label = tk.Label(right_frame,
                                 text=f"{ModernIcons.BALANCED} Chế độ: Cân bằng | {ModernIcons.WINDOW} 1440x1080",
                                 font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL, TypographyScale.MEDIUM),
                                 bg=ModernStyle.WHITE,
                                 fg=ModernStyle.GRAY_500)
        self.perf_label.pack(anchor=tk.E)
    
    def _create_content(self):
        """Tạo phần nội dung chính với tabs có icons hiện đại"""
        # Notebook container
        notebook_container = tk.Frame(self.main_container, bg=ModernStyle.GRAY_50)
        notebook_container.pack(fill=tk.BOTH, expand=True, pady=(0, ModernStyle.SPACE_LG))
        
        # Modern Notebook
        self.notebook = ttk.Notebook(notebook_container, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab Shortcuts với icon
        self.shortcuts_tab = tk.Frame(self.notebook, bg=ModernStyle.WHITE)
        self.notebook.add(self.shortcuts_tab, text=f"{ModernIcons.SHORTCUTS} Quản lý Shortcuts")
        self._create_shortcuts_tab()
        
        # Tab Settings với icon
        self.settings_tab = tk.Frame(self.notebook, bg=ModernStyle.WHITE)
        self.notebook.add(self.settings_tab, text=f"{ModernIcons.SETTINGS} Cài đặt")
        self._create_settings_tab()
    
    def _create_shortcuts_tab(self):
        """Tạo tab quản lý shortcuts với layout hiện đại"""
        # Container với padding
        container = tk.Frame(self.shortcuts_tab, bg=ModernStyle.WHITE)
        container.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_LG, pady=ModernStyle.SPACE_LG)
        
        # Layout responsive: 70% list, 30% form
        container.grid_columnconfigure(0, weight=7, minsize=400)
        container.grid_columnconfigure(1, weight=3, minsize=300)
        container.grid_rowconfigure(0, weight=1)
        
        # Left panel - Shortcuts list
        self._create_shortcuts_list(container)
        
        # Right panel - Form
        self._create_shortcut_form(container)
    
    def _create_shortcuts_list(self, parent):
        """Tạo danh sách shortcuts với icons hiện đại"""
        # List container
        list_frame = ttk.LabelFrame(parent, text=f"{ModernIcons.SHORTCUTS} Danh sách Shortcuts", style='Modern.TLabelframe')
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, ModernStyle.SPACE_MD))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)  # Treeview ở row 1
        
        # List content
        list_content = tk.Frame(list_frame, bg=ModernStyle.WHITE)
        list_content.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_MD, pady=ModernStyle.SPACE_MD)
        list_content.grid_columnconfigure(0, weight=1)
        list_content.grid_rowconfigure(1, weight=1)  # Treeview ở row 1
        
        # Search frame
        search_frame = tk.Frame(list_content, bg=ModernStyle.WHITE)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, ModernStyle.SPACE_SM))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search label
        search_label = tk.Label(search_frame, text=f"{ModernIcons.SEARCH} Tìm kiếm shortcut:",
                               font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.SEMIBOLD),
                               bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_700)
        search_label.grid(row=0, column=0, sticky="w", padx=(0, ModernStyle.SPACE_SM))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, 
                                     style='Modern.TEntry',
                                     font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL))
        self.search_entry.grid(row=0, column=1, sticky="ew")
        
        # Bind search event
        self.search_var.trace_add('write', self._on_search_changed)
        
        # Clear search button
        clear_search_btn = ttk.Button(search_frame, text=f"{ModernIcons.CLEAR}", 
                                     command=self._clear_search, style='Secondary.TButton')
        clear_search_btn.grid(row=0, column=2, sticky="w", padx=(ModernStyle.SPACE_XS, 0))
        
        # Treeview với style hiện đại và icons
        columns = ('keyword', 'type', 'content', 'status')
        self.tree = ttk.Treeview(list_content, columns=columns, show='headings', 
                               style='Modern.Treeview', height=15)
        
        # Configure columns với icons
        self.tree.heading('keyword', text=f'{ModernIcons.KEYWORD} Từ khóa')
        self.tree.heading('type', text=f'{ModernIcons.CONTENT} Loại')
        self.tree.heading('content', text=f'{ModernIcons.TEXT} Nội dung')
        self.tree.heading('status', text=f'{ModernIcons.ACTIVE} Trạng thái')
        
        self.tree.column('keyword', width=120, minwidth=80)
        self.tree.column('type', width=80, minwidth=60)
        self.tree.column('content', width=250, minwidth=150)
        self.tree.column('status', width=80, minwidth=60)
        
        # Scrollbar
        scrollbar_y = ttk.Scrollbar(list_content, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(list_content, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        # Grid layout - treeview ở row 1
        self.tree.grid(row=1, column=0, sticky="nsew")
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_select_shortcut)
        self.tree.bind('<Double-1>', lambda e: self._update_shortcut())
    
    def _create_shortcut_form(self, parent):
        """Tạo form thêm/sửa shortcut với icons hiện đại"""
        # Form container
        form_frame = ttk.LabelFrame(parent, text=f"{ModernIcons.EDIT} Thêm/Sửa Shortcut", style='Modern.TLabelframe')
        form_frame.grid(row=0, column=1, sticky="nsew")
        
        # Form content với scroll
        canvas = tk.Canvas(form_frame, bg=ModernStyle.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=ModernStyle.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=ModernStyle.SPACE_MD, pady=ModernStyle.SPACE_MD)
        scrollbar.pack(side="right", fill="y")
        
        # Form fields
        self._create_form_fields(scrollable_frame)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
    
    def _create_form_fields(self, parent):
        """Tạo các trường trong form với icons hiện đại"""
        # Keyword field
        keyword_frame = tk.Frame(parent, bg=ModernStyle.WHITE)
        keyword_frame.pack(fill=tk.X, pady=(0, ModernStyle.SPACE_MD))
        
        tk.Label(keyword_frame, text=f"{ModernIcons.KEYWORD} Từ khóa:", 
                font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.SEMIBOLD),
                bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_700).pack(anchor=tk.W)
        self.keyword_entry = ttk.Entry(keyword_frame, style='Modern.TEntry', 
                                     font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL))
        self.keyword_entry.pack(fill=tk.X, pady=(ModernStyle.SPACE_XS, 0))
        
        # Type selection
        type_frame = tk.Frame(parent, bg=ModernStyle.WHITE)
        type_frame.pack(fill=tk.X, pady=(0, ModernStyle.SPACE_MD))
        
        tk.Label(type_frame, text=f"{ModernIcons.CONTENT} Loại nội dung:",
                font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.SEMIBOLD),
                bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_700).pack(anchor=tk.W)
        
        self.type_var = tk.StringVar(value="text")
        type_buttons_frame = tk.Frame(type_frame, bg=ModernStyle.WHITE)
        type_buttons_frame.pack(fill=tk.X, pady=(ModernStyle.SPACE_XS, 0))
        
        # Tạo 3 radio buttons trên cùng 1 dòng
        ttk.Radiobutton(type_buttons_frame, text=f"{ModernIcons.TEXT} Văn bản", variable=self.type_var, 
                       value="text", style='Modern.TRadiobutton').pack(side=tk.LEFT)
        ttk.Radiobutton(type_buttons_frame, text=f"{ModernIcons.IMAGE} Hình ảnh", variable=self.type_var, 
                       value="image", style='Modern.TRadiobutton').pack(side=tk.LEFT, padx=(ModernStyle.SPACE_LG, 0))
        ttk.Radiobutton(type_buttons_frame, text=f"{ModernIcons.MIXED} Văn bản + Ảnh", variable=self.type_var, 
                       value="mixed", style='Modern.TRadiobutton').pack(side=tk.LEFT, padx=(ModernStyle.SPACE_LG, 0))
        
        # Content field
        content_frame = tk.Frame(parent, bg=ModernStyle.WHITE)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, ModernStyle.SPACE_MD))
        
        tk.Label(content_frame, text=f"{ModernIcons.CONTENT} Nội dung:",
                font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.SEMIBOLD),
                bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_700).pack(anchor=tk.W)
        
        # Text area với border hiện đại
        text_container = tk.Frame(content_frame, bg=ModernStyle.GRAY_300, bd=1, relief='solid')
        text_container.pack(fill=tk.BOTH, expand=True, pady=(ModernStyle.SPACE_XS, 0))
        
        self.content_text = tk.Text(text_container, wrap=tk.WORD, 
                                  font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL),
                                  bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_800,
                                  borderwidth=0, highlightthickness=0,
                                  padx=ModernStyle.SPACE_SM, pady=ModernStyle.SPACE_SM)
        content_scroll = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=content_scroll.set)
        
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Browse button cho image với icon
        self.browse_button = ttk.Button(content_frame, text=f"{ModernIcons.BROWSE} Chọn ảnh...", 
                                      command=self._browse_image, style='Secondary.TButton')
        self.browse_button.pack(pady=(ModernStyle.SPACE_XS, 0))
        self.browse_button.pack_forget()  # Ẩn mặc định
        
        # Mixed content area cho text + images
        self.mixed_frame = tk.Frame(content_frame, bg=ModernStyle.WHITE)
        self.mixed_frame.pack(fill=tk.X, pady=(ModernStyle.SPACE_XS, 0))
        self.mixed_frame.pack_forget()  # Ẩn mặc định
        
        # Text input cho mixed content
        mixed_text_label = tk.Label(self.mixed_frame, text=f"{ModernIcons.TEXT} Văn bản (thứ tự 1):",
                                   font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL, TypographyScale.MEDIUM),
                                   bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_600)
        mixed_text_label.pack(anchor=tk.W)
        
        self.mixed_text = tk.Text(self.mixed_frame, height=3, wrap=tk.WORD,
                                 font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL),
                                 bg=ModernStyle.GRAY_50, fg=ModernStyle.GRAY_800,
                                 borderwidth=1, relief='solid')
        self.mixed_text.pack(fill=tk.X, pady=(ModernStyle.SPACE_XS, ModernStyle.SPACE_SM))
        
        # Images list cho mixed content
        mixed_images_label = tk.Label(self.mixed_frame, text=f"{ModernIcons.IMAGE} Danh sách ảnh (thứ tự 1-20, tối đa 20 ảnh):",
                                     font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL, TypographyScale.MEDIUM),
                                     bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_600)
        mixed_images_label.pack(anchor=tk.W)
        
        # Container cho danh sách ảnh với scrollbar
        images_container = tk.Frame(self.mixed_frame, bg=ModernStyle.GRAY_300, bd=1, relief='solid')
        images_container.pack(fill=tk.BOTH, expand=True, pady=(ModernStyle.SPACE_XS, ModernStyle.SPACE_SM))
        
        # Listbox cho images với scrollbar
        images_listbox_frame = tk.Frame(images_container, bg=ModernStyle.WHITE)
        images_listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.images_listbox = tk.Listbox(images_listbox_frame, height=6,
                                        font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL),
                                        bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_800,
                                        borderwidth=0, selectbackground=ModernStyle.PRIMARY_LIGHT)
        images_scroll = ttk.Scrollbar(images_listbox_frame, orient=tk.VERTICAL, command=self.images_listbox.yview)
        self.images_listbox.configure(yscrollcommand=images_scroll.set)
        
        self.images_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_XS, pady=ModernStyle.SPACE_XS)
        images_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons cho quản lý ảnh
        images_buttons_frame = tk.Frame(self.mixed_frame, bg=ModernStyle.WHITE)
        images_buttons_frame.pack(fill=tk.X)
        
        images_buttons_frame.grid_columnconfigure(0, weight=1)
        images_buttons_frame.grid_columnconfigure(1, weight=1)
        images_buttons_frame.grid_columnconfigure(2, weight=1)
        
        ttk.Button(images_buttons_frame, text=f"{ModernIcons.ADD} Thêm ảnh", 
                  command=self._add_image_to_mixed, style='Secondary.TButton').grid(row=0, column=0, sticky="ew", padx=(0, ModernStyle.SPACE_XS))
        ttk.Button(images_buttons_frame, text=f"{ModernIcons.DELETE} Xóa ảnh", 
                  command=self._remove_image_from_mixed, style='Secondary.TButton').grid(row=0, column=1, sticky="ew", padx=(ModernStyle.SPACE_XS, ModernStyle.SPACE_XS))
        ttk.Button(images_buttons_frame, text=f"{ModernIcons.CLEAR} Xóa tất cả", 
                  command=self._clear_all_images, style='Secondary.TButton').grid(row=0, column=2, sticky="ew", padx=(ModernStyle.SPACE_XS, 0))
        
        # Enabled checkbox với icon
        enabled_frame = tk.Frame(parent, bg=ModernStyle.WHITE)
        enabled_frame.pack(fill=tk.X, pady=(0, ModernStyle.SPACE_LG))
        
        self.enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(enabled_frame, text=f"{ModernIcons.SUCCESS} Kích hoạt shortcut", 
                       variable=self.enabled_var, style='Modern.TCheckbutton').pack(anchor=tk.W)
        
        # Action buttons
        self._create_form_buttons(parent)
        
        # Bind type change event
        self.type_var.trace('w', self._on_type_changed)
    
    def _create_form_buttons(self, parent):
        """Tạo các nút action cho form với icons hiện đại"""
        buttons_frame = tk.Frame(parent, bg=ModernStyle.WHITE)
        buttons_frame.pack(fill=tk.X, pady=(ModernStyle.SPACE_LG, 0))
        
        # Primary actions
        primary_frame = tk.Frame(buttons_frame, bg=ModernStyle.WHITE)
        primary_frame.pack(fill=tk.X, pady=(0, ModernStyle.SPACE_SM))
        
        ttk.Button(primary_frame, text=f"{ModernIcons.ADD} Thêm mới", 
                  command=self._add_shortcut, style='Primary.TButton').pack(fill=tk.X, pady=(0, ModernStyle.SPACE_XS))
        ttk.Button(primary_frame, text=f"{ModernIcons.SAVE} Cập nhật", 
                  command=self._update_shortcut, style='Success.TButton').pack(fill=tk.X, pady=(0, ModernStyle.SPACE_XS))
        
        # Secondary actions
        secondary_frame = tk.Frame(buttons_frame, bg=ModernStyle.WHITE)
        secondary_frame.pack(fill=tk.X)
        
        secondary_frame.grid_columnconfigure(0, weight=1)
        secondary_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Button(secondary_frame, text=f"{ModernIcons.DELETE} Xóa", 
                  command=self._delete_shortcut, style='Danger.TButton').grid(row=0, column=0, sticky="ew", padx=(0, ModernStyle.SPACE_XS))
        ttk.Button(secondary_frame, text=f"{ModernIcons.CLEAR} Làm mới", 
                  command=self._clear_form, style='Secondary.TButton').grid(row=0, column=1, sticky="ew", padx=(ModernStyle.SPACE_XS, 0))
    
    def _create_settings_tab(self):
        """Tạo tab cài đặt với layout hiện đại"""
        # Container với padding
        container = tk.Frame(self.settings_tab, bg=ModernStyle.WHITE)
        container.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_LG, pady=ModernStyle.SPACE_LG)
        
        # Responsive grid layout
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        # Left column - Performance settings
        self._create_performance_settings(container)
        
        # Right column - System settings và info
        self._create_system_settings(container)
    
    def _create_performance_settings(self, parent):
        """Tạo cài đặt hiệu suất với icons hiện đại"""
        perf_frame = ttk.LabelFrame(parent, text=f"{ModernIcons.PERFORMANCE} Cài đặt hiệu suất", style='Modern.TLabelframe')
        perf_frame.grid(row=0, column=0, sticky="new", padx=(0, ModernStyle.SPACE_MD), pady=(0, ModernStyle.SPACE_LG))
        
        content = tk.Frame(perf_frame, bg=ModernStyle.WHITE)
        content.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_MD, pady=ModernStyle.SPACE_MD)
        
        # Instant trigger với icon
        self.instant_trigger_var = tk.BooleanVar(value=False)
        instant_check = ttk.Checkbutton(
            content,
            text=f"{ModernIcons.ULTRA_FAST} Trigger ngay lập tức (Tốc độ tối đa)",
            variable=self.instant_trigger_var,
            command=self._on_instant_trigger_changed,
            style='Modern.TCheckbutton'
        )
        instant_check.pack(anchor=tk.W, pady=(0, ModernStyle.SPACE_MD))
        
        # Delay setting với icon
        delay_frame = tk.Frame(content, bg=ModernStyle.WHITE)
        delay_frame.pack(fill=tk.X, pady=(0, ModernStyle.SPACE_MD))
        
        self.delay_label = tk.Label(delay_frame, text=f"{ModernIcons.LOADING} Thời gian chờ:",
                                  font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.SEMIBOLD),
                                  bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_700)
        self.delay_label.pack(anchor=tk.W)
        
        delay_input_frame = tk.Frame(delay_frame, bg=ModernStyle.WHITE)
        delay_input_frame.pack(fill=tk.X, pady=(ModernStyle.SPACE_XS, 0))
        
        self.delay_var = tk.DoubleVar(value=0.1)
        self.delay_spinbox = ttk.Spinbox(
            delay_input_frame, 
            from_=0.01, 
            to=1.0, 
            increment=0.01, 
            width=8,
            textvariable=self.delay_var,
            command=self._on_delay_changed,
            format="%.2f",
            font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL)
        )
        self.delay_spinbox.pack(side=tk.LEFT)
        tk.Label(delay_input_frame, text="giây", 
                font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL),
                bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_600).pack(side=tk.LEFT, padx=(ModernStyle.SPACE_XS, 0))
        
        # Preset buttons với icons hiện đại
        presets_frame = tk.Frame(content, bg=ModernStyle.WHITE)
        presets_frame.pack(fill=tk.X, pady=(ModernStyle.SPACE_MD, 0))
        
        tk.Label(presets_frame, text=f"{ModernIcons.FAST} Presets nhanh:",
                font=ModernStyle.get_font(ModernStyle.FONT_SIZE_NORMAL, TypographyScale.SEMIBOLD),
                bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_700).pack(anchor=tk.W, pady=(0, ModernStyle.SPACE_XS))
        
        preset_buttons = tk.Frame(presets_frame, bg=ModernStyle.WHITE)
        preset_buttons.pack(fill=tk.X)
        preset_buttons.grid_columnconfigure(0, weight=1)
        preset_buttons.grid_columnconfigure(1, weight=1)
        
        ttk.Button(preset_buttons, text=f"{ModernIcons.ULTRA_FAST} Siêu nhanh", 
                  command=lambda: self._set_preset("ultra"), style='Primary.TButton').grid(row=0, column=0, sticky="ew", padx=(0, ModernStyle.SPACE_XS), pady=(0, ModernStyle.SPACE_XS))
        ttk.Button(preset_buttons, text=f"{ModernIcons.FAST} Nhanh", 
                  command=lambda: self._set_preset("fast"), style='Secondary.TButton').grid(row=0, column=1, sticky="ew", padx=(ModernStyle.SPACE_XS, 0), pady=(0, ModernStyle.SPACE_XS))
        ttk.Button(preset_buttons, text=f"{ModernIcons.BALANCED} Cân bằng", 
                  command=lambda: self._set_preset("balanced"), style='Secondary.TButton').grid(row=1, column=0, sticky="ew", padx=(0, ModernStyle.SPACE_XS))
        ttk.Button(preset_buttons, text=f"{ModernIcons.SAFE} An toàn", 
                  command=lambda: self._set_preset("safe"), style='Secondary.TButton').grid(row=1, column=1, sticky="ew", padx=(ModernStyle.SPACE_XS, 0))
        
        # Bind events
        self.delay_var.trace('w', self._on_delay_changed)
    
    def _create_system_settings(self, parent):
        """Tạo cài đặt hệ thống với icons hiện đại"""
        # System settings
        system_frame = ttk.LabelFrame(parent, text=f"{ModernIcons.SYSTEM} Cài đặt hệ thống", style='Modern.TLabelframe')
        system_frame.grid(row=0, column=1, sticky="new", pady=(0, ModernStyle.SPACE_LG))
        
        system_content = tk.Frame(system_frame, bg=ModernStyle.WHITE)
        system_content.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_MD, pady=ModernStyle.SPACE_MD)
        
        # Autostart với icon
        self.autostart_var = tk.BooleanVar(value=is_autostart_enabled())
        autostart_check = ttk.Checkbutton(
            system_content, 
            text=f"{ModernIcons.PLAY} Khởi động cùng Windows",
            variable=self.autostart_var,
            command=self._toggle_autostart,
            style='Modern.TCheckbutton'
        )
        autostart_check.pack(anchor=tk.W, pady=(0, ModernStyle.SPACE_SM))
        
        # Minimize to tray với icon
        self.minimize_to_tray_var = tk.BooleanVar(value=True)
        minimize_check = ttk.Checkbutton(
            system_content,
            text=f"{ModernIcons.TRAY} Thu nhỏ xuống khay khi đóng",
            variable=self.minimize_to_tray_var,
            style='Modern.TCheckbutton'
        )
        minimize_check.pack(anchor=tk.W)
        
        # App info với layout hiện đại
        info_frame = ttk.LabelFrame(parent, text=f"{ModernIcons.INFO} Thông tin ứng dụng", style='Modern.TLabelframe')
        info_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, ModernStyle.SPACE_LG))
        
        info_content = tk.Frame(info_frame, bg=ModernStyle.WHITE)
        info_content.pack(fill=tk.BOTH, expand=True, padx=ModernStyle.SPACE_MD, pady=ModernStyle.SPACE_MD)
        
        info_text = tk.Text(info_content, height=12, wrap=tk.WORD,
                           font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL),
                           bg=ModernStyle.GRAY_50, fg=ModernStyle.GRAY_700,
                           borderwidth=0, padx=ModernStyle.SPACE_SM, pady=ModernStyle.SPACE_SM)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        info_content_text = f"""✨ Auto Text & Image v1.3.6 - Single Instance Control

{ModernIcons.TEXT} Font mới - SVN Poppins:
• Font tiếng Việt đẹp, hiện đại và dễ đọc
• Hỗ trợ đầy đủ dấu tiếng Việt
• Multiple weights: Regular, Medium, SemiBold, Bold
• Tự động fallback về Segoe UI nếu không load được

{ModernIcons.WINDOW} Chế độ cửa sổ 1440x1080:
• Kích thước cố định tối ưu cho màn hình desktop
• Có thể resize và di chuyển cửa sổ
• Kích thước tối thiểu 1200x800
• Hotkey thoát khẩn cấp: Ctrl+Alt+Q

{ModernIcons.LOCK} Single Instance Control:
• Chỉ cho phép 1 phiên bản chạy cùng lúc
• Tự động hiện cửa sổ khi mở app lần 2
• Ngăn multiple icons trong system tray
• File locking + inter-process communication

{ModernIcons.SEARCH} Tính năng tìm kiếm mới:
• Tìm kiếm shortcut theo keyword real-time
• Chỉ tìm theo từ khóa, không tìm theo loại/nội dung
• Giao diện hiện đại với icon 🔍 và nút xóa 🧹
• Hiển thị "X/Y shortcuts" khi có kết quả tìm kiếm

{ModernIcons.EDIT} Giao diện hiện đại:
• Thiết kế với SVN Poppins typography system
• Layout responsive, tối ưu cho kích thước 1440x1080
• Icons và visual elements giúp dễ nhận diện
• Hover effects và interactive elements

{ModernIcons.PERFORMANCE} Tính năng:
• Gộp Text & Rich Text: Chỉ "Văn bản" và "Ảnh"
• Hỗ trợ tất cả ký tự: @ # $ % ^ & * và ký tự đặc biệt
• Trigger ngay lập tức hoặc với delay tùy chỉnh
• Tối ưu thuật toán với cache và tìm kiếm thông minh

{ModernIcons.SUCCESS} Sửa lỗi tốc độ cao (v1.3.1):
• Sửa race condition ở chế độ "Siêu nhanh" và "Nhanh"
• Tuần tự hóa: Xóa → Copy → Paste (thay vì song song)
• Cải tiến clipboard verification cho ảnh
• Logging chi tiết để debug (xem console)

{ModernIcons.HOTKEY} Cách sử dụng:
1. Thêm shortcut: Nhập từ khóa + nội dung
2. Gõ từ khóa → thay thế tự động
3. Hỗ trợ text thuần và HTML
4. Từ khóa có thể chứa ký tự đặc biệt

{ModernIcons.FAST} Presets hiệu suất:
• {ModernIcons.ULTRA_FAST} Siêu nhanh: Phản hồi tức thì (đã sửa lỗi)
• {ModernIcons.FAST} Nhanh: Delay 0.05s (đã sửa lỗi)
• {ModernIcons.BALANCED} Cân bằng: Delay 0.1s (khuyến nghị)
• {ModernIcons.SAFE} An toàn: Delay 0.3s

{ModernIcons.SYSTEM} Điều khiển:
• Thoát: Click nút X hoặc Ctrl+Alt+Q
• Ẩn: Thu nhỏ xuống system tray
• Có thể minimize và resize cửa sổ
• Font SVN Poppins được load tự động khi khởi động"""
        
        info_text.insert(1.0, info_content_text)
        info_text.config(state=tk.DISABLED)
    
    def _create_footer(self):
        """Tạo footer với các nút action chính và icons"""
        footer_frame = tk.Frame(self.main_container, bg=ModernStyle.WHITE, relief='solid', bd=1)
        footer_frame.pack(fill=tk.X)
        
        footer_content = tk.Frame(footer_frame, bg=ModernStyle.WHITE)
        footer_content.pack(fill=tk.X, padx=ModernStyle.SPACE_LG, pady=ModernStyle.SPACE_MD)
        
        # Left side - Import/Export với icons
        left_frame = tk.Frame(footer_content, bg=ModernStyle.WHITE)
        left_frame.pack(side=tk.LEFT)
        
        ttk.Button(left_frame, text=f"{ModernIcons.IMPORT} Import", 
                  command=self._import_config, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, ModernStyle.SPACE_SM))
        ttk.Button(left_frame, text=f"{ModernIcons.EXPORT} Export", 
                  command=self._export_config, style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Right side - App info với version
        right_frame = tk.Frame(footer_content, bg=ModernStyle.WHITE)
        right_frame.pack(side=tk.RIGHT)
        
        tk.Label(right_frame, text=f"✨ Auto Text & Image v1.3.6 - Search + 1440x1080 {ModernIcons.WINDOW}",
                font=ModernStyle.get_font(ModernStyle.FONT_SIZE_SMALL, TypographyScale.MEDIUM),
                bg=ModernStyle.WHITE, fg=ModernStyle.GRAY_500).pack()
    
    def _on_resize(self, event):
        """Disabled - không cho phép resize cửa sổ"""
        # Method này đã được vô hiệu hóa vì cửa sổ chạy fullscreen cố định
        pass
    
    def _update_performance_info(self):
        """Cập nhật thông tin hiệu suất với icons hiện đại"""
        if self.instant_trigger_var.get():
            mode = "Siêu nhanh"
            mode_icon = ModernIcons.ULTRA_FAST
        else:
            delay = self.delay_var.get()
            if delay <= 0.05:
                mode = "Nhanh"
                mode_icon = ModernIcons.FAST
            elif delay <= 0.15:
                mode = "Cân bằng"
                mode_icon = ModernIcons.BALANCED
            else:
                mode = "An toàn"
                mode_icon = ModernIcons.SAFE
        
        # Cập nhật với icons hiện đại
        self.perf_label.config(text=f"{mode_icon} Chế độ: {mode} | {ModernIcons.WINDOW} 1440x1080")
    
    def _on_instant_trigger_changed(self):
        """Xử lý khi thay đổi chế độ instant trigger với icons hiện đại"""
        instant_enabled = self.instant_trigger_var.get()
        self.keyboard_monitor.set_instant_trigger(instant_enabled)
        
        # Vô hiệu hóa delay setting khi instant trigger được bật
        if instant_enabled:
            self.delay_spinbox.config(state='disabled')
            self.delay_label.config(text=f"{ModernIcons.ULTRA_FAST} Thời gian chờ (Đã tắt - Dùng trigger ngay):")
        else:
            self.delay_spinbox.config(state='normal')
            self.delay_label.config(text=f"{ModernIcons.LOADING} Thời gian chờ:")
        
        self._update_performance_info()
    
    def _on_delay_changed(self, *args):
        """Xử lý khi thay đổi thời gian delay"""
        try:
            new_delay = self.delay_var.get()
            if 0.01 <= new_delay <= 1.0:
                self.keyboard_monitor.set_auto_trigger_delay(new_delay)
                self._update_performance_info()
        except:
            pass  # Ignore invalid values
    
    def _on_type_changed(self, *args):
        """Xử lý khi thay đổi loại shortcut"""
        content_type = self.type_var.get()
        
        if content_type == "image":
            # Hiển thị browse button, ẩn mixed frame
            self.browse_button.pack(pady=(ModernStyle.SPACE_XS, 0))
            self.mixed_frame.pack_forget()
            self.content_text.config(height=6)
        elif content_type == "mixed":
            # Hiển thị mixed frame, ẩn browse button  
            self.browse_button.pack_forget()
            self.mixed_frame.pack(fill=tk.X, pady=(ModernStyle.SPACE_XS, 0))
            self.content_text.config(height=3)
        else:
            # Text content - ẩn cả hai
            self.browse_button.pack_forget()
            self.mixed_frame.pack_forget()
            self.content_text.config(height=12)
    
    def _browse_image(self):
        """Chọn file ảnh"""
        filename = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if filename:
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, filename)
    
    def _add_image_to_mixed(self):
        """Thêm ảnh vào mixed content"""
        if self.images_listbox.size() >= 20:
            messagebox.showwarning(f"{ModernIcons.WARNING} Cảnh báo", "Tối đa 20 ảnh!")
            return
            
        filename = filedialog.askopenfilename(
            title="Chọn ảnh để thêm",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if filename:
            # Thêm với số thứ tự (bắt đầu từ 1)
            order = self.images_listbox.size() + 1
            display_name = f"{order}. {filename.split('/')[-1]}"
            self.images_listbox.insert(tk.END, display_name)
            
            # Lưu full path vào listbox data
            if not hasattr(self.images_listbox, 'image_paths'):
                self.images_listbox.image_paths = []
            self.images_listbox.image_paths.append(filename)
    
    def _remove_image_from_mixed(self):
        """Xóa ảnh được chọn khỏi mixed content"""
        selection = self.images_listbox.curselection()
        if not selection:
            messagebox.showwarning(f"{ModernIcons.WARNING} Cảnh báo", "Vui lòng chọn ảnh cần xóa!")
            return
            
        index = selection[0]
        self.images_listbox.delete(index)
        
        # Xóa khỏi paths list
        if hasattr(self.images_listbox, 'image_paths') and index < len(self.images_listbox.image_paths):
            self.images_listbox.image_paths.pop(index)
        
        # Cập nhật lại số thứ tự
        self._update_image_numbers()
    
    def _clear_all_images(self):
        """Xóa tất cả ảnh khỏi mixed content"""
        if self.images_listbox.size() == 0:
            return
            
        if messagebox.askyesno(f"{ModernIcons.WARNING} Xác nhận", "Xóa tất cả ảnh?"):
            self.images_listbox.delete(0, tk.END)
            if hasattr(self.images_listbox, 'image_paths'):
                self.images_listbox.image_paths.clear()
    
    def _update_image_numbers(self):
        """Cập nhật lại số thứ tự cho các ảnh"""
        if not hasattr(self.images_listbox, 'image_paths'):
            return
            
        # Lưu lại các paths
        paths = self.images_listbox.image_paths.copy()
        
        # Xóa và thêm lại với số thứ tự mới
        self.images_listbox.delete(0, tk.END)
        
        for i, path in enumerate(paths):
            order = i + 1  # Bắt đầu từ 1
            display_name = f"{order}. {path.split('/')[-1]}"
            self.images_listbox.insert(tk.END, display_name)
    
    def _load_shortcuts(self):
        """Tải danh sách shortcuts vào treeview với icons hiện đại"""
        # Xóa các items cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy danh sách shortcuts
        all_shortcuts = self.config.get_shortcuts()
        
        # Lọc shortcuts nếu có tìm kiếm
        search_text = getattr(self, 'search_var', None)
        if search_text and search_text.get().strip():
            filtered_shortcuts = self._filter_shortcuts(all_shortcuts, search_text.get().strip())
        else:
            filtered_shortcuts = all_shortcuts
        
        # Lưu danh sách hiện tại để sử dụng trong _on_select_shortcut
        self.current_shortcuts = filtered_shortcuts
        
        # Thêm shortcuts với icons hiện đại
        for i, shortcut in enumerate(filtered_shortcuts):
            # Status icon với màu sắc
            status_icon = ModernIcons.get_status_icon(shortcut.get('enabled', True))
            status_text = "Bật" if shortcut.get('enabled', True) else "Tắt"
            
            content = shortcut['content']
            if isinstance(content, dict):
                # Mixed content - hiển thị text + số lượng ảnh
                text_part = content.get('text', '')
                images_count = len(content.get('images', []))
                if text_part and len(text_part) > 30:
                    text_part = text_part[:27] + "..."
                content = f"{text_part} + {images_count} ảnh" if images_count > 0 else text_part
            elif isinstance(content, str) and len(content) > 40:
                content = content[:37] + "..."
            
            # Hiển thị loại shortcut với icon hiện đại
            type_icon = ModernIcons.get_content_type_icon(shortcut['type'])
            if shortcut['type'] == 'mixed':
                display_type = f"{type_icon} Văn bản + Ảnh"
            elif shortcut['type'] in ['text', 'richtext']:
                display_type = f"{type_icon} Văn bản"
            else:
                display_type = f"{type_icon} Ảnh"
            
            # Insert với styling hiện đại
            self.tree.insert('', 'end', values=(
                f"{ModernIcons.KEYWORD} {shortcut['keyword']}",
                display_type,
                content,
                f"{status_icon} {status_text}"
            ))
        
        # Cập nhật số lượng với icon
        count = len(filtered_shortcuts)
        total_count = len(all_shortcuts)
        if search_text and search_text.get().strip():
            self.count_label.config(text=f"{ModernIcons.SHORTCUTS} {count}/{total_count} shortcuts")
        else:
            self.count_label.config(text=f"{ModernIcons.SHORTCUTS} {count} shortcuts")
        
        # Reload shortcuts trong manager
        self.shortcut_manager.reload_shortcuts()
        
        # 🔥 QUAN TRỌNG: Cập nhật cache keywords để có thể sử dụng shortcuts mới ngay lập tức
        self.keyboard_monitor.refresh_keywords_cache()

    def _filter_shortcuts(self, shortcuts_list, search_text):
        """Lọc danh sách shortcuts theo keyword (chỉ tìm theo keyword, không tìm theo loại hay nội dung)"""
        if not search_text:
            return shortcuts_list
        
        search_text = search_text.lower()
        filtered = []
        
        for shortcut in shortcuts_list:
            # Chỉ tìm kiếm theo keyword
            keyword = shortcut.get('keyword', '').lower()
            if search_text in keyword:
                filtered.append(shortcut)
        
        return filtered

    def _on_search_changed(self, *args):
        """Xử lý khi nội dung tìm kiếm thay đổi"""
        # Reload danh sách với tìm kiếm
        self._load_shortcuts()

    def _clear_search(self):
        """Xóa nội dung tìm kiếm"""
        if hasattr(self, 'search_var'):
            self.search_var.set("")
            self.search_entry.focus_set()
    
    def _on_select_shortcut(self, event):
        """Xử lý khi chọn shortcut trong danh sách"""
        selection = self.tree.selection()
        if selection:
            # Lấy index trong danh sách hiện tại (đã lọc)
            selected_index_in_filtered = self.tree.index(selection[0])
            
            # Lấy shortcut từ danh sách hiện tại
            if hasattr(self, 'current_shortcuts') and selected_index_in_filtered < len(self.current_shortcuts):
                shortcut = self.current_shortcuts[selected_index_in_filtered]
                
                # Tìm index của shortcut này trong danh sách gốc
                all_shortcuts = self.config.get_shortcuts()
                for i, original_shortcut in enumerate(all_shortcuts):
                    if original_shortcut['keyword'] == shortcut['keyword']:
                        self.selected_index = i
                        break
                else:
                    self.selected_index = None
                    return
            else:
                return
            
            # Load vào form với animation
            self.keyword_entry.delete(0, tk.END)
            self.keyword_entry.insert(0, shortcut['keyword'])
            
            # Gộp text và richtext thành text
            shortcut_type = shortcut['type']
            if shortcut_type in ['text', 'richtext']:
                self.type_var.set("text")
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(1.0, shortcut['content'])
            elif shortcut_type == 'mixed':
                self.type_var.set("mixed")
                # Load mixed content
                content = shortcut['content']
                if isinstance(content, dict):
                    # Load text part
                    self.content_text.delete(1.0, tk.END)
                    self.content_text.insert(1.0, content.get('text', ''))
                    
                    # Load text vào mixed_text
                    self.mixed_text.delete(1.0, tk.END)
                    self.mixed_text.insert(1.0, content.get('text', ''))
                    
                    # Load images
                    self.images_listbox.delete(0, tk.END)
                    if hasattr(self.images_listbox, 'image_paths'):
                        self.images_listbox.image_paths.clear()
                    else:
                        self.images_listbox.image_paths = []
                    
                    images = content.get('images', [])
                    for i, image_path in enumerate(images):
                        order = i + 1  # Bắt đầu từ 1
                        display_name = f"{order}. {image_path.split('/')[-1]}"
                        self.images_listbox.insert(tk.END, display_name)
                        self.images_listbox.image_paths.append(image_path)
                else:
                    # Legacy format - treat as text
                    self.content_text.delete(1.0, tk.END)
                    self.content_text.insert(1.0, content)
            else:
                self.type_var.set(shortcut_type)
                self.content_text.delete(1.0, tk.END)
                self.content_text.insert(1.0, shortcut['content'])
            
            self.enabled_var.set(shortcut.get('enabled', True))
            
            # Trigger type change để hiển thị UI phù hợp
            self._on_type_changed()
            
            # Visual feedback
            self.keyword_entry.config(style='Modern.TEntry')
    
    def _clear_form(self):
        """Xóa form nhập liệu với animation"""
        self.keyword_entry.delete(0, tk.END)
        self.type_var.set("text")
        self.content_text.delete(1.0, tk.END)
        
        # Clear mixed content
        self.mixed_text.delete(1.0, tk.END)
        self.images_listbox.delete(0, tk.END)
        if hasattr(self.images_listbox, 'image_paths'):
            self.images_listbox.image_paths.clear()
        
        self.enabled_var.set(True)
        self.selected_index = None
        self.tree.selection_remove(self.tree.selection())
        
        # Trigger type change để hiển thị UI phù hợp
        self._on_type_changed()
        
        # Focus vào keyword entry
        self.keyword_entry.focus_set()
    
    def _add_shortcut(self):
        """Thêm shortcut mới với validation cải tiến"""
        keyword = self.keyword_entry.get().strip()
        shortcut_type = self.type_var.get()
        
        if not keyword:
            messagebox.showerror("❌ Lỗi", "Vui lòng nhập từ khóa")
            return
        
        # Get content based on type
        if shortcut_type == "mixed":
            # Mixed content: text + images
            text_content = self.mixed_text.get(1.0, tk.END).strip()
            
            # Get images paths
            images = []
            if hasattr(self.images_listbox, 'image_paths'):
                images = self.images_listbox.image_paths.copy()
            
            # Validate: phải có ít nhất text hoặc images
            if not text_content and not images:
                messagebox.showerror("❌ Lỗi", "Vui lòng nhập văn bản hoặc chọn ít nhất 1 ảnh")
                return
            
            # Validate số lượng ảnh
            if len(images) > 20:
                messagebox.showerror("❌ Lỗi", "Tối đa 20 ảnh!")
                return
            
            # Tạo mixed content structure
            content = {
                'text': text_content,
                'images': images
            }
        else:
            # Regular content
            content = self.content_text.get(1.0, tk.END).strip()
            if not content:
                messagebox.showerror("❌ Lỗi", "Vui lòng nhập nội dung")
                return
        
        # Validation cho content size (chỉ với regular content)
        if shortcut_type != "mixed" and isinstance(content, str):
            if len(content) > 100000:  # 100KB
                if not messagebox.askyesno("⚠️ Cảnh báo", 
                    f"Nội dung rất dài ({len(content):,} ký tự).\n"
                    "Điều này có thể gây chậm khi sử dụng.\n\n"
                    "Bạn có muốn tiếp tục?"):
                    return
            elif len(content) > 10000:  # 10KB
                messagebox.showwarning("💡 Thông báo", 
                    f"Nội dung khá dài ({len(content):,} ký tự).\n"
                    "Có thể mất một chút thời gian khi trigger.")
        
        success = self.config.add_shortcut(
            keyword,
            content,
            shortcut_type,
            self.enabled_var.get()
        )
        
        if success:
            self._load_shortcuts()
            self._clear_form()
            
            if shortcut_type == "mixed":
                print(f"🎉 Mixed shortcut '{keyword}' đã được thêm với {len(content['images'])} ảnh!")
                messagebox.showinfo("✅ Thành công", 
                    f"Đã thêm shortcut '{keyword}' thành công!\n\n"
                    f"📝 Văn bản + {len(content['images'])} ảnh\n"
                    f"💡 Có thể sử dụng ngay không cần khởi động lại.")
            else:
                print(f"🎉 Shortcut '{keyword}' đã được thêm và có thể sử dụng ngay lập tức!")
                messagebox.showinfo("✅ Thành công", f"Đã thêm shortcut '{keyword}' thành công!\n\n💡 Có thể sử dụng ngay không cần khởi động lại.")
        else:
            messagebox.showerror("❌ Lỗi", f"Từ khóa '{keyword}' đã tồn tại!")
            self.keyword_entry.focus_set()
    
    def _update_shortcut(self):
        """Cập nhật shortcut đã chọn"""
        if self.selected_index is None:
            messagebox.showerror("❌ Lỗi", "Vui lòng chọn shortcut cần cập nhật")
            return
        
        keyword = self.keyword_entry.get().strip()
        shortcut_type = self.type_var.get()
        
        if not keyword:
            messagebox.showerror("❌ Lỗi", "Vui lòng nhập từ khóa")
            return
        
        # Get content based on type
        if shortcut_type == "mixed":
            # Mixed content: text + images
            text_content = self.mixed_text.get(1.0, tk.END).strip()
            
            # Get images paths
            images = []
            if hasattr(self.images_listbox, 'image_paths'):
                images = self.images_listbox.image_paths.copy()
            
            # Validate: phải có ít nhất text hoặc images
            if not text_content and not images:
                messagebox.showerror("❌ Lỗi", "Vui lòng nhập văn bản hoặc chọn ít nhất 1 ảnh")
                return
            
            # Validate số lượng ảnh
            if len(images) > 20:
                messagebox.showerror("❌ Lỗi", "Tối đa 20 ảnh!")
                return
            
            # Tạo mixed content structure
            content = {
                'text': text_content,
                'images': images
            }
        else:
            # Regular content
            content = self.content_text.get(1.0, tk.END).strip()
            if not content:
                messagebox.showerror("❌ Lỗi", "Vui lòng nhập nội dung")
                return
        
        # Validation cho content size (chỉ với regular content)
        if shortcut_type != "mixed" and isinstance(content, str):
            if len(content) > 100000:  # 100KB
                if not messagebox.askyesno("⚠️ Cảnh báo", 
                    f"Nội dung rất dài ({len(content):,} ký tự).\n"
                    "Điều này có thể gây chậm khi sử dụng.\n\n"
                    "Bạn có muốn tiếp tục?"):
                    return
            elif len(content) > 10000:  # 10KB
                messagebox.showwarning("💡 Thông báo", 
                    f"Nội dung khá dài ({len(content):,} ký tự).\n"
                    "Có thể mất một chút thời gian khi trigger.")
        
        success = self.config.update_shortcut(
            self.selected_index,
            keyword,
            content,
            shortcut_type,
            self.enabled_var.get()
        )
        
        if success:
            self._load_shortcuts()
            self._clear_form()
            
            if shortcut_type == "mixed":
                print(f"🎉 Mixed shortcut '{keyword}' đã được cập nhật với {len(content['images'])} ảnh!")
                messagebox.showinfo("✅ Thành công", 
                    f"Đã cập nhật shortcut '{keyword}' thành công!\n\n"
                    f"📝 Văn bản + {len(content['images'])} ảnh\n"
                    f"💡 Thay đổi được áp dụng ngay.")
            else:
                print(f"🎉 Shortcut '{keyword}' đã được cập nhật và áp dụng ngay lập tức!")
                messagebox.showinfo("✅ Thành công", f"Đã cập nhật shortcut '{keyword}' thành công!\n\n💡 Thay đổi được áp dụng ngay.")
    
    def _delete_shortcut(self):
        """Xóa shortcut đã chọn"""
        if self.selected_index is None:
            messagebox.showerror("❌ Lỗi", "Vui lòng chọn shortcut cần xóa")
            return
        
        shortcut = self.config.get_shortcuts()[self.selected_index]
        keyword = shortcut['keyword']
        
        if messagebox.askyesno("🗑️ Xác nhận xóa", 
                              f"Bạn có chắc muốn xóa shortcut '{keyword}'?\n\n"
                              "Hành động này không thể hoàn tác."):
            success = self.config.delete_shortcut(self.selected_index)
            if success:
                self._load_shortcuts()
                self._clear_form()
                print(f"🗑️ Shortcut '{keyword}' đã được xóa và ngừng hoạt động ngay lập tức!")
                messagebox.showinfo("✅ Thành công", f"Đã xóa shortcut '{keyword}' thành công!\n\n💡 Shortcut ngừng hoạt động ngay.")
    
    def _import_config(self):
        """Import cấu hình từ file"""
        filename = filedialog.askopenfilename(
            title="📥 Chọn file cấu hình để import",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            if self.config.import_config(filename):
                self._load_shortcuts()
                print(f"📥 Đã import {len(self.config.get_shortcuts())} shortcuts và có thể sử dụng ngay!")
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã import cấu hình thành công!\n\n"
                                  f"Số shortcuts đã import: {len(self.config.get_shortcuts())}\n"
                                  f"💡 Tất cả shortcuts có thể sử dụng ngay.")
            else:
                messagebox.showerror("❌ Lỗi", 
                                   "Không thể import cấu hình!\n\n"
                                   "Vui lòng kiểm tra:\n"
                                   "• File có đúng định dạng JSON\n"
                                   "• File không bị lỗi hoặc corrupt")
    
    def _export_config(self):
        """Export cấu hình ra file"""
        filename = filedialog.asksaveasfilename(
            title="📤 Lưu file cấu hình",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            if self.config.export_config(filename):
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã export cấu hình thành công!\n\n"
                                  f"File: {filename}\n"
                                  f"Số shortcuts: {len(self.config.get_shortcuts())}")
            else:
                messagebox.showerror("❌ Lỗi", 
                                   "Không thể export cấu hình!\n\n"
                                   "Vui lòng kiểm tra quyền ghi file.")
    
    def _on_monitoring_status_changed(self, is_active: bool):
        """Callback khi trạng thái monitoring thay đổi với icons hiện đại"""
        if is_active:
            self.status_label.config(text=f"{ModernIcons.HOTKEY} Đang theo dõi bàn phím")
            self.status_indicator.config(fg=ModernColors.SUCCESS, text=ModernIcons.ACTIVE)
        else:
            self.status_label.config(text=f"{ModernIcons.PAUSE} Đã dừng theo dõi")
            self.status_indicator.config(fg=ModernColors.DANGER, text=ModernIcons.INACTIVE)
    
    def _on_shortcut_triggered(self, keyword: str, type: str, content: str):
        """Callback khi shortcut được trigger với notification"""
        print(f"🔥 Triggered: {keyword} ({type})")
        # Có thể thêm toast notification ở đây
    
    def _toggle_autostart(self):
        """Bật/tắt khởi động cùng Windows"""
        success = toggle_autostart()
        if success:
            current = is_autostart_enabled()
            self.autostart_var.set(current)
            status = "bật" if current else "tắt"
            messagebox.showinfo("✅ Thành công", 
                              f"Đã {status} khởi động cùng Windows!\n\n"
                              f"Ứng dụng {'sẽ' if current else 'sẽ không'} tự động khởi động khi bật máy.")
        else:
            self.autostart_var.set(is_autostart_enabled())
            messagebox.showerror("❌ Lỗi", 
                                "Không thể thay đổi cài đặt khởi động!\n\n"
                                "Vui lòng chạy ứng dụng với quyền Administrator.")
    
    def _on_window_state_change(self, event):
        """Xử lý thay đổi trạng thái cửa sổ (đã disable để tránh loop)"""
        # Method này đã được disable để tránh infinite loop
        pass
    
    def _on_closing(self):
        """Xử lý khi đóng cửa sổ - chỉ cho phép thoát hoàn toàn hoặc ẩn"""
        if self.minimize_to_tray_var.get() and self.on_minimize_to_tray:
            # Thu nhỏ xuống tray (ẩn cửa sổ, không minimize)
            self.hide()
            self.on_minimize_to_tray()
            print("📤 Ẩn xuống system tray")
        else:
            # Thoát ứng dụng
            result = messagebox.askyesno("🚪 Thoát ứng dụng", 
                                       "Bạn có chắc muốn thoát ứng dụng?\n\n"
                                       "Ứng dụng sẽ ngừng theo dõi bàn phím.")
            if result:
                self.stop()
                self.root.destroy()
                print("🚪 Thoát ứng dụng hoàn toàn")
    
    def set_on_minimize_to_tray(self, callback):
        """Đặt callback khi minimize to tray"""
        self.on_minimize_to_tray = callback
    
    def show(self):
        """Hiển thị cửa sổ ở kích thước 1440x1080"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        print("📺 Hiển thị cửa sổ ở kích thước 1440x1080")
    
    def hide(self):
        """Ẩn cửa sổ"""
        self.root.withdraw()
        print("👁️ Ẩn cửa sổ")
    
    def start(self):
        """Khởi động ứng dụng"""
        self.keyboard_monitor.start_monitoring()
        self._update_performance_info()
        
        print("🚀 Khởi động ứng dụng ở kích thước 1440x1080")
        self.root.mainloop()
    
    def stop(self):
        """Dừng ứng dụng"""
        self.keyboard_monitor.stop_monitoring()
    
    def _set_preset(self, preset_type: str):
        """Đặt preset hiệu suất với icons hiện đại"""
        presets = {
            "ultra": {"instant": True, "delay": 0.01},
            "fast": {"instant": False, "delay": 0.05},
            "balanced": {"instant": False, "delay": 0.1},
            "safe": {"instant": False, "delay": 0.3}
        }
        
        if preset_type in presets:
            preset = presets[preset_type]
            self.instant_trigger_var.set(preset["instant"])
            self.delay_var.set(preset["delay"])
            self._on_instant_trigger_changed()
            self._on_delay_changed()
            self._update_performance_info()
            
            preset_names = {
                "ultra": f"{ModernIcons.ULTRA_FAST} Siêu nhanh",
                "fast": f"{ModernIcons.FAST} Nhanh", 
                "balanced": f"{ModernIcons.BALANCED} Cân bằng",
                "safe": f"{ModernIcons.SAFE} An toàn"
            }
            messagebox.showinfo(f"{ModernIcons.SUCCESS} Thành công", 
                              f"Đã áp dụng preset: {preset_names[preset_type]}")
    
    def _emergency_exit(self, event=None):
        """Thoát khẩn cấp bằng Ctrl+Alt+Q"""
        result = messagebox.askyesno("🆘 Thoát khẩn cấp", 
                                   "Thoát ứng dụng ngay lập tức?\n\n"
                                   "Phím tắt: Ctrl+Alt+Q")
        if result:
            print("🆘 Thoát khẩn cấp được kích hoạt!")
            self.stop()
            self.root.quit()
            self.root.destroy() 