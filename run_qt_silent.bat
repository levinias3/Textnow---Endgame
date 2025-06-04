@echo off
echo.
echo ===========================================
echo  TextNow Qt v2.0.0 - Silent Launcher
echo ===========================================
echo  🔇 Chạy ứng dụng độc lập (không gắn terminal)
echo ===========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo    Vui lòng cài đặt Python 3.8+ từ python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Kiểm tra và cài đặt dependencies
echo 📦 Checking dependencies...
pip install -r requirements_qt.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies!
    pause
    exit /b 1
)

echo ✅ Dependencies OK
echo.

REM Kiểm tra pythonw.exe (GUI version - không hiện terminal)
pythonw --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ pythonw.exe không tìm thấy, sử dụng python.exe với detached mode
    echo 🚀 Starting TextNow Qt (detached)...
    start /min python main_qt_silent.py
) else (
    echo 🚀 Starting TextNow Qt (silent GUI mode)...
    echo 💡 Sử dụng pythonw.exe - không hiển thị terminal
    pythonw main_qt_silent.py
)

echo.
echo ✅ Ứng dụng đã được khởi động độc lập!
echo 💡 Bạn có thể đóng terminal này mà không ảnh hưởng đến ứng dụng.
echo 📱 Tìm icon TextNow trong system tray để sử dụng.
echo.
echo Đóng cửa sổ launcher sau 2 giây...
timeout /t 2 >nul 