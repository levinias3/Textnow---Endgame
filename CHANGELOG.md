# Changelog - Auto Text & Image

## v2.0.1 - Terminal Independence (2025-01-06)

### 🔓 Terminal Independence Solutions
- **NEW**: `run_qt_silent.bat` - Chế độ khởi động silent với thông tin
- **NEW**: `start_textnow.bat` - Khởi động nhanh hoàn toàn độc lập
- **NEW**: Documentation `STARTUP_MODES.md` với hướng dẫn chi tiết
- **SOLVED**: Vấn đề app bị tắt khi đóng terminal

### 🚀 Multiple Startup Modes
1. **🖥️ Debug Mode**: `run_qt.bat` / `run_qt_enhanced.bat` - Có logs, gắn terminal
2. **🔇 Silent Mode**: `run_qt_silent.bat` - Hiển thị info, chạy độc lập  
3. **⚡ Quick Mode**: `start_textnow.bat` - Khởi động siêu nhanh, hoàn toàn ẩn

### 🔧 Technical Implementation
- **ENHANCED**: Sử dụng `pythonw.exe` thay vì `python.exe` cho GUI mode
- **ADDED**: Fallback với `start /min` nếu không có pythonw
- **IMPROVED**: `main_qt_silent.py` với `startup_mode = True`
- **OPTIMIZED**: Silent dependency installation và error handling

### 💡 User Experience
- **INDEPENDENT**: App chạy hoàn toàn độc lập khỏi terminal
- **FLEXIBLE**: 3 chế độ khởi động phù hợp từng mục đích
- **SEAMLESS**: Single instance vẫn hoạt động bình thường
- **INFORMATIVE**: Hiển thị trạng thái khi cần, ẩn khi không cần

### 📋 How To Use
```batch
# Sử dụng hằng ngày (khuyến nghị)
start_textnow.bat

# Muốn xem thông tin khởi động  
run_qt_silent.bat

# Debug và phát triển
run_qt.bat
```

### ✅ Problem Solved
- ❌ Tắt terminal → tắt app → ✅ App độc lập hoàn toàn
- ❌ Terminal luôn hiển thị → ✅ Có thể ẩn hoặc hiện tuỳ chọn
- ❌ Không biết app đã khởi động → ✅ Thông báo rõ ràng khi cần

## v1.3.6 - Single Instance Control (2025-01-06)

### 🔒 Single Instance Management
- **NEW**: Single instance control mechanism (`utils/single_instance.py`)
- **NEW**: File locking system để đảm bảo chỉ có 1 phiên bản chạy
- **NEW**: Inter-process communication qua TCP socket (Windows)
- **NEW**: Auto signal existing instance khi thử mở phiên bản mới
- **FIXED**: Vấn đề multiple instances trong system tray

### 🔧 Technical Implementation
- **ADDED**: File lock sử dụng `msvcrt.locking()` trên Windows
- **ADDED**: Cross-platform socket communication
- **ADDED**: Periodic signal checking (500ms intervals)
- **ADDED**: Proper lock cleanup khi thoát ứng dụng
- **ENHANCED**: Main window show/hide logic

### 🎯 User Experience Improvements
- **IMPROVED**: Khi mở app lần 2, tự động hiện cửa sổ của instance đang chạy
- **PREVENTED**: Multiple instances gây confusion trong system tray
- **MAINTAINED**: Tất cả tính năng minimize to tray và exit
- **SIMPLIFIED**: Chỉ 1 icon trong system tray thay vì nhiều

### 🐛 Bug Fixes
- **FIXED**: Multiple system tray icons khi mở/đóng app nhiều lần
- **FIXED**: Background processes không được cleanup
- **FIXED**: Memory leaks từ duplicate instances
- **IMPROVED**: Resource management và cleanup

### 📋 New Files
```
+ utils/single_instance.py  # Single instance control module
* main.py                   # Updated với single instance logic
```

### 🔄 How it Works
1. **First launch**: Acquire file lock, start normally
2. **Second launch**: Detect existing lock, send "SHOW_WINDOW" signal
3. **Existing instance**: Receive signal, show main window  
4. **Exit**: Release lock, cleanup resources

