# 🚀 Windows Startup Fixes

## 📋 Vấn Đề Đã Fix

### ❌ **Vấn đề trước đây**:
1. **Terminal hiển thị**: Khi khởi động cùng Windows, terminal/console window xuất hiện
2. **Tắt terminal = tắt app**: Đóng terminal sẽ làm ứng dụng tự động tắt
3. **Data path sai**: Phần mềm sử dụng bộ data khác thay vì shortcuts đã lưu

### ✅ **Giải pháp đã triển khai**:

## 🔧 Fix 1: Config Path Resolution

### **Vấn đề**: 
Config file sử dụng relative path, khi khởi động từ Windows có thể tìm sai thư mục.

### **Giải pháp**:
```python
# utils/config.py
def __init__(self, config_file: str = "shortcuts.json"):
    # Always use absolute path relative to script location
    if not os.path.isabs(config_file):
        script_dir = Path(__file__).parent.parent
        self.config_file = str(script_dir / config_file)
    else:
        self.config_file = config_file
```

### **Kết quả**:
- ✅ Config file luôn được tìm đúng vị trí
- ✅ Shortcuts được load từ file đúng
- ✅ Working directory không ảnh hưởng

## 🔇 Fix 2: Silent Startup Script

### **Vấn đề**: 
`python.exe` luôn hiển thị console window khi chạy script.

### **Giải pháp**:
Tạo `main_qt_silent.py`:
```python
def main():
    """Main entry point for silent startup"""
    try:
        from main_qt import TextNowQtApp
        app = TextNowQtApp()
        app.startup_mode = True  # Start minimized
        return app.run()
    except Exception as e:
        # Log to file instead of console
        error_log = project_root / "startup_error.log"
        with open(error_log, 'w', encoding='utf-8') as f:
            f.write(f"TextNow startup error: {e}\n")
```

### **Kết quả**:
- ✅ Không có console window
- ✅ Error logging vào file thay vì console
- ✅ App chạy minimized khi startup

## 🐍 Fix 3: Use pythonw.exe

### **Vấn đề**: 
`python.exe` tạo console window, `pythonw.exe` không.

### **Giải pháp**:
```python
# qt_ui/main_window_qt.py - _enable_startup()
if getattr(sys, 'frozen', False):
    # EXE mode - use exe directly
    app_path = f'"{sys.executable}"'
else:
    # Script mode - use pythonw.exe + silent script
    python_exe = sys.executable
    if python_exe.endswith('python.exe'):
        pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
    else:
        pythonw_exe = python_exe
    
    script_path = Path(__file__).parent.parent / "main_qt_silent.py"
    app_path = f'"{pythonw_exe}" "{script_path}"'
```

### **Kết quả**:
- ✅ Không có terminal window
- ✅ App chạy hoàn toàn im lặng
- ✅ Tự động detect pythonw.exe

## 📱 Fix 4: Startup Mode Support

### **Vấn đề**: 
App luôn hiển thị main window khi khởi động.

### **Giải pháp**:
```python
# main_qt.py - TextNowQtApp
def __init__(self):
    self.startup_mode = False  # Flag for silent startup

def run(self):
    if self.startup_mode:
        # Start minimized to tray
        print("🔇 Starting in silent mode (minimized to tray)")
        # Don't call show(), use system tray
    else:
        self.main_window.show()
```

### **Kết quả**:
- ✅ Chạy hidden khi startup
- ✅ System tray available để user mở
- ✅ Normal behavior khi user mở thủ công

## 🧪 Testing

### **Test Script**: `test_startup_fixes.py`

```bash
python test_startup_fixes.py
```

### **Test Results**:
```
📁 Test 1: Config path resolution
   📄 Config file: C:\...\shortcuts.json
   📍 Absolute path: True
   📂 Exists: True
   🔗 Shortcuts loaded: 15
   ✅ Config path test passed

🚀 Test 2: Startup command format
   🐍 Script mode: "C:\...\pythonw.exe" "C:\...\main_qt_silent.py"
   🔇 Using pythonw: True
   📄 Silent script exists: True
   ✅ Startup command test passed

📝 Test 3: Registry key check
   🔑 Current registry value: "C:\...\pythonw.exe" "C:\...\main_qt_silent.py"
   ✅ Using pythonw.exe (no terminal)
   ✅ Using silent startup script
   ✅ Registry test passed

🔇 Test 4: Silent script validation
   📄 Silent script path: C:\...\main_qt_silent.py
   📂 Exists: True
   📊 File size: 1024 characters
   🏃 Has main(): True
   🔇 Has startup_mode: True
   ✅ Silent script test passed
```

## 🎯 User Experience

### **Trước khi fix**:
- ❌ Terminal window xuất hiện khi boot
- ❌ Đóng terminal = tắt app
- ❌ Shortcuts không load được
- ❌ Trải nghiệm user kém

### **Sau khi fix**:
- ✅ Chạy hoàn toàn im lặng khi boot
- ✅ App chạy trong background
- ✅ System tray sẵn sàng sử dụng
- ✅ Tất cả shortcuts hoạt động bình thường
- ✅ Trải nghiệm user mượt mà

## 📝 Registry Entry

### **Trước**:
```
"C:\Python\python.exe" "C:\TextNow\main_qt.py"
```

### **Sau**:
```
"C:\Python\pythonw.exe" "C:\TextNow\main_qt_silent.py"
```

## 🚀 Hướng Dẫn Sử Dụng

### **Enable Startup**:
1. Mở TextNow
2. Click system tray → Settings
3. Check "🚀 Khởi động cùng Windows"
4. Restart để test

### **Verify**:
1. Restart Windows
2. Không có terminal window
3. Check system tray cho TextNow icon
4. Double-click để mở main window
5. Test shortcuts - tất cả hoạt động bình thường

## 💡 Technical Notes

### **File Structure**:
```
TextNow/
├── main_qt.py              # Regular entry point
├── main_qt_silent.py       # Silent startup entry
├── shortcuts.json          # Config file (absolute path)
├── utils/config.py         # Fixed path resolution
└── qt_ui/main_window_qt.py # Fixed startup registration
```

### **Registry Key**:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
Name: TextNow
Value: "pythonw.exe path" "silent script path"
```

### **Error Handling**:
- Startup errors logged to `startup_error.log`
- No console popups for errors
- Graceful fallback behavior

## ✅ Conclusion

Tất cả 3 vấn đề đã được fix hoàn toàn:

1. **🔇 No Terminal**: Sử dụng `pythonw.exe` + silent script
2. **📱 Independent App**: App không phụ thuộc vào terminal
3. **📂 Correct Data**: Config path được resolve tuyệt đối

**Người dùng giờ có trải nghiệm khởi động Windows hoàn hảo!** 🎉 