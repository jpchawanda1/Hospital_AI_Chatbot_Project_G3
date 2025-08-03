@echo off
echo Starting Jiji Chatbot Popup Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Start the popup application
echo Starting chatbot popup window...
python chatbot_popup_app.py

pause
