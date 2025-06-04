# 🔇 Hướng dẫn sử dụng tính năng Startup Ẩn - TextNow Qt

## 📋 Tổng quan

Tính năng **Startup Ẩn** cho phép TextNow khởi động cùng Windows mà không hiển thị giao diện chính, ứng dụng sẽ chạy ngầm trong system tray.

## 🚀 Các cách khởi động ẩn

### 1. Sử dụng Command Line Arguments

```bash
# Khởi động ẩn với Python script
python main_qt.py --hidden
python main_qt.py --silent
python main_qt.py --minimized
python main_qt.py --tray

# Hoặc sử dụng short flags
python main_qt.py -h
python main_qt.py -s
```

### 2. Sử dụng File Batch chuyên dụng

```batch
# Chạy file batch được tạo sẵn
start_textnow_hidden.bat
```

### 3. Sử dụng File Silent Startup

```bash
# Sử dụng file startup chuyên dụng
python main_qt_silent.py
```

### 4. Từ trong ứng dụng

1. Mở TextNow
2. Nhấp chuột phải vào **System Tray Icon** (khay hệ thống)
3. Chọn **"🚀 Khởi động cùng Windows"**
4. Ứng dụng sẽ tự động đăng ký vào Windows Registry

## 📱 Sử dụng System Tray

Khi ứng dụng chạy ẩn, bạn có thể:

### Mở cửa sổ chính:
- **Nhấp đúp** vào icon TextNow trong system tray
- **Chuột phải** → **"Hiển thị cửa sổ"**

### Menu System Tray gồm:
- 📺 **Hiển thị cửa sổ** - Mở giao diện chính
- 📋 **Shortcuts: X** - Số lượng shortcuts hiện có
- 🔄 **Đang theo dõi bàn phím** - Trạng thái hoạt động
- ⚙️ **Cài đặt** - Mở cài đặt
- 🚀 **Khởi động cùng Windows** - Bật/tắt auto startup
- 🚪 **Thoát** - Đóng ứng dụng hoàn toàn

## 🔧 Registry Configuration

Khi bật **"Khởi động cùng Windows"**, ứng dụng sẽ:

### Cho file EXE:
```
Đăng ký: "TextNow.exe" --hidden
Vị trí: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

### Cho Python script:
```
Đăng ký: "pythonw.exe" "main_qt.py" --hidden
Vị trí: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

## 📂 Files liên quan

- `main_qt.py` - Entry point chính (hỗ trợ --hidden flag)
- `main_qt_silent.py` - Entry point startup ẩn chuyên dụng
- `start_textnow_hidden.bat` - Batch script khởi động ẩn
- `run_qt_silent.bat` - Batch script legacy

## 🛠️ Troubleshooting

### Ứng dụng không khởi động ẩn?

1. **Kiểm tra System Tray:**
   - Tìm icon TextNow trong khay hệ thống
   - Có thể icon bị ẩn trong "Hidden icons"

2. **Kiểm tra Python:**
   ```bash
   python --version
   pythonw --version
   ```

3. **Kiểm tra Dependencies:**
   ```bash
   pip install -r requirements_qt.txt
   ```

### System Tray không hiển thị icon?

1. **Kiểm tra Windows Settings:**
   - Settings → Personalization → Taskbar
   - Turn on "Always show all icons in the notification area"

2. **Restart Explorer:**
   ```cmd
   taskkill /f /im explorer.exe
   start explorer.exe
   ```

### Auto startup không hoạt động?

1. **Kiểm tra Registry manually:**
   ```cmd
   regedit
   # Navigate to: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
   # Look for "TextNow" entry
   ```

2. **Chạy với quyền Admin:**
   - Thử chạy ứng dụng với Run as Administrator

## 💡 Tips và Lưu ý

### ✅ Nên:
- Sử dụng `pythonw.exe` thay vì `python.exe` để tránh hiện terminal
- Kiểm tra system tray thường xuyên để đảm bảo ứng dụng đang chạy
- Sử dụng notification để biết khi nào ứng dụng khởi động

### ❌ Không nên:
- Đóng ứng dụng từ Task Manager mà không thoát đúng cách
- Xóa entry trong Registry một cách thủ công
- Chạy nhiều instance cùng lúc

## 🔔 Notifications

Khi khởi động ẩn, ứng dụng sẽ **không hiển thị notification** để đảm bảo khởi động hoàn toàn im lặng:

- ✅ **Im lặng hoàn toàn**: Không có thông báo popup nào
- 📱 **System tray icon**: Xuất hiện ngay trong khay hệ thống  
- 🔇 **Không làm phiền**: Chạy ngầm mà không gây chú ý
- 👀 **Kiểm tra trạng thái**: Nhìn vào system tray để xác nhận ứng dụng đang chạy

**Lưu ý**: Notifications chỉ xuất hiện khi:
- Sử dụng shortcuts (báo shortcut đã được trigger)
- Đóng cửa sổ chính (báo ứng dụng đã thu nhỏ xuống tray)
- Các thao tác khác từ giao diện chính

## 🆘 Hỗ trợ

Nếu gặp vấn đề, hãy:

1. Kiểm tra file log: `startup_error.log` (nếu có)
2. Chạy ở chế độ development để xem chi tiết:
   ```bash
   python main_qt.py --hidden
   ```
3. Báo cáo bug kèm thông tin hệ thống

---

**📝 Lưu ý:** Tính năng này yêu cầu Python 3.8+ và Windows 10/11 để hoạt động tối ưu. 