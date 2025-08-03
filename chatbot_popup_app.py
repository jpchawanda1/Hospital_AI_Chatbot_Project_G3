#!/usr/bin/env python3
"""
Modern Jiji Chatbot Popup Application
A clean, professional desktop interface for the Jiji AI Assistant
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import tkinter.font as tkFont
import requests
import threading
import sys
from datetime import datetime


class ChatbotPopup:
    def __init__(self):
        """Initialize the modern chatbot popup"""
        self.root = tk.Tk()
        self.backend_url = "http://localhost:5000"
        self.is_connected = False
        self.setup_window()
        self.setup_colors()
        self.setup_fonts()
        self.create_ui()
        
    def setup_window(self):
        """Configure main window with modern styling"""
        self.root.title("Jiji AI Assistant")
        self.root.geometry("450x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8f9fa')
        
        # Modern window styling
        try:
            self.root.wm_attributes("-alpha", 0.98)
        except:
            pass
            
        # Set window icon and properties
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window
        self.center_window()
        
    def setup_colors(self):
        """Define modern color palette"""
        self.colors = {
            'primary': '#007bff',
            'success': '#28a745', 
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'white': '#ffffff',
            'border': '#dee2e6',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'text_muted': '#adb5bd',
            'user_bubble': '#007bff',
            'user_text': '#ffffff',
            'bot_bubble': '#e9ecef',
            'bot_text': '#495057'
        }
        
    def setup_fonts(self):
        """Configure modern typography"""
        self.fonts = {
            'title': tkFont.Font(family="Segoe UI", size=18, weight="bold"),
            'subtitle': tkFont.Font(family="Segoe UI", size=14, weight="bold"),
            'body': tkFont.Font(family="Segoe UI", size=11),
            'small': tkFont.Font(family="Segoe UI", size=9),
            'chat': tkFont.Font(family="Segoe UI", size=10),
            'emoji': tkFont.Font(family="Segoe UI Emoji", size=12)
        }
        
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['light'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.create_header(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Chat area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Initialize
        self.setup_placeholder()
        self.check_backend_status()
        self.add_welcome_message()
        
    def create_header(self, parent):
        """Create modern header with branding"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo and title
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = tk.Label(title_frame, text="🛒 Jiji AI Assistant",
                              font=self.fonts['title'], bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(expand=True)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame, text="Your smart marketplace companion",
                                 font=self.fonts['small'], bg=self.colors['primary'],
                                 fg=self.colors['white'])
        subtitle_label.pack()
        
    def create_status_bar(self, parent):
        """Create status bar with connection info"""
        status_frame = tk.Frame(parent, bg=self.colors['white'], height=40)
        status_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        # Status icon
        self.status_icon = tk.Label(status_frame, text="🔄", font=self.fonts['emoji'],
                                   bg=self.colors['white'])
        self.status_icon.pack(side=tk.LEFT, padx=(10, 5))
        
        # Status text
        self.status_label = tk.Label(status_frame, text="Connecting...",
                                    font=self.fonts['small'], bg=self.colors['white'],
                                    fg=self.colors['text_secondary'])
        self.status_label.pack(side=tk.LEFT)
        
        # Online indicator
        self.online_indicator = tk.Frame(status_frame, bg=self.colors['danger'],
                                        width=8, height=8)
        self.online_indicator.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Stats
        self.stats_label = tk.Label(status_frame, text="", font=self.fonts['small'],
                                   bg=self.colors['white'], fg=self.colors['info'])
        self.stats_label.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_chat_area(self, parent):
        """Create chat display area"""
        # Chat container
        chat_container = tk.Frame(parent, bg=self.colors['border'])
        chat_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 0))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=self.fonts['chat'],
            bg=self.colors['white'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Configure text tags
        self.setup_chat_tags()
        
    def setup_chat_tags(self):
        """Configure chat message styling"""
        # System messages
        self.chat_display.tag_configure("system",
                                      foreground=self.colors['info'],
                                      font=self.fonts['small'],
                                      justify=tk.CENTER)
        
        # User messages
        self.chat_display.tag_configure("user",
                                      foreground=self.colors['primary'],
                                      font=self.fonts['chat'])
        
        # Bot messages
        self.chat_display.tag_configure("bot",
                                      foreground=self.colors['text_primary'],
                                      font=self.fonts['chat'])
        
        # Error messages
        self.chat_display.tag_configure("error",
                                      foreground=self.colors['danger'],
                                      font=self.fonts['small'])
        
        # Timestamps
        self.chat_display.tag_configure("timestamp",
                                      foreground=self.colors['text_muted'],
                                      font=self.fonts['small'])
        
    def create_input_area(self, parent):
        """Create message input area"""
        # Input container
        input_container = tk.Frame(parent, bg=self.colors['light'], height=100)
        input_container.pack(fill=tk.X, padx=20, pady=20)
        input_container.pack_propagate(False)
        
        # Input frame
        input_frame = tk.Frame(input_container, bg=self.colors['white'],
                              relief=tk.SOLID, bd=1)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text input
        self.message_entry = tk.Text(input_frame,
                                   height=3,
                                   font=self.fonts['body'],
                                   relief=tk.FLAT,
                                   borderwidth=0,
                                   bg=self.colors['white'],
                                   fg=self.colors['text_primary'],
                                   wrap=tk.WORD,
                                   padx=15,
                                   pady=12)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_entry.bind("<Return>", self.send_message_event)
        self.message_entry.bind("<Shift-Return>", self.new_line_event)
        
        # Send button
        send_frame = tk.Frame(input_frame, bg=self.colors['white'], width=60)
        send_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)
        send_frame.pack_propagate(False)
        
        self.send_btn = tk.Button(send_frame,
                                 text="Send",
                                 font=self.fonts['body'],
                                 bg=self.colors['primary'],
                                 fg=self.colors['white'],
                                 border=0,
                                 cursor="hand2",
                                 command=self.send_message)
        self.send_btn.pack(fill=tk.BOTH, expand=True)
        
    def setup_placeholder(self):
        """Setup placeholder text for input"""
        placeholder = "Type your message here... (Enter to send, Shift+Enter for new line)"
        
        def add_placeholder():
            if not self.message_entry.get("1.0", tk.END).strip():
                self.message_entry.insert("1.0", placeholder)
                self.message_entry.configure(fg=self.colors['text_muted'])
        
        def remove_placeholder(event):
            if self.message_entry.get("1.0", tk.END).strip() == placeholder:
                self.message_entry.delete("1.0", tk.END)
                self.message_entry.configure(fg=self.colors['text_primary'])
        
        def readd_placeholder(event):
            if not self.message_entry.get("1.0", tk.END).strip():
                add_placeholder()
        
        self.message_entry.bind("<FocusIn>", remove_placeholder)
        self.message_entry.bind("<FocusOut>", readd_placeholder)
        
        # Set initial placeholder
        add_placeholder()
        
    def add_welcome_message(self):
        """Add welcome message to chat"""
        welcome_text = """👋 Welcome to Jiji AI Assistant!

I can help you with:
• Product information & pricing
• Payment methods & delivery options
• Returns & exchanges
• Seller verification
• General marketplace questions

Just type your question below and I'll do my best to help! 🚀"""
        
        self.add_system_message(welcome_text)
        
    def add_system_message(self, message):
        """Add system message to chat"""
        self.chat_display.configure(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\n[{timestamp}] System\n", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", "system")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_user_message(self, message):
        """Add user message to chat"""
        self.chat_display.configure(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] You: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", "user")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_bot_message(self, message):
        """Add bot message to chat"""
        self.chat_display.configure(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] 🤖 Jiji Assistant: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", "bot")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_error_message(self, message):
        """Add error message to chat"""
        self.chat_display.configure(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"[{timestamp}] ❌ Error: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", "error")
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def show_typing_indicator(self):
        """Show typing indicator"""
        self.chat_display.configure(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        typing_start = self.chat_display.index(tk.END)
        self.chat_display.insert(tk.END, f"[{timestamp}] 🤖 Jiji Assistant: typing...\n\n", "system")
        typing_end = self.chat_display.index(tk.END)
        
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        return typing_start, typing_end
        
    def remove_typing_indicator(self, start_pos, end_pos):
        """Remove typing indicator"""
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.delete(start_pos, end_pos)
        self.chat_display.configure(state=tk.DISABLED)
        
    def send_message_event(self, event):
        """Handle Enter key press"""
        if event.state & 0x1:  # Shift key pressed
            return None  # Allow new line
        else:
            self.send_message()
            return "break"  # Prevent default behavior
            
    def new_line_event(self, event):
        """Handle Shift+Enter for new line"""
        return None  # Allow default behavior
        
    def send_message(self):
        """Send message to chatbot"""
        message = self.message_entry.get("1.0", tk.END).strip()
        placeholder = "Type your message here... (Enter to send, Shift+Enter for new line)"
        
        # Check if message is empty or just placeholder
        if not message or message == placeholder:
            self.update_status("Please enter a message", "error")
            return
            
        # Clear input
        self.message_entry.delete("1.0", tk.END)
        
        # Add user message
        self.add_user_message(message)
        
        # Show typing indicator
        typing_pos = self.show_typing_indicator()
        
        # Send to backend
        threading.Thread(target=self.process_message, args=(message, typing_pos), daemon=True).start()
        
    def process_message(self, message, typing_pos):
        """Process message in background thread"""
        try:
            self.root.after(0, lambda: self.update_status("Processing...", "processing"))
            
            response = requests.post(
                f"{self.backend_url}/chat",
                json={"message": message},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get('response', 'Sorry, I could not process your request.')
                confidence = data.get('confidence', 0)
                
                # Remove typing indicator and add response
                self.root.after(0, self.handle_response, bot_response, confidence, typing_pos)
                
            else:
                error_msg = f"Server error: {response.status_code}"
                self.root.after(0, self.handle_error, error_msg, typing_pos)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            self.root.after(0, self.handle_error, error_msg, typing_pos)
            
    def handle_response(self, response, confidence, typing_pos):
        """Handle successful response"""
        start_pos, end_pos = typing_pos
        self.remove_typing_indicator(start_pos, end_pos)
        self.add_bot_message(response)
        
        # Update stats
        confidence_percent = int(confidence * 100)
        self.stats_label.config(text=f"Confidence: {confidence_percent}%")
        self.update_status("Response received", "success")
        
    def handle_error(self, error_msg, typing_pos):
        """Handle error response"""
        start_pos, end_pos = typing_pos
        self.remove_typing_indicator(start_pos, end_pos)
        self.add_error_message(error_msg)
        self.update_status("Error occurred", "error")
        
    def update_status(self, message, status_type="info"):
        """Update status with color coding"""
        colors = {
            "success": self.colors['success'],
            "error": self.colors['danger'],
            "processing": self.colors['warning'],
            "info": self.colors['info']
        }
        
        icons = {
            "success": "✅",
            "error": "❌", 
            "processing": "🔄",
            "info": "ℹ️"
        }
        
        color = colors.get(status_type, self.colors['text_primary'])
        icon = icons.get(status_type, "")
        
        self.status_icon.config(text=icon)
        self.status_label.config(text=message, fg=color)
        
        # Update online indicator
        if status_type == "success":
            self.online_indicator.config(bg=self.colors['success'])
        elif status_type == "error":
            self.online_indicator.config(bg=self.colors['danger'])
        else:
            self.online_indicator.config(bg=self.colors['warning'])
            
        # Auto clear status after 3 seconds
        if status_type in ["error", "processing"]:
            self.root.after(3000, self.clear_status)
            
    def clear_status(self):
        """Clear status message"""
        self.status_label.config(text="Ready", fg=self.colors['text_primary'])
        self.status_icon.config(text="ℹ️")
        
    def check_backend_status(self):
        """Check if backend is running"""
        def check():
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=3)
                if response.status_code == 200:
                    self.is_connected = True
                    self.root.after(0, lambda: self.update_status("Connected to server", "success"))
                    return
            except:
                pass
                
            self.is_connected = False
            self.root.after(0, lambda: self.update_status("Server not available", "error"))
        
        threading.Thread(target=check, daemon=True).start()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
    def run(self):
        """Start the chatbot popup"""
        self.root.mainloop()
        
    def on_closing(self):
        """Handle window closing"""
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    try:
        app = ChatbotPopup()
        app.run()
    except KeyboardInterrupt:
        print("\nChatbot popup closed by user")
    except Exception as e:
        print(f"Error running chatbot popup: {e}")
        input("Press Enter to exit...")
