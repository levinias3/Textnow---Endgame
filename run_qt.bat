@echo off
echo.
echo ===========================================
echo  TextNow Qt v2.0.0 - PySide6 UI
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

REM Chạy app
echo 🚀 Starting TextNow Qt...
echo.
python main_qt.py

if errorlevel 1 (
    echo.
    echo ❌ Application exited with error
    pause
) else (
    echo.
    echo ✅ Application exited normally
)

echo.
pause 