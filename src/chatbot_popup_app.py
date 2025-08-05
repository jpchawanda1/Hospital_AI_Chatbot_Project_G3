#!/usr/bin/env python3
"""
Hospital AI Agent Desktop Application - Professional Version
============================================================

Professional tkinter-based desktop chat interface for the Hospital AI Agent system.
Connects to the Flask backend API for intelligent medical information assistance.

Author: AI Term Project G3
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading
import time
from datetime import datetime

class HospitalAIAgentApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.backend_url = "http://localhost:5000"
        self.check_backend_connection()
        
    def setup_window(self):
        """Configure main window with clean styling"""
        self.root.title("Hospital AI - Medical Information Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
        # Clean window styling
        self.root.configure(bg='#f8f9fa')
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def setup_styles(self):
        """Configure professional color scheme and styles"""
        self.colors = {
            'primary': '#1e3a8a',      # Medical blue
            'secondary': '#374151',    # Dark gray
            'accent': '#059669',       # Medical green
            'success': '#10b981',      # Success green
            'warning': '#f59e0b',      # Warning orange
            'danger': '#ef4444',       # Emergency red
            'light': '#f8fafc',        # Very light gray
            'white': '#ffffff',        # Pure white
            'text': '#1f2937',         # Dark text
            'text_light': '#6b7280',   # Light gray text
            'medical_blue': '#3b82f6', # Professional medical blue
            'emergency_red': '#dc2626' # Emergency red
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles with medical theme
        style.configure('Send.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 8))
        
        style.configure('Emergency.TButton',
                       background=self.colors['emergency_red'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 9, 'bold'),
                       padding=(15, 6))
        
        style.configure('Clear.TButton',
                       background=self.colors['text_light'],
                       foreground=self.colors['white'],
                       font=('Segoe UI', 9),
                       padding=(15, 6))
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Chat area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """Create header with title and connection status"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Title with simple medical icon
        title_frame = tk.Frame(header_frame, bg=self.colors['white'])
        title_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Simple medical icon
        icon_label = tk.Label(title_frame,
                             text="[H]",
                             font=('Segoe UI', 16),
                             fg=self.colors['accent'],
                             bg=self.colors['white'])
        icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        title_label = tk.Label(title_frame,
                              text="Hospital AI",
                              font=('Segoe UI', 16, 'bold'),
                              fg=self.colors['primary'],
                              bg=self.colors['white'])
        title_label.pack(side=tk.LEFT)
        
        # Simple subtitle
        subtitle_label = tk.Label(header_frame,
                                 text="Medical Information Assistant",
                                 font=('Segoe UI', 9),
                                 fg=self.colors['text_light'],
                                 bg=self.colors['white'])
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 0))
        
        # Simple connection status
        self.status_label = tk.Label(
            header_frame,
            text="Connecting...",
            font=('Segoe UI', 8),
            fg=self.colors['warning'],
            bg=self.colors['white']
        )
        self.status_label.grid(row=0, column=1, sticky=tk.E)
        
    def create_chat_area(self, parent):
        """Create scrollable chat display area with ChatGPT-style layout"""
        chat_frame = ttk.Frame(parent)
        chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas for custom chat bubbles
        self.chat_canvas = tk.Canvas(
            chat_frame,
            bg='#f8f9fa',
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.chat_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create scrollbar for canvas
        chat_scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_canvas.yview)
        chat_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
        
        # Create frame inside canvas for chat messages
        self.chat_frame = tk.Frame(self.chat_canvas, bg='#f8f9fa')
        self.canvas_frame = self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        
        # Bind events for responsive scrolling
        self.chat_frame.bind('<Configure>', self.on_frame_configure)
        self.chat_canvas.bind('<Configure>', self.on_canvas_configure)
        self.chat_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Message counter for unique widget names
        self.message_count = 0
        
        # Welcome message - simplified
        self.add_chat_message("ai", "Hello! I'm your hospital information assistant. Ask me about:\n\n• Emergency contacts\n• Appointments\n• Services & pricing\n• Hospital information\n\nHow can I help you today?")
        
    def on_frame_configure(self, event):
        """Update scroll region when frame size changes"""
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """Update frame width when canvas size changes"""
        canvas_width = event.width
        self.chat_canvas.itemconfig(self.canvas_frame, width=canvas_width)
        
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def add_chat_message(self, sender_type, message, timestamp=None):
        """Add a chat message with bubble-style layout"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
            
        self.message_count += 1
        
        # Create container frame for the message
        msg_container = tk.Frame(self.chat_frame, bg='#f8f9fa', pady=5)
        msg_container.pack(fill=tk.X, padx=10, pady=2)
        
        if sender_type == "user":
            # User message - right aligned with blue bubble
            self.create_user_message(msg_container, message, timestamp)
        elif sender_type == "ai":
            # AI message - left aligned with gray bubble
            self.create_ai_message(msg_container, message, timestamp)
        else:
            # System message - centered
            self.create_system_message(msg_container, message, timestamp)
            
        # Auto-scroll to bottom
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
        
    def create_user_message(self, parent, message, timestamp):
        """Create user message bubble (right side, blue)"""
        # Create right-aligned container
        right_frame = tk.Frame(parent, bg='#f8f9fa')
        right_frame.pack(side=tk.RIGHT, anchor='e', padx=(50, 0))
        
        # Timestamp (right-aligned, above bubble)
        time_label = tk.Label(
            right_frame, 
            text=f"You • {timestamp}", 
            font=('Segoe UI', 8),
            fg='#6c757d',
            bg='#f8f9fa',
            anchor='e'
        )
        time_label.pack(anchor='e', pady=(0, 2))
        
        # Message bubble
        bubble_frame = tk.Frame(
            right_frame,
            bg='#0084ff',
            relief=tk.FLAT,
            bd=0
        )
        bubble_frame.pack(anchor='e')
        
        # Message text
        msg_label = tk.Label(
            bubble_frame,
            text=message,
            font=('Segoe UI', 10),
            fg='white',
            bg='#0084ff',
            wraplength=300,
            justify=tk.LEFT,
            anchor='w',
            padx=12,
            pady=8
        )
        msg_label.pack()
        
    def create_ai_message(self, parent, message, timestamp):
        """Create AI message bubble (left side, gray)"""
        # Create left-aligned container
        left_frame = tk.Frame(parent, bg='#f8f9fa')
        left_frame.pack(side=tk.LEFT, anchor='w', padx=(0, 50))
        
        # AI avatar and name container
        header_frame = tk.Frame(left_frame, bg='#f8f9fa')
        header_frame.pack(anchor='w', pady=(0, 2))
        
        # AI indicator - simplified
        ai_label = tk.Label(
            header_frame,
            text="AI Assistant",
            font=('Segoe UI', 8, 'bold'),
            fg='#28a745',
            bg='#f8f9fa'
        )
        ai_label.pack(side=tk.LEFT)
        
        # Timestamp
        time_label = tk.Label(
            header_frame,
            text=f"• {timestamp}",
            font=('Segoe UI', 8),
            fg='#6c757d',
            bg='#f8f9fa'
        )
        time_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Message bubble
        bubble_frame = tk.Frame(
            left_frame,
            bg='#e9ecef',
            relief=tk.FLAT,
            bd=0
        )
        bubble_frame.pack(anchor='w')
        
        # Message text
        msg_label = tk.Label(
            bubble_frame,
            text=message,
            font=('Segoe UI', 10),
            fg='#212529',
            bg='#e9ecef',
            wraplength=350,
            justify=tk.LEFT,
            anchor='w',
            padx=12,
            pady=8
        )
        msg_label.pack()
        
    def create_system_message(self, parent, message, timestamp):
        """Create system message (centered, small)"""
        # Center container
        center_frame = tk.Frame(parent, bg='#f8f9fa')
        center_frame.pack(anchor='center', pady=5)
        
        # System message
        sys_label = tk.Label(
            center_frame,
            text=f"{message}",
            font=('Segoe UI', 9, 'italic'),
            fg='#6c757d',
            bg='#f8f9fa',
            wraplength=400,
            justify=tk.CENTER
        )
        sys_label.pack()
        
    def create_input_area(self, parent):
        """Create modern input field with ChatGPT-style design"""
        input_frame = ttk.Frame(parent)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Simple input container
        input_container = tk.Frame(
            input_frame,
            bg='#ffffff',
            relief=tk.SOLID,
            bd=1,
            highlightbackground='#d1d5db',
            highlightthickness=1
        )
        input_container.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        input_container.grid_columnconfigure(0, weight=1)
        
        # Simple input field
        self.message_entry = tk.Text(
            input_container,
            height=2,
            font=('Segoe UI', 11),
            bg='#ffffff',
            fg='#374151',
            relief=tk.FLAT,
            borderwidth=0,
            wrap=tk.WORD,
            padx=12,
            pady=8
        )
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.message_entry.bind('<Return>', self.on_enter_key)
        self.message_entry.bind('<Shift-Return>', self.insert_newline)
        self.message_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.message_entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        # Simple send button
        self.send_button = tk.Button(
            input_container,
            text="Send",
            command=self.send_message,
            font=('Segoe UI', 10, 'bold'),
            bg='#3b82f6',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.send_button.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=(8, 8))
        
        # Simple button frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Clear button only
        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_chat,
            font=('Segoe UI', 9),
            bg='#6c757d',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=5,
            cursor='hand2'
        )
        clear_button.pack(side=tk.LEFT)
        
    def on_entry_focus_in(self, event):
        """Handle input focus in"""
        self.message_entry.config(highlightbackground='#3b82f6')
        
    def on_entry_focus_out(self, event):
        """Handle input focus out"""
        self.message_entry.config(highlightbackground='#d1d5db')
        
    def create_status_bar(self, parent):
        """Create status bar with backend info"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.backend_status = tk.Label(
            status_frame,
            text="Checking connection...",
            font=('Segoe UI', 8),
            fg=self.colors['text_light'],
            bg=self.colors['white'],
            anchor=tk.W
        )
        self.backend_status.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
    def check_backend_connection(self):
        """Check if backend is running and update status - with retry logic"""
        def check():
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    qa_pairs = data.get('qa_pairs_loaded', 0)
                    model_type = data.get('model_type', 'Unknown')
                    self.root.after(0, self.update_connection_status, True, qa_pairs, model_type)
                    return
                else:
                    self.root.after(0, self.update_connection_status, False)
            except:
                self.root.after(0, self.update_connection_status, False)
            
            # Schedule retry in 3 seconds if connection failed
            self.root.after(3000, self.check_backend_connection)
        
        threading.Thread(target=check, daemon=True).start()
        
    def update_connection_status(self, connected, qa_pairs=0, model_type="Unknown"):
        """Update connection status display"""
        if connected:
            self.status_label.config(
                text="Connected",
                fg=self.colors['success']
            )
            
            # Show different status based on model type
            if "Loading..." in model_type:
                status_text = f"Loading... ({qa_pairs} items)"
                self.backend_status.config(text=status_text, fg=self.colors['warning'])
                self.send_button.config(state='disabled')
                # Continue checking until model loads
                self.root.after(2000, self.check_backend_connection)
            elif "Context-Only" in model_type:
                status_text = f"Ready • {qa_pairs} items loaded"
                self.backend_status.config(text=status_text, fg=self.colors['success'])
                self.send_button.config(state='normal')
            else:
                status_text = f"Ready • {qa_pairs} items • AI mode"
                self.backend_status.config(text=status_text, fg=self.colors['success'])
                self.send_button.config(state='normal')
            
            # Stop retrying connection checks
            if hasattr(self, '_connection_retry_timer'):
                self.root.after_cancel(self._connection_retry_timer)
                
        else:
            self.status_label.config(
                text="Connecting...",
                fg=self.colors['warning']
            )
            self.backend_status.config(
                text="Connecting to server...",
                fg=self.colors['text_light']
            )
            self.send_button.config(state='disabled')
            
    def add_message(self, sender, message, tag=""):
        """Add a message using the new bubble-style layout"""
        if sender == "You":
            self.add_chat_message("user", message)
        elif sender == "AI Assistant":
            self.add_chat_message("ai", message)
        else:
            self.add_chat_message("system", message)
        
    def send_message(self):
        """Send message to backend and display response"""
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            return
            
        # Clear input field
        self.message_entry.delete("1.0", tk.END)
        
        # Add user message to chat
        self.add_message("You", message)
        
        # Show typing indicator
        self.show_typing_indicator()
        
        # Disable send button while processing
        self.send_button.config(state='disabled', text="...")
        
        # Send to backend in separate thread
        def send_request():
            try:
                response = requests.post(
                    f"{self.backend_url}/chat",
                    json={"message": message},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    bot_response = data.get('response', 'Sorry, I could not process your request.')
                    confidence = data.get('confidence', 0)
                    
                    # Add confidence info for low confidence responses
                    if confidence < 0.5 and confidence > 0:
                        bot_response += f"\n\nTip: Try rephrasing your question for better results (Confidence: {confidence:.1%})"
                        
                    self.root.after(0, self.hide_typing_indicator)
                    self.root.after(0, self.add_message, "AI Assistant", bot_response)
                else:
                    self.root.after(0, self.hide_typing_indicator)
                    self.root.after(0, self.add_message, "AI Assistant", f"Sorry, I encountered an error (Status: {response.status_code}). Please try again.")
                    
            except requests.exceptions.Timeout:
                self.root.after(0, self.hide_typing_indicator)
                self.root.after(0, self.add_message, "AI Assistant", "Request timed out. Please try again with a shorter question.")
            except requests.exceptions.ConnectionError:
                self.root.after(0, self.hide_typing_indicator)
                self.root.after(0, self.add_message, "AI Assistant", "Cannot connect to AI backend. Please ensure the server is running.")
            except Exception as e:
                self.root.after(0, self.hide_typing_indicator)
                self.root.after(0, self.add_message, "AI Assistant", f"Unexpected error: {str(e)}")
            finally:
                self.root.after(0, self.reset_send_button)
                
        threading.Thread(target=send_request, daemon=True).start()
        
    def show_typing_indicator(self):
        """Show AI typing indicator"""
        # Simple typing indicator
        self.typing_container = tk.Frame(self.chat_frame, bg='#f8f9fa', pady=5)
        self.typing_container.pack(fill=tk.X, padx=10, pady=2)
        
        left_frame = tk.Frame(self.typing_container, bg='#f8f9fa')
        left_frame.pack(side=tk.LEFT, anchor='w', padx=(0, 50))
        
        # Simple typing bubble
        bubble_frame = tk.Frame(
            left_frame,
            bg='#e9ecef',
            relief=tk.FLAT,
            bd=0
        )
        bubble_frame.pack(anchor='w')
        
        # Simple typing text
        self.typing_dots = tk.Label(
            bubble_frame,
            text="Typing...",
            font=('Segoe UI', 10),
            fg='#6c757d',
            bg='#e9ecef',
            padx=12,
            pady=8
        )
        self.typing_dots.pack()
        
        # Auto-scroll to bottom
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
        
    def hide_typing_indicator(self):
        """Hide AI typing indicator"""
        if hasattr(self, 'typing_container') and self.typing_container.winfo_exists():
            self.typing_container.destroy()
        
    def reset_send_button(self):
        """Reset send button to normal state"""
        self.send_button.config(state='normal', text="Send")
        
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if event.state & 0x1:  # Shift is pressed
            return  # Allow new line
        else:
            self.send_message()
            return "break"  # Prevent default behavior
            
    def insert_newline(self, event):
        """Insert newline when Shift+Enter is pressed"""
        self.message_entry.insert(tk.INSERT, "\n")
        return "break"
        
    def clear_chat(self):
        """Clear the chat display"""
        # Clear all messages from the chat frame
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        # Reset message counter
        self.message_count = 0
        
        # Add welcome message
        self.add_chat_message("system", "Chat cleared. How can I help you today?")

def main():
    """Main function to run the application"""
    try:
        root = tk.Tk()
        app = HospitalAIAgentApp(root)
        
        # Set up proper window closing
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to close the Hospital AI?"):
                root.destroy()
                
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the application
        print("Hospital AI starting...")
        print("Ready to help with medical information")
        print("GUI ready")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting desktop application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()
