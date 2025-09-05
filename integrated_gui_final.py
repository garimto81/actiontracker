"""
Integrated Action Tracker GUI - Final Version
플레이어 이름, 칩, 자동 감지 통합 GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyautogui
import time
from datetime import datetime
import threading
from threading import Thread
import json
import pandas as pd
import requests
from io import StringIO
import numpy as np
import os

# Coordinates
PLAYER_COORDS = {
    1: (233, 361), 2: (374, 359), 3: (544, 362), 4: (722, 359), 5: (886, 356),
    6: (1051, 354), 7: (1213, 355), 8: (1385, 383), 9: (1549, 367), 10: (1705, 356)
}

# Chip coordinates for each seat - actual chip input field positions
CHIP_COORDS = {
    1: (220, 620),
    2: (400, 620),
    3: (555, 620),
    4: (700, 620),
    5: (870, 620),
    6: (1060, 620),
    7: (1220, 620),
    8: (1370, 620),
    9: (1555, 620),
    10: (1720, 620)
}

SUB_NAME_FIELD = (785, 291)
COMPLETE_BUTTON = (1720, 139)
DELETE_BUTTON = (721, 112)

class IntegratedActionTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Action Tracker - Complete Management System")
        self.root.geometry("1400x900")
        
        # Google Sheets URL
        self.sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDY_i4330JANAjIz4sMncdJdRHsOkfUCjQusHTGQk2tykrhA4d09LeIp3XRbLd8hkN6SgSB47k_nux/pub?gid=998576925&single=true&output=csv"
        
        # Data storage
        self.table_data = {}
        self.current_table = None
        
        # GUI elements storage
        self.empty_seats = {}
        self.player_names = {}
        self.chip_amounts = {}
        self.delete_players = {}
        self.seat_status_labels = {}
        
        # Speed settings
        self.speed_vars = {
            "mouse_click_delay": tk.DoubleVar(value=0.3),
            "keyboard_type_interval": tk.DoubleVar(value=0.02),
            "action_delay": tk.DoubleVar(value=0.5),
            "screen_wait": tk.DoubleVar(value=1.0)
        }
        
        pyautogui.PAUSE = 0.3
        
        self.create_widgets()
        
        # Auto-load data from Google Sheets on startup
        self.root.after(500, self.auto_load_data)
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Top Frame - Title and Table Selection (increased height for table selection)
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=180)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        title_container = tk.Frame(top_frame, bg='#2c3e50')
        title_container.pack(expand=True)
        
        tk.Label(title_container, text="ACTION TRACKER COMPLETE SYSTEM", 
                font=('Arial', 22, 'bold'), fg='white', bg='#2c3e50').pack(pady=10)
        
        # Table selection frame - Cleaner design
        table_frame = tk.Frame(title_container, bg='#2c3e50')
        table_frame.pack(pady=(10, 5))
        
        # Main table selection container
        table_select_frame = tk.Frame(table_frame, bg='#2c3e50')
        table_select_frame.pack(pady=(5, 10), padx=20)
        
        self.table_var = tk.StringVar()
        
        # Container for table buttons with scrolling support
        button_container = tk.Frame(table_select_frame, bg='#2c3e50')
        button_container.pack(pady=5)
        
        # Create two rows of table buttons
        self.button_row1 = tk.Frame(button_container, bg='#2c3e50')
        self.button_row1.pack(pady=2)
        
        self.button_row2 = tk.Frame(button_container, bg='#2c3e50')
        self.button_row2.pack(pady=2)
        
        self.quick_table_buttons = []
        
        # Create bigger table buttons (up to 10 tables in 2 rows)
        for i in range(1, 11):
            if i <= 9:
                table_id = f"T0{i}"
            else:
                table_id = f"T{i}"
            
            # Determine which row to place the button
            if i <= 5:
                parent_frame = self.button_row1
            else:
                parent_frame = self.button_row2
            
            btn = tk.Button(parent_frame, text=table_id,
                          command=lambda t=table_id: self.quick_select_table(t),
                          bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                          width=8, height=2, relief=tk.RAISED, bd=3,
                          activebackground='#2ecc71', cursor='hand2')
            btn.pack(side=tk.LEFT, padx=3)
            self.quick_table_buttons.append(btn)
        
        # Navigation buttons for many tables (prev/next pages)
        nav_frame = tk.Frame(table_select_frame, bg='#2c3e50')
        nav_frame.pack(pady=5)
        
        self.current_page = 0
        self.tables_per_page = 10
        
        self.prev_btn = tk.Button(nav_frame, text="◀", 
                                command=self.prev_table_page,
                                bg='#34495e', fg='white', font=('Arial', 12, 'bold'),
                                width=3, height=1, state=tk.DISABLED)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.page_label = tk.Label(nav_frame, text="Page 1", 
                                  font=('Arial', 10), fg='white', bg='#2c3e50')
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = tk.Button(nav_frame, text="▶", 
                                command=self.next_table_page,
                                bg='#34495e', fg='white', font=('Arial', 12, 'bold'),
                                width=3, height=1, state=tk.DISABLED)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Reload button for refreshing table data from Google Sheets
        tk.Label(nav_frame, text=" ", bg='#2c3e50', width=2).pack(side=tk.LEFT)  # Spacer
        self.reload_btn = tk.Button(nav_frame, text="🔄 Reload", 
                                   command=self.reload_tables,
                                   bg='#e67e22', fg='white', font=('Arial', 11, 'bold'),
                                   width=8, height=1, cursor='hand2')
        self.reload_btn.pack(side=tk.LEFT, padx=5)
        
        # Advanced table management frame
        advanced_frame = tk.Frame(table_select_frame, bg='#2c3e50')
        advanced_frame.pack(pady=5)
        
        # Search frame
        search_frame = tk.Frame(advanced_frame, bg='#2c3e50')
        search_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(search_frame, text="🔍", font=('Arial', 14), 
                bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=2)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                    font=('Arial', 12), width=15)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_entry.bind('<KeyRelease>', self.search_tables)
        
        tk.Button(search_frame, text="Search", command=self.search_tables,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(side=tk.LEFT, padx=2)
        
        # Favorites and Recent buttons
        tk.Button(advanced_frame, text="⭐ Favorites", 
                 command=self.show_favorites,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(advanced_frame, text="🕒 Recent", 
                 command=self.show_recent,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(advanced_frame, text="📊 Groups", 
                 command=self.show_groups,
                 bg='#1abc9c', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Test mode button for demonstrating 100+ tables
        tk.Button(advanced_frame, text="🧪 Test 100 Tables", 
                 command=lambda: self.generate_test_tables(100),
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Initialize lists for favorites and recent
        self.favorite_tables = []
        self.recent_tables = []
        self.table_groups = {}  # For grouping tables
        
        # 저장된 즐겨찾기와 최근 목록 로드
        self.load_favorites()
        self.load_recent()
        
        # Compact dropdown as alternative (hidden by default, shown when many tables)
        dropdown_frame = tk.Frame(table_select_frame, bg='#2c3e50')
        # Will be packed only when there are more than 10 tables
        self.dropdown_frame = dropdown_frame
        
        # Style for larger combobox
        style = ttk.Style()
        style.configure('Large.TCombobox', 
                       fieldbackground='#ecf0f1',
                       selectbackground='#3498db',
                       selectforeground='white',
                       arrowsize=20,
                       borderwidth=2,
                       relief='raised')
        
        self.table_combo = ttk.Combobox(dropdown_frame, textvariable=self.table_var, 
                                       width=15, font=('Arial', 12, 'bold'),
                                       height=25, style='Large.TCombobox',
                                       state='readonly')
        self.table_combo.pack(side=tk.LEFT, padx=5, pady=2)
        self.table_combo.bind('<<ComboboxSelected>>', self.on_table_selected)
        self.table_combo.bind('<Button-1>', self.on_combo_click)
        
        # Make dropdown list bigger
        self.table_combo.option_add('*TCombobox*Listbox.font', ('Arial', 11, 'bold'))
        self.table_combo.option_add('*TCombobox*Listbox.background', '#ecf0f1')
        self.table_combo.option_add('*TCombobox*Listbox.selectBackground', '#3498db')
        self.table_combo.option_add('*TCombobox*Listbox.selectForeground', 'white')
        
        # Current table indicator
        self.current_table_label = tk.Label(table_select_frame, 
                                           text="", 
                                           font=('Arial', 12, 'bold'),
                                           fg='#2ecc71', bg='#2c3e50')
        self.current_table_label.pack(pady=(5, 2))
        
        # Buttons removed - auto-load and auto-apply enabled
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Left Panel - Player & Chip Management
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Auto Detection Frame
        detect_frame = tk.LabelFrame(left_panel, text="🔍 Auto Detection & Quick Actions",
                                   font=('Arial', 12, 'bold'), padx=10, pady=10)
        detect_frame.pack(fill=tk.X, pady=5)
        
        detect_row1 = tk.Frame(detect_frame)
        detect_row1.pack(fill=tk.X, pady=3)
        
        tk.Button(detect_row1, text="🔍 Auto Detect", command=self.auto_detect,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=3)
        
        tk.Button(detect_row1, text="📊 Load State", command=self.load_state,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=3)
        
        tk.Button(detect_row1, text="💾 Save State", command=self.save_state,
                 bg='#34495e', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=3)
        
        tk.Button(detect_row1, text="🗑️ Clear All", command=self.clear_all,
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                 width=15, height=2).pack(side=tk.LEFT, padx=3)
        
        # Player Management Frame
        player_frame = tk.LabelFrame(left_panel, text="Player & Chip Management",
                                    font=('Arial', 12, 'bold'), padx=10, pady=10)
        player_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Headers
        header_frame = tk.Frame(player_frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(header_frame, text="Seat", font=('Arial', 10, 'bold'), width=5).pack(side=tk.LEFT, padx=2)
        tk.Label(header_frame, text="Status", font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, padx=2)
        tk.Label(header_frame, text="Empty", font=('Arial', 10, 'bold'), width=6).pack(side=tk.LEFT, padx=2)
        tk.Label(header_frame, text="Player Name", font=('Arial', 10, 'bold'), width=20).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Chips", font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(header_frame, text="Delete", font=('Arial', 10, 'bold'), width=6).pack(side=tk.LEFT, padx=2)
        
        # Player rows
        for seat in range(1, 11):
            row_frame = tk.Frame(player_frame)
            row_frame.pack(fill=tk.X, pady=2)
            
            # Seat number
            tk.Label(row_frame, text=f"{seat}", font=('Arial', 11, 'bold'), 
                    width=5).pack(side=tk.LEFT, padx=2)
            
            # Status indicator
            self.seat_status_labels[seat] = tk.Label(row_frame, text="⚫", 
                                                    font=('Arial', 10), width=8)
            self.seat_status_labels[seat].pack(side=tk.LEFT, padx=2)
            
            # Empty checkbox
            self.empty_seats[seat] = tk.BooleanVar(value=False)
            empty_cb = tk.Checkbutton(row_frame, variable=self.empty_seats[seat],
                                     command=lambda s=seat: self.on_empty_changed(s))
            empty_cb.pack(side=tk.LEFT, padx=5)
            
            # Player name entry
            self.player_names[seat] = tk.Entry(row_frame, width=25, font=('Arial', 10))
            self.player_names[seat].pack(side=tk.LEFT, padx=5)
            
            # Chip amount entry
            self.chip_amounts[seat] = tk.Entry(row_frame, width=12, font=('Arial', 10))
            self.chip_amounts[seat].pack(side=tk.LEFT, padx=5)
            
            # Delete checkbox
            self.delete_players[seat] = tk.BooleanVar(value=False)
            delete_cb = tk.Checkbutton(row_frame, variable=self.delete_players[seat])
            delete_cb.pack(side=tk.LEFT, padx=5)
        
        # Right Panel - Controls & Log
        right_panel = tk.Frame(main_container, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        right_panel.pack_propagate(False)
        
        # Speed Control
        speed_frame = tk.LabelFrame(right_panel, text="Speed Settings",
                                  font=('Arial', 11, 'bold'), padx=10, pady=5)
        speed_frame.pack(fill=tk.X, pady=5)
        
        # Preset Speed Buttons
        speed_buttons = tk.Frame(speed_frame)
        speed_buttons.pack(fill=tk.X)
        
        tk.Button(speed_buttons, text="Ultra Fast", command=self.set_ultra_fast,
                 bg='#e74c3c', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(speed_buttons, text="Fast", command=self.set_fast,
                 bg='#f39c12', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(speed_buttons, text="Normal", command=self.set_normal,
                 bg='#3498db', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(speed_buttons, text="Slow", command=self.set_slow,
                 bg='#95a5a6', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        
        # Custom Speed Settings
        tk.Label(speed_frame, text="Custom Speed (seconds):", 
                font=('Arial', 9)).pack(anchor=tk.W, pady=(10, 5))
        
        custom_speed_frame = tk.Frame(speed_frame)
        custom_speed_frame.pack(fill=tk.X, pady=5)
        
        # Create custom speed input fields
        self.custom_speed_entries = {}
        speed_labels = [
            ("Mouse Click:", "mouse_click_delay"),
            ("Keyboard Type:", "keyboard_type_interval"),
            ("Action Delay:", "action_delay"),
            ("Screen Wait:", "screen_wait")
        ]
        
        for i, (label_text, key) in enumerate(speed_labels):
            row = i // 2
            col = i % 2
            
            label_frame = tk.Frame(custom_speed_frame)
            label_frame.grid(row=row, column=col*2, padx=5, pady=2, sticky='w')
            
            tk.Label(label_frame, text=label_text, width=12, 
                    font=('Arial', 9), anchor='w').pack(side=tk.LEFT)
            
            entry = tk.Entry(label_frame, width=8, font=('Arial', 9))
            entry.insert(0, str(self.speed_vars[key].get()))
            entry.pack(side=tk.LEFT)
            self.custom_speed_entries[key] = entry
        
        # Apply Custom Speed Button
        custom_button_frame = tk.Frame(speed_frame)
        custom_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(custom_button_frame, text="Apply Custom", 
                 command=self.apply_custom_speed,
                 bg='#9b59b6', fg='white', width=15).pack(side=tk.LEFT, padx=2)
        tk.Button(custom_button_frame, text="Save Preset", 
                 command=self.save_speed_preset,
                 bg='#16a085', fg='white', width=15).pack(side=tk.LEFT, padx=2)
        tk.Button(custom_button_frame, text="Load Preset", 
                 command=self.load_speed_preset,
                 bg='#2c3e50', fg='white', width=15).pack(side=tk.LEFT, padx=2)
        
        # Action Buttons
        action_frame = tk.LabelFrame(right_panel, text="Actions",
                                   font=('Arial', 11, 'bold'), padx=10, pady=10)
        action_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(action_frame, text="📝 UPDATE NAMES ONLY",
                 command=self.update_names_only,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                 height=2).pack(fill=tk.X, pady=3)
        
        tk.Button(action_frame, text="💰 UPDATE CHIPS ONLY",
                 command=self.update_chips_only,
                 bg='#f39c12', fg='white', font=('Arial', 11, 'bold'),
                 height=2).pack(fill=tk.X, pady=3)
        
        tk.Button(action_frame, text="🔄 UPDATE ALL (Names + Chips)",
                 command=self.update_all,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 height=2).pack(fill=tk.X, pady=3)
        
        tk.Button(action_frame, text="🗑️ DELETE SELECTED",
                 command=self.delete_selected,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 height=2).pack(fill=tk.X, pady=3)
        
        # Status
        self.status_label = tk.Label(action_frame, text="Ready",
                                    bg='green', fg='white', font=('Arial', 11, 'bold'),
                                    height=2)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Log
        log_frame = tk.LabelFrame(right_panel, text="Activity Log",
                                font=('Arial', 11, 'bold'), padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=20, width=45,
                               yscrollcommand=log_scroll.set, font=('Consolas', 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        self.log("System ready. Load data from Google Sheets to start.")
        
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def on_empty_changed(self, seat):
        """Handle empty checkbox change"""
        if self.empty_seats[seat].get():
            self.seat_status_labels[seat].config(text="⚪ Empty")
            self.log(f"Seat {seat} marked as empty")
        else:
            self.seat_status_labels[seat].config(text="🔴 Occupied")
            self.log(f"Seat {seat} marked as occupied")
    
    def auto_load_data(self):
        """Auto-load data from Google Sheets on startup"""
        self.load_google_sheets()
    
    def on_table_selected(self, event=None):
        """Auto-apply table data when table is selected"""
        if self.table_var.get():
            self.current_table = self.table_var.get()  # 현재 테이블 업데이트
            self.current_table_label.config(text=f"▶ {self.table_var.get()} ◀", 
                                           fg='#2ecc71')
            self.apply_table_data()
            # Update button colors to show selection
            self.update_table_button_states()
            # Empty 체크박스는 현재 GFX 상태를 유지 (자동 로드 하지 않음)
            # 최근 사용 목록에 추가
            self.add_to_recent(self.table_var.get())
    
    def prev_table_page(self):
        """Show previous page of tables"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table_buttons()
    
    def next_table_page(self):
        """Show next page of tables"""
        total_tables = len(self.table_data)
        max_pages = (total_tables - 1) // self.tables_per_page
        if self.current_page < max_pages:
            self.current_page += 1
            self.update_table_buttons()
    
    def update_table_buttons(self):
        """Update table buttons based on current page"""
        if not hasattr(self, 'table_data') or not self.table_data:
            return
        
        tables = sorted(list(self.table_data.keys()))
        total_tables = len(tables)
        start_idx = self.current_page * self.tables_per_page
        end_idx = min(start_idx + self.tables_per_page, total_tables)
        
        # First hide all buttons
        for btn in self.quick_table_buttons:
            btn.pack_forget()
        
        # Show buttons for current page
        for i in range(self.tables_per_page):
            table_idx = start_idx + i
            if table_idx < end_idx and i < len(self.quick_table_buttons):
                table_id = tables[table_idx]
                btn = self.quick_table_buttons[i]
                btn.config(text=table_id, state=tk.NORMAL,
                          command=lambda t=table_id: self.quick_select_table(t))
                
                # Determine which row
                if i < 5:
                    btn.pack(side=tk.LEFT, padx=3, in_=self.button_row1)
                else:
                    btn.pack(side=tk.LEFT, padx=3, in_=self.button_row2)
        
        # Update navigation buttons
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED)
        max_pages = (total_tables - 1) // self.tables_per_page if total_tables > 0 else 0
        self.next_btn.config(state=tk.NORMAL if self.current_page < max_pages else tk.DISABLED)
        self.page_label.config(text=f"Page {self.current_page + 1}/{max_pages + 1}")
        
        # Show page info in log
        if total_tables > self.tables_per_page:
            self.log(f"📄 페이지 {self.current_page + 1}/{max_pages + 1} - {total_tables}개 테이블")
    
    def quick_select_table(self, table_id):
        """Quick select a table using button"""
        if hasattr(self, 'table_data') and self.table_data and table_id in self.table_data:
            self.table_var.set(table_id)
            self.on_table_selected()
        else:
            self.log(f"⚠️ Table {table_id} not available in database")
    
    def on_combo_click(self, event=None):
        """Make combobox easier to click by expanding on hover"""
        # Force dropdown to open when clicked anywhere on the widget
        self.table_combo.event_generate('<Down>')
    
    def update_table_button_states(self):
        """Update button colors to show which table is selected"""
        if not hasattr(self, 'quick_table_buttons'):
            return
        current_table = self.table_var.get()
        for btn in self.quick_table_buttons:
            if btn['text'] == current_table:
                btn.config(bg='#2ecc71', relief=tk.SUNKEN)
            else:
                btn.config(bg='#3498db', relief=tk.RAISED)
    
    def load_google_sheets(self):
        """Load data from Google Sheets"""
        def load():
            self.status_label.config(text="Loading...", bg='orange')
            self.log("📥 Loading data from Google Sheets...")
            
            try:
                response = requests.get(self.sheet_url)
                response.raise_for_status()
                
                df = pd.read_csv(StringIO(response.text))
                
                # Group by table
                self.table_data = {}
                for _, row in df.iterrows():
                    table = str(row['Table'])
                    if table not in self.table_data:
                        self.table_data[table] = {}
                    
                    seat = int(row['Seat'])
                    self.table_data[table][seat] = {
                        'player': row['player'],
                        'chips': row['Chips'],
                        'notable': row['Notable']
                    }
                
                # Update table combo
                tables = list(self.table_data.keys())
                self.table_combo['values'] = tables
                
                # Update buttons to show available tables
                self.update_table_buttons()
                
                # Show dropdown if more than 10 tables
                if len(tables) > 10:
                    self.dropdown_frame.pack(pady=5)
                
                # Auto-select first table if available
                if tables:
                    self.table_var.set(tables[0])
                    self.current_table_label.config(text=f"▶ {tables[0]} ◀", 
                                                   fg='#2ecc71')
                
                self.log(f"✅ Loaded {len(tables)} tables from database")
                self.log(f"📊 Tables available: {', '.join(tables)}")
                self.status_label.config(text="Ready", bg='green')
                
            except Exception as e:
                self.log(f"❌ Error loading data: {e}")
                self.status_label.config(text="Error", bg='red')
        
        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()
    
    def reload_tables(self):
        """Reload table data from Google Sheets while preserving current selection"""
        def reload():
            self.status_label.config(text="Reloading...", bg='orange')
            self.log("🔄 Reloading table data from Google Sheets...")
            
            # 현재 선택된 테이블 기억
            current_selection = self.table_var.get()
            
            try:
                response = requests.get(self.sheet_url)
                response.raise_for_status()
                
                df = pd.read_csv(StringIO(response.text))
                
                # Group by table
                self.table_data = {}
                for _, row in df.iterrows():
                    table = str(row['Table'])
                    if table not in self.table_data:
                        self.table_data[table] = {}
                    
                    seat = int(row['Seat'])
                    self.table_data[table][seat] = {
                        'player': row['player'],
                        'chips': row['Chips'],
                        'notable': row['Notable']
                    }
                
                # Update table combo
                tables = list(self.table_data.keys())
                self.table_combo['values'] = tables
                
                # Update buttons to show available tables
                self.update_table_buttons()
                
                # Show dropdown if more than 10 tables
                if len(tables) > 10:
                    self.dropdown_frame.pack(pady=5)
                
                # 이전 선택 테이블이 여전히 존재하면 다시 선택
                if current_selection and current_selection in tables:
                    self.table_var.set(current_selection)
                    self.current_table_label.config(text=f"▶ {current_selection} ◀", 
                                                   fg='#2ecc71')
                    self.log(f"✅ Table {current_selection} reselected")
                    # 데이터 적용
                    self.apply_table_data()
                elif tables:
                    # 이전 선택이 없으면 첫 번째 테이블 선택
                    self.table_var.set(tables[0])
                    self.current_table_label.config(text=f"▶ {tables[0]} ◀", 
                                                   fg='#2ecc71')
                    self.log(f"📋 Previous table not found, selected {tables[0]}")
                
                self.log(f"✅ Reloaded {len(tables)} tables from database")
                self.log(f"📊 Tables available: {', '.join(tables)}")
                self.status_label.config(text="Ready", bg='green')
                
            except Exception as e:
                self.log(f"❌ Error reloading data: {e}")
                self.status_label.config(text="Error", bg='red')
        
        thread = threading.Thread(target=reload)
        thread.daemon = True
        thread.start()
    
    def apply_table_data(self):
        """Apply selected table data to fields"""
        table = self.table_var.get()
        if not table or not hasattr(self, 'table_data') or table not in self.table_data:
            self.log("❌ Please select a valid table or wait for data to load")
            return
        
        self.log(f"📋 Applying data for Table {table}")
        self.current_table = table
        
        # Clear all first
        self.clear_all()
        
        # Apply table data
        table_players = self.table_data[table]
        for seat, info in table_players.items():
            # Mark as occupied
            self.empty_seats[seat].set(False)
            self.seat_status_labels[seat].config(text="🔴 Occupied")
            
            # Set player name
            self.player_names[seat].delete(0, tk.END)
            self.player_names[seat].insert(0, info['player'])
            
            # Set chip amount
            self.chip_amounts[seat].delete(0, tk.END)
            self.chip_amounts[seat].insert(0, str(info['chips']))
            
            self.log(f"  Seat {seat}: {info['player']} - {info['chips']} chips")
        
        # Mark empty seats
        for seat in range(1, 11):
            if seat not in table_players:
                self.empty_seats[seat].set(True)
                self.seat_status_labels[seat].config(text="⚪ Empty")
        
        self.log(f"✅ Table {table} data applied")
    
    def auto_detect(self):
        """Auto detect current player status"""
        def detect():
            self.status_label.config(text="Detecting...", bg='blue')
            self.log("🔍 Starting auto detection...")
            
            for seat in range(1, 11):
                coords = PLAYER_COORDS[seat]
                
                try:
                    # Take screenshot of player area
                    region = pyautogui.screenshot(
                        region=(coords[0]-50, coords[1]-20, 100, 40)
                    )
                    
                    # Analyze colors
                    img_array = np.array(region)
                    red_pixels = np.sum(
                        (img_array[:,:,0] > 180) & 
                        (img_array[:,:,0] < 220) & 
                        (img_array[:,:,1] < 80)
                    )
                    
                    if red_pixels > 500:  # Threshold for occupied
                        self.empty_seats[seat].set(False)
                        self.seat_status_labels[seat].config(text="🔴 Detected")
                        self.log(f"  Seat {seat}: Occupied")
                    else:
                        self.empty_seats[seat].set(True)
                        self.seat_status_labels[seat].config(text="⚪ Empty")
                        self.log(f"  Seat {seat}: Empty")
                        
                except Exception as e:
                    self.log(f"  Seat {seat}: Detection failed - {e}")
                
                time.sleep(0.1)
            
            self.log("✅ Auto detection complete")
            self.status_label.config(text="Ready", bg='green')
        
        thread = threading.Thread(target=detect)
        thread.daemon = True
        thread.start()
    
    def save_state(self):
        """Save current state to file (with dialog)"""
        state = {
            'table': self.current_table or 'unknown',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'seats': {}
        }
        
        for seat in range(1, 11):
            state['seats'][seat] = {
                'empty': self.empty_seats[seat].get(),
                'name': self.player_names[seat].get(),
                'chips': self.chip_amounts[seat].get()
            }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            self.log(f"💾 State saved to {filename}")
    
    def auto_save_state(self):
        """자동으로 현재 상태 저장 (Empty 체크박스는 저장하지 않음 - GFX 상태 유지)"""
        state = {
            'table': self.current_table or 'unknown',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'seats': {}
        }
        
        for seat in range(1, 11):
            # Empty 체크박스 상태는 저장하지 않음 (GFX 상태 유지)
            name = self.player_names[seat].get().strip()
            chips = self.chip_amounts[seat].get().strip()
            
            state['seats'][seat] = {
                # 'empty': 저장하지 않음 - 현재 GFX 상태를 유지
                'name': name,
                'chips': chips
            }
        
        # 자동 저장 파일명
        filename = f"seat_state_{self.current_table or 'default'}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            self.log(f"💾 상태 자동 저장: {filename} (Empty 상태 제외)")
        except Exception as e:
            self.log(f"❌ 자동 저장 실패: {e}")
    
    def load_state(self):
        """Load state from file (with dialog)"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Apply state
                for seat_str, data in state['seats'].items():
                    seat = int(seat_str)
                    self.empty_seats[seat].set(data['empty'])
                    
                    self.player_names[seat].delete(0, tk.END)
                    self.player_names[seat].insert(0, data['name'])
                    
                    self.chip_amounts[seat].delete(0, tk.END)
                    self.chip_amounts[seat].insert(0, data['chips'])
                
                self.log(f"📂 State loaded from {filename}")
            except Exception as e:
                self.log(f"❌ Error loading state: {e}")
    
    def auto_load_state(self):
        """자동으로 저장된 상태 로드 (Empty 체크박스는 변경하지 않음 - GFX 상태 유지)"""
        filename = f"seat_state_{self.current_table or 'default'}.json"
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Apply state (Empty 체크박스는 변경하지 않음)
                for seat_str, data in state['seats'].items():
                    seat = int(seat_str)
                    
                    # Empty 체크박스는 현재 GFX 상태 유지 (변경하지 않음)
                    # 이름과 칩만 로드
                    self.player_names[seat].delete(0, tk.END)
                    self.chip_amounts[seat].delete(0, tk.END)
                    
                    name = data.get('name', '')
                    chips = data.get('chips', '')
                    
                    if name:
                        self.player_names[seat].insert(0, name)
                    if chips:
                        self.chip_amounts[seat].insert(0, chips)
                
                self.log(f"✅ 상태 로드: {filename} (Empty 상태는 GFX 유지)")
                self.log(f"   테이블: {state.get('table', 'unknown')}")
                self.log(f"   저장 시간: {state.get('timestamp', 'unknown')}")
                
            except Exception as e:
                self.log(f"ℹ️ 저장된 상태 없음 또는 로드 실패: {e}")
        else:
            self.log(f"ℹ️ 저장된 상태 파일 없음: {filename}")
    
    def clear_all(self):
        """Clear all fields"""
        for seat in range(1, 11):
            self.empty_seats[seat].set(False)
            self.player_names[seat].delete(0, tk.END)
            self.chip_amounts[seat].delete(0, tk.END)
            self.delete_players[seat].set(False)
            self.seat_status_labels[seat].config(text="⚫")
        self.log("🗑️ All fields cleared")
    
    def set_ultra_fast(self):
        self.speed_vars["mouse_click_delay"].set(0.08)
        self.speed_vars["keyboard_type_interval"].set(0.008)
        self.speed_vars["action_delay"].set(0.15)
        self.speed_vars["screen_wait"].set(0.4)
        pyautogui.PAUSE = 0.08
        self.log("⚡ Speed: Ultra Fast")
        self.update_custom_entries()
    
    def set_fast(self):
        self.speed_vars["mouse_click_delay"].set(0.1)
        self.speed_vars["keyboard_type_interval"].set(0.01)
        self.speed_vars["action_delay"].set(0.2)
        self.speed_vars["screen_wait"].set(0.2)
        pyautogui.PAUSE = 0.1
        self.log("🏃 Speed: Fast")
        self.update_custom_entries()
    
    def set_normal(self):
        self.speed_vars["mouse_click_delay"].set(0.3)
        self.speed_vars["keyboard_type_interval"].set(0.02)
        self.speed_vars["action_delay"].set(0.5)
        self.speed_vars["screen_wait"].set(1.0)
        pyautogui.PAUSE = 0.3
        self.log("🚶 Speed: Normal")
        self.update_custom_entries()
    
    def set_slow(self):
        self.speed_vars["mouse_click_delay"].set(0.5)
        self.speed_vars["keyboard_type_interval"].set(0.05)
        self.speed_vars["action_delay"].set(1.0)
        self.speed_vars["screen_wait"].set(2.0)
        pyautogui.PAUSE = 0.5
        self.log("🐌 Speed: Slow")
        # Update custom speed entries
        self.update_custom_entries()
    
    def apply_custom_speed(self):
        """Apply custom speed settings from input fields"""
        try:
            for key, entry in self.custom_speed_entries.items():
                value = float(entry.get())
                if value < 0:
                    raise ValueError("Speed values must be positive")
                self.speed_vars[key].set(value)
            
            # Set pyautogui.PAUSE to mouse_click_delay
            pyautogui.PAUSE = self.speed_vars["mouse_click_delay"].get()
            
            self.log(f"🎯 Custom Speed Applied:")
            self.log(f"  Mouse Click: {self.speed_vars['mouse_click_delay'].get()}s")
            self.log(f"  Keyboard Type: {self.speed_vars['keyboard_type_interval'].get()}s")
            self.log(f"  Action Delay: {self.speed_vars['action_delay'].get()}s")
            self.log(f"  Screen Wait: {self.speed_vars['screen_wait'].get()}s")
            
        except ValueError as e:
            self.log(f"❌ Invalid speed values: {e}")
            messagebox.showerror("Error", "Please enter valid positive numbers for speed values")
    
    def save_speed_preset(self):
        """Save current speed settings to a file"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="speed_preset.json"
        )
        
        if filename:
            try:
                preset = {
                    "mouse_click_delay": self.speed_vars["mouse_click_delay"].get(),
                    "keyboard_type_interval": self.speed_vars["keyboard_type_interval"].get(),
                    "action_delay": self.speed_vars["action_delay"].get(),
                    "screen_wait": self.speed_vars["screen_wait"].get(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(preset, f, indent=2)
                
                self.log(f"💾 Speed preset saved to {filename}")
                
            except Exception as e:
                self.log(f"❌ Error saving preset: {e}")
                messagebox.showerror("Error", f"Failed to save preset: {e}")
    
    def load_speed_preset(self):
        """Load speed settings from a file"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="speed_preset.json"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    preset = json.load(f)
                
                # Apply loaded settings
                for key in ["mouse_click_delay", "keyboard_type_interval", 
                           "action_delay", "screen_wait"]:
                    if key in preset:
                        self.speed_vars[key].set(preset[key])
                        self.custom_speed_entries[key].delete(0, tk.END)
                        self.custom_speed_entries[key].insert(0, str(preset[key]))
                
                pyautogui.PAUSE = self.speed_vars["mouse_click_delay"].get()
                
                self.log(f"📂 Speed preset loaded from {filename}")
                self.log(f"  Saved: {preset.get('timestamp', 'unknown')}")
                
            except Exception as e:
                self.log(f"❌ Error loading preset: {e}")
                messagebox.showerror("Error", f"Failed to load preset: {e}")
    
    def update_custom_entries(self):
        """Update custom speed entry fields with current values"""
        for key, entry in self.custom_speed_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(self.speed_vars[key].get()))
    
    def update_names_only(self):
        """Update only player names"""
        def run():
            try:
                self.status_label.config(text="Updating Names...", bg='orange')
                self.log("📝 Starting name updates...")
                self.log(f"DEBUG: Speed settings - click: {self.speed_vars['mouse_click_delay'].get()}, type: {self.speed_vars['keyboard_type_interval'].get()}")
                
                for seat in range(1, 11):
                    name = self.player_names[seat].get().strip()
                    is_empty = self.empty_seats[seat].get()
                    
                    self.log(f"DEBUG: Seat {seat} - Name: '{name}', Empty: {is_empty}")
                    
                    # Delete 체크박스도 확인
                    is_delete = self.delete_players[seat].get()
                    
                    # Delete가 체크되어 있으면 무조건 삭제 (Empty 상태 무관)
                    if is_delete:
                        self.log(f"Seat {seat}: Delete ✅ → 삭제 작업 수행")
                        current_status = self.seat_status_labels[seat].cget("text")
                        if "Occupied" in current_status or "Detected" in current_status:
                            self.delete_existing_player(seat)
                            self.empty_seats[seat].set(True)  # 삭제 후 Empty 체크
                        else:
                            self.log(f"  이미 Empty 상태")
                        continue
                    
                    # Empty 체크박스가 체크되어 있고 이름도 없으면 건너뜀
                    if is_empty and not name:
                        self.log(f"Seat {seat}: Empty 체크 + 이름 없음, 건너뜀")
                        continue
                    
                    # Empty 체크박스가 체크되어 있지만 이름이 있으면 신규 등록
                    if is_empty and name:
                        self.log(f"Seat {seat}: Empty 체크 + 이름 있음 → 신규 등록")
                        self.register_new_name(seat, name)
                        # 등록 후 Empty 체크 해제
                        self.empty_seats[seat].set(False)
                        continue
                    
                    # Check current status
                    current_status = self.seat_status_labels[seat].cget("text")
                    self.log(f"DEBUG: Seat {seat} status: '{current_status}'")
                    
                    # 이름이 없으면 항상 삭제 처리 (상태와 무관)
                    if not name:
                        self.log(f"Seat {seat}: 이름 없음 - Delete 체크박스 체크 후 삭제 처리...")
                        # Delete 체크박스 자동 체크
                        self.delete_players[seat].set(True)
                        if "Occupied" in current_status or "Detected" in current_status:
                            self.delete_existing_player(seat)
                            # Empty 상태로 마킹하여 저장
                            self.empty_seats[seat].set(True)
                            self.auto_save_state()  # 상태 자동 저장
                        else:
                            self.log(f"  이미 Empty 상태")
                            self.empty_seats[seat].set(True)
                        continue
                    
                    # 상태 판단: Occupied, Detected는 기존 플레이어, Empty나 초기상태(⚫)는 신규
                    if "Occupied" in current_status or "Detected" in current_status:
                        # Update existing name (5-step process - no clearing)
                        self.log(f"Seat {seat}: Updating existing name to '{name}'")
                        self.update_existing_name(seat, name)
                    elif "Empty" in current_status or current_status == "⚫":
                        # Register new name (3-step process)
                        self.log(f"Seat {seat}: Registering new name '{name}'")
                        self.register_new_name(seat, name)
                    else:
                        # 알 수 없는 상태 - 신규로 처리
                        self.log(f"Seat {seat}: Unknown status '{current_status}' - treating as new")
                        self.register_new_name(seat, name)
                
                self.status_label.config(text="Ready", bg='green')
                self.log("✅ Name updates completed")
                
            except Exception as e:
                self.log(f"❌ ERROR in update_names_only: {e}")
                import traceback
                self.log(f"TRACEBACK: {traceback.format_exc()}")
                self.status_label.config(text="Error", bg='red')
        
        Thread(target=run).start()
    
    def update_chips_only(self):
        """Update only chip amounts"""
        def run():
            self.status_label.config(text="Updating Chips...", bg='orange')
            self.log("💰 Starting chip updates...")
            
            for seat in range(1, 11):
                chips = self.chip_amounts[seat].get().strip()
                is_empty = self.empty_seats[seat].get()
                
                if is_empty:
                    self.log(f"Seat {seat}: Empty, skipping")
                    continue
                
                if not chips:
                    self.log(f"Seat {seat}: No chips, skipping")
                    continue
                
                # Input chips
                self.log(f"Seat {seat}: Inputting chips: {chips}")
                self.input_chips(seat, chips)
            
            self.status_label.config(text="Ready", bg='green')
            self.log("✅ Chip updates completed")
        
        Thread(target=run).start()
    
    def update_all(self):
        """Update names and chips for each player sequentially"""
        def run():
            try:
                self.status_label.config(text="Updating All...", bg='orange')
                self.log("🔄 Starting complete update...")
                self.log("Processing each player: Name → Chips → Next player")
                
                # Process each seat one by one (name then chips)
                for seat in range(1, 11):
                    name = self.player_names[seat].get().strip()
                    chips = self.chip_amounts[seat].get().strip()
                    is_empty = self.empty_seats[seat].get()
                    is_delete = self.delete_players[seat].get()
                    
                    # Delete가 체크되어 있으면 무조건 삭제 (Empty 상태 무관)
                    if is_delete:
                        self.log(f"Seat {seat}: Delete ✅ → 삭제 작업 수행")
                        current_status = self.seat_status_labels[seat].cget("text")
                        if "Occupied" in current_status or "Detected" in current_status:
                            self.delete_existing_player(seat)
                            self.empty_seats[seat].set(True)  # 삭제 후 Empty 체크
                        else:
                            self.log(f"  이미 Empty 상태")
                        continue
                    
                    # Empty 체크 + 이름 없음 = 건너뜀
                    if is_empty and not name:
                        self.log(f"Seat {seat}: Empty 체크 + 이름 없음, 건너뜀")
                        continue
                    
                    # Empty 체크 + 이름 있음 = 신규 등록 필요
                    if is_empty and name:
                        self.log(f"Seat {seat}: Empty 체크 + 이름 있음 → 신규 등록")
                        self.register_new_name(seat, name)
                        if chips:
                            self.input_chips(seat, chips)
                        self.empty_seats[seat].set(False)  # Empty 체크 해제
                        continue
                    
                    self.log(f"\n--- Processing Seat {seat} ---")
                    
                    # Step 1: Check current status
                    current_status = self.seat_status_labels[seat].cget("text")
                    
                    # 이름이 없으면 항상 삭제 처리 (상태와 무관)
                    if not name:
                        self.log(f"Seat {seat}: 이름 없음 - Delete 체크박스 체크 후 삭제 처리...")
                        # Delete 체크박스 자동 체크
                        self.delete_players[seat].set(True)
                        if "Occupied" in current_status or "Detected" in current_status:
                            self.delete_existing_player(seat)
                            # Empty 상태로 마킹하여 저장
                            self.empty_seats[seat].set(True)
                            self.auto_save_state()  # 상태 자동 저장
                        else:
                            self.log(f"  이미 Empty 상태")
                            # Empty 상태 확인 및 저장
                            if not self.empty_seats[seat].get():
                                self.empty_seats[seat].set(True)
                                self.auto_save_state()  # 상태 자동 저장
                        continue
                    
                    # 상태 판단: Occupied, Detected는 기존 플레이어, Empty나 초기상태(⚫)는 신규
                    if "Occupied" in current_status or "Detected" in current_status:
                        self.log(f"Seat {seat}: Updating existing name to '{name}'")
                        self.update_existing_name(seat, name)
                    elif "Empty" in current_status or current_status == "⚫":
                        self.log(f"Seat {seat}: Registering new name '{name}'")
                        self.register_new_name(seat, name)
                    else:
                        # 알 수 없는 상태 - 신규로 처리
                        self.log(f"Seat {seat}: Unknown status '{current_status}' - treating as new")
                        self.register_new_name(seat, name)
                    
                    # Step 2: Input chips for this player (if chips value exists)
                    if chips:
                        self.log(f"Seat {seat}: Inputting chips: {chips}")
                        self.input_chips(seat, chips)
                    else:
                        self.log(f"Seat {seat}: No chips to input")
                    
                    self.log(f"Seat {seat}: ✅ Complete")
                
                self.status_label.config(text="Ready", bg='green')
                self.log("\n✅ All updates completed")
                
            except Exception as e:
                self.log(f"❌ ERROR in update_all: {e}")
                import traceback
                self.log(f"TRACEBACK: {traceback.format_exc()}")
                self.status_label.config(text="Error", bg='red')
        
        Thread(target=run).start()
    
    def update_existing_name(self, seat, new_name):
        """Update existing player name (5-step process - clearing removed)"""
        try:
            coords = PLAYER_COORDS[seat]
            self.log(f"DEBUG: update_existing_name - Seat {seat} coords: {coords}")
            
            # Step 1: Click player on main screen
            self.log(f"  Step 1: Clicking player at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 2: Click name field in sub screen
            self.log(f"  Step 2: Clicking name field at {SUB_NAME_FIELD}")
            pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 3: Type new name (clearing step removed)
            self.log(f"  Step 3: Typing new name: '{new_name}'")
            pyautogui.typewrite(new_name, interval=self.speed_vars["keyboard_type_interval"].get())
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 4: Press Enter
            self.log(f"  Step 4: Pressing Enter")
            pyautogui.press('enter')
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 5: Click Complete button
            self.log(f"  Step 5: Clicking Complete at {COMPLETE_BUTTON}")
            pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
            time.sleep(self.speed_vars["screen_wait"].get())
            
            self.log(f"  ✅ Successfully updated seat {seat}")
            
        except Exception as e:
            self.log(f"❌ Error updating seat {seat}: {e}")
            import traceback
            self.log(f"TRACEBACK: {traceback.format_exc()}")
    
    def register_new_name(self, seat, name):
        """Register new player name (3-step process)"""
        try:
            coords = PLAYER_COORDS[seat]
            self.log(f"DEBUG: register_new_name - Seat {seat} coords: {coords}")
            
            # Step 1: Click player position
            self.log(f"  Step 1: Clicking player at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 2: Type name
            self.log(f"  Step 2: Typing name: '{name}'")
            pyautogui.typewrite(name, interval=self.speed_vars["keyboard_type_interval"].get())
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 3: Press Enter
            self.log(f"  Step 3: Pressing Enter")
            pyautogui.press('enter')
            time.sleep(self.speed_vars["screen_wait"].get())
            
            self.log(f"  ✅ Successfully registered seat {seat}")
            
        except Exception as e:
            self.log(f"❌ Error registering seat {seat}: {e}")
            import traceback
            self.log(f"TRACEBACK: {traceback.format_exc()}")
    
    def input_chips(self, seat, chips):
        """Input chip amount for a seat"""
        try:
            coords = CHIP_COORDS[seat]
            self.log(f"  Inputting chips for seat {seat} at {coords}")
            
            # Step 1: Click chip input field
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["mouse_click_delay"].get())
            
            # Step 2: Type new chip amount (no need to clear - field auto-selects)
            pyautogui.typewrite(str(chips), interval=self.speed_vars["keyboard_type_interval"].get())
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 3: Press Enter to confirm
            pyautogui.press('enter')
            time.sleep(self.speed_vars["action_delay"].get())
            
            self.log(f"  ✓ Chips input complete for seat {seat}")
            
        except Exception as e:
            self.log(f"❌ Error inputting chips for seat {seat}: {e}")
    
    def delete_selected(self):
        """Delete selected players"""
        def run():
            self.status_label.config(text="Deleting...", bg='orange')
            self.log("🗑️ Starting deletions...")
            
            for seat in range(1, 11):
                if self.delete_players[seat].get():
                    self.log(f"Seat {seat}: Deleting player")
                    self.delete_player(seat)
            
            self.status_label.config(text="Ready", bg='green')
            self.log("✅ Deletions completed")
        
        Thread(target=run).start()
    
    def delete_player(self, seat):
        """Delete a player from a seat (2단계 간소화)"""
        try:
            coords = PLAYER_COORDS[seat]
            
            # Step 1: Click player
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 2: Click Delete button
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(self.speed_vars["screen_wait"].get())
            
            self.log(f"✓ Seat {seat}: 삭제 완료")
            
        except Exception as e:
            self.log(f"❌ Error deleting seat {seat}: {e}")
    
    def delete_existing_player(self, seat):
        """자동으로 이름이 없는 기존 플레이어 삭제 (2단계 간소화)"""
        try:
            coords = PLAYER_COORDS[seat]
            
            self.log(f"  Step 1: 플레이어 위치 클릭 ({coords[0]}, {coords[1]})")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            self.log(f"  Step 2: Delete 버튼 클릭 ({DELETE_BUTTON[0]}, {DELETE_BUTTON[1]})")
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(self.speed_vars["screen_wait"].get())
            
            self.log(f"  ✓ Seat {seat}: 플레이어 삭제 완료 (2단계)")
            
            # UI 상태 업데이트
            self.seat_status_labels[seat].config(text="⚪ Empty")
            # Empty 체크박스 자동 체크
            self.empty_seats[seat].set(True)
            
        except Exception as e:
            self.log(f"❌ Seat {seat} 삭제 중 오류: {e}")
    
    def search_tables(self, event=None):
        """Search for tables by name"""
        if not hasattr(self, 'table_data') or not self.table_data:
            return
        
        search_text = self.search_var.get().upper()
        if not search_text:
            # 검색어가 없으면 모든 테이블 표시
            self.update_table_buttons()
            return
        
        # 검색 결과 찾기
        matching_tables = []
        for table in self.table_data.keys():
            if search_text in table.upper():
                matching_tables.append(table)
        
        if matching_tables:
            self.log(f"🔍 검색 결과: {len(matching_tables)}개 테이블 찾음")
            # 검색 결과로 버튼 업데이트
            self.update_search_results(matching_tables)
        else:
            self.log(f"❌ '{search_text}'와 일치하는 테이블 없음")
    
    def update_search_results(self, tables):
        """Update buttons to show search results"""
        # Hide all buttons first
        for btn in self.quick_table_buttons:
            btn.pack_forget()
        
        # Show matching tables
        for i, table_id in enumerate(tables[:10]):  # 최대 10개만 표시
            if i < len(self.quick_table_buttons):
                btn = self.quick_table_buttons[i]
                btn.config(text=table_id, state=tk.NORMAL,
                          command=lambda t=table_id: self.quick_select_table(t))
                
                # Determine which row
                if i < 5:
                    btn.pack(side=tk.LEFT, padx=3, in_=btn.master)
                else:
                    btn.pack(side=tk.LEFT, padx=3, in_=btn.master)
        
        # Update dropdown with search results
        self.table_combo['values'] = tables
    
    def show_favorites(self):
        """Show favorite tables"""
        if not self.favorite_tables:
            self.log("⭐ 즐겨찾기 테이블이 없습니다")
            # 즐겨찾기 추가 옵션 제공
            if hasattr(self, 'current_table') and self.current_table:
                self.add_to_favorites(self.current_table)
            return
        
        self.log(f"⭐ 즐겨찾기 테이블: {', '.join(self.favorite_tables)}")
        self.update_search_results(self.favorite_tables)
    
    def add_to_favorites(self, table_id):
        """Add table to favorites"""
        if table_id not in self.favorite_tables:
            self.favorite_tables.append(table_id)
            self.log(f"⭐ {table_id}를 즐겨찾기에 추가했습니다")
            # 파일에 저장
            self.save_favorites()
        else:
            # 이미 있으면 제거
            self.favorite_tables.remove(table_id)
            self.log(f"⭐ {table_id}를 즐겨찾기에서 제거했습니다")
            self.save_favorites()
    
    def save_favorites(self):
        """Save favorites to file"""
        try:
            import json
            with open('favorite_tables.json', 'w') as f:
                json.dump(self.favorite_tables, f)
        except Exception as e:
            self.log(f"❌ 즐겨찾기 저장 실패: {e}")
    
    def load_favorites(self):
        """Load favorites from file"""
        try:
            import json
            with open('favorite_tables.json', 'r') as f:
                self.favorite_tables = json.load(f)
        except:
            self.favorite_tables = []
    
    def show_recent(self):
        """Show recently used tables"""
        if not self.recent_tables:
            self.log("🕒 최근 사용한 테이블이 없습니다")
            return
        
        self.log(f"🕒 최근 테이블: {', '.join(self.recent_tables[:10])}")
        self.update_search_results(self.recent_tables[:10])
    
    def add_to_recent(self, table_id):
        """Add table to recent list"""
        # 중복 제거
        if table_id in self.recent_tables:
            self.recent_tables.remove(table_id)
        
        # 맨 앞에 추가
        self.recent_tables.insert(0, table_id)
        
        # 최대 20개만 유지
        if len(self.recent_tables) > 20:
            self.recent_tables = self.recent_tables[:20]
        
        # 파일에 저장
        self.save_recent()
    
    def save_recent(self):
        """Save recent tables to file"""
        try:
            import json
            with open('recent_tables.json', 'w') as f:
                json.dump(self.recent_tables, f)
        except:
            pass
    
    def load_recent(self):
        """Load recent tables from file"""
        try:
            import json
            with open('recent_tables.json', 'r') as f:
                self.recent_tables = json.load(f)
        except:
            self.recent_tables = []
    
    def show_groups(self):
        """Show table groups dialog"""
        # 그룹 다이얼로그 생성
        group_window = tk.Toplevel(self.root)
        group_window.title("테이블 그룹 관리")
        group_window.geometry("400x300")
        
        tk.Label(group_window, text="테이블 그룹", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # 그룹 리스트
        group_frame = tk.Frame(group_window)
        group_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 스테이크별 그룹 자동 생성
        if hasattr(self, 'table_data') and self.table_data:
            self.auto_create_groups()
        
        # 그룹 버튼 생성
        for group_name, tables in self.table_groups.items():
            btn = tk.Button(group_frame, text=f"{group_name} ({len(tables)}개)",
                           command=lambda g=group_name: self.select_group(g),
                           bg='#3498db', fg='white', font=('Arial', 10),
                           width=30, height=2)
            btn.pack(pady=5)
        
        tk.Button(group_window, text="닫기", 
                 command=group_window.destroy,
                 bg='#e74c3c', fg='white').pack(pady=10)
    
    def auto_create_groups(self):
        """Automatically create groups based on table names"""
        self.table_groups = {}
        
        # 테이블 수에 따라 동적으로 그룹 생성
        total_tables = len(self.table_data)
        
        if total_tables <= 20:
            # 20개 이하: 단순 그룹
            self.table_groups = {
                "All Tables": list(self.table_data.keys())
            }
        elif total_tables <= 50:
            # 50개 이하: 10개씩 그룹
            tables = sorted(list(self.table_data.keys()))
            for i in range(0, total_tables, 10):
                group_name = f"Tables {i+1}-{min(i+10, total_tables)}"
                self.table_groups[group_name] = tables[i:i+10]
        else:
            # 50개 초과: 범위별 그룹 (1-30, 31-60, 61-90, 91+)
            tables = sorted(list(self.table_data.keys()))
            ranges = [
                ("Tables 1-30", 0, 30),
                ("Tables 31-60", 30, 60),
                ("Tables 61-90", 60, 90),
                ("Tables 91-120", 90, 120),
                ("Tables 121+", 120, 9999)
            ]
            
            for group_name, start, end in ranges:
                group_tables = []
                for i, table in enumerate(tables):
                    if start <= i < min(end, total_tables):
                        group_tables.append(table)
                if group_tables:
                    self.table_groups[group_name] = group_tables
        
        # 빈 그룹 제거
        self.table_groups = {k: v for k, v in self.table_groups.items() if v}
    
    def select_group(self, group_name):
        """Select a group of tables"""
        if group_name in self.table_groups:
            tables = self.table_groups[group_name]
            self.log(f"📊 그룹 '{group_name}' 선택: {len(tables)}개 테이블")
            self.update_search_results(tables)
    
    def toggle_favorite(self):
        """Toggle favorite status for current table"""
        if hasattr(self, 'current_table') and self.current_table:
            self.add_to_favorites(self.current_table)
            # 즐겨찾기 버튼 업데이트는 on_table_selected에서 처리
    
    def generate_test_tables(self, count=100):
        """Generate test tables for demonstration (100+ tables)"""
        self.table_data = {}
        for i in range(1, count + 1):
            table_id = f"T{i:03d}"  # T001, T002, ... T100
            self.table_data[table_id] = {}
            
            # 일부 좌석에만 플레이어 추가 (시뮬레이션)
            import random
            seats_occupied = random.randint(3, 8)
            for seat in random.sample(range(1, 11), seats_occupied):
                self.table_data[table_id][seat] = {
                    'player': f"Player_{seat}",
                    'chips': random.randint(100, 10000),
                    'notable': ""
                }
        
        # Update UI with generated tables
        tables = list(self.table_data.keys())
        self.table_combo['values'] = tables
        self.update_table_buttons()
        
        # Show dropdown for many tables
        if len(tables) > 10:
            self.dropdown_frame.pack(pady=5)
        
        self.log(f"✅ 테스트용 {count}개 테이블 생성 완료")
        self.log(f"📊 페이지네이션 테스트: {(count-1)//10 + 1}페이지")


def main():
    root = tk.Tk()
    app = IntegratedActionTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()