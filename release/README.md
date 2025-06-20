# 🎨 Auto Text & Image v1.3.3 - Modern UI Edition

## ✨ Tính năng mới: Giao diện hiện đại

**Phiên bản v1.3.3** mang đến giao diện hoàn toàn mới với:
- 🎨 **Icon System hiện đại**: Bộ icons nhất quán và đẹp mắt  
- 📝 **Typography Scale**: Font SVN Poppins với hierarchy rõ ràng
- 🎯 **Visual Hierarchy**: Cấu trúc thị giác dễ nhìn và hiện đại
- 🔵 **Semantic Colors**: Màu sắc có ý nghĩa (xanh=hoạt động, đỏ=dừng)

## 📋 Tổng quan

Ứng dụng tự động thay thế text và chèn hình ảnh khi gõ từ khóa với:
- ✨ **Giao diện fullscreen hiện đại** với font SVN Poppins
- 🎨 **Icon system nhất quán** cho tất cả elements
- ⚡ **Tốc độ trigger tùy chỉnh** (từ tức thì đến 1 giây)
- 📝 **Shortcuts text/image** không giới hạn
- 🚀 **Khởi động cùng Windows** (tuỳ chọn)
- 📤 **System tray integration** hoàn chỉnh

## 🎯 Giao diện mới v1.3.3

### Header hiện đại
```
✨ Auto Text & Image 📺        🟢 ⌨️ Đang theo dõi bàn phím
                              📝 5 shortcuts | ⚖️ Chế độ: Cân bằng | 📺 Toàn màn hình
```

### Navigation với icons
- 📝 **Quản lý Shortcuts**: Danh sách và form chỉnh sửa
- ⚙️ **Cài đặt**: Performance và System settings

### Form controls hiện đại
- 🔤 **Từ khóa**: Input với typography semibold
- 📝 **Loại**: Radio buttons với icons (📄 Văn bản / 🖼️ Hình ảnh)
- 📝 **Nội dung**: Textarea responsive
- ✅ **Kích hoạt**: Checkbox với success icon

### Action buttons với semantic colors
- ➕ **Thêm mới** (Primary blue)
- 💾 **Cập nhật** (Success green)  
- 🗑️ **Xóa** (Danger red)
- 🧹 **Làm mới** (Secondary gray)

## 🚀 Performance Presets với icons

- ⚡ **Siêu nhanh**: Trigger tức thì (0ms delay)
- 🚀 **Nhanh**: Delay 0.05s  
- ⚖️ **Cân bằng**: Delay 0.1s (khuyến nghị)
- 🛡️ **An toàn**: Delay 0.3s

## 📊 Typography Scale

Font SVN Poppins với hierarchy rõ ràng:
- **32px Display**: App title (Bold)
- **26px H1**: Section headers (Bold)  
- **20px H2**: Subsections (Semibold)
- **14px Large**: Important text (Medium)
- **12px Body**: Regular content (Regular)
- **10px Caption**: Small info (Medium)

## 🎨 Color Palette

- 🔵 **Primary**: #3b82f6 (Blue) - Actions, links
- 🟢 **Success**: #10b981 (Green) - Success states  
- 🟡 **Warning**: #f59e0b (Amber) - Warnings
- 🔴 **Danger**: #ef4444 (Red) - Errors, delete
- ⚫ **Text**: #1f2937 (Dark gray) - Primary text
- 🔘 **Secondary**: #6b7280 (Gray) - Secondary text

## 📋 Shortcuts Management

### Danh sách với icons
```
✨ Từ khóa    📝 Loại          📝 Nội dung         🟢 Trạng thái
hello        📄 Văn bản       Xin chào!          🟢 Bật
logo         🖼️ Ảnh          /path/to/logo.png   🟢 Bật
sig          📄🖼️ Văn bản + Ảnh  Chữ ký + ảnh      🟢 Bật
```

### Form thêm/sửa hiện đại
```
🔤 Từ khóa:        [___________________]
📝 Loại nội dung:  ○ 📄 Văn bản  ○ 🖼️ Hình ảnh  ○ 📄🖼️ Văn bản + Ảnh
📝 Nội dung:       [_____________________]
                   [                     ]
                   [_____________________]
✅ Kích hoạt shortcut

➕ Thêm mới    💾 Cập nhật
🗑️ Xóa        🧹 Làm mới
```

### 📄🖼️ Mixed Content (Văn bản + Ảnh)
Tính năng mới cho phép tạo shortcut chứa cả văn bản và nhiều ảnh:

