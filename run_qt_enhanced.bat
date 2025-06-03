@echo off
echo.
echo ===========================================
echo  TextNow Qt v2.0.0 - Enhanced Version
echo ===========================================
echo   ✨ System Tray Integration
echo   ✨ Auto Startup Support  
echo   ✨ Image Content Support
echo   ✨ Close to Tray Behavior
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

REM Test registry access
echo 🔑 Testing Windows integration...
python -c "import winreg; print('✅ Registry access OK')" 2>nul
if errorlevel 1 (
    echo ⚠️ Registry access limited (startup feature may not work)
) else (
    echo ✅ Windows integration ready
)
echo.

REM Chạy app
echo 🚀 Starting TextNow Qt Enhanced...
echo.
echo 💡 Tính năng mới:
echo    - Nhấp đúp system tray icon để hiển thị
echo    - Right-click tray icon để toggle auto startup
echo    - Chọn loại content: Văn bản / Hình ảnh / Văn bản + Ảnh
echo    - Đóng cửa sổ sẽ thu nhỏ xuống system tray
echo.

python main_qt.py

if errorlevel 1 (
    echo.
    echo ❌ Application exited with error
    echo 💡 Để debug: python test_qt_full.py
    pause
) else (
    echo.
    echo ✅ Application exited normally
)

echo.
pause 