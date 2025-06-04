@echo off
REM ==========================================
REM  TextNow Qt v2.0.1 - Hidden Startup
REM ==========================================
REM  🔇 Khởi động ẩn - Chạy ngay vào system tray
REM ==========================================

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo    Vui lòng cài đặt Python 3.8+ từ python.org
    pause
    exit /b 1
)

REM Cài đặt dependencies nếu cần
pip install -r requirements_qt.txt --quiet >nul 2>&1

REM Khởi động ẩn với pythonw.exe (không hiện terminal)
pythonw --version >nul 2>&1
if errorlevel 1 (
    REM Fallback sử dụng python với detached mode
    start /min python main_qt.py --hidden
) else (
    REM Sử dụng pythonw.exe - không hiển thị terminal
    pythonw main_qt.py --hidden
)

REM Script này sẽ tự đóng ngay lập tức sau khi khởi động
exit /b 0 