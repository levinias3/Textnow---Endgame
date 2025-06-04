@echo off
REM TextNow Qt v2.0.0 - Quick Silent Launcher
REM Khởi động nhanh mà không hiển thị terminal

REM Tắt echo để không hiển thị commands
cls

REM Kiểm tra Python nhanh
python --version >nul 2>&1
if errorlevel 1 (
    echo Python không được cài đặt! Vui lòng cài Python 3.8+
    pause
    exit /b 1
)

REM Cài dependencies silent
pip install -r requirements_qt.txt --quiet >nul 2>&1

REM Khởi động ứng dụng
pythonw --version >nul 2>&1
if errorlevel 1 (
    REM Fallback: sử dụng python với start /min
    start /min python main_qt_silent.py
) else (
    REM Tốt nhất: sử dụng pythonw (GUI mode, không terminal)
    pythonw main_qt_silent.py
)

REM Script sẽ kết thúc ngay sau khi khởi động app
exit /b 0 