**Thứ tự xử lý:**
- 📝 Văn bản: Paste trước (nếu có)
- 🖼️ Ảnh 1: Paste sau văn bản  
- 🖼️ Ảnh 2: Paste tiếp theo
- 🖼️ Ảnh 3: Paste tiếp theo
- ... (tối đa 20 ảnh)

**Cách sử dụng:**
1. Chọn "📄🖼️ Văn bản + Ảnh"
2. Nhập văn bản (có thể để trống)
3. Thêm ảnh (1-20 ảnh, đánh số từ 1)
4. Khi trigger: văn bản paste trước → ảnh 1 → ảnh 2 → ... → ảnh 20

## ⚙️ Settings hiện đại

### 🚀 Performance Settings
```
⚡ Trigger ngay lập tức (Tốc độ tối đa)
⏳ Thời gian chờ: [0.10] giây

🚀 Presets nhanh:
⚡ Siêu nhanh    🚀 Nhanh
⚖️ Cân bằng      🛡️ An toàn
```

### 🔧 System Settings  
```
▶️ Khởi động cùng Windows
📤 Thu nhỏ xuống khay khi đóng
```

## 🔧 Installation & Setup

### Yêu cầu hệ thống
- Windows 10/11
- Python 3.8+ (hoặc chạy file .exe)
- **Font SVN Poppins** (đã bao gồm trong package)

### Cài đặt
```bash
# Clone repository
git clone [repo-url]
cd auto-text-image

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py

# Hoặc build executable
pyinstaller AutoTextImage.spec
```

### Cách sử dụng
1. **Thêm shortcut**: 
   - Nhập từ khóa (VD: `@email`, `#phone`, `logo`)
   - Chọn loại: Văn bản hoặc Hình ảnh
   - Nhập nội dung hoặc chọn file ảnh
   - Click "Thêm mới"

2. **Sử dụng shortcut**:
   - Gõ từ khóa bất kỳ đâu
   - Văn bản/ảnh sẽ tự động thay thế

3. **Tùy chỉnh hiệu suất**:
   - Chọn preset phù hợp với nhu cầu
   - Hoặc tùy chỉnh delay thủ công

## 📈 Version History

- **v1.3.3** (2025-01-06): Modern UI với icon system và typography scale
- **v1.3.2** (2025-01-06): SVN Poppins font + Fullscreen mode
- **v1.3.1** (2024-12-XX): Sửa lỗi race condition tốc độ cao
- **v1.3.0** (2024-12-XX): Gộp text types, cải tiến performance
- **v1.2.0** (2024-12-XX): UI hiện đại với tabs
- **v1.1.0** (2024-12-XX): Thêm rich text support
- **v1.0.0** (2024-12-XX): Phiên bản đầu tiên

## 🎯 Screenshots

*Giao diện v1.3.3 với icons hiện đại và typography SVN Poppins trong chế độ fullscreen*

---

**Auto Text & Image v1.3.3 - Modern UI Edition**  
*Giao diện đẹp, hiệu suất cao, trải nghiệm tuyệt vời* ✨

## 🔤 Tính năng mới - Font SVN Poppins

**Font tiếng Việt đẹp mắt và hiện đại!**

- ✨ **Font SVN Poppins**: Font Sans-serif hiện đại, dễ đọc
- 🇻🇳 **Hỗ trợ tiếng Việt hoàn chỉnh**: Tất cả dấu tiếng Việt hiển thị đẹp mắt
- ⚖️ **9 Font weights**: Thin, ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold, Black
- 🔄 **Auto fallback**: Tự động dùng Segoe UI nếu không load được SVN Poppins
- 🚀 **Load tự động**: Font được load ngay khi khởi động ứng dụng

## 🎨 Giao diện hiện đại

- **Modern Dark Theme** với màu sắc hiện đại
- **Responsive Layout** tự động điều chỉnh theo kích thước cửa sổ  
- **Icons & Visual Elements** giúp dễ nhận diện
- **Typography System** với SVN Poppins đa dạng font weights
- **Interactive Elements** với hover effects và animations

## 🚀 Tính năng chính

### ⌨️ Auto Text Replacement
- Gõ từ khóa → thay thế tự động bằng văn bản hoặc hình ảnh
- Hỗ trợ **tất cả ký tự đặc biệt**: `@ # $ % ^ & * ( ) - + = [ ] { } | \ : ; " ' < > , . ? /`
- **Text và HTML**: Văn bản thuần hoặc rich text với formatting
- **Image shortcuts**: Chèn ảnh trực tiếp vào clipboard

