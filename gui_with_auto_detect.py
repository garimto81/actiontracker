"""
Enhanced GUI with Auto Detection Feature
자동 감지 기능이 추가된 GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
from datetime import datetime
import threading
import json
import numpy as np
from PIL import Image

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

class AutoDetectionMixin:
    """Auto detection functionality mixin"""
    
    def auto_detect_players(self):
        """Auto detect player status using color detection"""
        self.log("🔍 Starting auto detection...")
        self.status_label.config(text="Detecting...", bg='blue')
        
        def detect():
            results = {}
            
            for player_num in range(1, 11):
                # Get player position
                coords = PLAYER_COORDS[player_num]
                
                # Capture small region around player
                try:
                    region = pyautogui.screenshot(
                        region=(coords[0]-50, coords[1]-20, 100, 40)
                    )
                    
                    # Convert to numpy array
                    img_array = np.array(region)
                    
                    # Check for red (occupied) vs gray (empty)
                    red_pixels = np.sum(
                        (img_array[:,:,0] > 180) & 
                        (img_array[:,:,0] < 220) & 
                        (img_array[:,:,1] < 80) & 
                        (img_array[:,:,2] < 80)
                    )
                    
                    gray_pixels = np.sum(
                        (img_array[:,:,0] > 100) & 
                        (img_array[:,:,0] < 150) & 
                        (img_array[:,:,1] > 100) & 
                        (img_array[:,:,1] < 150)
                    )
                    
                    # Determine status
                    if red_pixels > gray_pixels * 2:
                        results[player_num] = "occupied"
                        self.empty_seats[player_num].set(False)
                        self.log(f"  Player {player_num}: ✓ Occupied (has name)")
                    else:
                        results[player_num] = "empty"
                        self.empty_seats[player_num].set(True)
                        self.log(f"  Player {player_num}: ○ Empty")
                        
                except Exception as e:
                    self.log(f"  Player {player_num}: ❌ Detection failed - {e}")
                    results[player_num] = "unknown"
                
                time.sleep(0.1)
            
            # Count results
            empty_count = sum(1 for v in results.values() if v == "empty")
            occupied_count = sum(1 for v in results.values() if v == "occupied")
            
            self.log(f"🔍 Detection complete!")
            self.log(f"  📊 Occupied: {occupied_count}, Empty: {empty_count}")
            self.status_label.config(text="Ready", bg='green')
            
            # Auto-fill common patterns
            if occupied_count == 4 and empty_count == 6:
                self.log("  💡 Pattern detected: 1-4 occupied, 5-10 empty (common setup)")
            
            return results
        
        # Run in thread
        thread = threading.Thread(target=detect)
        thread.daemon = True
        thread.start()
    
    def quick_detect_and_fill(self):
        """Quick detect and suggest actions"""
        self.log("⚡ Quick detect and analysis...")
        
        def quick_scan():
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Quick analysis of all players
            suggestions = []
            
            for player_num in range(1, 11):
                coords = PLAYER_COORDS[player_num]
                
                # Get pixel color at player position
                pixel = screenshot.getpixel((coords[0], coords[1]))
                
                # Simple color check
                if pixel[0] > 180 and pixel[1] < 80:  # Reddish
                    self.empty_seats[player_num].set(False)
                    suggestions.append(f"Player {player_num}: Update existing")
                else:  # Grayish
                    self.empty_seats[player_num].set(True)
                    suggestions.append(f"Player {player_num}: Register new")
            
            self.log("⚡ Quick scan complete!")
            for suggestion in suggestions:
                self.log(f"  • {suggestion}")
            
            self.status_label.config(text="Ready", bg='green')
        
        thread = threading.Thread(target=quick_scan)
        thread.daemon = True
        thread.start()
    
    def load_saved_detection(self):
        """Load previously saved detection results"""
        try:
            with open("gui_auto_config.json", 'r') as f:
                config = json.load(f)
            
            # Apply configuration
            for player_num in range(1, 11):
                if player_num in config.get("empty_seats", []):
                    self.empty_seats[player_num].set(True)
                else:
                    self.empty_seats[player_num].set(False)
                
                # Fill detected names if available
                if str(player_num) in config.get("detected_names", {}):
                    name = config["detected_names"][str(player_num)]
                    self.player_names[player_num].delete(0, tk.END)
                    self.player_names[player_num].insert(0, name)
            
            self.log(f"✅ Loaded saved detection from {config.get('timestamp', 'unknown time')}")
            
        except FileNotFoundError:
            self.log("❌ No saved detection found. Run auto-detect first.")
        except Exception as e:
            self.log(f"❌ Error loading detection: {e}")


# Main GUI class that includes auto detection
class ActionTrackerGUIWithDetection(AutoDetectionMixin):
    def __init__(self, root):
        self.root = root
        self.root.title("Action Tracker Manager - Auto Detection")
        self.root.geometry("1200x850")
        
        # Initialize variables
        self.empty_seats = {}
        self.player_names = {}
        self.delete_players = {}
        self.status_label = None
        self.log_text = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create GUI with auto detection buttons"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="ACTION TRACKER - AUTO DETECTION", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Left panel - Players
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Auto Detection Frame - NEW!
        detect_frame = tk.LabelFrame(left_panel, text="🔍 Auto Detection", 
                                    font=('Arial', 12, 'bold'), padx=10, pady=10)
        detect_frame.pack(fill=tk.X, pady=10)
        
        detect_buttons = tk.Frame(detect_frame)
        detect_buttons.pack(fill=tk.X)
        
        tk.Button(detect_buttons, text="🔍 Auto Detect All", 
                 command=self.auto_detect_players, 
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(detect_buttons, text="⚡ Quick Scan", 
                 command=self.quick_detect_and_fill,
                 bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(detect_buttons, text="💾 Load Saved", 
                 command=self.load_saved_detection,
                 bg='#34495e', fg='white', font=('Arial', 11, 'bold'),
                 width=20, height=2).pack(side=tk.LEFT, padx=5)
        
        # Player management frame
        player_frame = tk.LabelFrame(left_panel, text="Player Management", 
                                    font=('Arial', 12, 'bold'), padx=15, pady=15)
        player_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Headers
        headers = tk.Frame(player_frame)
        headers.pack(fill=tk.X, pady=5)
        
        tk.Label(headers, text="Player", font=('Arial', 11, 'bold'), width=10).pack(side=tk.LEFT)
        tk.Label(headers, text="Empty", font=('Arial', 11, 'bold'), width=8).pack(side=tk.LEFT)
        tk.Label(headers, text="Name", font=('Arial', 11, 'bold'), width=25).pack(side=tk.LEFT)
        tk.Label(headers, text="Delete", font=('Arial', 11, 'bold'), width=8).pack(side=tk.LEFT)
        
        # Player rows
        for i in range(1, 11):
            row = tk.Frame(player_frame)
            row.pack(fill=tk.X, pady=3)
            
            # Player label with status indicator
            player_label = tk.Label(row, text=f"Player {i}", font=('Arial', 11), width=10)
            player_label.pack(side=tk.LEFT)
            
            # Empty checkbox
            self.empty_seats[i] = tk.BooleanVar(value=False)
            empty_cb = tk.Checkbutton(row, variable=self.empty_seats[i],
                                     command=lambda p=i: self.on_empty_changed(p))
            empty_cb.pack(side=tk.LEFT, padx=20)
            
            # Name entry
            self.player_names[i] = tk.Entry(row, width=30, font=('Arial', 10))
            self.player_names[i].pack(side=tk.LEFT, padx=10)
            
            # Delete checkbox
            self.delete_players[i] = tk.BooleanVar(value=False)
            delete_cb = tk.Checkbutton(row, variable=self.delete_players[i])
            delete_cb.pack(side=tk.LEFT, padx=20)
        
        # Right panel - Controls
        right_panel = tk.Frame(main_container, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)
        
        # Actions
        action_frame = tk.LabelFrame(right_panel, text="Actions", 
                                    font=('Arial', 12, 'bold'), padx=15, pady=15)
        action_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(action_frame, text="UPDATE/REGISTER", 
                 command=self.process_updates, bg='#27ae60', fg='white',
                 font=('Arial', 12, 'bold'), height=2).pack(fill=tk.X, pady=5)
        
        tk.Button(action_frame, text="DELETE SELECTED", 
                 command=self.process_deletes, bg='#e74c3c', fg='white',
                 font=('Arial', 12, 'bold'), height=2).pack(fill=tk.X, pady=5)
        
        # Status
        self.status_label = tk.Label(action_frame, text="Ready", 
                                    bg='green', fg='white', font=('Arial', 11, 'bold'))
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Log
        log_frame = tk.LabelFrame(right_panel, text="Log", 
                                 font=('Arial', 12, 'bold'), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=20, width=45, font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log("System ready. Click 'Auto Detect All' to scan players.")
    
    def log(self, message):
        """Add message to log"""
        if self.log_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
            self.root.update()
    
    def on_empty_changed(self, player_num):
        """Handle empty checkbox change"""
        if self.empty_seats[player_num].get():
            self.delete_players[player_num].set(False)
            self.log(f"Player {player_num} marked as empty")
        else:
            self.log(f"Player {player_num} marked as occupied")
    
    def process_updates(self):
        """Process updates (placeholder)"""
        self.log("Processing updates...")
        # Implementation here
    
    def process_deletes(self):
        """Process deletes (placeholder)"""
        self.log("Processing deletes...")
        # Implementation here


def main():
    root = tk.Tk()
    app = ActionTrackerGUIWithDetection(root)
    root.mainloop()


if __name__ == "__main__":
    main()