#!/usr/bin/env python3
"""
Jiji Chatbot System Launcher
============================

Central launcher for the complete Jiji AI chatbot system.
This script handles starting the backend server and desktop popup application.

Usage:
    python run.py                    # Start both backend and popup
    python run.py --backend-only     # Start only backend server
    python run.py --popup-only       # Start only popup (requires backend running)
    python run.py --test            # Run system tests
    python run.py --help            # Show help

Author: AI Term Project G3
Date: August 2025
"""

import sys
import os
import time
import threading
import subprocess
import requests
import argparse
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Print startup banner"""
    banner = f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                    🛍️  JIJI AI CHATBOT SYSTEM                ║
║                                                              ║
║           Intelligent Customer Support for African          ║
║                     Marketplace Businesses                  ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
{Colors.OKCYAN}🚀 Starting Jiji AI Assistant...{Colors.ENDC}
"""
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print(f"{Colors.OKBLUE}📦 Checking dependencies...{Colors.ENDC}")
    
    # Core dependencies with import names
    dependencies = [
        ('flask', 'flask'),
        ('flask-cors', 'flask_cors'),
        ('requests', 'requests'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scikit-learn', 'sklearn'),
        ('nltk', 'nltk'),
        ('tkinter', 'tkinter')
    ]
    
    missing_modules = []
    
    for package_name, import_name in dependencies:
        try:
            # Quick import test with timeout-like behavior
            if import_name == 'sklearn':
                # Test sklearn more carefully due to slow imports
                import importlib.util
                spec = importlib.util.find_spec('sklearn')
                if spec is None:
                    raise ImportError(f"No module named '{import_name}'")
                print(f"  ✅ {package_name}")
            elif import_name == 'tkinter':
                # Test tkinter which might not be available on some systems
                import tkinter
                print(f"  ✅ {package_name}")
            else:
                __import__(import_name)
                print(f"  ✅ {package_name}")
                
        except ImportError:
            missing_modules.append(package_name)
            print(f"  ❌ {package_name} - {Colors.FAIL}MISSING{Colors.ENDC}")
        except Exception as e:
            # Handle other import issues
            print(f"  ⚠️  {package_name} - {Colors.WARNING}WARNING: {str(e)[:50]}...{Colors.ENDC}")
    
    if missing_modules:
        print(f"\n{Colors.WARNING}⚠️  Missing dependencies detected!{Colors.ENDC}")
        print(f"{Colors.WARNING}Please install missing packages:{Colors.ENDC}")
        print(f"{Colors.WARNING}pip install -r requirements.txt{Colors.ENDC}")
        return False
    
    print(f"{Colors.OKGREEN}✅ All dependencies satisfied!{Colors.ENDC}\n")
    return True

def check_backend_health(max_retries=10, delay=1):
    """Check if backend server is running and healthy"""
    health_url = "http://localhost:5000/health"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(health_url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                qa_pairs = data.get('qa_pairs_loaded', 0)
                print(f"{Colors.OKGREEN}✅ Backend healthy! {qa_pairs} Q&A pairs loaded{Colors.ENDC}")
                return True
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                print(f"  🔄 Attempt {attempt + 1}/{max_retries} - waiting for backend...")
                time.sleep(delay)
            else:
                print(f"{Colors.FAIL}❌ Backend health check failed{Colors.ENDC}")
    
    return False

def start_backend():
    """Start the Flask backend server"""
    print(f"{Colors.OKBLUE}🔧 Starting backend server...{Colors.ENDC}")
    
    # Check if backend file exists
    backend_file = Path("chatbot_backend.py")
    if not backend_file.exists():
        print(f"{Colors.FAIL}❌ Backend file not found: {backend_file}{Colors.ENDC}")
        return None
    
    try:
        # Start backend process
        process = subprocess.Popen([
            sys.executable, "chatbot_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"{Colors.OKGREEN}✅ Backend server started (PID: {process.pid}){Colors.ENDC}")
        
        # Wait a moment for server to initialize
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"{Colors.FAIL}❌ Backend failed to start:{Colors.ENDC}")
            print(f"{Colors.FAIL}{stderr}{Colors.ENDC}")
            return None
            
        return process
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to start backend: {e}{Colors.ENDC}")
        return None

def start_popup():
    """Start the desktop popup application"""
    print(f"{Colors.OKBLUE}🖥️  Starting desktop popup application...{Colors.ENDC}")
    
    # Check if popup file exists
    popup_file = Path("chatbot_popup_app.py")
    if not popup_file.exists():
        print(f"{Colors.FAIL}❌ Popup file not found: {popup_file}{Colors.ENDC}")
        return None
    
    try:
        # Start popup process
        process = subprocess.Popen([
            sys.executable, "chatbot_popup_app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"{Colors.OKGREEN}✅ Desktop popup started (PID: {process.pid}){Colors.ENDC}")
        return process
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to start popup: {e}{Colors.ENDC}")
        return None

def run_tests():
    """Run system tests"""
    print(f"{Colors.OKBLUE}🧪 Running system tests...{Colors.ENDC}")
    
    test_file = Path("test_chatbot.py")
    if not test_file.exists():
        print(f"{Colors.FAIL}❌ Test file not found: {test_file}{Colors.ENDC}")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "test_chatbot.py"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}✅ All tests passed!{Colors.ENDC}")
            print(result.stdout)
            return True
        else:
            print(f"{Colors.FAIL}❌ Tests failed!{Colors.ENDC}")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"{Colors.FAIL}❌ Tests timed out{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"{Colors.FAIL}❌ Test execution failed: {e}{Colors.ENDC}")
        return False

def cleanup_processes(processes):
    """Clean up running processes"""
    print(f"\n{Colors.WARNING}🔄 Shutting down processes...{Colors.ENDC}")
    
    for name, process in processes.items():
        if process and process.poll() is None:
            print(f"  🛑 Terminating {name} (PID: {process.pid})")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"  ⚡ Force killing {name}")
                process.kill()
            except Exception as e:
                print(f"  ⚠️  Error stopping {name}: {e}")
    
    print(f"{Colors.OKGREEN}✅ Cleanup complete{Colors.ENDC}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Jiji AI Chatbot System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Start complete system
  python run.py --backend-only     # Start only backend
  python run.py --popup-only       # Start only popup  
  python run.py --test            # Run tests
        """
    )
    
    parser.add_argument('--backend-only', action='store_true',
                       help='Start only the backend server')
    parser.add_argument('--popup-only', action='store_true',
                       help='Start only the popup application')
    parser.add_argument('--test', action='store_true',
                       help='Run system tests')
    parser.add_argument('--no-health-check', action='store_true',
                       help='Skip backend health check')
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print(f"{Colors.FAIL}❌ Dependency check failed. Please install requirements.{Colors.ENDC}")
        return 1
    
    # Handle test mode
    if args.test:
        success = run_tests()
        return 0 if success else 1
    
    processes = {}
    
    try:
        # Start backend unless popup-only mode
        if not args.popup_only:
            backend_process = start_backend()
            if backend_process:
                processes['backend'] = backend_process
                
                # Health check
                if not args.no_health_check:
                    print(f"{Colors.OKBLUE}🏥 Performing health check...{Colors.ENDC}")
                    if not check_backend_health():
                        print(f"{Colors.FAIL}❌ Backend health check failed{Colors.ENDC}")
                        cleanup_processes(processes)
                        return 1
            else:
                print(f"{Colors.FAIL}❌ Failed to start backend{Colors.ENDC}")
                return 1
        
        # Start popup unless backend-only mode
        if not args.backend_only:
            # If popup-only, check if backend is running
            if args.popup_only:
                print(f"{Colors.OKBLUE}🔍 Checking for running backend...{Colors.ENDC}")
                if not check_backend_health(max_retries=3):
                    print(f"{Colors.FAIL}❌ No backend found. Please start backend first.{Colors.ENDC}")
                    return 1
            
            popup_process = start_popup()
            if popup_process:
                processes['popup'] = popup_process
            else:
                print(f"{Colors.FAIL}❌ Failed to start popup{Colors.ENDC}")
                cleanup_processes(processes)
                return 1
        
        # Success message
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Jiji AI Chatbot System is running!{Colors.ENDC}")
        
        if 'backend' in processes:
            print(f"{Colors.OKGREEN}   📡 Backend API: http://localhost:5000{Colors.ENDC}")
        if 'popup' in processes:
            print(f"{Colors.OKGREEN}   🖥️  Desktop Popup: Active{Colors.ENDC}")
        
        print(f"\n{Colors.OKCYAN}💡 Tips:{Colors.ENDC}")
        print(f"   • Use the desktop popup to chat with the AI")
        print(f"   • Backend API endpoints: /chat, /health, /stats")
        print(f"   • Press Ctrl+C to stop all services")
        
        # Wait for processes to complete
        if args.backend_only and 'backend' in processes:
            print(f"\n{Colors.OKBLUE}⏳ Backend running... Press Ctrl+C to stop{Colors.ENDC}")
            processes['backend'].wait()
        elif 'popup' in processes:
            print(f"\n{Colors.OKBLUE}⏳ Popup active... Close popup window to exit{Colors.ENDC}")
            processes['popup'].wait()
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Received interrupt signal{Colors.ENDC}")
        cleanup_processes(processes)
        return 0
        
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        cleanup_processes(processes)
        return 1
        
    finally:
        cleanup_processes(processes)

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"{Colors.FAIL}💥 Fatal error: {e}{Colors.ENDC}")
        sys.exit(1)