### ⚡ Tốc độ cao đã tối ưu
- **4 chế độ hiệu suất**:
  - 🔥 **Siêu nhanh**: Trigger ngay lập tức (đã sửa lỗi race condition)
  - 🚀 **Nhanh**: Delay 0.05s (đã sửa lỗi)  
  - ⚖️ **Cân bằng**: Delay 0.1s (khuyến nghị)
  - 🛡️ **An toàn**: Delay 0.3s
- **Smart caching** và thuật toán tìm kiếm tối ưu
- **Real-time updates**: Shortcuts mới có thể dùng ngay không cần restart

## 🔧 Tính năng nâng cao

### Font Management
- **Font auto-loading**: SVN Poppins được load tự động khi khởi động
- **Multiple weights**: Sử dụng đa dạng font weights cho different UI elements
- **Fallback system**: Tự động chuyển về Segoe UI nếu có vấn đề
- **Font caching**: Cache fonts để tăng tốc độ load

### Import/Export
- **Backup cấu hình**: Export shortcuts ra file JSON
- **Restore từ backup**: Import shortcuts từ file khác
- **Share với team**: Chia sẻ shortcuts với đồng nghiệp

### System Integration  
- **Startup với Windows**: Tự động khởi động cùng hệ thống
- **System tray**: Thu nhỏ xuống khay hệ thống
- **Global hotkeys**: Hoạt động trong mọi ứng dụng

## 🧪 Testing

### Font Test
```bash
# Test font SVN Poppins
python test_font.py
```

### Manual Testing
1. Kiểm tra font trong console log khi khởi động
2. So sánh giao diện trước/sau khi áp dụng font
3. Test các font weights khác nhau trong UI

## 🤝 Contribution

Đóng góp ý kiến và báo cáo lỗi tại Issues.

**Font SVN Poppins**: Tải từ nguồn official để đảm bảo chất lượng tốt nhất.

---

**Made with ❤️ in Vietnam - Powered by SVN Poppins Typography** 

# 🚀 TextNow - Auto Text & Image v2.0.1

**Ứng dụng gõ tắt thông minh cho Windows với giao diện PySide6 hiện đại**

## ✨ Tính năng chính

- 🔤 **Auto Text**: Gõ tắt để chèn văn bản đã định sẵn
- 🖼️ **Auto Image**: Gõ tắt để chèn hình ảnh
- 🎭 **Mixed Mode**: Kết hợp văn bản và hình ảnh
- 📱 **System Tray**: Chạy ngầm trong khay hệ thống
- 🔇 **Hidden Startup**: Khởi động ẩn cùng Windows
- 🎨 **Modern UI**: Giao diện đẹp mắt với PySide6
- 🛡️ **Single Instance**: Chỉ chạy một phiên bản
- 💾 **Import/Export**: Sao lưu và khôi phục cài đặt

## 🔇 Tính năng Startup Ẩn - MỚI!

### 🚀 Khởi động ẩn - Nhiều cách sử dụng:

#### 1. **Command Line**
```bash
# Các cách khởi động ẩn
python main_qt.py --hidden
python main_qt.py --silent
python main_qt.py --minimized
python main_qt.py --tray

# Hoặc dùng flag ngắn
python main_qt.py -h
python main_qt.py -s
```

#### 2. **Batch File - Đơn giản nhất**
```batch
# Chạy file có sẵn
start_textnow_hidden.bat
```

#### 3. **Auto Startup cùng Windows**
1. Mở TextNow
2. Nhấp chuột phải vào **System Tray Icon**
3. Chọn **"🚀 Khởi động cùng Windows"**
4. ✅ **Xong!** Phần mềm sẽ tự động chạy ẩn mỗi khi khởi động Windows

### 📱 Sử dụng System Tray:
- **Nhấp đúp** icon để mở cửa sổ chính
- **Chuột phải** để xem menu với đầy đủ tùy chọn
- **Im lặng hoàn toàn**: Không có notification khi khởi động ẩn
- **Kiểm tra tray**: Tìm icon TextNow trong khay hệ thống để xác nhận đang chạy

## 💻 Yêu cầu hệ thống

- **Windows 10/11** (64-bit)
- **Python 3.8+** 
- **PySide6** (tự động cài đặt)

