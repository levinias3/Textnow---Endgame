# Changelog - Auto Text & Image

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

---

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