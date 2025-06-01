# 📺 Auto Text & Image - Chế độ Toàn màn hình

## 🔧 Thay đổi quan trọng

Ứng dụng hiện chạy ở **chế độ toàn màn hình** với các đặc điểm sau:

### ✅ Tính năng mới
- ✨ **Fullscreen tự động**: Ứng dụng luôn ở chế độ toàn màn hình
- 🔒 **Không thể minimize**: Cửa sổ không thể thu nhỏ xuống taskbar
- 🚫 **Không thể resize**: Kích thước cửa sổ cố định theo màn hình
- ⌨️ **Hotkey thoát khẩn cấp**: `Ctrl+Alt+Q` để thoát nhanh

### 🎯 Các cách điều khiển

1. **Hiển thị ứng dụng**:
   - Click icon trong system tray
   - Chọn "📺 Hiển thị (Toàn màn hình)"

2. **Ẩn ứng dụng**:
   - Click nút X trên title bar
   - Chọn option "Thu nhỏ xuống khay"

3. **Thoát ứng dụng**:
   - Click nút X và chọn "Thoát"
   - Hoặc dùng hotkey `Ctrl+Alt+Q`
   - Hoặc click chuột phải vào system tray → "🚪 Thoát"

### 📋 System Tray Menu

Khi ẩn xuống system tray, bạn có thể:
- **📺 Hiển thị (Toàn màn hình)**: Mở lại ứng dụng
- **ℹ️ Thông tin**: Xem hướng dẫn nhanh
- **🚪 Thoát**: Đóng ứng dụng hoàn toàn

### 🛠️ Kỹ thuật

- **Font SVN Poppins**: Vẫn được load và sử dụng đầy đủ
- **Responsive UI**: Giao diện tự động điều chỉnh theo kích thước màn hình
- **Performance**: Không ảnh hưởng đến hiệu suất shortcuts
- **Fallback safety**: Luôn có cách thoát khẩn cấp

### ⚠️ Lưu ý quan trọng

1. **Không minimize được**: Đây là tính năng, không phải lỗi
2. **Hotkey thoát**: Nhớ `Ctrl+Alt+Q` để thoát khẩn cấp
3. **System tray**: Ứng dụng có thể ẩn xuống tray thay vì minimize
4. **Multiple monitors**: Fullscreen áp dụng cho monitor chính

### 🔄 Khôi phục về chế độ thường

Nếu muốn quay lại chế độ cửa sổ thường:
1. Mở file `ui/main_window.py`
2. Tìm dòng `self.root.resizable(False, False)`
3. Thay đổi thành `self.root.resizable(True, True)`
4. Xóa hoặc comment các dòng liên quan đến fullscreen

---

**v1.3.2 - SVN Poppins Edition + Fullscreen Mode** 