## v1.3.5 - Window Size Optimization (2025-01-06)

### 📺 Window Size Changes
- **CHANGED**: Kích thước cửa sổ từ fullscreen xuống 1440x1080
- **IMPROVED**: Có thể resize và di chuyển cửa sổ 
- **ADDED**: Kích thước tối thiểu 1200x800
- **ENHANCED**: Cửa sổ hiển thị ở giữa màn hình khi khởi động

### 🎨 UI Updates
- **UPDATED**: App title icon từ 📺 (fullscreen) sang 🪟 (window)
- **UPDATED**: Performance info hiển thị "1440x1080" thay vì "Toàn màn hình"
- **UPDATED**: Footer version thành v1.3.5
- **UPDATED**: Settings info phản ánh chế độ cửa sổ mới

### 🔧 Technical Improvements
- **OPTIMIZED**: Layout responsive cho kích thước 1440x1080
- **REMOVED**: Force fullscreen functions (không còn cần thiết)
- **SIMPLIFIED**: Window management code
- **MAINTAINED**: Tất cả tính năng core và search

## v1.3.4 - Search Feature Edition (2025-01-06)

### 🔍 New Search Feature
- **NEW**: Tìm kiếm shortcut theo keyword trong giao diện quản lý
- **NEW**: Ô tìm kiếm ở phía trên danh sách shortcuts
- **NEW**: Tìm kiếm real-time không phân biệt hoa/thường
- **NEW**: Nút xóa tìm kiếm nhanh (🧹)
- **NEW**: Hiển thị số lượng "X/Y shortcuts" khi tìm kiếm

### 🎯 Search Capabilities
- **FOCUSED**: Chỉ tìm kiếm theo giá trị shortcut keyword
- **SMART**: Không tìm theo "loại" hay "nội dung" như yêu cầu
- **FAST**: Tìm kiếm từng phần, không cần gõ đầy đủ từ khóa
- **SEAMLESS**: Giữ nguyên tất cả tính năng chọn/sửa/xóa shortcuts

### 🎨 UI/UX Integration
- **MODERN**: Sử dụng icon 🔍 và typography SVN Poppins
- **RESPONSIVE**: Grid layout tự động điều chỉnh
- **CONSISTENT**: Tuân theo ModernStyle và ModernColors
- **INTUITIVE**: Vị trí hợp lý ngay trên danh sách

### 🔧 Technical Implementation
- **EFFICIENT**: O(n) search algorithm với in-memory filtering
- **RELIABLE**: Index mapping đúng giữa filtered và original list
- **COMPATIBLE**: Không thay đổi data format hay core functionality
- **MAINTAINABLE**: Clean code với proper separation of concerns

### 📋 New Functions
```python
_filter_shortcuts()     # Lọc shortcuts theo keyword
_on_search_changed()    # Handle search input changes  
_clear_search()         # Reset search state
```

## v1.3.3 - Modern UI Edition (2025-01-06)

### 🎨 Major UI/UX Improvements
- **NEW**: Hệ thống icon hiện đại với `utils/icon_manager.py`
- **NEW**: Typography scale chuẩn theo Major Third (1.25)
- **NEW**: Color system semantic với `ModernColors`
- **IMPROVED**: Visual hierarchy rõ ràng với font weights
- **IMPROVED**: Icons nhất quán cho tất cả components
- **IMPROVED**: Button styling với semantic colors

### 🎯 Enhanced User Experience
- **Header**: App title với typography H1 + fullscreen icon
- **Status**: Dynamic icons với màu semantic (green/red)
- **Tabs**: Icons rõ ràng cho Shortcuts và Settings
- **Form**: Labels với semibold weight + matching icons
- **Buttons**: Primary/Success/Danger styling với icons
- **Performance**: Dynamic icons theo preset mode

### 🔧 Technical Improvements
- Font size scale: Display(32) → H1(26) → H2(20) → Body(12) → Caption(10)
- Consistent icon mapping: Text(📄), Image(🖼️), Status(🟢/🔴)
- Semantic colors: Blue(Primary), Green(Success), Red(Danger)
- Typography weights: Bold(titles), Semibold(labels), Regular(body)

