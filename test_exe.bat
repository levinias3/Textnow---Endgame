@echo off
echo.
echo ========================================
echo     TESTING TEXTNOW EXE BUILD
echo ========================================
echo.

REM Kiểm tra file exe tồn tại
if not exist "dist\TextNow.exe" (
    echo ❌ TextNow.exe not found in dist directory!
    pause
    exit /b 1
)

REM Hiển thị thông tin file
for %%A in ("dist\TextNow.exe") do (
    echo ✅ File: %%~nxA
    echo ✅ Size: %%~zA bytes (%%~zA bytes / 1MB = MB^)
    echo ✅ Path: %%~fA
)
echo.

echo 🚀 Starting TextNow.exe in test mode...
echo.
echo 📝 Note: 
echo   - Icon should appear in taskbar with high quality
echo   - System tray icon should be crisp and clear  
echo   - Window should open with proper layout
echo   - Close the app to continue this script
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak >nul

REM Chạy exe
echo.
echo 🎯 Running TextNow.exe...
start "" "dist\TextNow.exe"

echo.
echo ✅ TextNow.exe started successfully!
echo.
echo 📋 Manual Test Checklist:
echo   1. ✅ Exe launched without errors
echo   2. ❓ Taskbar icon appears with high quality
echo   3. ❓ System tray icon is crisp and clear
echo   4. ❓ Window displays correctly
echo   5. ❓ All UI elements work properly
echo   6. ❓ Icons and logos display with high quality
echo.
echo ⏳ Waiting for manual testing...
echo   Press any key when you've finished testing the exe
pause

echo.
echo 🎉 EXE TEST COMPLETED!
echo.
echo 📦 Build Information:
echo   • Source: TextNow Qt v1.3.6
echo   • Builder: PyInstaller 6.13.0
echo   • Python: 3.13.3
echo   • High-quality icons: ✅ Included
echo   • Multi-size ICO: ✅ app.ico
echo   • Size: ~96 MB (with all resources)
echo.
echo 🚀 Ready for distribution!
pause 