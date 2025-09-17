"""
Action Tracker GUI Manager
GUI-based player management system
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
        self.root.title("Action Tracker Manager GUI")
        self.root.geometry("800x700")
        
        # Speed settings
        self.speeds = {
            "mouse_click_delay": 0.3,
            "keyboard_type_interval": 0.02,
            "action_delay": 0.5,
            "screen_wait": 1.0,
            "pyautogui_pause": 0.3
        }
        
        # Player data
        self.empty_seats = {}
        self.player_names = {}
        self.delete_players = {}
        
        # Log
        self.log_text = None
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="ACTION TRACKER MANAGER", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=15)
        
        # Main container with scrollbar
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Player management
        left_panel = tk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Player list frame
        player_frame = tk.LabelFrame(left_panel, text="Player Management", 
                                    font=('Arial', 12, 'bold'), padx=10, pady=10)
        player_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Headers
        headers_frame = tk.Frame(player_frame)
        headers_frame.grid(row=0, column=0, columnspan=5, sticky='w', pady=5)
        
        tk.Label(headers_frame, text="Player", font=('Arial', 10, 'bold'), width=8).grid(row=0, column=0)
        tk.Label(headers_frame, text="Empty", font=('Arial', 10, 'bold'), width=6).grid(row=0, column=1)
        tk.Label(headers_frame, text="Player Name", font=('Arial', 10, 'bold'), width=20).grid(row=0, column=2)
        tk.Label(headers_frame, text="Delete", font=('Arial', 10, 'bold'), width=6).grid(row=0, column=3)
        
        # Player rows
        for i in range(1, 11):
            row_frame = tk.Frame(player_frame)
            row_frame.grid(row=i, column=0, columnspan=5, sticky='w', pady=2)
            
            # Player number
            tk.Label(row_frame, text=f"Player {i}", width=8).grid(row=0, column=0)
            
            # Empty checkbox
            self.empty_seats[i] = tk.BooleanVar(value=False)
            empty_cb = tk.Checkbutton(row_frame, variable=self.empty_seats[i],
                                     command=lambda p=i: self.on_empty_changed(p))
            empty_cb.grid(row=0, column=1, padx=10)
            
            # Name entry
            self.player_names[i] = tk.Entry(row_frame, width=25)
            self.player_names[i].grid(row=0, column=2, padx=5)
            
            # Delete checkbox
            self.delete_players[i] = tk.BooleanVar(value=False)
            delete_cb = tk.Checkbutton(row_frame, variable=self.delete_players[i])
            delete_cb.grid(row=0, column=3, padx=10)
        
        # Quick fill section
        quick_frame = tk.LabelFrame(left_panel, text="Quick Actions", 
                                   font=('Arial', 10, 'bold'), padx=10, pady=5)
        quick_frame.pack(fill=tk.X, padx=5, pady=10)
        
        button_row1 = tk.Frame(quick_frame)
        button_row1.pack(fill=tk.X, pady=2)
        
        tk.Button(button_row1, text="Mark 1-4 as Occupied", 
                 command=self.mark_1_4_occupied, width=18).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row1, text="Mark 5-10 as Empty", 
                 command=self.mark_5_10_empty, width=18).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row1, text="Clear All", 
                 command=self.clear_all, width=18).pack(side=tk.LEFT, padx=2)
        
        button_row2 = tk.Frame(quick_frame)
        button_row2.pack(fill=tk.X, pady=2)
        
        tk.Button(button_row2, text="Fill Test Names", 
                 command=self.fill_test_names, width=18).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row2, text="Select All Delete", 
                 command=self.select_all_delete, width=18).pack(side=tk.LEFT, padx=2)
        tk.Button(button_row2, text="Deselect All", 
                 command=self.deselect_all_delete, width=18).pack(side=tk.LEFT, padx=2)
        
        # Right panel - Controls and Log
        right_panel = tk.Frame(main_container, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        
        # Speed control frame
        speed_frame = tk.LabelFrame(right_panel, text="Speed Settings", 
                                   font=('Arial', 10, 'bold'), padx=10, pady=5)
        speed_frame.pack(fill=tk.X, pady=5)
        
        speed_options = ["Fast", "Normal", "Slow", "Custom"]
        self.speed_var = tk.StringVar(value="Normal")
        
        for option in speed_options:
            tk.Radiobutton(speed_frame, text=option, variable=self.speed_var,
                          value=option, command=self.update_speed).pack(anchor='w')
        
        # Action buttons
        action_frame = tk.LabelFrame(right_panel, text="Actions", 
                                    font=('Arial', 10, 'bold'), padx=10, pady=10)
        action_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(action_frame, text="UPDATE/REGISTER NAMES", 
                 command=self.process_updates, bg='#27ae60', fg='white',
                 font=('Arial', 11, 'bold'), height=2).pack(fill=tk.X, pady=3)
        
        tk.Button(action_frame, text="DELETE SELECTED", 
                 command=self.process_deletes, bg='#e74c3c', fg='white',
                 font=('Arial', 11, 'bold'), height=2).pack(fill=tk.X, pady=3)
        
        tk.Button(action_frame, text="PROCESS ALL", 
                 command=self.process_all, bg='#3498db', fg='white',
                 font=('Arial', 11, 'bold'), height=2).pack(fill=tk.X, pady=3)
        
        # Status indicator
        self.status_label = tk.Label(action_frame, text="Ready", 
                                    bg='green', fg='white', font=('Arial', 10))
        self.status_label.pack(fill=tk.X, pady=5)
        
        # Log frame
        log_frame = tk.LabelFrame(right_panel, text="Log", 
                                 font=('Arial', 10, 'bold'), padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Log text with scrollbar
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=35, 
                                yscrollcommand=log_scroll.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        # Bottom buttons
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(bottom_frame, text="Screenshot", 
                 command=self.take_screenshot, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Clear Log", 
                 command=self.clear_log, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Save Log", 
                 command=self.save_log, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Exit", 
                 command=self.root.quit, width=15).pack(side=tk.RIGHT, padx=5)
    
    def on_empty_changed(self, player_num):
        """Handle empty checkbox change"""
        if self.empty_seats[player_num].get():
            # If marked as empty, clear delete checkbox
            self.delete_players[player_num].set(False)
            self.log(f"Player {player_num} marked as empty seat")
        else:
            self.log(f"Player {player_num} marked as occupied")
    
    def mark_1_4_occupied(self):
        """Mark players 1-4 as occupied"""
        for i in range(1, 5):
            self.empty_seats[i].set(False)
        self.log("Players 1-4 marked as occupied")
    
    def mark_5_10_empty(self):
        """Mark players 5-10 as empty"""
        for i in range(5, 11):
            self.empty_seats[i].set(True)
        self.log("Players 5-10 marked as empty")
    
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
        self.log("Test names filled")
    
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
    
    def update_speed(self):
        """Update speed settings based on selection"""
        speed = self.speed_var.get()
        
        if speed == "Fast":
            self.speeds = {
                "mouse_click_delay": 0.1,
                "keyboard_type_interval": 0.01,
                "action_delay": 0.2,
                "screen_wait": 0.5,
                "pyautogui_pause": 0.1
            }
        elif speed == "Normal":
            self.speeds = {
                "mouse_click_delay": 0.3,
                "keyboard_type_interval": 0.02,
                "action_delay": 0.5,
                "screen_wait": 1.0,
                "pyautogui_pause": 0.3
            }
        elif speed == "Slow":
            self.speeds = {
                "mouse_click_delay": 0.5,
                "keyboard_type_interval": 0.05,
                "action_delay": 1.0,
                "screen_wait": 2.0,
                "pyautogui_pause": 0.5
            }
        
        pyautogui.PAUSE = self.speeds["pyautogui_pause"]
        self.log(f"Speed set to: {speed}")
    
    def log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Clear log text"""
        self.log_text.delete(1.0, tk.END)
    
    def save_log(self):
        """Save log to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gui_log_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(self.log_text.get(1.0, tk.END))
        
        self.log(f"Log saved to {filename}")
        messagebox.showinfo("Success", f"Log saved to {filename}")
    
    def take_screenshot(self):
        """Take screenshot"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"gui_screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        self.log(f"Screenshot saved: {filename}")
    
    def update_existing_name(self, player_num, new_name):
        """Update existing player name"""
        try:
            coords = PLAYER_COORDS[player_num]
            
            # Click player
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speeds["screen_wait"])
            
            # Click name field
            pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
            time.sleep(self.speeds["mouse_click_delay"])
            
            # Clear and type
            pyautogui.tripleClick()
            time.sleep(0.2)
            pyautogui.typewrite(new_name, interval=self.speeds["keyboard_type_interval"])
            time.sleep(self.speeds["action_delay"])
            
            # Press Enter
            pyautogui.press('enter')
            time.sleep(self.speeds["action_delay"])
            
            # Complete
            pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
            time.sleep(self.speeds["screen_wait"])
            
            return True
        except Exception as e:
            self.log(f"Error updating player {player_num}: {e}")
            return False
    
    def register_new_name(self, player_num, new_name):
        """Register new player name"""
        try:
            coords = PLAYER_COORDS[player_num]
            
            # Click player
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speeds["mouse_click_delay"])
            
            # Type name
            pyautogui.typewrite(new_name, interval=self.speeds["keyboard_type_interval"])
            time.sleep(self.speeds["action_delay"])
            
            # Press Enter
            pyautogui.press('enter')
            time.sleep(self.speeds["action_delay"])
            
            return True
        except Exception as e:
            self.log(f"Error registering player {player_num}: {e}")
            return False
    
    def delete_player(self, player_num):
        """Delete player"""
        try:
            coords = PLAYER_COORDS[player_num]
            
            # Click player
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speeds["screen_wait"])
            
            # Click delete
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(self.speeds["screen_wait"])
            
            return True
        except Exception as e:
            self.log(f"Error deleting player {player_num}: {e}")
            return False
    
    def process_updates(self):
        """Process name updates and registrations"""
        def run():
            self.status_label.config(text="Processing...", bg='orange')
            self.log("Starting name updates...")
            
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
                            self.log(f"Player {i} registered successfully")
                    else:
                        # Update existing name
                        self.log(f"Updating Player {i}: {name}")
                        if self.update_existing_name(i, name):
                            success += 1
                            self.log(f"Player {i} updated successfully")
                    
                    time.sleep(self.speeds["action_delay"])
            
            self.log(f"Updates complete: {success}/{total} successful")
            self.status_label.config(text="Ready", bg='green')
            
            if success == total:
                messagebox.showinfo("Success", f"All {total} updates completed successfully!")
            elif success > 0:
                messagebox.showwarning("Partial Success", f"{success}/{total} updates completed")
            
        # Run in thread to prevent GUI freeze
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def process_deletes(self):
        """Process deletions"""
        def run():
            self.status_label.config(text="Processing...", bg='orange')
            self.log("Starting deletions...")
            
            success = 0
            total = 0
            
            for i in range(1, 11):
                if self.delete_players[i].get():
                    total += 1
                    self.log(f"Deleting Player {i}")
                    if self.delete_player(i):
                        success += 1
                        self.log(f"Player {i} deleted successfully")
                    time.sleep(self.speeds["action_delay"])
            
            self.log(f"Deletions complete: {success}/{total} successful")
            self.status_label.config(text="Ready", bg='green')
            
            if total > 0:
                if success == total:
                    messagebox.showinfo("Success", f"All {total} deletions completed!")
                else:
                    messagebox.showwarning("Partial Success", f"{success}/{total} deletions completed")
            else:
                messagebox.showinfo("Info", "No players selected for deletion")
        
        # Confirm before deletion
        to_delete = [i for i in range(1, 11) if self.delete_players[i].get()]
        if to_delete:
            if messagebox.askyesno("Confirm", f"Delete players: {to_delete}?"):
                thread = threading.Thread(target=run)
                thread.daemon = True
                thread.start()
        else:
            messagebox.showinfo("Info", "No players selected for deletion")
    
    def process_all(self):
        """Process all operations"""
        def run():
            self.status_label.config(text="Processing...", bg='orange')
            self.log("Starting all operations...")
            
            # First process updates/registrations
            for i in range(1, 11):
                name = self.player_names[i].get().strip()
                if name and not self.delete_players[i].get():
                    if self.empty_seats[i].get():
                        self.log(f"Registering Player {i}: {name}")
                        self.register_new_name(i, name)
                    else:
                        self.log(f"Updating Player {i}: {name}")
                        self.update_existing_name(i, name)
                    time.sleep(self.speeds["action_delay"])
            
            # Then process deletions
            for i in range(1, 11):
                if self.delete_players[i].get():
                    self.log(f"Deleting Player {i}")
                    self.delete_player(i)
                    time.sleep(self.speeds["action_delay"])
            
            self.log("All operations complete")
            self.status_label.config(text="Ready", bg='green')
            messagebox.showinfo("Complete", "All operations completed!")
        
        if messagebox.askyesno("Confirm", "Process all operations?\nThis will update/register names and delete selected players."):
            thread = threading.Thread(target=run)
            thread.daemon = True
            thread.start()


def main():
    root = tk.Tk()
    app = ActionTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()