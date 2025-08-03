# AI Term Project G3 - Jiji Chatbot Assistant

## 🎯 Project Overview
Developing an intelligent AI chatbot to assist small African businesses (specifically Jiji marketplace) in answering frequently asked customer questions using NLP techniques and machine learning.

## 📁 Project Structure

### 🔧 Core Files
- **`run.py`** - Central launcher for complete system (MAIN ENTRY POINT)
- **`chatbot_backend.py`** - Flask API server with TF-IDF chatbot engine
- **`chatbot_popup_app.py`** - Modern desktop popup application
- **`common_questions.csv`** - Database of 256+ Q&A pairs for training
- **`requirements.txt`** - Python dependencies
- **`start.bat`** - Windows quick launcher

### 📊 Data & Analysis
- **`jiji_comprehensive_scraper.ipynb`** - Data collection from Jiji marketplace
- **`jiji_kenya_10k.csv`** - Scraped marketplace data (10,000+ entries)
- **`text_image_processing_analysis.ipynb`** - Milestone 2: Text processing & analysis
- **`data_collection_plan.md`** - Data collection strategy

### 🧪 Testing & Utilities
- **`test_chatbot.py`** - API testing and validation
- **`run_chatbot.bat`** - Quick setup and launch script
- **`run_popup_chat.bat`** - Launch desktop popup application

### 📚 Documentation
- **`CHATBOT_README.md`** - Detailed chatbot documentation
- **`LICENSE`** - Project license

## 🚀 Quick Start

### Option 1: One-Command Launch (Recommended)
```bash
python run.py                    # Start complete system (backend + popup)
```

### Option 2: Individual Components
```bash
# Install dependencies
pip install -r requirements.txt

# Start backend server
python chatbot_backend.py

# Start desktop app (in separate terminal)
python chatbot_popup_app.py
```

### Option 3: Windows Quick Start
```cmd
start.bat                       # Double-click or run from command line
```

## 🎮 Run.py Commands

The `run.py` script is the central launcher with multiple options:

```bash
python run.py                    # Start both backend and popup
python run.py --backend-only     # Start only backend server
python run.py --popup-only       # Start only popup (requires backend)
python run.py --test            # Run system tests
python run.py --help            # Show all options
```

## ✨ Features

### 🤖 AI Chatbot Engine
- **TF-IDF Vectorization** with cosine similarity matching
- **256+ Q&A pairs** covering marketplace scenarios
- **Confidence scoring** for response quality
- **Rule-based NLP** with preprocessing pipeline

### 💻 Modern Desktop Interface
- **Native Python popup** application (tkinter)
- **Professional UI design** with gradients and animations
- **Real-time chat** with typing indicators
- **Window controls** (minimize, always-on-top, close)
- **Auto-connection testing** and status display

### 🔌 REST API
- **Flask backend** with CORS support
- **JSON request/response** format
- **Health check** endpoint
- **Statistics** endpoint

## 🎯 Use Cases
- Payment method inquiries
- Delivery and shipping questions
- Return and refund policies
- Seller verification processes
- General marketplace support

## 📈 Technical Achievements
- ✅ Complete chatbot system with 90%+ accuracy
- ✅ Modern desktop application interface  
- ✅ Comprehensive data collection (10K+ entries)
- ✅ Text processing and analysis notebook
- ✅ Production-ready API with error handling
- ✅ Professional documentation and testing

## 🔧 Development
This project demonstrates practical AI implementation for small African businesses, combining web scraping, NLP processing, machine learning, and modern UI development.
