"""
Module quản lý icons hiện đại cho ứng dụng Auto Text & Image
"""

class ModernIcons:
    """Bộ sưu tập icons hiện đại với Unicode và Emoji"""
    
    # ===== NAVIGATION & TABS =====
    SHORTCUTS = "📝"           # Tab Shortcuts
    SETTINGS = "⚙️"           # Tab Settings
    PERFORMANCE = "🚀"        # Performance settings
    SYSTEM = "🔧"             # System settings
    INFO = "ℹ️"              # Information
    
    # ===== ACTIONS =====
    ADD = "➕"                # Add new
    EDIT = "✏️"              # Edit/Update
    DELETE = "🗑️"           # Delete
    SAVE = "💾"              # Save
    CLEAR = "🧹"             # Clear/Reset
    IMPORT = "📥"            # Import
    EXPORT = "📤"            # Export
    BROWSE = "📁"            # Browse files
    
    # ===== STATUS & INDICATORS =====
    ACTIVE = "🟢"            # Active/Online
    INACTIVE = "🔴"          # Inactive/Offline
    SUCCESS = "✅"           # Success
    ERROR = "❌"             # Error
    WARNING = "⚠️"          # Warning
    LOADING = "⏳"           # Loading
    
    # ===== CONTENT TYPES =====
    TEXT = "📄"              # Text content
    IMAGE = "🖼️"            # Image content
    MIXED = "📄🖼️"           # Text + Images content
    KEYWORD = "🔤"           # Keyword
    CONTENT = "📝"           # General content
    
    # ===== CONTROLS =====
    PLAY = "▶️"              # Start/Play
    PAUSE = "⏸️"             # Pause
    STOP = "⏹️"              # Stop
    REFRESH = "🔄"           # Refresh
    SEARCH = "🔍"            # Search
    
    # ===== UI ELEMENTS =====
    WINDOW = "📺"            # Window/Display
    MENU = "☰"               # Menu
    CLOSE = "✖️"             # Close
    MINIMIZE = "🔽"          # Minimize
    MAXIMIZE = "🔼"          # Maximize
    LOCK = "🔒"              # Lock/Security
    
    # ===== ADVANCED =====
    FULLSCREEN = "📺"        # Fullscreen mode
    TRAY = "📤"              # System tray
    NOTIFICATION = "📢"      # Notification
    HOTKEY = "⌨️"            # Hotkey/Keyboard
    
    # ===== SPEED & PERFORMANCE =====
    ULTRA_FAST = "⚡"        # Ultra fast mode
    FAST = "🚀"              # Fast mode
    BALANCED = "⚖️"          # Balanced mode
    SAFE = "🛡️"             # Safe mode
    
    @staticmethod
    def get_status_icon(enabled: bool) -> str:
        """Lấy icon trạng thái theo enabled state"""
        return ModernIcons.ACTIVE if enabled else ModernIcons.INACTIVE
    
    @staticmethod
    def get_content_type_icon(content_type: str) -> str:
        """Lấy icon theo loại content"""
        icon_map = {
            'text': ModernIcons.TEXT,
            'richtext': ModernIcons.TEXT, 
            'image': ModernIcons.IMAGE,
            'mixed': ModernIcons.MIXED
        }
        return icon_map.get(content_type, ModernIcons.CONTENT)
    
    @staticmethod
    def get_speed_icon(mode: str) -> str:
        """Lấy icon theo chế độ tốc độ"""
        icon_map = {
            'ultra': ModernIcons.ULTRA_FAST,
            'fast': ModernIcons.FAST,
            'balanced': ModernIcons.BALANCED,
            'safe': ModernIcons.SAFE
        }
        return icon_map.get(mode, ModernIcons.BALANCED)

class ModernColors:
    """Bộ màu hiện đại cho icons và UI elements"""
    
    # Primary colors
    PRIMARY = "#3b82f6"        # Blue 500
    PRIMARY_DARK = "#1d4ed8"   # Blue 700
    PRIMARY_LIGHT = "#60a5fa"  # Blue 400
    
    # Accent colors
    SUCCESS = "#10b981"        # Emerald 500
    SUCCESS_LIGHT = "#34d399"  # Emerald 400
    
    WARNING = "#f59e0b"        # Amber 500
    WARNING_LIGHT = "#fbbf24"  # Amber 400
    
    DANGER = "#ef4444"         # Red 500
    DANGER_LIGHT = "#f87171"   # Red 400
    
    # Neutral colors
    TEXT_PRIMARY = "#1f2937"   # Gray 800
    TEXT_SECONDARY = "#6b7280" # Gray 500
    TEXT_MUTED = "#9ca3af"     # Gray 400
    
    BACKGROUND = "#ffffff"     # White
    SURFACE = "#f9fafb"        # Gray 50
    BORDER = "#e5e7eb"         # Gray 200
    
    @staticmethod
    def get_status_color(enabled: bool) -> str:
        """Lấy màu trạng thái"""
        return ModernColors.SUCCESS if enabled else ModernColors.DANGER
    
    @staticmethod
    def get_priority_color(priority: str) -> str:
        """Lấy màu theo mức độ ưu tiên"""
        color_map = {
            'high': ModernColors.DANGER,
            'medium': ModernColors.WARNING, 
            'low': ModernColors.SUCCESS,
            'info': ModernColors.PRIMARY
        }
        return color_map.get(priority, ModernColors.TEXT_SECONDARY)

class TypographyScale:
    """Thang đo typography hiện đại"""
    
    # Font sizes (theo scale 1.25 - Major Third)
    DISPLAY = 32    # Display text
    H1 = 26         # Main headings
    H2 = 20         # Section headings  
    H3 = 16         # Subsection headings
    H4 = 14         # Small headings
    
    BODY_LARGE = 14 # Large body text
    BODY = 12       # Regular body text
    BODY_SMALL = 11 # Small body text
    CAPTION = 10    # Captions and labels
    MICRO = 9       # Micro text
    
    # Font weights
    THIN = 'thin'           # 100
    LIGHT = 'light'         # 300
    REGULAR = 'regular'     # 400
    MEDIUM = 'medium'       # 500
    SEMIBOLD = 'semibold'   # 600
    BOLD = 'bold'           # 700
    BLACK = 'black'         # 900
    
    @staticmethod
    def get_heading_style(level: int) -> tuple:
        """Lấy style cho heading theo level"""
        styles = {
            1: (TypographyScale.H1, TypographyScale.BOLD),
            2: (TypographyScale.H2, TypographyScale.SEMIBOLD),
            3: (TypographyScale.H3, TypographyScale.SEMIBOLD),
            4: (TypographyScale.H4, TypographyScale.MEDIUM)
        }
        return styles.get(level, (TypographyScale.BODY, TypographyScale.REGULAR)) 