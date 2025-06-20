# TextNow Qt - Hướng Dẫn Khởi Động

## Vấn Đề Terminal Dependency
Khi chạy ứng dụng Python từ terminal, ứng dụng vẫn gắn liền với terminal process và sẽ bị tắt khi terminal đóng.

## Các Chế độ Khởi Động

### 1. 🖥️ Chế Độ Thông Thường
**File**: `run_qt.bat` hoặc `run_qt_enhanced.bat`
- **Đặc điểm**: Hiển thị thông tin chi tiết trong terminal
- **Ưu điểm**: Dễ debug, thấy được logs
- **Nhược điểm**: Gắn liền với terminal, tắt terminal = tắt app
- **Phù hợp**: Debug, phát triển, lần đầu sử dụng

### 2. 🔇 Chế Độ Silent (Khuyến Nghị)
**File**: `run_qt_silent.bat`
- **Đặc điểm**: Hiển thị thông tin khởi động, sau đó chạy độc lập
- **Ưu điểm**: 
  - Ứng dụng chạy độc lập khỏi terminal
  - Có thể đóng terminal mà không ảnh hưởng app
  - Hiển thị thông tin để biết trạng thái
- **Phù hợp**: Sử dụng hằng ngày

### 3. ⚡ Chế Độ Nhanh
**File**: `start_textnow.bat`
- **Đặc điểm**: Khởi động nhanh, tối thiểu thông tin
- **Ưu điểm**:
  - Khởi động cực nhanh
  - Không hiển thị terminal sau khi khởi động
  - Hoàn toàn độc lập
- **Phù hợp**: Startup cùng Windows, khởi động nhanh

## Công Nghệ Sử Dụng

### 1. `pythonw.exe` vs `python.exe`
```batch
python main_qt.py      # Có terminal, gắn liền với CMD
pythonw main_qt.py     # Không terminal, chạy GUI thuần
```

### 2. `start` Command Options
```batch
start /b python app.py     # Background, nhưng vẫn gắn terminal
start /min python app.py   # Minimized window
pythonw app.py             # Không terminal (tốt nhất)
```

### 3. Silent Mode với `main_qt_silent.py`
- Sử dụng `startup_mode = True`
- Khởi động minimized to system tray
- Không hiển thị cửa sổ chính ngay lập tức

## Cơ Chế Single Instance
Tất cả các chế độ đều hỗ trợ single instance:
- Chỉ cho phép 1 instance chạy
- Instance thứ 2 sẽ gửi signal cho instance đầu để hiển thị
- Instance thứ 2 tự động thoát

## Khuyến Nghị Sử Dụng

### Cho Người Dùng Cuối
```batch
# Khởi động hằng ngày
start_textnow.bat

# Hoặc để xem thông tin
run_qt_silent.bat
```

### Cho Developer
```batch
# Debug và phát triển
run_qt.bat
run_qt_enhanced.bat
```

### Cho Auto Startup (Windows)
```batch
# Thêm vào Registry hoặc Startup folder
start_textnow.bat
```

## Test Độc Lập Terminal
1. Chạy `start_textnow.bat`
2. Đợi vài giây để app khởi động
3. Đóng terminal/command prompt
4. ✅ App vẫn chạy trong system tray

## Troubleshooting

### Lỗi "pythonw không tìm thấy"
- Script sẽ tự động fallback về `python` với `/min`
- Cần cài đặt Python đầy đủ (có pythonw.exe)

### App không khởi động
- Kiểm tra `startup_error.log` trong thư mục gốc
- Chạy `run_qt.bat` để xem logs chi tiết

### Multiple instances
- Chỉ có 1 instance được phép chạy
- Instance mới sẽ signal instance cũ để hiển thị
- Nếu có vấn đề, restart máy để reset lock files 