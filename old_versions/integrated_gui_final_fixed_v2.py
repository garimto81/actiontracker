"""
Integrated Action Tracker GUI - Enhanced Version with Auto-Refresh
플레이어 이름, 칩, 자동 감지 통합 GUI - 자동 새로고침 기능 추가
Version 2.0 - Added periodic auto-refresh from Google Sheets
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
        self.root.title("Action Tracker - Complete Management System v2.0")
        self.root.geometry("1400x900")
        
        # Google Sheets URL - 캐시 제어 파라미터 추가
        self.sheet_url_base = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDY_i4330JANAjIz4sMncdJdRHsOkfUCjQusHTGQk2tykrhA4d09LeIp3XRbLd8hkN6SgSB47k_nux/pub?gid=998576925&single=true&output=csv"
        
        # Data storage
        self.table_data = {}
        self.current_table = None
        self.last_update_time = None
        
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
        
        # Auto-refresh settings
        self.refresh_interval = 30000  # 30 seconds in milliseconds
        self.auto_refresh_enabled = True
        self.refresh_timer = None
        
        # Recent and favorite tables
        self.recent_tables = []
        self.favorite_tables = []
        self.load_recent_tables()
        self.load_favorites()
        
        pyautogui.PAUSE = 0.3
        
        self.create_widgets()
        
        # Auto-load data from Google Sheets on startup
        self.root.after(500, self.auto_load_data)
        
    def get_sheet_url_with_no_cache(self):
        """Get Google Sheets URL with cache-busting parameter"""
        import random
        timestamp = int(time.time() * 1000)
        random_num = random.randint(1000, 9999)
        return f"{self.sheet_url_base}&nocache={timestamp}&r={random_num}"
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Top Frame - Title and Table Selection (increased height for table selection)
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=180)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        title_container = tk.Frame(top_frame, bg='#2c3e50')
        title_container.pack(expand=True)
        
        tk.Label(title_container, text="ACTION TRACKER COMPLETE SYSTEM v2.0", 
                font=('Arial', 22, 'bold'), fg='white', bg='#2c3e50').pack(pady=10)
        
        # Add last update time label
        self.update_time_label = tk.Label(title_container, text="Last Update: Never", 
                                         font=('Arial', 10), fg='#95a5a6', bg='#2c3e50')
        self.update_time_label.pack()
        
        # Auto-refresh status label
        self.auto_refresh_label = tk.Label(title_container, text="🔄 Auto-refresh: ON (30s)", 
                                          font=('Arial', 10, 'bold'), fg='#2ecc71', bg='#2c3e50')
        self.auto_refresh_label.pack()
        
        # Table selection frame - Cleaner design
        table_frame = tk.Frame(title_container, bg='#2c3e50')
        table_frame.pack(pady=(10, 5))
        
        # Main table selection container
        table_select_frame = tk.Frame(table_frame, bg='#2c3e50')
        table_select_frame.pack(pady=(5, 10), padx=20)
        
        # Table selection label
        tk.Label(table_select_frame, text="Select Table:", 
                font=('Arial', 12), fg='white', bg='#2c3e50').pack(side=tk.LEFT, padx=5)
        
        # Table dropdown
        self.table_var = tk.StringVar()
        self.table_combo = ttk.Combobox(table_select_frame, textvariable=self.table_var, 
                                       state='readonly', width=15, font=('Arial', 11))
        self.table_combo.pack(side=tk.LEFT, padx=5)
        self.table_combo.bind('<<ComboboxSelected>>', self.on_table_selected)
        
        # Apply button
        tk.Button(table_select_frame, text="APPLY", 
                 command=self.apply_table_data,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Load data button - FORCE REFRESH 기능 추가
        tk.Button(table_select_frame, text="LOAD DATA (Force)", 
                 command=self.force_refresh_data,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Reload button for refreshing table data
        tk.Button(table_select_frame, text="RELOAD", 
                 command=self.reload_tables,
                 bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Auto-refresh toggle button
        tk.Button(table_select_frame, text="AUTO-REFRESH", 
                 command=self.toggle_auto_refresh,
                 bg='#e67e22', fg='white', font=('Arial', 11, 'bold'),
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Current table display
        self.current_table_label = tk.Label(table_select_frame, text="No Table Selected", 
                                           font=('Arial', 12, 'bold'), fg='#e74c3c', bg='#2c3e50')
        self.current_table_label.pack(side=tk.LEFT, padx=20)
        
        # Quick access table buttons frame
        self.table_buttons_frame = tk.Frame(top_frame, bg='#2c3e50')
        self.table_buttons_frame.pack(pady=(0, 10))
        
        # This will be populated with quick access buttons for first 10 tables
        self.table_buttons = []
        
        # Dropdown frame for additional controls (hidden by default)
        self.dropdown_frame = tk.Frame(table_frame, bg='#2c3e50')
        # Not packed initially - will be shown when there are many tables
        
        # Add pagination controls for large number of tables
        pagination_frame = tk.Frame(self.dropdown_frame, bg='#2c3e50')
        pagination_frame.pack()
        
        self.page_label = tk.Label(pagination_frame, text="Page 1", 
                                  font=('Arial', 10), fg='white', bg='#2c3e50')
        self.page_label.pack(side=tk.LEFT, padx=10)
        
        tk.Button(pagination_frame, text="◀", command=self.prev_page,
                 bg='#34495e', fg='white', width=3).pack(side=tk.LEFT, padx=2)
        tk.Button(pagination_frame, text="▶", command=self.next_page,
                 bg='#34495e', fg='white', width=3).pack(side=tk.LEFT, padx=2)
        
        self.current_page = 0
        
        # Search frame for finding specific tables
        search_frame = tk.Frame(self.dropdown_frame, bg='#2c3e50')
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Search:", 
                font=('Arial', 10), fg='white', bg='#2c3e50').pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search_changed)
        
        # Main content area with scrollbar
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas and scrollbar for scrollable content
        canvas = tk.Canvas(main_container)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Player table frame
        table_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Headers
        headers_frame = tk.Frame(table_frame, bg='#34495e')
        headers_frame.pack(fill=tk.X)
        
        tk.Label(headers_frame, text="Seat", width=8, bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
        tk.Label(headers_frame, text="Empty?", width=8, bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
        tk.Label(headers_frame, text="Player Name", width=20, bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
        tk.Label(headers_frame, text="Chips", width=15, bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
        tk.Label(headers_frame, text="Delete?", width=8, bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
        tk.Label(headers_frame, text="Status", width=15, bg='#34495e', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
        
        # Player rows
        for seat in range(1, 11):
            row_frame = tk.Frame(table_frame, bg='white' if seat % 2 == 0 else '#ecf0f1')
            row_frame.pack(fill=tk.X)
            
            # Seat number
            tk.Label(row_frame, text=f"Seat {seat}", width=8, 
                    font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=1)
            
            # Empty checkbox
            empty_var = tk.BooleanVar(value=True)
            self.empty_seats[seat] = empty_var
            tk.Checkbutton(row_frame, variable=empty_var, width=6).pack(side=tk.LEFT, padx=1)
            
            # Player name
            name_entry = tk.Entry(row_frame, width=20, font=('Arial', 10))
            name_entry.pack(side=tk.LEFT, padx=1)
            self.player_names[seat] = name_entry
            
            # Chip amount
            chip_entry = tk.Entry(row_frame, width=15, font=('Arial', 10))
            chip_entry.pack(side=tk.LEFT, padx=1)
            self.chip_amounts[seat] = chip_entry
            
            # Delete checkbox
            delete_var = tk.BooleanVar(value=False)
            self.delete_players[seat] = delete_var
            tk.Checkbutton(row_frame, variable=delete_var, width=6).pack(side=tk.LEFT, padx=1)
            
            # Status label
            status_label = tk.Label(row_frame, text="⚪ Empty", width=15, font=('Arial', 10))
            status_label.pack(side=tk.LEFT, padx=1)
            self.seat_status_labels[seat] = status_label
        
        # Control panel
        control_frame = tk.Frame(scrollable_frame, bg='#2c3e50', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Action buttons
        button_frame = tk.Frame(control_frame, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="PROCESS NAMES", 
                 command=self.process_names,
                 bg='#2ecc71', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="PROCESS CHIPS", 
                 command=self.process_chips,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="AUTO DETECT", 
                 command=self.auto_detect,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        # Speed control frame
        speed_frame = tk.Frame(control_frame, bg='#2c3e50')
        speed_frame.pack(pady=10)
        
        tk.Label(speed_frame, text="SPEED CONTROL", bg='#2c3e50', fg='white',
                font=('Arial', 12, 'bold')).pack()
        
        # Speed presets
        preset_frame = tk.Frame(speed_frame, bg='#2c3e50')
        preset_frame.pack(pady=5)
        
        tk.Button(preset_frame, text="Ultra Fast", 
                 command=lambda: self.set_speed_preset('ultra_fast'),
                 bg='#e74c3c', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="Fast", 
                 command=lambda: self.set_speed_preset('fast'),
                 bg='#f39c12', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="Normal", 
                 command=lambda: self.set_speed_preset('normal'),
                 bg='#3498db', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="Slow", 
                 command=lambda: self.set_speed_preset('slow'),
                 bg='#95a5a6', fg='white', width=10).pack(side=tk.LEFT, padx=2)
        
        # Log display
        log_frame = tk.Frame(scrollable_frame, bg='black', relief=tk.RAISED, bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(log_frame, text="ACTIVITY LOG", bg='black', fg='lime',
                font=('Courier', 12, 'bold')).pack()
        
        self.log_text = tk.Text(log_frame, height=10, bg='black', fg='lime',
                               font=('Courier', 10), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#2c3e50', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Ready", bg='green', fg='white',
                                    font=('Arial', 10, 'bold'), padx=10)
        self.status_label.pack(side=tk.LEFT)
        
        # State management buttons
        tk.Button(status_frame, text="Save State", command=self.save_state,
                 bg='#3498db', fg='white').pack(side=tk.RIGHT, padx=5)
        tk.Button(status_frame, text="Load State", command=self.load_state,
                 bg='#9b59b6', fg='white').pack(side=tk.RIGHT, padx=5)
    
    def auto_load_data(self):
        """Auto-load data from Google Sheets on startup"""
        self.log("🚀 Initializing auto-load from Google Sheets...")
        self.load_google_sheets()
        
        # Set up periodic refresh every 30 seconds
        self.schedule_periodic_refresh()
    
    def schedule_periodic_refresh(self):
        """Schedule periodic refresh of Google Sheets data"""
        if self.auto_refresh_enabled:
            self.log("⏰ Next auto-refresh scheduled in 30 seconds...")
            self.refresh_timer = self.root.after(self.refresh_interval, self.periodic_refresh)
    
    def periodic_refresh(self):
        """Perform periodic refresh of data"""
        if self.auto_refresh_enabled:
            self.log("🔄 Auto-refreshing data from Google Sheets...")
            self.reload_tables()
            # Schedule next refresh
            self.schedule_periodic_refresh()
    
    def toggle_auto_refresh(self):
        """Toggle automatic refresh on/off"""
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        if self.auto_refresh_enabled:
            self.log("✅ Auto-refresh enabled (every 30 seconds)")
            self.auto_refresh_label.config(text="🔄 Auto-refresh: ON (30s)", fg='#2ecc71')
            self.schedule_periodic_refresh()
        else:
            self.log("❌ Auto-refresh disabled")
            self.auto_refresh_label.config(text="🔄 Auto-refresh: OFF", fg='#e74c3c')
            if self.refresh_timer:
                self.root.after_cancel(self.refresh_timer)
                self.refresh_timer = None
    
    def force_refresh_data(self):
        """Force refresh data from Google Sheets with cache bypass"""
        def force_load():
            self.status_label.config(text="Force Refreshing...", bg='red')
            self.log("🔄 Force refreshing data from Google Sheets (bypassing cache)...")
            
            try:
                # Clear existing data first
                self.table_data = {}
                
                # Use cache-busting URL
                url = self.get_sheet_url_with_no_cache()
                
                # Add headers to prevent caching
                headers = {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                # Clear response cache
                response.connection.close()
                
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
                
                # Update last update time
                self.last_update_time = datetime.now()
                self.update_time_label.config(text=f"Last Update: {self.last_update_time.strftime('%H:%M:%S')}")
                
                self.log(f"✅ Force refresh complete! Loaded {len(tables)} tables")
                self.log(f"📊 Tables available: {', '.join(tables)}")
                self.status_label.config(text="Ready", bg='green')
                
                # Auto-apply if current table is selected
                if self.current_table and self.current_table in tables:
                    self.apply_table_data()
                    self.log(f"🔄 Re-applied data for table {self.current_table}")
                
            except Exception as e:
                self.log(f"❌ Error during force refresh: {e}")
                self.status_label.config(text="Error", bg='red')
        
        thread = threading.Thread(target=force_load)
        thread.daemon = True
        thread.start()
    
    def load_google_sheets(self):
        """Load data from Google Sheets with cache bypass"""
        def load():
            self.status_label.config(text="Loading...", bg='orange')
            self.log("📥 Loading data from Google Sheets...")
            
            try:
                # Use cache-busting URL
                url = self.get_sheet_url_with_no_cache()
                
                # Add headers to prevent caching
                headers = {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                response = requests.get(url, headers=headers)
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
                
                # Update last update time
                self.last_update_time = datetime.now()
                self.update_time_label.config(text=f"Last Update: {self.last_update_time.strftime('%H:%M:%S')}")
                
                self.log(f"✅ Loaded {len(tables)} tables from database")
                self.log(f"📊 Tables available: {', '.join(tables[:5])}{'...' if len(tables) > 5 else ''}")
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
                # Use cache-busting URL
                url = self.get_sheet_url_with_no_cache()
                
                # Add headers to prevent caching
                headers = {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                response = requests.get(url, headers=headers)
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
                    # 데이터도 다시 적용
                    self.apply_table_data()
                    self.log(f"🔄 Reloaded and applied data for {current_selection}")
                
                # Update last update time
                self.last_update_time = datetime.now()
                self.update_time_label.config(text=f"Last Update: {self.last_update_time.strftime('%H:%M:%S')}")
                
                self.log(f"✅ Reloaded {len(tables)} tables from database")
                self.status_label.config(text="Ready", bg='green')
                
            except Exception as e:
                self.log(f"❌ Error reloading data: {e}")
                self.status_label.config(text="Error", bg='red')
        
        thread = threading.Thread(target=reload)
        thread.daemon = True
        thread.start()
    
    def log(self, message):
        """Add message to log display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def on_table_selected(self, event=None):
        """Handle table selection from dropdown"""
        selected = self.table_var.get()
        if selected:
            self.current_table = selected
            self.current_table_label.config(text=f"▶ {selected} ◀", fg='#2ecc71')
            self.log(f"📋 Table {selected} selected")
            
            # Add to recent tables
            self.add_to_recent(selected)
    
    def apply_table_data(self):
        """Apply selected table data to the form"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Please select a table first")
            return
        
        if self.current_table not in self.table_data:
            messagebox.showerror("Error", f"Table {self.current_table} not found in data")
            return
        
        # Clear all fields first
        for seat in range(1, 11):
            self.empty_seats[seat].set(True)
            self.player_names[seat].delete(0, tk.END)
            self.chip_amounts[seat].delete(0, tk.END)
            self.delete_players[seat].set(False)
            self.seat_status_labels[seat].config(text="⚪ Empty")
        
        # Apply table data
        table_players = self.table_data[self.current_table]
        self.log(f"📝 Applying data for table {self.current_table}:")
        
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
        
        self.log(f"✅ Table {self.current_table} data applied")
    
    def process_names(self):
        """Process player names"""
        self.log("🚀 Starting name processing...")
        # Implementation would go here
        messagebox.showinfo("Process Names", "Name processing started")
    
    def process_chips(self):
        """Process chip amounts"""
        self.log("💰 Starting chip processing...")
        # Implementation would go here
        messagebox.showinfo("Process Chips", "Chip processing started")
    
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
    
    def set_speed_preset(self, preset):
        """Set speed values based on preset"""
        presets = {
            'ultra_fast': {'mouse_click_delay': 0.08, 'keyboard_type_interval': 0.008, 
                          'action_delay': 0.1, 'screen_wait': 0.3},
            'fast': {'mouse_click_delay': 0.15, 'keyboard_type_interval': 0.012, 
                    'action_delay': 0.2, 'screen_wait': 0.5},
            'normal': {'mouse_click_delay': 0.3, 'keyboard_type_interval': 0.02, 
                      'action_delay': 0.5, 'screen_wait': 1.0},
            'slow': {'mouse_click_delay': 0.5, 'keyboard_type_interval': 0.05, 
                    'action_delay': 0.8, 'screen_wait': 1.5}
        }
        
        if preset in presets:
            for key, value in presets[preset].items():
                self.speed_vars[key].set(value)
            self.log(f"⚡ Speed set to {preset}")
    
    def save_state(self):
        """Save current state to file"""
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
    
    def load_state(self):
        """Load state from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Apply loaded state
                for seat in range(1, 11):
                    if str(seat) in state['seats']:
                        seat_data = state['seats'][str(seat)]
                        self.empty_seats[seat].set(seat_data.get('empty', True))
                        
                        self.player_names[seat].delete(0, tk.END)
                        self.player_names[seat].insert(0, seat_data.get('name', ''))
                        
                        self.chip_amounts[seat].delete(0, tk.END)
                        self.chip_amounts[seat].insert(0, seat_data.get('chips', ''))
                        
                        if seat_data.get('empty'):
                            self.seat_status_labels[seat].config(text="⚪ Empty")
                        else:
                            self.seat_status_labels[seat].config(text="🔴 Occupied")
                
                self.log(f"📂 State loaded from {filename}")
                self.log(f"  Table: {state.get('table', 'unknown')}")
                self.log(f"  Saved at: {state.get('timestamp', 'unknown')}")
                
            except Exception as e:
                self.log(f"❌ Error loading state: {e}")
                messagebox.showerror("Error", f"Failed to load state: {e}")
    
    def update_table_buttons(self):
        """Update quick access table buttons"""
        # Clear existing buttons
        for btn in self.table_buttons:
            btn.destroy()
        self.table_buttons = []
        
        # Create buttons for first 10 tables (or less)
        tables = list(self.table_data.keys())[:10]
        for i, table in enumerate(tables):
            if i < 5:
                row = 0
                col = i
            else:
                row = 1
                col = i - 5
            
            btn = tk.Button(self.table_buttons_frame, text=table,
                          command=lambda t=table: self.quick_select_table(t),
                          bg='#34495e', fg='white', font=('Arial', 10),
                          width=8, height=1)
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.table_buttons.append(btn)
    
    def quick_select_table(self, table):
        """Quick select a table from button"""
        self.table_var.set(table)
        self.current_table = table
        self.current_table_label.config(text=f"▶ {table} ◀", fg='#2ecc71')
        self.log(f"📋 Quick selected table {table}")
        self.apply_table_data()
        
        # Add to recent tables
        self.add_to_recent(table)
    
    def prev_page(self):
        """Go to previous page of tables"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table_buttons()
            self.page_label.config(text=f"Page {self.current_page + 1}")
    
    def next_page(self):
        """Go to next page of tables"""
        max_pages = (len(self.table_data) - 1) // 10 + 1
        if self.current_page < max_pages - 1:
            self.current_page += 1
            self.update_table_buttons()
            self.page_label.config(text=f"Page {self.current_page + 1}")
    
    def on_search_changed(self, event=None):
        """Handle search text change"""
        search_text = self.search_var.get().lower()
        if not search_text:
            # Show all tables
            self.table_combo['values'] = list(self.table_data.keys())
        else:
            # Filter tables
            filtered = [t for t in self.table_data.keys() if search_text in t.lower()]
            self.table_combo['values'] = filtered
            
            if filtered:
                self.log(f"🔍 Found {len(filtered)} tables matching '{search_text}'")
    
    def add_to_recent(self, table):
        """Add table to recent tables list"""
        if table in self.recent_tables:
            self.recent_tables.remove(table)
        self.recent_tables.insert(0, table)
        
        # Keep only last 5 recent tables
        self.recent_tables = self.recent_tables[:5]
        self.save_recent_tables()
    
    def save_recent_tables(self):
        """Save recent tables to file"""
        try:
            with open('recent_tables.json', 'w') as f:
                json.dump(self.recent_tables, f)
        except:
            pass
    
    def load_recent_tables(self):
        """Load recent tables from file"""
        try:
            with open('recent_tables.json', 'r') as f:
                self.recent_tables = json.load(f)
        except:
            self.recent_tables = []
    
    def load_favorites(self):
        """Load favorite tables from file"""
        try:
            with open('favorite_tables.json', 'r') as f:
                self.favorite_tables = json.load(f)
        except:
            self.favorite_tables = []
    
    def save_favorites(self):
        """Save favorite tables to file"""
        try:
            with open('favorite_tables.json', 'w') as f:
                json.dump(self.favorite_tables, f)
        except:
            pass
    
    def add_to_favorites(self, table):
        """Add/remove table from favorites"""
        if table in self.favorite_tables:
            self.favorite_tables.remove(table)
            self.log(f"⭐ Removed {table} from favorites")
        else:
            self.favorite_tables.append(table)
            self.log(f"⭐ Added {table} to favorites")
        self.save_favorites()


def main():
    root = tk.Tk()
    app = IntegratedActionTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()