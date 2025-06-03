# TextNow Qt Migration v2.0.0

Migration từ Tkinter sang PySide6 để tạo giao diện hiện đại khớp 100% với mockup design.

## 🚀 Tính năng mới

### UI Framework
- **PySide6 (Qt 6)**: Framework UI mạnh mẽ và hiện đại
- **QSS Styling**: Design tokens và styling system hoàn chỉnh  
- **QUiLoader**: Load UI từ file .ui để tách biệt design và code
- **High DPI Support**: Hỗ trợ màn hình độ phân giải cao

### Content Types Support ✨ **NEW**
- **📝 Văn bản**: Text-only shortcuts với rich text support
- **🖼️ Hình ảnh**: Single image shortcuts với file picker
- **📝🖼️ Văn bản + Ảnh**: Mixed content với text và multiple images (tối đa 20 ảnh)
- **Dynamic UI**: Ẩn/hiện form fields tùy theo loại content được chọn

### System Integration ✨ **NEW**
- **🔔 System Tray**: Thu nhỏ xuống khay hệ thống khi đóng cửa sổ
- **🚀 Auto Startup**: Khởi động cùng Windows với toggle trong tray menu
- **💬 Notifications**: Thông báo khi trigger shortcuts
- **📱 Single Instance**: Chỉ cho phép 1 instance chạy

### Design System
- **SVN Poppins Font**: Typography system hoàn chỉnh với multiple weights
- **Design Tokens**: Màu sắc, spacing, typography được định nghĩa trong QSS
- **Modern Colors**: Primary #7FD0FF, Success #34B369, Danger #FC6157
- **Responsive Layout**: 65% cho danh sách shortcuts, 32% cho form

### Components
- **ShortcutTableModel**: Table model với tô màu trạng thái tự động
- **Search Functionality**: Tìm kiếm real-time chỉ theo keyword
- **Status Indicators**: Chấm màu và text status động
- **Modern Buttons**: Styling theo mockup với hover effects
- **Image Manager**: Quản lý danh sách ảnh với drag & drop order

## 📁 Cấu trúc dự án

```
qt_ui/
├── forms/
│   └── main_window.ui          # UI layout file
├── models/
│   └── shortcut_table_model.py # Table model với màu sắc
├── resources/
│   ├── style.qss              # QSS styling với design tokens
│   └── resources.qrc          # Qt resources file
└── main_window_qt.py          # Main window controller

main_qt.py                     # Entry point cho Qt app
run_qt.bat                     # Batch file để chạy Qt app
requirements_qt.txt            # Dependencies cho Qt
test_qt_full.py               # Test script đầy đủ ✨ NEW
```

## 🛠️ Cài đặt và chạy

### Yêu cầu hệ thống
- **Python 3.8+**
- **Windows 10/11** (đã test)
- **PySide6 6.5.0+**

### Cách 1: Chạy trực tiếp (khuyến nghị)
```bash
# Cài đặt dependencies
pip install -r requirements_qt.txt

# Chạy app
python main_qt.py
```

### Cách 2: Sử dụng batch file
```bash
# Chạy file batch (Windows)
run_qt.bat
```

### Cách 3: Test đầy đủ
```bash
# Test tất cả tính năng
python test_qt_full.py
```

## 🎨 Design Implementation

### Layout theo mockup
- **Header**: Logo gấu 40x40px + thông tin status bên phải
- **Main Content**: 
  - Danh sách shortcuts (65% width) với search bar và nút "Tạo Shortcut"
  - Form thêm/sửa (32% width) với radio buttons và action buttons
- **Footer**: Import/Export buttons và settings button

### Colors từ mockup
- **Primary Button**: #7FD0FF (nút "Tạo Shortcut")
- **Success Status**: #34B369 (trạng thái "Bật")
- **Danger Status**: #FC6157 (trạng thái "Tắt")
- **Success Button**: #34B369 (nút "Cập nhật")
- **Danger Button**: #FC6157 (nút "Xóa")

### Typography
- **Font Family**: SVN Poppins (fallback: Segoe UI)
- **Header Text**: 16px, weight 500
- **Body Text**: 14px, weight 400
- **Table Headers**: 12px, weight 600, uppercase

## 📱 Tính năng System Tray

### Tray Menu
- **Hiển thị cửa sổ**: Restore từ system tray
- **Shortcuts: X**: Hiển thị số shortcuts hiện có
- **Trạng thái monitoring**: Hiển thị status keyboard monitoring
- **⚙️ Cài đặt**: Mở settings dialog
- **🚀 Khởi động cùng Windows**: Toggle auto startup
- **Thoát**: Đóng app hoàn toàn

### Behaviors
- **Close to Tray**: Đóng cửa sổ sẽ hide xuống tray thay vì thoát
- **Double-click**: Hiển thị lại cửa sổ
- **Notifications**: Thông báo khi trigger shortcuts
- **First time**: Hiển thị hướng dẫn về system tray

## 🖼️ Image Content Support

### Loại Văn bản
- Chỉ hiển thị text area
- Ẩn section quản lý ảnh
- Hoạt động như trước

### Loại Hình ảnh
- Ẩn text area
- Hiển thị image manager với:
  - **Chọn ảnh**: File picker cho images
  - **Xóa ảnh đã chọn**: Remove selected image
  - **Xóa tất cả**: Clear all images
  - **Danh sách**: Hiển thị thứ tự 1-20

