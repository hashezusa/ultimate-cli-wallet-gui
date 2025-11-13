@echo off
REM Ultimate CLI Wallet GUI Launcher for Windows

echo.
echo ================================
echo Ultimate CLI Wallet GUI Launcher
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3 from python.org
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Launch GUI
echo Launching Wallet GUI...
echo.
python wallet_gui.py

echo.
echo Wallet GUI closed.
echo.
pause
