@echo off
REM TextNow Qt v2.0.1 - EXE Launcher
REM Ultra silent launcher for exe mode - No dependencies needed

REM Clear console
cls

REM Check if TextNow.exe exists
if not exist "TextNow.exe" (
    echo ❌ TextNow.exe not found!
    echo 💡 Please run build_qt.bat first to create the exe
    echo    Or copy TextNow.exe to this directory
    pause
    exit /b 1
)

REM Launch exe completely detached
start "" "TextNow.exe"

REM Exit immediately - no waiting
exit /b 0 