### 📊 Visual Enhancements
- Form controls với icons: Add(➕), Save(💾), Delete(🗑️), Clear(🧹)
- Performance presets: Ultra Fast(⚡), Fast(🚀), Balanced(⚖️), Safe(🛡️)
- System settings: Autostart(▶️), Tray(📤), Info(ℹ️)
- Treeview columns với icons cho headers và data

## v1.3.2 - SVN Poppins Edition + Fullscreen Mode (2025-01-06)

### 🔤 Font SVN Poppins Integration
- **NEW**: Tích hợp font SVN Poppins với 9 font weights
- **NEW**: Font Manager module (`utils/font_manager.py`)
  - Auto-loading fonts từ Windows GDI32 API
  - Support 9 weights: Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, Black
  - Fallback system về Segoe UI nếu load lỗi
  - Font caching để tăng tốc độ
- **NEW**: Font test tool (`test_font.py`)
- **IMPROVED**: ModernStyle class với typography system hoàn chỉnh

### 🎨 UI Typography Updates
- **UPDATED**: Tất cả fonts trong UI chuyển sang SVN Poppins
- **IMPROVED**: Button fonts với SemiBold weight
- **IMPROVED**: Header fonts với Bold weight  
- **IMPROVED**: Heading fonts với SemiBold weight
- **UPDATED**: App title và version info
- **ENHANCED**: Font consistency across all UI elements

### 📁 File Structure Changes
```
+ fonts/
  + SVN-Poppins (18 fonts) + webfonts/
    + TTF/
      + SVN-Poppins-*.ttf (9 files)
+ utils/font_manager.py
+ test_font.py
* ui/main_window.py (updated với font system)
* README.md (major rewrite)
```

### 🔧 Technical Improvements
- **ADDED**: Windows GDI32 API integration for font loading
- **ADDED**: Cross-platform font loading support
- **ADDED**: Font validation và error handling
- **ENHANCED**: Style configuration với font tuples
- **IMPROVED**: Debug logging cho font operations

## v1.3.1 - Speed Fix (2025-01-05)

### 🐛 Critical Bug Fixes
- **FIXED**: Race condition ở chế độ "Siêu nhanh" và "Nhanh"
- **FIXED**: Shortcuts mới append text thay vì replace
- **FIXED**: Clipboard verification cho image shortcuts

### ⚡ Performance Improvements
- **IMPROVED**: Serialized workflow: Delete → Copy → Paste
- **ENHANCED**: Timing optimization với delays tăng cường
- **ADDED**: Real-time shortcut updates (không cần restart)
- **IMPROVED**: Enhanced debugging với emoji logs

### 🔄 New Features
- **NEW**: `refresh_keywords_cache()` method
- **NEW**: Comprehensive state management
- **NEW**: Auto-apply shortcuts sau add/update/delete

---

## v1.3.0 - Modern UI (2025-01-04)

### 🎨 UI/UX Overhaul
- **NEW**: Modern Dark Theme với color palette chuyên nghiệp
- **NEW**: Responsive layout với grid system
- **NEW**: Typography system với size/weight hierarchy
- **NEW**: Icons và visual indicators

### 🚀 Performance Features
- **NEW**: 4 preset modes: Ultra/Fast/Balanced/Safe
- **NEW**: Instant trigger mode
- **NEW**: Performance monitoring
- **NEW**: Smart caching system

### 🔧 Core Improvements
- **ENHANCED**: Form validation và UX flows
- **IMPROVED**: Error handling và user feedback
- **ADDED**: Status indicators và progress feedback

---

## v1.2.0 - Core Features (Previous)

### 📝 Basic Functionality
- Text và Image shortcuts
- Keyboard monitoring
- Clipboard handling
- Import/Export config
- System tray integration

---

## Upcoming Features 🚀

### v1.4.0 - Advanced Typography
- [ ] Variable font support
- [ ] Custom font selection
- [ ] Theme customization
- [ ] RTL language support

### v1.5.0 - Cloud Sync
- [ ] Cloud backup
- [ ] Multi-device sync  
- [ ] Team sharing
- [ ] Version control

---

**Contributors**: Development Team
**License**: MIT
**Platform**: Windows 10/11 