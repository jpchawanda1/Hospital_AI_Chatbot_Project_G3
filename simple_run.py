#!/usr/bin/env python3
"""
Hospital AI Agent System Launcher - Professional Version
=========================================================

Central launcher for the complete Hospital AI Agent system.
This script handles starting the backend server and desktop popup application.

Usage:
    python simple_run.py                # Start both backend and popup
    python simple_run.py backend        # Start only backend server
    python simple_run.py popup          # Start only popup (requires backend running)

Author: AI Term Project G3
"""

import sys
import os
import time
import subprocess
import requests
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("         HOSPITAL AI AGENT SYSTEM")
    print("")
    print("    Intelligent Medical Information Assistant")
    print("      for Nairobi & Kenyatta Hospitals")
    print("="*60)
    print("Starting Hospital AI Agent...\n")

def check_backend_health(show_error=True):
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            qa_pairs = data.get('qa_pairs_loaded', 0)
            model_type = data.get('model_type', 'Unknown')
            print(f"[OK] Backend healthy! {qa_pairs} Q&A pairs loaded, Model: {model_type}")
            return True
    except:
        pass
    if show_error:
        print("[INFO] Backend still loading AI models...")
    return False

def start_backend():
    """Start the Flask backend server"""
    print("Starting backend server...")
    
    if not Path("src/chatbot_backend.py").exists():
        print("[ERROR] Backend file not found: src/chatbot_backend.py")
        return None
    
    try:
        process = subprocess.Popen([
            sys.executable, "src/chatbot_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"[OK] Backend server started (PID: {process.pid})")
        
        # Wait for backend to be ready (AI models take time to load)
        print("Waiting for backend to be ready...")
        for i in range(30):  # Wait up to 30 seconds for AI models
            time.sleep(2)
            if check_backend_health(show_error=(i > 10)):
                break
            if i % 5 == 0:
                print(f"[INFO] Still waiting for AI models to load... ({i*2}s)")
        else:
            print("[WARNING] Backend may still be loading AI models")
            print("[INFO] This is normal for first startup - models need to download")
        
        return process
        
    except Exception as e:
        print(f"[ERROR] Failed to start backend: {e}")
        return None

def start_popup():
    """Start the desktop popup application"""
    print("Starting desktop popup application...")
    
    if not Path("src/chatbot_popup_app.py").exists():
        print("[ERROR] Popup file not found: src/chatbot_popup_app.py")
        return None
    
    try:
        process = subprocess.Popen([
            sys.executable, "src/chatbot_popup_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"[OK] Desktop popup started (PID: {process.pid})")
        
        # Give the GUI time to initialize
        time.sleep(2)
        print("[INFO] GUI window should now be visible")
        
        return process
        
    except Exception as e:
        print(f"[ERROR] Failed to start popup: {e}")
        return None

def run_basic_tests():
    """Run basic system validation tests"""
    print("Running basic system tests...")
    print("=" * 50)
    
    # Test 1: Check required files exist
    required_files = [
        "src/chatbot_backend.py",
        "src/chatbot_popup_app.py", 
        "data/common_questions.csv"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"[OK] {file} exists")
        else:
            print(f"[ERROR] {file} missing")
            return 1
    
    # Test 2: Check data file structure
    try:
        import csv
        with open("data/common_questions.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            print(f"[OK] Data file loaded: {len(rows)-1} Q&A pairs")  # -1 for header
    except Exception as e:
        print(f"[ERROR] Data loading failed: {e}")
        return 1
    
    print("\n[SUCCESS] All basic tests passed!")
    return 0

def main():
    """Main function"""
    print_banner()
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    
    # Handle test mode
    if mode == "test":
        return run_basic_tests()
    
    if mode in ["both", "backend"]:
        backend_process = start_backend()
        if not backend_process and mode == "backend":
            return 1
    
    if mode in ["both", "popup"]:
        if mode == "popup":
            print("Checking for running backend...")
            if not check_backend_health():
                print("[ERROR] No backend found. Please start backend first.")
                return 1
        
        popup_process = start_popup()
        if not popup_process:
            return 1
    
    print("\n[SUCCESS] Hospital AI Agent System is running!")
    print("\nTips:")
    print("  • Use the desktop popup to chat with the AI about medical information")
    print("  • Ask about appointments, pricing, departments, or emergency contacts")
    print("  • Backend runs locally for security (localhost only)")
    print("  • Press Ctrl+C to stop all services")
    
    try:
        if mode == "both":
            # Keep running until interrupted
            print("\nPress Ctrl+C to stop...")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
