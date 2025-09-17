"""
Action Tracker GUI Manager - Enhanced Version
크기 확대, 세밀한 속도 조절, Tab 네비게이션 지원
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
from datetime import datetime
import threading

# Safety settings
pyautogui.FAILSAFE = True

# Player coordinates
PLAYER_COORDS = {
    1: (233, 361),
    2: (374, 359),
    3: (544, 362),
    4: (722, 359),
    5: (886, 356),
    6: (1051, 354),
    7: (1213, 355),
    8: (1385, 383),
    9: (1549, 367),
    10: (1705, 356)
}

SUB_NAME_FIELD = (785, 291)
COMPLETE_BUTTON = (1720, 139)
DELETE_BUTTON = (721, 112)

class ActionTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Action Tracker Manager GUI - Enhanced")
        self.root.geometry("1200x800")  # 더 큰 크기로 설정
        self.root.minsize(1000, 700)
        
        # Enhanced speed settings with numerical control
        self.speed_vars = {
            "mouse_click_delay": tk.DoubleVar(value=0.3),
            "keyboard_type_interval": tk.DoubleVar(value=0.02),
            "action_delay": tk.DoubleVar(value=0.5),
            "screen_wait": tk.DoubleVar(value=1.0),
            "pyautogui_pause": tk.DoubleVar(value=0.3)
        }
        
        # Player data
        self.empty_seats = {}
        self.player_names = {}
        self.delete_players = {}
        
        # Log
        self.log_text = None
        
        # Style configuration
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Large.TButton', font=('Arial', 12, 'bold'))
        
        self.create_widgets()
        self.setup_tab_navigation()
        
    def create_widgets(self):
        """Create all GUI widgets with enhanced size"""
        
        # Title frame - 더 큰 제목
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="ACTION TRACKER MANAGER - ENHANCED", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left panel - Player management (더 넓게)
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Player list frame
        player_frame = tk.LabelFrame(left_panel, text="Player Management", 
                                    font=('Arial', 14, 'bold'), padx=15, pady=15)
        player_frame.pack(fill=tk.BOTH, expand=True)
        
        # Headers with better spacing
        headers_frame = tk.Frame(player_frame)
        headers_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(headers_frame, text="Player", font=('Arial', 12, 'bold'), width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Empty Seat", font=('Arial', 12, 'bold'), width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(headers_frame, text="Player Name", font=('Arial', 12, 'bold'), width=25).pack(side=tk.LEFT, padx=10)
        tk.Label(headers_frame, text="Delete", font=('Arial', 12, 'bold'), width=8).pack(side=tk.LEFT, padx=5)
        
        # Player rows with enhanced size
        self.player_frame = tk.Frame(player_frame)
        self.player_frame.pack(fill=tk.BOTH, expand=True)
        
        for i in range(1, 11):
            row_frame = tk.Frame(self.player_frame)
            row_frame.pack(fill=tk.X, pady=5)
            
            # Player number - 더 큰 텍스트
            player_label = tk.Label(row_frame, text=f"Player {i}", 
                                   font=('Arial', 12, 'bold'), width=10)
            player_label.pack(side=tk.LEFT, padx=5)
            
            # Empty checkbox - 더 큰 체크박스
            self.empty_seats[i] = tk.BooleanVar(value=False)
            empty_cb = tk.Checkbutton(row_frame, variable=self.empty_seats[i],
                                     command=lambda p=i: self.on_empty_changed(p),
                                     font=('Arial', 10))
            empty_cb.pack(side=tk.LEFT, padx=(40, 5))
            
            # Name entry - 더 큰 입력 필드
            self.player_names[i] = tk.Entry(row_frame, width=30, font=('Arial', 11))
            self.player_names[i].pack(side=tk.LEFT, padx=10)
            
            # Delete checkbox - 더 큰 체크박스
            self.delete_players[i] = tk.BooleanVar(value=False)
            delete_cb = tk.Checkbutton(row_frame, variable=self.delete_players[i],
                                      font=('Arial', 10))
            delete_cb.pack(side=tk.LEFT, padx=(30, 5))
        
        # Quick actions with bigger buttons
        quick_frame = tk.LabelFrame(left_panel, text="Quick Actions", 
                                   font=('Arial', 12, 'bold'), padx=15, pady=10)
        quick_frame.pack(fill=tk.X, pady=10)
        
        button_row1 = tk.Frame(quick_frame)
        button_row1.pack(fill=tk.X, pady=5)
        
        tk.Button(button_row1, text="Mark 1-4 as Occupied", 
                 command=self.mark_1_4_occupied, width=20, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row1, text="Mark 5-10 as Empty", 
                 command=self.mark_5_10_empty, width=20, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row1, text="Clear All", 
                 command=self.clear_all, width=15, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        button_row2 = tk.Frame(quick_frame)
        button_row2.pack(fill=tk.X, pady=5)
        
        tk.Button(button_row2, text="Fill Test Names", 
                 command=self.fill_test_names, width=20, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="Select All Delete", 
                 command=self.select_all_delete, width=20, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_row2, text="Deselect All", 
                 command=self.deselect_all_delete, width=15, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Controls and Log (더 넓게)
        right_panel = tk.Frame(main_container, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        right_panel.pack_propagate(False)
        
        # Enhanced speed control frame with numerical inputs
        speed_frame = tk.LabelFrame(right_panel, text="Speed Settings (seconds)", 
                                   font=('Arial', 12, 'bold'), padx=15, pady=10)
        speed_frame.pack(fill=tk.X, pady=5)
        
        # Speed presets
        preset_frame = tk.Frame(speed_frame)
        preset_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(preset_frame, text="Presets:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        
        tk.Button(preset_frame, text="Ultra Fast", command=self.set_ultra_fast,
                 bg='#ff4757', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="Fast", command=self.set_fast,
                 bg='#ff6b35', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="Normal", command=self.set_normal,
                 bg='#26d0ce', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="Slow", command=self.set_slow,
                 bg='#a4b0be', fg='white', font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=2)
        
        # Numerical speed controls
        speed_labels = {
            "mouse_click_delay": "Mouse Click Delay",
            "keyboard_type_interval": "Keyboard Type Speed", 
            "action_delay": "Action Delay",
            "screen_wait": "Screen Wait Time",
            "pyautogui_pause": "Global Pause"
        }
        
        for key, label in speed_labels.items():
            control_frame = tk.Frame(speed_frame)
            control_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(control_frame, text=f"{label}:", width=18, anchor='w',
                    font=('Arial', 9)).pack(side=tk.LEFT)
            
            # Spinbox for precise control
            spinbox = tk.Spinbox(control_frame, from_=0.001, to=5.0, increment=0.01,
                               textvariable=self.speed_vars[key], width=8,
                               font=('Arial', 9), command=self.update_speeds)
            spinbox.pack(side=tk.LEFT, padx=5)
            
            # Quick buttons
            tk.Button(control_frame, text="-", width=2,
                     command=lambda k=key: self.adjust_speed(k, -0.1)).pack(side=tk.LEFT, padx=1)
            tk.Button(control_frame, text="+", width=2,
                     command=lambda k=key: self.adjust_speed(k, 0.1)).pack(side=tk.LEFT, padx=1)
        
        # Action buttons - larger size
        action_frame = tk.LabelFrame(right_panel, text="Actions", 
                                    font=('Arial', 12, 'bold'), padx=15, pady=15)
        action_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(action_frame, text="UPDATE/REGISTER NAMES", 
                 command=self.process_updates, bg='#27ae60', fg='white',
                 font=('Arial', 12, 'bold'), height=3).pack(fill=tk.X, pady=5)
        
        tk.Button(action_frame, text="DELETE SELECTED", 
                 command=self.process_deletes, bg='#e74c3c', fg='white',
                 font=('Arial', 12, 'bold'), height=3).pack(fill=tk.X, pady=5)
        
        tk.Button(action_frame, text="PROCESS ALL", 
                 command=self.process_all, bg='#3498db', fg='white',
                 font=('Arial', 12, 'bold'), height=3).pack(fill=tk.X, pady=5)
        
        # Status indicator - larger
        self.status_label = tk.Label(action_frame, text="Ready", 
                                    bg='green', fg='white', font=('Arial', 12, 'bold'),
                                    height=2)
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Log frame - larger
        log_frame = tk.LabelFrame(right_panel, text="Activity Log", 
                                 font=('Arial', 12, 'bold'), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Log text with scrollbar - larger
        log_container = tk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        log_scroll = tk.Scrollbar(log_container)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_container, height=15, width=45,
                                yscrollcommand=log_scroll.set, font=('Consolas', 9))
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        # Bottom buttons - larger
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Button(bottom_frame, text="Take Screenshot", 
                 command=self.take_screenshot, width=18, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Clear Log", 
                 command=self.clear_log, width=18, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Save Log", 
                 command=self.save_log, width=18, height=2,
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Exit Program", 
                 command=self.root.quit, width=18, height=2,
                 font=('Arial', 10)).pack(side=tk.RIGHT, padx=5)
        
        # Initial speed update
        self.update_speeds()
    
    def setup_tab_navigation(self):
        """Set up Tab key navigation between name entry fields"""
        for i in range(1, 11):
            next_player = i + 1 if i < 10 else 1
            self.player_names[i].bind('<Tab>', lambda e, next_p=next_player: self.focus_next_player(next_p))
            # Also bind Shift+Tab for reverse navigation
            prev_player = i - 1 if i > 1 else 10
            self.player_names[i].bind('<Shift-Tab>', lambda e, prev_p=prev_player: self.focus_prev_player(prev_p))
    
    def focus_next_player(self, next_player):
        """Focus on next player name field"""
        self.player_names[next_player].focus_set()
        self.player_names[next_player].select_range(0, tk.END)
        return "break"  # Prevent default tab behavior
    
    def focus_prev_player(self, prev_player):
        """Focus on previous player name field"""
        self.player_names[prev_player].focus_set()
        self.player_names[prev_player].select_range(0, tk.END)
        return "break"  # Prevent default tab behavior
    
    def set_ultra_fast(self):
        """Set ultra fast speed preset - maximum speed"""
        speeds = {
            "mouse_click_delay": 0.08,
            "keyboard_type_interval": 0.008,
            "action_delay": 0.15,
            "screen_wait": 0.4,
            "pyautogui_pause": 0.08
        }
        for key, value in speeds.items():
            self.speed_vars[key].set(value)
        self.update_speeds()
        self.log("Speed set to: ULTRA FAST (Maximum speed - Use with caution!)")
    
    def set_fast(self):
        """Set fast speed preset - balanced speed"""
        speeds = {
            "mouse_click_delay": 0.15,
            "keyboard_type_interval": 0.012,
            "action_delay": 0.25,
            "screen_wait": 0.6,
            "pyautogui_pause": 0.15
        }
        for key, value in speeds.items():
            self.speed_vars[key].set(value)
        self.update_speeds()
        self.log("Speed set to: FAST (Balanced for speed and stability)")
    
    def set_normal(self):
        """Set normal speed preset"""
        speeds = {
            "mouse_click_delay": 0.3,
            "keyboard_type_interval": 0.02,
            "action_delay": 0.5,
            "screen_wait": 1.0,
            "pyautogui_pause": 0.3
        }
        for key, value in speeds.items():
            self.speed_vars[key].set(value)
        self.update_speeds()
        self.log("Speed set to: NORMAL")
    
    def set_slow(self):
        """Set slow speed preset"""
        speeds = {
            "mouse_click_delay": 0.5,
            "keyboard_type_interval": 0.05,
            "action_delay": 1.0,
            "screen_wait": 2.0,
            "pyautogui_pause": 0.5
        }
        for key, value in speeds.items():
            self.speed_vars[key].set(value)
        self.update_speeds()
        self.log("Speed set to: SLOW")
    
    def adjust_speed(self, key, delta):
        """Adjust individual speed setting"""
        current = self.speed_vars[key].get()
        new_value = max(0.001, current + delta)
        self.speed_vars[key].set(round(new_value, 3))
        self.update_speeds()
    
    def update_speeds(self):
        """Update PyAutoGUI speed settings"""
        pyautogui.PAUSE = self.speed_vars["pyautogui_pause"].get()
        
        # Show current speeds in log
        speeds_text = "Current speeds: " + ", ".join([
            f"{key.replace('_', ' ').title()}: {var.get():.3f}s" 
            for key, var in self.speed_vars.items()
        ])
        # Only log if not initial setup
        if hasattr(self, 'log_text') and self.log_text:
            self.log(f"Speeds updated")
    
    def get_current_speeds(self):
        """Get current speed settings as dictionary"""
        return {key: var.get() for key, var in self.speed_vars.items()}
    
    def on_empty_changed(self, player_num):
        """Handle empty checkbox change"""
        if self.empty_seats[player_num].get():
            # If marked as empty, clear delete checkbox
            self.delete_players[player_num].set(False)
            self.log(f"Player {player_num} marked as empty seat (new registration)")
        else:
            self.log(f"Player {player_num} marked as occupied (name update)")
    
    def mark_1_4_occupied(self):
        """Mark players 1-4 as occupied"""
        for i in range(1, 5):
            self.empty_seats[i].set(False)
        self.log("Players 1-4 marked as occupied (existing names)")
    
    def mark_5_10_empty(self):
        """Mark players 5-10 as empty"""
        for i in range(5, 11):
            self.empty_seats[i].set(True)
        self.log("Players 5-10 marked as empty (new registrations)")
    
    def clear_all(self):
        """Clear all inputs"""
        for i in range(1, 11):
            self.empty_seats[i].set(False)
            self.player_names[i].delete(0, tk.END)
            self.delete_players[i].set(False)
        self.log("All fields cleared")
    
    def fill_test_names(self):
        """Fill test names for all players"""
        test_names = [
            "Phil Ivey", "Daniel Negreanu", "Doyle Brunson", "Phil Hellmuth",
            "Tom Dwan", "Patrik Antonius", "Gus Hansen", "Vanessa Selbst",
            "Erik Seidel", "Johnny Chan"
        ]
        for i in range(1, 11):
            self.player_names[i].delete(0, tk.END)
            self.player_names[i].insert(0, test_names[i-1])
        self.log("Test poker player names filled")
    
    def select_all_delete(self):
        """Select all players for deletion"""
        for i in range(1, 11):
            self.delete_players[i].set(True)
        self.log("All players selected for deletion")
    
    def deselect_all_delete(self):
        """Deselect all delete checkboxes"""
        for i in range(1, 11):
            self.delete_players[i].set(False)
        self.log("All delete selections cleared")
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        if self.log_text:
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            self.root.update()
    
    def clear_log(self):
        """Clear log text"""
        if self.log_text:
            self.log_text.delete(1.0, tk.END)
    
    def save_log(self):
        """Save log to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gui_enhanced_log_{timestamp}.txt"
        
        if self.log_text:
            with open(filename, 'w') as f:
                f.write(self.log_text.get(1.0, tk.END))
            
            self.log(f"✓ Log saved to {filename}")
    
    def take_screenshot(self):
        """Take screenshot"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"gui_enhanced_screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        self.log(f"Screenshot saved: {filename}")
    
    def update_existing_name(self, player_num, new_name):
        """Update existing player name with current speed settings"""
        try:
            speeds = self.get_current_speeds()
            coords = PLAYER_COORDS[player_num]
            
            self.log(f"  🖱️ Clicking Player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(speeds["screen_wait"])
            
            self.log(f"  🖱️ Clicking name field at {SUB_NAME_FIELD}")
            pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
            time.sleep(speeds["mouse_click_delay"])
            
            self.log(f"  ⌨️ Typing new name: {new_name}")
            pyautogui.tripleClick()
            time.sleep(0.1)
            pyautogui.typewrite(new_name, interval=speeds["keyboard_type_interval"])
            time.sleep(speeds["action_delay"])
            
            self.log(f"  ⏎ Pressing Enter")
            pyautogui.press('enter')
            time.sleep(speeds["action_delay"])
            
            self.log(f"  🖱️ Clicking Complete button")
            pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
            time.sleep(speeds["screen_wait"])
            
            return True
        except Exception as e:
            self.log(f"❌ ERROR updating player {player_num}: {e}")
            return False
    
    def register_new_name(self, player_num, new_name):
        """Register new player name with current speed settings"""
        try:
            speeds = self.get_current_speeds()
            coords = PLAYER_COORDS[player_num]
            
            self.log(f"  🖱️ Clicking Player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(speeds["mouse_click_delay"])
            
            self.log(f"  ⌨️ Typing new name: {new_name}")
            pyautogui.typewrite(new_name, interval=speeds["keyboard_type_interval"])
            time.sleep(speeds["action_delay"])
            
            self.log(f"  ⏎ Pressing Enter")
            pyautogui.press('enter')
            time.sleep(speeds["action_delay"])
            
            return True
        except Exception as e:
            self.log(f"❌ ERROR registering player {player_num}: {e}")
            return False
    
    def delete_player(self, player_num):
        """Delete player with current speed settings"""
        try:
            speeds = self.get_current_speeds()
            coords = PLAYER_COORDS[player_num]
            
            self.log(f"  🖱️ Clicking Player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(speeds["screen_wait"])
            
            self.log(f"  🗑️ Clicking Delete button at {DELETE_BUTTON}")
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(speeds["screen_wait"])
            
            return True
        except Exception as e:
            self.log(f"❌ ERROR deleting player {player_num}: {e}")
            return False
    
    def process_updates(self):
        """Process name updates and registrations"""
        def run():
            self.status_label.config(text="Processing Updates...", bg='orange')
            self.log("=== STARTING NAME UPDATES ===")
            
            success = 0
            total = 0
            
            for i in range(1, 11):
                name = self.player_names[i].get().strip()
                if name and not self.delete_players[i].get():
                    total += 1
                    if self.empty_seats[i].get():
                        # Register new name
                        self.log(f"Registering Player {i}: {name}")
                        if self.register_new_name(i, name):
                            success += 1
                            self.log(f"✓ Player {i} registered successfully")
                        else:
                            self.log(f"✗ Player {i} registration failed")
                    else:
                        # Update existing name
                        self.log(f"Updating Player {i}: {name}")
                        if self.update_existing_name(i, name):
                            success += 1
                            self.log(f"✓ Player {i} updated successfully")
                        else:
                            self.log(f"✗ Player {i} update failed")
                    
                    # Small delay between operations
                    time.sleep(self.get_current_speeds()["action_delay"])
            
            self.log(f"=== UPDATES COMPLETE: {success}/{total} successful ===")
            self.status_label.config(text="Ready", bg='green')
            
            if total == 0:
                self.log("ℹ️ No names to process")
            elif success == total:
                self.log(f"🎉 All {total} updates completed successfully!")
            else:
                self.log(f"⚠️ Partial success: {success}/{total} updates completed")
        
        # Run in thread to prevent GUI freeze
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def process_deletes(self):
        """Process deletions"""
        def run():
            self.status_label.config(text="Processing Deletes...", bg='red')
            self.log("=== STARTING DELETIONS ===")
            
            success = 0
            total = 0
            
            for i in range(1, 11):
                if self.delete_players[i].get():
                    total += 1
                    self.log(f"Deleting Player {i}")
                    if self.delete_player(i):
                        success += 1
                        self.log(f"✓ Player {i} deleted successfully")
                    else:
                        self.log(f"✗ Player {i} deletion failed")
                    time.sleep(self.get_current_speeds()["action_delay"])
            
            self.log(f"=== DELETIONS COMPLETE: {success}/{total} successful ===")
            self.status_label.config(text="Ready", bg='green')
            
            if total > 0:
                if success == total:
                    self.log(f"🎉 All {total} deletions completed successfully!")
                else:
                    self.log(f"⚠️ Partial success: {success}/{total} deletions completed")
            else:
                self.log("ℹ️ No players selected for deletion")
        
        # Confirm before deletion
        to_delete = [i for i in range(1, 11) if self.delete_players[i].get()]
        if to_delete:
            # Direct execution without confirmation popup
            self.log(f"⚠️ Starting deletion of players: {to_delete}")
            thread = threading.Thread(target=run)
            thread.daemon = True
            thread.start()
        else:
            self.log("ℹ️ No players selected for deletion")
    
    def process_all(self):
        """Process all operations"""
        def run():
            self.status_label.config(text="Processing All...", bg='purple')
            self.log("=== STARTING ALL OPERATIONS ===")
            
            # First process updates/registrations
            update_count = 0
            for i in range(1, 11):
                name = self.player_names[i].get().strip()
                if name and not self.delete_players[i].get():
                    if self.empty_seats[i].get():
                        self.log(f"Registering Player {i}: {name}")
                        if self.register_new_name(i, name):
                            update_count += 1
                    else:
                        self.log(f"Updating Player {i}: {name}")
                        if self.update_existing_name(i, name):
                            update_count += 1
                    time.sleep(self.get_current_speeds()["action_delay"])
            
            # Then process deletions
            delete_count = 0
            for i in range(1, 11):
                if self.delete_players[i].get():
                    self.log(f"Deleting Player {i}")
                    if self.delete_player(i):
                        delete_count += 1
                    time.sleep(self.get_current_speeds()["action_delay"])
            
            self.log(f"=== ALL OPERATIONS COMPLETE ===")
            self.log(f"📊 Updates/Registrations: {update_count}")
            self.log(f"📊 Deletions: {delete_count}")
            self.log(f"🎉 All operations completed successfully!")
            self.status_label.config(text="Ready", bg='green')
        
        operations = []
        for i in range(1, 11):
            if self.player_names[i].get().strip() and not self.delete_players[i].get():
                operations.append(f"Player {i}: {'Register' if self.empty_seats[i].get() else 'Update'}")
            if self.delete_players[i].get():
                operations.append(f"Player {i}: Delete")
        
        if operations:
            op_text = "\n".join(operations)
            self.log(f"🚀 Starting batch operations:")
            for op in operations:
                self.log(f"  - {op}")
            thread = threading.Thread(target=run)
            thread.daemon = True
            thread.start()
        else:
            self.log("ℹ️ No operations to process")


def main():
    root = tk.Tk()
    app = ActionTrackerGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()