### Loại Văn bản + Ảnh
- Hiển thị cả text area và image manager
- Mixed content structure:
  ```json
  {
    "text": "Nội dung văn bản",
    "images": ["/path/to/image1.png", "/path/to/image2.jpg"]
  }
  ```

## 🔧 Tích hợp với hệ thống cũ

### Compatibility
- **100% tương thích** với core modules hiện tại
- **Sử dụng lại**: Config, ShortcutManager, KeyboardMonitor
- **Single Instance**: Giữ nguyên tính năng single instance
- **Data Format**: Tương thích với shortcuts.json hiện tại
- **Mixed Content**: Hỗ trợ đầy đủ mixed content đã có sẵn

### Auto Startup với Windows
- **Registry Integration**: Sử dụng Windows Registry để quản lý startup
- **User-level**: Cài đặt cho user hiện tại (không cần admin)
- **Toggle**: Bật/tắt dễ dàng từ tray menu
- **Path Detection**: Tự động detect executable path (script hoặc exe)

### Migration Path
1. **Giữ nguyên Tkinter app** (`main.py`) để backup
2. **Qt app mới** (`main_qt.py`) sử dụng cùng data và logic
3. **Chuyển đổi từ từ** hoặc **chạy song song** để test

## 📊 So sánh Tkinter vs Qt

| Tính năng | Tkinter (cũ) | PySide6 (mới) |
|-----------|--------------|---------------|
| **UI Framework** | Tkinter | PySide6 (Qt 6) |
| **Styling** | Code-based | QSS (CSS-like) |
| **Layout** | Manual sizing | Designer + responsive |
| **Colors** | Hard-coded | Design tokens |
| **Table** | Treeview | QTableView + Model |
| **Icons** | Text emojis | Proper styling |
| **DPI Support** | Limited | Full support |
| **Performance** | Good | Excellent |
| **System Tray** | Custom implementation | Native Qt support |
| **Image Support** | Basic | Advanced with UI |
| **Auto Startup** | Manual registry | Built-in management |

## 🐛 Debugging

### Chạy với debug output
```bash
python main_qt.py
```

Console sẽ hiển thị:
- ✅ Font loading status
- ✅ UI loading progress  
- ✅ Component setup status
- ✅ System tray setup
- ✅ Registry access status
- 🔥 Shortcut trigger events
- ❌ Error messages với traceback

### Test Registry Access
```bash
python test_qt_full.py
```

Sẽ test:
- Registry read access
- Registry write access  
- Startup entry detection
- System tray availability

### Common Issues

1. **UI file not found**
   - Kiểm tra path: `qt_ui/forms/main_window.ui`
   - Chạy từ project root directory

2. **Font loading failed**
   - Kiểm tra fonts trong `fonts/` directory
   - Fallback tự động về Segoe UI

3. **PySide6 import error**
   - Cài đặt: `pip install PySide6`
   - Kiểm tra Python version >= 3.8

4. **System tray not available**
   - Kiểm tra Windows system tray enabled
   - App vẫn hoạt động bình thường, chỉ không có tray

5. **Registry access denied**
   - Chạy với user permissions bình thường
   - Không cần admin rights

## 🔮 Roadmap

### Đã hoàn thành ✅
- [x] UI layout theo mockup 100%
- [x] Design tokens và QSS styling
- [x] Table model với màu sắc trạng thái
- [x] Tích hợp với core functionality
- [x] Search và CRUD operations
- [x] Single instance support
- [x] System tray integration ✨ **NEW**
- [x] Auto startup với Windows ✨ **NEW**
- [x] Image content support ✨ **NEW**
- [x] Mixed content với UI ✨ **NEW**
- [x] Dynamic form visibility ✨ **NEW**
- [x] Close to tray behavior ✨ **NEW**

### Tiếp theo 🚧
- [ ] Settings dialog với Qt design
- [ ] Drag & drop image reordering
- [ ] Image preview thumbnails
- [ ] Build script với cx_Freeze/PyInstaller
- [ ] Auto-update mechanism
- [ ] Dark mode support
- [ ] Hotkey settings UI
- [ ] Export/Import ảnh với shortcuts

## 📸 Screenshots

Screenshots sẽ được lưu trong `docs/screenshots/`:
- `qt_text_mode.png`: Text mode UI
- `qt_image_mode.png`: Image mode UI  
- `qt_mixed_mode.png`: Mixed mode UI
- `qt_system_tray.png`: System tray menu
- `comparison.png`: Tkinter vs Qt comparison

## 🤝 Contributing

1. **Test Qt app**: Chạy `python test_qt_full.py` và test tất cả chức năng
2. **Test content types**: Thử tạo shortcuts với text, image, mixed content
3. **Test system tray**: Thử close to tray, startup settings
4. **So sánh với mockup**: Đảm bảo UI khớp 100%
5. **Report bugs**: Tạo issues với console output
6. **Suggest improvements**: UI/UX enhancements

## 📄 License

Giữ nguyên license của project gốc.

---

**Made with ❤️ using PySide6 & Qt Designer** 
**Enhanced with System Tray & Windows Integration** ✨ 