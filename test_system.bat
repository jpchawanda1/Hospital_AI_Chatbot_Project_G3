@echo off
echo Testing Jiji Chatbot System...
echo ================================

echo.
echo 1. Testing Backend Health...
python -c "import requests; r = requests.get('http://localhost:5000/health'); print('Status:', r.status_code, '- Response:', r.json())" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Backend not responding or not started
    echo Please run: python chatbot_backend.py
) else (
    echo ✅ Backend is healthy!
)

echo.
echo 2. Testing Chat API...
python -c "import requests; r = requests.post('http://localhost:5000/chat', json={'message': 'What payment methods do you accept?'}); print('Status:', r.status_code, '- Response:', r.json())" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Chat API not responding
) else (
    echo ✅ Chat API is working!
)

echo.
echo 3. Checking if Popup is Running...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq Jiji*" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Popup application appears to be running!
) else (
    echo ℹ️ Popup status unclear - check if window is visible
)

echo.
echo ================================
echo System Test Complete!
echo ================================
pause
