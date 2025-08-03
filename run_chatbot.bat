@echo off
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Setup complete! 

echo.
echo To run the chatbot:
echo 1. Run: python chatbot_backend.py (for API server)
echo 2. Run: python chatbot_popup_app.py (for desktop popup)
echo 3. Or test API with: python test_chatbot.py

echo.
echo Starting backend server...
python chatbot_backend.py
