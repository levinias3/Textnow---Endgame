@echo off
echo.
echo ===========================================
echo  TextNow Qt v2.0.1 - Build to EXE
echo ===========================================
echo  🔧 Building independent executable
echo ===========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo    Cần Python để build exe
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Kiểm tra PyInstaller
echo 📦 Checking PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ PyInstaller chưa được cài đặt
    echo 📥 Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

echo ✅ PyInstaller ready
echo.

REM Check dependencies
echo 📋 Installing build dependencies...
pip install -r requirements_qt.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies!
    pause
    exit /b 1
)

echo ✅ Dependencies ready
echo.

REM Tạo icon nếu chưa có
if not exist "icon.ico" (
    echo 🎨 Creating app icon...
    python create_sample_logo.py >nul 2>&1
)

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "build" rmdir /s /q build >nul 2>&1
if exist "dist" rmdir /s /q dist >nul 2>&1
if exist "release" rmdir /s /q release >nul 2>&1

echo ✅ Clean completed
echo.

REM Build exe with Qt spec
echo 🔨 Building TextNow.exe...
echo    This may take 2-5 minutes depending on your system...
echo.

pyinstaller TextNowQt.spec --clean

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo 💡 Check the error messages above
    echo 💡 Try: pip install --upgrade pyside6 pyinstaller
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Build completed successfully!
echo ========================================
echo.

REM Create release package
echo 📦 Creating release package...
mkdir release >nul 2>&1

REM Copy main exe
copy dist\TextNow.exe release\ >nul
if errorlevel 1 (
    echo ❌ Failed to copy exe file!
    pause
    exit /b 1
)

REM Copy essential files
copy shortcuts.json release\ >nul 2>&1
copy README.md release\ >nul 2>&1
copy STARTUP_MODES.md release\ >nul 2>&1

REM Calculate file size
for %%I in (release\TextNow.exe) do set size=%%~zI
set /a sizeKB=%size%/1024
set /a sizeMB=%sizeKB%/1024

echo.
echo 🎉 Release package created!
echo 📁 Location: release\TextNow.exe
echo 📊 Size: %sizeMB% MB (%sizeKB% KB)
echo.
echo ✅ TextNow.exe is now completely independent:
echo    - No Python installation required
echo    - No terminal dependency  
echo    - Direct Windows startup support
echo    - All resources bundled inside
echo.
echo 💡 Test the exe:
echo    1. Double-click release\TextNow.exe
echo    2. Should start silently to system tray
echo    3. No console windows should appear
echo.

REM Ask về auto startup test
set /p test_startup="🚀 Test startup integration? (y/n): "
if /i "%test_startup%"=="y" (
    echo.
    echo 📝 To add TextNow.exe to Windows startup:
    echo    1. Press Win+R, type: shell:startup
    echo    2. Copy TextNow.exe shortcut to that folder
    echo    3. Restart Windows to test
    echo.
    echo 💡 Or use the app's built-in startup toggle
)

echo.
echo Build completed! 🎯
pause 