## 🚀 Cách sử dụng

### Cài đặt nhanh:
```bash
# Clone hoặc tải về
git clone <repository-url>
cd textnow

# Cài đặt dependencies
pip install -r requirements_qt.txt

# Chạy ứng dụng
python main_qt.py

# Hoặc chạy ẩn ngay
python main_qt.py --hidden
```

### Khởi động thông thường:
```bash
# Chạy với giao diện
python main_qt.py

# Hoặc dùng batch file
run_qt.bat
```

### Khởi động ẩn:
```bash
# Chạy ẩn ngay vào system tray
start_textnow_hidden.bat

# Hoặc dùng lệnh
python main_qt.py --hidden
```

## 📋 Hướng dẫn sử dụng

### Tạo Shortcut:
1. Nhập **Shortcut** (từ khóa gõ tắt)
2. Chọn **loại**: Văn bản, Hình ảnh, hoặc Văn bản + Ảnh
3. Nhập **nội dung** hoặc chọn ảnh
4. **Bấm "Thêm Shortcut"**

### Sử dụng Shortcut:
- Gõ từ khóa shortcut trong bất kỳ ứng dụng nào
- Nội dung sẽ tự động được chèn vào

### Quản lý ảnh:
- Kéo thả ảnh vào vùng **Quản lý ảnh**
- Tối đa **20 ảnh**, thứ tự từ 1-20
- Sử dụng các nút điều khiển để sắp xếp

## 🎛️ System Tray Menu

Khi chạy ẩn, menu system tray bao gồm:
- 📺 **Hiển thị cửa sổ** - Mở giao diện chính
- 📋 **Shortcuts: X** - Số lượng shortcuts
- 🔄 **Trạng thái** - Đang theo dõi/Tạm dừng
- ⚙️ **Cài đặt** - Tùy chọn
- 🚀 **Khởi động cùng Windows** - Bật/tắt
- 🚪 **Thoát** - Đóng ứng dụng

## 🔧 Build thành EXE

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build
python -m PyInstaller TextNowQt.spec

# File EXE sẽ ở trong thư mục dist/
```

## 📂 Cấu trúc dự án

```
textnow/
├── main_qt.py              # Entry point chính
├── main_qt_silent.py       # Entry point startup ẩn  
├── start_textnow_hidden.bat # Batch khởi động ẩn
├── qt_ui/                   # Giao diện PySide6
│   ├── main_window_qt.py   # Main window controller
│   └── forms/              # UI files
├── core/                    # Logic chính
│   ├── shortcut_manager.py # Quản lý shortcuts
│   └── keyboard_monitor.py # Theo dõi bàn phím
├── utils/                   # Tiện ích
└── docs/                    # Tài liệu
```

## 🆘 Troubleshooting

### Ứng dụng không khởi động ẩn?
1. Kiểm tra **System Tray** (có thể bị ẩn)
2. Kiểm tra Python: `python --version`
3. Cài lại dependencies: `pip install -r requirements_qt.txt`

### System Tray không hiện icon?
1. **Windows Settings** → Taskbar → "Show all icons"
2. Restart Windows Explorer:
   ```cmd
   taskkill /f /im explorer.exe
   start explorer.exe
   ```

### Auto startup không hoạt động?
1. Chạy với quyền **Administrator**
2. Kiểm tra Registry: `regedit` → `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`

## 📖 Tài liệu bổ sung

- [`HIDDEN_STARTUP_GUIDE.md`](HIDDEN_STARTUP_GUIDE.md) - Hướng dẫn chi tiết tính năng startup ẩn
- [`CHANGELOG.md`](CHANGELOG.md) - Lịch sử cập nhật
- [`README_QT_MIGRATION.md`](README_QT_MIGRATION.md) - Quá trình chuyển đổi UI

## 📞 Hỗ trợ

- 🐛 **Bug Reports**: Tạo issue với thông tin chi tiết
- 💡 **Feature Requests**: Đề xuất tính năng mới
- 📧 **Contact**: Email hỗ trợ

## 🏷️ Version Info

- **Version**: 2.0.1
- **UI Framework**: PySide6 (Qt 6)
- **Platform**: Windows 10/11
- **Python**: 3.8+

---

**🔇 Lưu ý**: Để sử dụng tính năng startup ẩn, hãy đọc [`HIDDEN_STARTUP_GUIDE.md`](HIDDEN_STARTUP_GUIDE.md) để biết chi tiết! 