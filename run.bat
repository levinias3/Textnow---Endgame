@echo off
echo Auto Text ^& Image - Starting...
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python không được cài đặt hoặc không có trong PATH
    echo Vui lòng cài đặt Python 3.10+ từ python.org
    pause
    exit /b 1
)

REM Kiểm tra và cài đặt dependencies
echo Đang kiểm tra các thư viện cần thiết...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Không thể cài đặt thư viện
    pause
    exit /b 1
)

echo.
echo Đang khởi động ứng dụng...
echo Lưu ý: Ứng dụng hoạt động tốt nhất khi chạy với quyền Administrator
echo.

REM Chạy ứng dụng
python main.py

pause 