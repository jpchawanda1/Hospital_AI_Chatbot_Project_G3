@echo off
title Jiji AI Chatbot System

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🛍️  JIJI AI CHATBOT SYSTEM                ║
echo ║                                                              ║
echo ║           Intelligent Customer Support for African          ║
echo ║                     Marketplace Businesses                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again.
    pause
    exit /b 1
)

echo 🚀 Starting Jiji AI Assistant...
echo.

REM Start the complete system using run.py
python run.py

echo.
echo 👋 Thanks for using Jiji AI Chatbot System!
pause
