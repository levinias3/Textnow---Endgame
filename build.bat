@echo off
echo Auto Text ^& Image - Build Script
echo =================================
echo.

REM Kiểm tra PyInstaller
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller chưa được cài đặt
    echo Đang cài đặt PyInstaller...
    pip install pyinstaller
)

REM Tạo logo mẫu nếu chưa có
if not exist "icon.ico" (
    echo Tạo icon mẫu...
    python create_sample_logo.py
)

REM Clean build cũ
echo Dọn dẹp build cũ...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

REM Build với spec file
echo.
echo Đang build ứng dụng...
pyinstaller AutoTextImage.spec

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build thất bại!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build thành công!
echo File EXE: dist\AutoTextImage.exe
echo ========================================
echo.

REM Tạo thư mục release
if not exist "release" mkdir release

REM Copy các file cần thiết
echo Đang tạo bản phát hành...
copy dist\AutoTextImage.exe release\ >nul
copy shortcuts.json release\ >nul
copy README.md release\ >nul

echo.
echo Bản phát hành đã được tạo trong thư mục 'release'
echo.

pause 