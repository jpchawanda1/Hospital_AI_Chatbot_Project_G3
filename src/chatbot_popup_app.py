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
        self.query_count = 0
        self.accuracy = 89.2
        self.ai_model_active = False
        self.backend_ready = False
        self.send_button_active = False
        self.input_focused = False
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.backend_url = "http://localhost:5000"
        self.check_backend_connection()
        
    def setup_window(self):
        """Configure main window with dark theme styling"""
        self.root.title("Hospital AI Assistant")
        self.root.geometry("750x550")
        self.root.minsize(650, 450)
        
        # Center the window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (750 // 2)
        y = (self.root.winfo_screenheight() // 2) - (550 // 2)
        self.root.geometry(f"750x550+{x}+{y}")
        
        # Dark theme styling
        self.root.configure(bg='#1e1e1e')
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
    def setup_styles(self):
        """Configure dark theme color scheme and styles"""
        self.colors = {
            'bg_primary': '#1e1e1e',       # Dark background
            'bg_sidebar': '#2d2d2d',       # Dark sidebar
            'bg_chat': '#1e1e1e',          # Dark chat area
            'bg_input': '#2d2d2d',         # Dark input field
            'text_primary': '#ffffff',     # White text
            'text_secondary': '#cccccc',   # Light gray text
            'text_muted': '#999999',       # Muted gray text
            'accent_blue': '#0078d4',      # Microsoft blue
            'accent_green': '#16a085',     # Teal green
            'accent_gray': '#666666',      # Medium gray
            'border_light': '#404040',     # Dark border
            'border_medium': '#555555',    # Medium dark border
            'hover': '#3c3c3c',            # Hover state
            'active': '#0078d4',           # Active/selected state
            'success': '#16a085',          # Success teal
            'warning': '#f39c12',          # Warning orange
            'danger': '#e74c3c'            # Error red
        }
        
    def create_widgets(self):
        """Create and arrange all GUI widgets with sidebar layout"""
        # Create sidebar
        self.create_sidebar()
        
        # Create main chat area
        self.create_main_chat_area()
        
    def create_sidebar(self):
        """Create the left sidebar with professional styling"""
        sidebar_frame = tk.Frame(
            self.root,
            bg=self.colors['bg_sidebar'],
            width=150,
            relief=tk.FLAT
        )
        sidebar_frame.grid(row=0, column=0, sticky=(tk.W, tk.N, tk.S), padx=0, pady=0)
        sidebar_frame.grid_propagate(False)
        sidebar_frame.grid_rowconfigure(3, weight=1)
        
        # Add subtle border
        border_frame = tk.Frame(sidebar_frame, bg=self.colors['border_light'], width=1)
        border_frame.place(relx=1.0, rely=0, relheight=1.0, anchor='ne')
        
        # Sidebar title
        title_frame = tk.Frame(sidebar_frame, bg=self.colors['bg_sidebar'])
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=12, pady=(12, 10))
        
        # Professional title
        title_label = tk.Label(
            title_frame,
            text="⚙️ Controls",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_sidebar']
        )
        title_label.pack(anchor='w')
        
        # AI Model Status
        self.create_professional_status_card(sidebar_frame, "AI Model", "Active", self.colors['success'], row=1)
        
        # Accuracy Status
        self.create_professional_status_card(sidebar_frame, "Accuracy", f"{self.accuracy}%", self.colors['accent_blue'], row=2)
        
        # New Chat Button with dark theme styling
        new_chat_button = tk.Button(
            sidebar_frame,
            text="💬 New Chat",
            command=self.new_chat,
            font=('Segoe UI', 9, 'bold'),
            bg=self.colors['accent_blue'],
            fg='white',
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=8,
            cursor='hand2',
            activebackground=self.colors['active'],
            activeforeground='white'
        )
        new_chat_button.grid(row=5, column=0, sticky=(tk.W, tk.E), padx=12, pady=(12, 6))
        
        # Clear Chat Button with dark theme styling
        clear_button = tk.Button(
            sidebar_frame,
            text="🗑 Clear",
            command=self.clear_chat,
            font=('Segoe UI', 8),
            bg=self.colors['bg_chat'],
            fg=self.colors['text_secondary'],
            relief=tk.FLAT,
            bd=1,
            padx=12,
            pady=6,
            cursor='hand2',
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text_primary'],
            highlightbackground=self.colors['border_light'],
            highlightthickness=1
        )
        clear_button.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=12, pady=(6, 12))
    
    def create_professional_status_card(self, parent, title, status, color, row):
        """Create a professional status card with rounded appearance"""
        # Card container with border
        card_container = tk.Frame(
            parent,
            bg=self.colors['bg_chat'],
            relief=tk.FLAT,
            bd=0,
            highlightbackground=self.colors['border_light'],
            highlightthickness=1
        )
        card_container.grid(row=row, column=0, sticky=(tk.W, tk.E), padx=12, pady=(0, 6))
        
        # Inner card frame
        card_frame = tk.Frame(card_container, bg=self.colors['bg_chat'])
        card_frame.pack(fill=tk.BOTH, padx=8, pady=6)
        
        # Status indicator dot and text
        content_frame = tk.Frame(card_frame, bg=self.colors['bg_chat'])
        content_frame.pack(fill=tk.BOTH)
        
        # Colored status dot
        dot_label = tk.Label(
            content_frame,
            text="●",
            font=('Segoe UI', 8),
            bg=self.colors['bg_chat'],
            fg=color
        )
        dot_label.pack(side=tk.LEFT, padx=(0, 6))
        
        # Text content
        text_frame = tk.Frame(content_frame, bg=self.colors['bg_chat'])
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            text_frame,
            text=title,
            font=('Segoe UI', 7),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_chat']
        )
        title_label.pack(anchor='w')
        
        status_label = tk.Label(
            text_frame,
            text=status,
            font=('Segoe UI', 9, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_chat']
        )
        status_label.pack(anchor='w')
        
        # Store reference for updates
        if "AI Model" in title:
            self.ai_status_label = status_label
        elif "Accuracy" in title:
            self.accuracy_label = status_label
    
    def create_main_chat_area(self):
        """Create the main chat area with professional styling"""
        main_frame = tk.Frame(
            self.root,
            bg=self.colors['bg_chat']
        )
        main_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=0, pady=0)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Chat area
        self.create_chat_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
    def create_chat_area(self, parent):
        """Create scrollable chat display area with professional styling"""
        chat_container = tk.Frame(parent, bg=self.colors['bg_chat'])
        chat_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=12, pady=(12, 6))
        chat_container.grid_rowconfigure(0, weight=1)
        chat_container.grid_columnconfigure(0, weight=1)
        
        # Create canvas for custom chat bubbles
        self.chat_canvas = tk.Canvas(
            chat_container,
            bg=self.colors['bg_chat'],
            highlightthickness=0,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.chat_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create professional scrollbar
        chat_scrollbar = tk.Scrollbar(
            chat_container, 
            orient="vertical", 
            command=self.chat_canvas.yview,
            bg=self.colors['bg_sidebar'],
            troughcolor=self.colors['bg_chat'],
            borderwidth=0,
            highlightthickness=0,
            width=10
        )
        chat_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=(3, 0))
        self.chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
        
        # Create frame inside canvas for chat messages
        self.chat_frame = tk.Frame(self.chat_canvas, bg=self.colors['bg_chat'])
        self.canvas_frame = self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        
        # Bind events for responsive scrolling
        self.chat_frame.bind('<Configure>', self.on_frame_configure)
        self.chat_canvas.bind('<Configure>', self.on_canvas_configure)
        self.chat_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Message counter for unique widget names
        self.message_count = 0
        
        # Welcome message
        self.add_chat_message("ai", "I specialize in hospital information and medical assistance. Please let me know if you need help with appointments, hospital locations, or medical guidance.")
        
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
        """Add a chat message with professional bubble-style layout"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%H:%M")
            
        self.message_count += 1
        
        # Create container frame for the message
        msg_container = tk.Frame(self.chat_frame, bg=self.colors['bg_chat'], pady=6)
        msg_container.pack(fill=tk.X, padx=12, pady=3)
        
        if sender_type == "user":
            # User message - right aligned with blue bubble
            self.create_user_message(msg_container, message, timestamp)
        elif sender_type == "ai":
            # AI message - left aligned with white bubble
            self.create_ai_message(msg_container, message, timestamp)
        else:
            # System message - centered
            self.create_system_message(msg_container, message, timestamp)
            
        # Auto-scroll to bottom
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
        
    def create_rounded_frame(self, parent, bg_color, border_color=None, corner_radius=8):
        """Create a frame with rounded corner appearance using overlapping frames"""
        if border_color is None:
            border_color = self.colors['border_light']
            
        # Main container
        container = tk.Frame(parent, bg=parent['bg'])
        
        # Create the main rounded frame using a Canvas for true rounded corners
        canvas = tk.Canvas(
            container,
            highlightthickness=0,
            borderwidth=0,
            bg=parent['bg']
        )
        
        def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
            """Draw a rounded rectangle on canvas"""
            points = []
            for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                        (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                        (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                        (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
                points.extend([x, y])
            return canvas.create_polygon(points, smooth=True, **kwargs)
        
        # We'll use a simpler approach with layered frames for rounded effect
        outer_frame = tk.Frame(container, bg=border_color, bd=0, relief=tk.FLAT)
        inner_frame = tk.Frame(outer_frame, bg=bg_color, bd=0, relief=tk.FLAT)
        inner_frame.pack(padx=1, pady=1, fill=tk.BOTH, expand=True)
        
        return container, inner_frame

    def create_user_message(self, parent, message, timestamp):
        """Create user message bubble with rounded corners using Canvas"""
        # Create right-aligned container
        right_frame = tk.Frame(parent, bg=self.colors['bg_chat'])
        right_frame.pack(side=tk.RIGHT, anchor='e', padx=(60, 0))
        
        # Timestamp (right-aligned, above bubble)
        time_label = tk.Label(
            right_frame, 
            text=f"👤 You • {timestamp}", 
            font=('Segoe UI', 7),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_chat'],
            anchor='e'
        )
        time_label.pack(anchor='e', pady=(0, 3))
        
        # Create rounded message bubble using Canvas
        self.create_rounded_message_bubble(
            right_frame, 
            message, 
            self.colors['accent_blue'], 
            self.colors['text_primary'], 
            align='right'
        )
    
    def create_ai_message(self, parent, message, timestamp):
        """Create AI message bubble with rounded corners using Canvas"""
        # Create left-aligned container
        left_frame = tk.Frame(parent, bg=self.colors['bg_chat'])
        left_frame.pack(side=tk.LEFT, anchor='w', padx=(0, 60))
        
        # AI avatar and name container
        header_frame = tk.Frame(left_frame, bg=self.colors['bg_chat'])
        header_frame.pack(anchor='w', pady=(0, 3))
        
        # AI indicator
        ai_label = tk.Label(
            header_frame,
            text="🤖 AI Assistant",
            font=('Segoe UI', 7, 'bold'),
            fg=self.colors['accent_green'],
            bg=self.colors['bg_chat']
        )
        ai_label.pack(side=tk.LEFT)
        
        # Timestamp
        time_label = tk.Label(
            header_frame,
            text=f"• {timestamp}",
            font=('Segoe UI', 7),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_chat']
        )
        time_label.pack(side=tk.LEFT, padx=(3, 0))
        
        # Create rounded message bubble using Canvas
        self.create_rounded_message_bubble(
            left_frame, 
            message, 
            self.colors['hover'], 
            self.colors['text_primary'], 
            align='left'
        )
    
    def create_rounded_message_bubble(self, parent, message, bg_color, text_color, align='left'):
        """Create a rounded message bubble using Canvas for smooth corners"""
        # Calculate text dimensions
        temp_label = tk.Label(parent, text=message, font=('Segoe UI', 9), wraplength=300)
        temp_label.update_idletasks()
        text_width = min(temp_label.winfo_reqwidth(), 300)
        text_height = temp_label.winfo_reqheight()
        temp_label.destroy()
        
        # Canvas dimensions with padding
        canvas_width = text_width + 32  # 16px padding on each side
        canvas_height = text_height + 24  # 12px padding top/bottom
        
        # Create canvas for rounded rectangle
        canvas = tk.Canvas(
            parent,
            width=canvas_width,
            height=canvas_height,
            bg=self.colors['bg_chat'],
            highlightthickness=0,
            relief=tk.FLAT
        )
        canvas.pack(anchor='e' if align == 'right' else 'w', pady=2)
        
        # Enhanced rounded rectangle with larger radius
        radius = 16  # Increased radius for more pronounced rounding
        x1, y1 = 3, 3
        x2, y2 = canvas_width - 3, canvas_height - 3
        
        # Create smooth rounded rectangle with better arc coverage
        # Top-left corner
        canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                         start=90, extent=90, fill=bg_color, outline='', width=0)
        # Top-right corner  
        canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                         start=0, extent=90, fill=bg_color, outline='', width=0)
        # Bottom-left corner
        canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                         start=180, extent=90, fill=bg_color, outline='', width=0)
        # Bottom-right corner
        canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                         start=270, extent=90, fill=bg_color, outline='', width=0)
        
        # Fill the main body rectangles
        canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=bg_color, outline='', width=0)
        canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=bg_color, outline='', width=0)
        
        # Add subtle shadow effect for depth
        if align == 'right':
            # User message - blue with slight shadow
            canvas.create_rectangle(x1 + radius + 1, y1 + 1, x2 - radius + 1, y2 + 1, 
                                  fill='#005a9f', outline='', width=0)
            canvas.create_rectangle(x1 + 1, y1 + radius + 1, x2 + 1, y2 - radius + 1, 
                                  fill='#005a9f', outline='', width=0)
        
        # Add text on top of the rounded rectangle
        canvas.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text=message,
            font=('Segoe UI', 9),
            fill=text_color,
            width=text_width,
            anchor='center'
        )
        
    def create_system_message(self, parent, message, timestamp):
        """Create system message (centered, small) with dark theme"""
        # Center container
        center_frame = tk.Frame(parent, bg=self.colors['bg_chat'])
        center_frame.pack(anchor='center', pady=5)
        
        # System message
        sys_label = tk.Label(
            center_frame,
            text=f"{message}",
            font=('Segoe UI', 9, 'italic'),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_chat'],
            wraplength=400,
            justify=tk.CENTER
        )
        sys_label.pack()
        
    def create_input_area(self, parent):
        """Create modern ChatGPT-style input field with rounded corners"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_chat'])
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=16, pady=(0, 16))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Create rounded input container using Canvas
        self.create_rounded_input_container(input_frame)
    
    def create_rounded_input_container(self, parent):
        """Create a rounded input container similar to ChatGPT"""
        # Container frame
        container_frame = tk.Frame(parent, bg=self.colors['bg_chat'])
        container_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        container_frame.grid_columnconfigure(0, weight=1)

        # Canvas for rounded rectangle background
        canvas_height = 48
        self.input_canvas = tk.Canvas(
            container_frame,
            height=canvas_height,
            bg=self.colors['bg_chat'],
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.input_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Bind canvas resize to redraw background
        self.input_canvas.bind('<Configure>', self.redraw_input_background)

        # Text input frame (positioned over canvas)
        input_text_frame = tk.Frame(container_frame, bg=self.colors['bg_chat'])
        input_text_frame.place(in_=self.input_canvas, x=16, y=8, relwidth=1.0, width=-80, height=32)

        # Text input field
        self.message_entry = tk.Text(
            input_text_frame,
            height=1,
            font=('Segoe UI', 11),
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary'],
            relief=tk.FLAT,
            borderwidth=0,
            wrap=tk.WORD,
            padx=0,
            pady=6,
            insertbackground=self.colors['text_primary']
        )
        self.message_entry.pack(fill=tk.BOTH, expand=True)
        self.message_entry.bind('<Return>', self.on_enter_key)
        self.message_entry.bind('<Shift-Return>', self.insert_newline)
        self.message_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.message_entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.message_entry.bind('<KeyRelease>', self.on_text_change)

        # Send button frame (positioned over canvas)
        send_frame = tk.Frame(container_frame, bg=self.colors['bg_chat'])
        send_frame.place(in_=self.input_canvas, relx=1.0, x=-48, y=8, width=32, height=32, anchor='nw')

        # Create circular send button using Canvas
        self.send_canvas = tk.Canvas(
            send_frame,
            width=32,
            height=32,
            bg=self.colors['bg_input'],
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.send_canvas.pack()

        # Draw circular send button
        self.draw_send_button()

        # Bind send button events
        self.send_canvas.bind('<Button-1>', lambda e: self.send_message())
        self.send_canvas.bind('<Enter>', self.on_send_hover)
        self.send_canvas.bind('<Leave>', self.on_send_leave)

        # Add placeholder text
        self.placeholder_text = ""
        self.add_placeholder()
        
        # Initial state
        self.send_button_active = False
        self.input_focused = False
    
    def redraw_input_background(self, event=None):
        """Redraw the rounded input background when canvas resizes"""
        self.input_canvas.delete("input_bg")
        
        canvas_width = self.input_canvas.winfo_width()
        canvas_height = 48
        
        if canvas_width > 1:  # Only draw if canvas has been properly sized
            # Draw rounded rectangle background
            radius = 24  # Half of height for fully rounded corners
            x1, y1 = 2, 2
            x2, y2 = canvas_width - 2, canvas_height - 2
            
            # Determine border color based on focus state
            border_color = self.colors['accent_blue'] if self.input_focused else self.colors['border_medium']
            
            # Draw border (slightly larger)
            self.input_canvas.create_arc(x1-1, y1-1, x1 + 2*radius+1, y1 + 2*radius+1, 
                                       start=90, extent=90, fill=border_color, outline='', width=0, tags="input_bg")
            self.input_canvas.create_arc(x2 - 2*radius-1, y1-1, x2+1, y1 + 2*radius+1, 
                                       start=0, extent=90, fill=border_color, outline='', width=0, tags="input_bg")
            self.input_canvas.create_arc(x1-1, y2 - 2*radius-1, x1 + 2*radius+1, y2+1, 
                                       start=180, extent=90, fill=border_color, outline='', width=0, tags="input_bg")
            self.input_canvas.create_arc(x2 - 2*radius-1, y2 - 2*radius-1, x2+1, y2+1, 
                                       start=270, extent=90, fill=border_color, outline='', width=0, tags="input_bg")
            self.input_canvas.create_rectangle(x1 + radius-1, y1-1, x2 - radius+1, y2+1, fill=border_color, outline='', width=0, tags="input_bg")
            self.input_canvas.create_rectangle(x1-1, y1 + radius-1, x2+1, y2 - radius+1, fill=border_color, outline='', width=0, tags="input_bg")
            
            # Draw main background
            self.input_canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                                       start=90, extent=90, fill=self.colors['bg_input'], outline='', width=0, tags="input_bg")
            self.input_canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                                       start=0, extent=90, fill=self.colors['bg_input'], outline='', width=0, tags="input_bg")
            self.input_canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                                       start=180, extent=90, fill=self.colors['bg_input'], outline='', width=0, tags="input_bg")
            self.input_canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                                       start=270, extent=90, fill=self.colors['bg_input'], outline='', width=0, tags="input_bg")
            self.input_canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=self.colors['bg_input'], outline='', width=0, tags="input_bg")
            self.input_canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=self.colors['bg_input'], outline='', width=0, tags="input_bg")
    
    def draw_send_button(self):
        """Draw the circular send button with arrow icon"""
        self.send_canvas.delete("send_btn")
        
        # Button colors based on state
        if self.send_button_active:
            bg_color = self.colors['accent_blue']
            icon_color = 'white'
        else:
            bg_color = self.colors['accent_gray']
            icon_color = self.colors['text_muted']
        
        # Draw circular background
        self.send_canvas.create_oval(4, 4, 28, 28, fill=bg_color, outline='', width=0, tags="send_btn")
        
        # Draw send arrow icon (ChatGPT style)
        # Arrow pointing up-right
        self.send_canvas.create_line(12, 20, 20, 12, fill=icon_color, width=2, tags="send_btn")  # Main arrow line
        self.send_canvas.create_line(20, 12, 17, 12, fill=icon_color, width=2, tags="send_btn")  # Arrow head horizontal
        self.send_canvas.create_line(20, 12, 20, 15, fill=icon_color, width=2, tags="send_btn")  # Arrow head vertical
    
    def on_send_hover(self, event):
        """Handle send button hover"""
        if self.send_button_active:
            self.send_canvas.delete("send_btn")
            # Slightly darker blue on hover
            self.send_canvas.create_oval(4, 4, 28, 28, fill=self.colors['active'], outline='', width=0, tags="send_btn")
            self.send_canvas.create_line(12, 20, 20, 12, fill='white', width=2, tags="send_btn")
            self.send_canvas.create_line(20, 12, 17, 12, fill='white', width=2, tags="send_btn")
            self.send_canvas.create_line(20, 12, 20, 15, fill='white', width=2, tags="send_btn")
    
    def on_send_leave(self, event):
        """Handle send button leave"""
        self.draw_send_button()
    
    def on_text_change(self, event=None):
        """Handle text changes to update send button state"""
        text_content = self.message_entry.get('1.0', 'end-1c').strip()
        has_text = text_content and text_content != self.placeholder_text
        
        if has_text != self.send_button_active:
            self.send_button_active = has_text
            self.draw_send_button()
    
    def add_placeholder(self):
        """Add placeholder text to input field"""
        self.message_entry.insert('1.0', self.placeholder_text)
        self.message_entry.config(fg=self.colors['text_muted'])
        
    def remove_placeholder(self):
        """Remove placeholder text"""
        if self.message_entry.get('1.0', 'end-1c') == self.placeholder_text:
            self.message_entry.delete('1.0', tk.END)
            self.message_entry.config(fg=self.colors['text_primary'])
        
    def on_entry_focus_in(self, event):
        """Handle input focus in and remove placeholder"""
        self.remove_placeholder()
        self.input_focused = True
        self.redraw_input_background()
        
    def on_entry_focus_out(self, event):
        """Handle input focus out and add placeholder if empty"""
        if not self.message_entry.get('1.0', 'end-1c').strip():
            self.add_placeholder()
        self.input_focused = False
        self.redraw_input_background()
        
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
        """Update connection status and AI model status"""
        if connected:
            # Update AI model status in sidebar
            if hasattr(self, 'ai_status_label'):
                self.ai_status_label.config(text="Active")
            self.ai_model_active = True
            
            # Show different status based on model type
            if "Loading..." in model_type:
                self.send_button_active = False
                self.draw_send_button()
                # Continue checking until model loads
                self.root.after(2000, self.check_backend_connection)
            else:
                self.backend_ready = True
                
        else:
            # Update AI model status to inactive
            if hasattr(self, 'ai_status_label'):
                self.ai_status_label.config(text="Inactive")
            self.ai_model_active = False
            self.backend_ready = False
            
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
        # Check if send button is active and backend is ready
        if not self.send_button_active or not self.backend_ready:
            return
            
        message = self.message_entry.get("1.0", tk.END).strip()
        
        # Check if message is empty or just placeholder
        if not message or message == self.placeholder_text:
            return
            
        # Clear input field and add placeholder back
        self.message_entry.delete("1.0", tk.END)
        self.add_placeholder()
        
        # Increment query counter
        self.query_count += 1
        
        # Add user message to chat
        self.add_message("You", message)
        
        # Show typing indicator
        self.show_typing_indicator()
        
        # Disable send button while processing
        self.send_button_active = False
        self.draw_send_button()
        
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
                    
                    # Update accuracy based on confidence
                    self.update_accuracy(confidence)
                    
                    # Add confidence info for low confidence responses
                    if confidence < 0.5 and confidence > 0:
                        bot_response += f"\n\n💡 Tip: Try rephrasing your question for better results (Confidence: {confidence:.1%})"
                        
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
    
    def update_accuracy(self, confidence):
        """Update accuracy display based on response confidence"""
        # Simple running average
        current_accuracy = self.accuracy / 100.0
        new_accuracy = (current_accuracy * 0.9) + (confidence * 0.1)
        self.accuracy = new_accuracy * 100
        self.accuracy_label.config(text=f"{self.accuracy:.1f}%")
        
    def show_typing_indicator(self):
        """Show AI typing indicator with professional styling"""
        # Professional typing indicator
        self.typing_container = tk.Frame(self.chat_frame, bg=self.colors['bg_chat'], pady=6)
        self.typing_container.pack(fill=tk.X, padx=12, pady=3)
        
        left_frame = tk.Frame(self.typing_container, bg=self.colors['bg_chat'])
        left_frame.pack(side=tk.LEFT, anchor='w', padx=(0, 60))
        
        # Typing bubble with rounded styling
        bubble_outer = tk.Frame(left_frame, bg=self.colors['bg_chat'])
        bubble_outer.pack(anchor='w')
        
        bubble_border = tk.Frame(
            bubble_outer,
            bg=self.colors['border_light'],
            bd=0,
            relief=tk.FLAT
        )
        bubble_border.pack(padx=1, pady=1)
        
        bubble_inner = tk.Frame(
            bubble_border,
            bg=self.colors['bg_primary'],
            bd=0,
            relief=tk.FLAT
        )
        bubble_inner.pack(padx=1, pady=1)
        
        # Typing text
        self.typing_dots = tk.Label(
            bubble_inner,
            text="🤖 AI is typing...",
            font=('Segoe UI', 9),
            fg=self.colors['text_muted'],
            bg=self.colors['bg_primary'],
            padx=10,
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
        # Check if there's text to determine button state
        text_content = self.message_entry.get('1.0', 'end-1c').strip()
        self.send_button_active = text_content and text_content != self.placeholder_text and self.backend_ready
        self.draw_send_button()
        
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
    def new_chat(self):
        """Start a new chat session"""
        # Clear the current chat
        self.clear_chat()
        
        # Add welcome message for new chat
        timestamp = datetime.now().strftime("%H:%M")
        self.add_message("AI", "Hello! Welcome to Hospital AI Agent. I'm here to help you with medical information about Nairobi Hospital and Kenyatta National Hospital. How can I assist you today?", timestamp)
        
    def clear_chat(self):
        """Clear the chat display and reset counters"""
        # Clear all messages from the chat frame
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        # Reset message counter
        self.message_count = 0
        
        # Reset query counter
        self.query_count = 0
        
        # Reset accuracy
        self.accuracy = 89.2
        self.accuracy_label.config(text=f"{self.accuracy}%")
        
        # Add welcome message
        self.add_chat_message("ai", "I specialize in hospital information and medical assistance. Please let me know if you need help with appointments, hospital locations, or medical guidance.")

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
