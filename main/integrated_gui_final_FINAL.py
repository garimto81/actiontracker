"""
Integrated Action Tracker GUI - FINAL VERSION
플레이어 이름, 칩 관리, 자동 감지 통합 GUI
Version FINAL - Fixed chip input overflow and optimized Ultra Fast settings
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
import queue

# Coordinates
PLAYER_COORDS = {
    1: (233, 361), 2: (374, 359), 3: (544, 362), 4: (722, 359), 5: (886, 356),
    6: (1051, 354), 7: (1213, 355), 8: (1385, 383), 9: (1549, 367), 10: (1705, 356)
}

# Chip coordinates for each seat - UPDATED with correct values
CHIP_COORDS = {
    1: (211, 480),
    2: (377, 480),
    3: (547, 480),
    4: (719, 480),
    5: (913, 480),
    6: (1031, 480),
    7: (1211, 480),
    8: (1378, 480),
    9: (1546, 480),
    10: (1696, 480)
}

SUB_NAME_FIELD = (785, 291)
COMPLETE_BUTTON = (1720, 139)
DELETE_BUTTON = (721, 112)

class IntegratedActionTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Action Tracker - FINAL VERSION")
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
        
        # FIXED Ultra Fast speed settings - 수정된 값
        self.speed_vars = {
            "mouse_click_delay": tk.DoubleVar(value=0.1),      # 0.3 -> 0.1
            "keyboard_type_interval": tk.DoubleVar(value=0.05), # 0.02 -> 0.05 (느리게)
            "action_delay": tk.DoubleVar(value=0.1),           # 0.5 -> 0.1
            "screen_wait": tk.DoubleVar(value=0.2)             # 1.0 -> 0.2
        }
        
        pyautogui.PAUSE = 0.1  # Global pause 설정
        
        # Thread-safe logging queue
        self.log_queue = queue.Queue()
        
        self.create_widgets()
        
        # Start the log queue processor
        self.process_log_queue()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Top Frame - Title and Table Selection
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=150)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        title_container = tk.Frame(top_frame, bg='#2c3e50')
        title_container.pack(expand=True)
        
        tk.Label(title_container, text="ACTION TRACKER - FINAL VERSION", 
                font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50').pack(pady=10)
        
        # Table selection frame
        table_frame = tk.Frame(title_container, bg='#2c3e50')
        table_frame.pack(pady=10)
        
        tk.Label(table_frame, text="Table:", font=('Arial', 12), fg='white', bg='#2c3e50').pack(side=tk.LEFT, padx=5)
        
        self.table_var = tk.StringVar()
        self.table_combo = ttk.Combobox(table_frame, textvariable=self.table_var, state='readonly', width=20)
        self.table_combo.pack(side=tk.LEFT, padx=5)
        self.table_combo.bind('<<ComboboxSelected>>', self.on_table_selected)
        
        tk.Button(table_frame, text="LOAD DATA", command=self.load_google_sheets,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(table_frame, text="APPLY TABLE", command=self.apply_table_data,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), padx=15).pack(side=tk.LEFT, padx=5)
        
        self.current_table_label = tk.Label(table_frame, text="No Table Selected", 
                                           font=('Arial', 11, 'bold'), fg='#e74c3c', bg='#2c3e50')
        self.current_table_label.pack(side=tk.LEFT, padx=20)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Player management
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Player list frame
        player_frame = tk.LabelFrame(left_panel, text="Player Management", font=('Arial', 12, 'bold'))
        player_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Headers
        headers_frame = tk.Frame(player_frame)
        headers_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(headers_frame, text="Seat", font=('Arial', 10, 'bold'), width=5).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Empty", font=('Arial', 10, 'bold'), width=6).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Player Name", font=('Arial', 10, 'bold'), width=20).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Chips", font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Delete", font=('Arial', 10, 'bold'), width=6).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Status", font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT, padx=5)
        
        # Player rows
        players_container = tk.Frame(player_frame)
        players_container.pack(fill=tk.BOTH, expand=True)
        
        for i in range(1, 11):
            row_frame = tk.Frame(players_container)
            row_frame.pack(fill=tk.X, pady=2)
            
            # Seat number
            tk.Label(row_frame, text=f"#{i}", font=('Arial', 10), width=5).pack(side=tk.LEFT, padx=5)
            
            # Empty checkbox - MUCH LARGER SIZE
            self.empty_seats[i] = tk.BooleanVar(value=True)
            empty_cb = tk.Checkbutton(row_frame, variable=self.empty_seats[i], 
                          command=lambda x=i: self.on_empty_changed(x),
                          font=('Arial', 14, 'bold'), width=3, height=1, 
                          borderwidth=2, relief="solid")
            empty_cb.pack(side=tk.LEFT, padx=5)
            
            # Player name
            self.player_names[i] = tk.Entry(row_frame, width=20, font=('Arial', 10))
            self.player_names[i].pack(side=tk.LEFT, padx=5)
            
            # Chip amount
            self.chip_amounts[i] = tk.Entry(row_frame, width=12, font=('Arial', 10))
            self.chip_amounts[i].pack(side=tk.LEFT, padx=5)
            
            # Delete checkbox - MUCH LARGER SIZE
            self.delete_players[i] = tk.BooleanVar()
            delete_cb = tk.Checkbutton(row_frame, variable=self.delete_players[i],
                                      font=('Arial', 14, 'bold'), width=3, height=1,
                                      borderwidth=2, relief="solid")
            delete_cb.pack(side=tk.LEFT, padx=5)
            
            # Status label
            self.seat_status_labels[i] = tk.Label(row_frame, text="⚪ Empty", 
                                                  font=('Arial', 9), width=12)
            self.seat_status_labels[i].pack(side=tk.LEFT, padx=5)
        
        # Right panel - Controls and Log
        right_panel = tk.Frame(main_container, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        right_panel.pack_propagate(False)
        
        # Control buttons frame
        control_frame = tk.LabelFrame(right_panel, text="Controls", font=('Arial', 12, 'bold'))
        control_frame.pack(fill=tk.X, pady=5)
        
        # Process buttons - Main actions
        tk.Label(control_frame, text="Main Actions:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        button_frame1 = tk.Frame(control_frame)
        button_frame1.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(button_frame1, text="UPDATE ALL", command=self.update_all,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'), height=2).pack(fill=tk.X, pady=2)
        
        button_frame2 = tk.Frame(control_frame)
        button_frame2.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(button_frame2, text="UPDATE NAMES", command=self.update_names_only,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(button_frame2, text="UPDATE CHIPS", command=self.update_chips_only,
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Detection and Delete
        button_frame3 = tk.Frame(control_frame)
        button_frame3.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(button_frame3, text="AUTO DETECT", command=self.auto_detect,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(button_frame3, text="DELETE SELECTED", command=self.delete_selected,
                 bg='#c0392b', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Speed control
        speed_frame = tk.LabelFrame(right_panel, text="Speed Settings", font=('Arial', 12, 'bold'))
        speed_frame.pack(fill=tk.X, pady=5)
        
        # Speed presets - Ultra Fast가 기본값
        preset_frame = tk.Frame(speed_frame)
        preset_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(preset_frame, text="Presets:", font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        for preset in ['ultra_fast', 'fast', 'normal', 'slow']:
            btn_text = preset.replace('_', ' ').title()
            btn_color = '#e74c3c' if preset == 'ultra_fast' else '#95a5a6'
            tk.Button(preset_frame, text=btn_text, 
                     command=lambda p=preset: self.set_speed_preset(p),
                     bg=btn_color, fg='white', width=10).pack(side=tk.LEFT, padx=2)
        
        # Speed details (숨김 가능)
        details_frame = tk.Frame(speed_frame)
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        for key, var in self.speed_vars.items():
            row = tk.Frame(details_frame)
            row.pack(fill=tk.X, pady=2)
            
            label_text = key.replace('_', ' ').title() + ':'
            tk.Label(row, text=label_text, width=20, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row, textvariable=var, width=8, anchor=tk.W).pack(side=tk.LEFT)
        
        # State management
        state_frame = tk.Frame(control_frame)
        state_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(state_frame, text="SAVE STATE", command=self.save_state,
                 bg='#27ae60', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(state_frame, text="LOAD STATE", command=self.load_state,
                 bg='#2980b9', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Log display
        log_frame = tk.LabelFrame(right_panel, text="Activity Log", font=('Arial', 12, 'bold'))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Log text with scrollbar
        log_container = tk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(log_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_container, height=15, width=50, 
                                yscrollcommand=scrollbar.set, font=('Courier', 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", bg='green', fg='white', 
                                     font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initial log
        self.log("System initialized - FINAL VERSION")
        self.log("Ultra Fast mode enabled by default")
        self.log("Chip input overflow issue FIXED")
        
    def set_speed_preset(self, preset):
        """Set speed values based on preset"""
        presets = {
            'ultra_fast': {
                'mouse_click_delay': 0.1,      # Updated value
                'keyboard_type_interval': 0.05, # Slower to prevent overflow
                'action_delay': 0.1,            # Updated value
                'screen_wait': 0.2              # Updated value
            },
            'fast': {
                'mouse_click_delay': 0.15,
                'keyboard_type_interval': 0.03,
                'action_delay': 0.2,
                'screen_wait': 0.5
            },
            'normal': {
                'mouse_click_delay': 0.3,
                'keyboard_type_interval': 0.02,
                'action_delay': 0.5,
                'screen_wait': 1.0
            },
            'slow': {
                'mouse_click_delay': 0.5,
                'keyboard_type_interval': 0.05,
                'action_delay': 0.8,
                'screen_wait': 1.5
            }
        }
        
        if preset in presets:
            for key, value in presets[preset].items():
                self.speed_vars[key].set(value)
            self.log(f"⚡ Speed set to {preset}")
            
            # Update global PyAutoGUI pause
            if preset == 'ultra_fast':
                pyautogui.PAUSE = 0.05
            elif preset == 'fast':
                pyautogui.PAUSE = 0.1
            elif preset == 'normal':
                pyautogui.PAUSE = 0.3
            else:
                pyautogui.PAUSE = 0.5
    
    def input_chips(self, seat, chips):
        """FIXED: Click player name coordinate, type chips, then press Enter"""
        try:
            # Use PLAYER coordinates, not CHIP coordinates!
            coords = PLAYER_COORDS[seat]
            self.log(f"  Inputting chips for seat {seat} at player coord {coords}: {chips}")
            
            # Step 1: Click player name field
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["mouse_click_delay"].get())
            
            # Step 2: Clear existing value (triple click to select all)
            pyautogui.tripleClick()
            time.sleep(0.1)
            
            # Step 3: Type chip amount
            chip_str = str(chips)
            for digit in chip_str:
                pyautogui.press(digit)
                time.sleep(0.1)  # Delay to prevent overflow
            
            # Step 4: Press Enter to confirm
            time.sleep(0.2)
            pyautogui.press('enter')
            time.sleep(0.3)
            
            self.log(f"  ✓ Chips input complete: {chips}")
            
        except Exception as e:
            self.log(f"❌ Error inputting chips for seat {seat}: {e}")
    
    def load_google_sheets(self):
        """Load data from Google Sheets"""
        def load():
            self.root.after(0, lambda: self.status_label.config(text="Loading...", bg='orange'))
            self.log("Loading data from Google Sheets...")
            
            try:
                response = requests.get(self.sheet_url)
                response.raise_for_status()
                
                df = pd.read_csv(StringIO(response.text))
                
                self.table_data = {}
                for _, row in df.iterrows():
                    table = str(row['Table'])
                    if table not in self.table_data:
                        self.table_data[table] = {}
                    
                    seat = int(row['Seat'])
                    self.table_data[table][seat] = {
                        'player': row['player'],
                        'chips': row['Chips']
                    }
                
                # Update combo box
                self.table_combo['values'] = list(self.table_data.keys())
                
                self.log(f"✅ Loaded {len(self.table_data)} tables")
                self.root.after(0, lambda: self.status_label.config(text="Ready", bg='green'))
                
            except Exception as e:
                self.log(f"❌ Error loading data: {e}")
                self.root.after(0, lambda: self.status_label.config(text="Error", bg='red'))
        
        thread = threading.Thread(target=load)
        thread.daemon = True
        thread.start()
    
    def on_table_selected(self, event=None):
        """Handle table selection"""
        selected = self.table_var.get()
        if selected:
            self.current_table = selected
            self.current_table_label.config(text=f"Table: {selected}", fg='#27ae60')
            self.log(f"Table {selected} selected")
    
    def apply_table_data(self):
        """Apply selected table data to the form"""
        if not self.current_table:
            messagebox.showwarning("No Table", "Please select a table first")
            return
        
        if self.current_table not in self.table_data:
            messagebox.showerror("Error", f"Table {self.current_table} not found")
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
        self.log(f"Applying data for table {self.current_table}:")
        
        for seat, info in table_players.items():
            self.empty_seats[seat].set(False)
            self.seat_status_labels[seat].config(text="🔴 Occupied")
            
            self.player_names[seat].delete(0, tk.END)
            self.player_names[seat].insert(0, info['player'])
            
            self.chip_amounts[seat].delete(0, tk.END)
            self.chip_amounts[seat].insert(0, str(info['chips']))
            
            self.log(f"  Seat {seat}: {info['player']} - {info['chips']} chips")
        
        self.log(f"✅ Table {self.current_table} data applied")
    
    def on_empty_changed(self, seat):
        """Handle empty checkbox change"""
        is_empty = self.empty_seats[seat].get()
        if is_empty:
            self.seat_status_labels[seat].config(text="⚪ Empty")
        else:
            self.seat_status_labels[seat].config(text="🔴 Occupied")
    
    def log(self, message):
        """Thread-safe logging - adds message to queue"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}\n")
    
    def process_log_queue(self):
        """Process log messages from queue in main thread"""
        try:
            while True:
                try:
                    message = self.log_queue.get_nowait()
                    self.log_text.insert(tk.END, message)
                    self.log_text.see(tk.END)
                except queue.Empty:
                    break
        except:
            pass
        # Schedule next check
        self.root.after(100, self.process_log_queue)
    
    def update_names_only(self):
        """Update only player names"""
        def run():
            # Use root.after to update GUI from thread
            self.root.after(0, lambda: self.status_label.config(text="Updating Names...", bg='orange'))
            self.log("🔄 Starting name updates...")
            
            for seat in range(1, 11):
                name = self.player_names[seat].get().strip()
                is_empty = self.empty_seats[seat].get()
                
                if is_empty and name:
                    self.log(f"Seat {seat}: Registering new name '{name}'")
                    self.register_new_name(seat, name)
                elif not is_empty and name:
                    self.log(f"Seat {seat}: Updating existing name to '{name}'")
                    self.update_existing_name(seat, name)
                else:
                    self.log(f"Seat {seat}: Skipping (empty or no name)")
            
            self.root.after(0, lambda: self.status_label.config(text="Ready", bg='green'))
            self.log("✅ Name updates completed")
        
        Thread(target=run).start()
    
    def update_chips_only(self):
        """Update only chip amounts"""
        def run():
            self.root.after(0, lambda: self.status_label.config(text="Updating Chips...", bg='orange'))
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
                
                self.log(f"Seat {seat}: Inputting chips: {chips}")
                self.input_chips(seat, chips)
            
            self.root.after(0, lambda: self.status_label.config(text="Ready", bg='green'))
            self.log("✅ Chip updates completed")
        
        Thread(target=run).start()
    
    def update_all(self):
        """Update names and chips for all players"""
        def run():
            try:
                self.root.after(0, lambda: self.status_label.config(text="Updating All...", bg='orange'))
                self.log("🔄 Starting complete update...")
                
                for seat in range(1, 11):
                    name = self.player_names[seat].get().strip()
                    chips = self.chip_amounts[seat].get().strip()
                    is_empty = self.empty_seats[seat].get()
                    is_delete = self.delete_players[seat].get()
                    
                    if is_delete:
                        self.log(f"Seat {seat}: Deleting player")
                        self.delete_player(seat)
                        continue
                    
                    if is_empty and not name:
                        self.log(f"Seat {seat}: Empty, skipping")
                        continue
                    
                    # For new player: name and chips are entered together
                    if is_empty and name:
                        self.log(f"Seat {seat}: Registering new player '{name}' with chips '{chips}'")
                        self.register_new_player_with_chips(seat, name, chips)
                    elif not is_empty and name:
                        self.log(f"Seat {seat}: Updating existing name to '{name}'")
                        self.update_existing_name(seat, name)
                        # Note: For existing players, chips might need separate handling
                
                self.root.after(0, lambda: self.status_label.config(text="Ready", bg='green'))
                self.log("✅ All updates completed")
                
            except Exception as e:
                self.log(f"❌ ERROR: {e}")
                self.root.after(0, lambda: self.status_label.config(text="Error", bg='red'))
        
        Thread(target=run).start()
    
    def update_existing_name(self, seat, new_name):
        """Update existing player name - NO Ctrl+A"""
        try:
            coords = PLAYER_COORDS[seat]
            
            # Step 1: Click player
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 2: Click name field
            pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 3: Type new name directly (NO Ctrl+A)
            pyautogui.typewrite(new_name, interval=self.speed_vars["keyboard_type_interval"].get())
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 4: Press Enter
            pyautogui.press('enter')
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 5: Click Complete
            pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
            time.sleep(self.speed_vars["screen_wait"].get())
            
        except Exception as e:
            self.log(f"❌ Error updating seat {seat}: {e}")
    
    def register_new_player_with_chips(self, seat, name, chips=None):
        """Register new player - name only, NO chip typing during registration"""
        try:
            coords = PLAYER_COORDS[seat]
            
            # Step 1: Click empty player position
            self.log(f"  Clicking seat {seat} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 2: Type player name
            self.log(f"  Typing name: {name}")
            pyautogui.typewrite(name, interval=self.speed_vars["keyboard_type_interval"].get())
            time.sleep(0.2)
            
            # Step 3: Press Enter to confirm (NO chip typing here)
            pyautogui.press('enter')
            time.sleep(self.speed_vars["screen_wait"].get())
            
            self.log(f"  ✓ Player registered: {name}")
            
            # Chips will be entered separately through input_chips function
            
        except Exception as e:
            self.log(f"❌ Error registering seat {seat}: {e}")
    
    def register_new_name(self, seat, name):
        """Register new player name only (backward compatibility)"""
        self.register_new_player_with_chips(seat, name, None)
    
    def delete_player(self, seat):
        """Delete a player from a seat - NO Complete button"""
        try:
            coords = PLAYER_COORDS[seat]
            
            # Step 1: Click player
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speed_vars["action_delay"].get())
            
            # Step 2: Click Delete button (Final step)
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(self.speed_vars["screen_wait"].get())
            
            # NO Complete button click - deletion is done
            
        except Exception as e:
            self.log(f"❌ Error deleting seat {seat}: {e}")
    
    def delete_selected(self):
        """Delete selected players"""
        def run():
            self.root.after(0, lambda: self.status_label.config(text="Deleting...", bg='orange'))
            self.log("🗑️ Starting deletions...")
            
            for seat in range(1, 11):
                if self.delete_players[seat].get():
                    self.log(f"Seat {seat}: Deleting player")
                    self.delete_player(seat)
            
            self.root.after(0, lambda: self.status_label.config(text="Ready", bg='green'))
            self.log("✅ Deletions completed")
        
        Thread(target=run).start()
    
    def auto_detect(self):
        """Auto detect current player status"""
        def detect():
            self.root.after(0, lambda: self.status_label.config(text="Detecting...", bg='blue'))
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
            self.root.after(0, lambda: self.status_label.config(text="Ready", bg='green'))
        
        thread = threading.Thread(target=detect)
        thread.daemon = True
        thread.start()
    
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
                
                # Apply state
                for seat_str, data in state['seats'].items():
                    seat = int(seat_str)
                    self.empty_seats[seat].set(data['empty'])
                    
                    self.player_names[seat].delete(0, tk.END)
                    self.player_names[seat].insert(0, data['name'])
                    
                    self.chip_amounts[seat].delete(0, tk.END)
                    self.chip_amounts[seat].insert(0, data['chips'])
                    
                    if data['empty']:
                        self.seat_status_labels[seat].config(text="⚪ Empty")
                    else:
                        self.seat_status_labels[seat].config(text="🔴 Occupied")
                
                self.log(f"📂 State loaded from {filename}")
                
            except Exception as e:
                self.log(f"❌ Error loading state: {e}")
                messagebox.showerror("Error", f"Failed to load state: {e}")

def main():
    root = tk.Tk()
    app = IntegratedActionTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()