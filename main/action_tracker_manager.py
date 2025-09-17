"""
Action Tracker Manager - Integrated App
Unified management for name update, register, and delete
"""

import pyautogui
import time
from datetime import datetime
import json
import os

# Safety settings
pyautogui.FAILSAFE = True

# Coordinates
PLAYERS = {
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

SUB_NAME_FIELD = (785, 291)    # Sub screen name field
COMPLETE_BUTTON = (1720, 139)  # Complete button
DELETE_BUTTON = (721, 112)     # Delete button

# Speed settings (in seconds)
DEFAULT_SPEEDS = {
    "mouse_click_delay": 0.3,      # Delay after mouse click
    "keyboard_type_interval": 0.02, # Interval between keystrokes
    "action_delay": 0.5,            # Delay between actions
    "screen_wait": 1.0,             # Wait for screen transitions
    "pyautogui_pause": 0.3          # PyAutoGUI global pause
}

class ActionTrackerManager:
    def __init__(self, custom_speeds=None):
        """Initialize with custom or default speed settings"""
        self.speeds = DEFAULT_SPEEDS.copy()
        if custom_speeds:
            self.speeds.update(custom_speeds)
        
        # Apply PyAutoGUI global pause
        pyautogui.PAUSE = self.speeds["pyautogui_pause"]
        
        self.log = []
        
    def log_action(self, message):
        """Log action with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.log.append(log_entry)
    
    def save_log(self, filename=None):
        """Save log to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"action_log_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("\n".join(self.log))
        self.log_action(f"Log saved to: {filename}")
    
    def take_screenshot(self, prefix="screenshot"):
        """Take and save screenshot"""
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        self.log_action(f"Screenshot saved: {filename}")
        return filename
    
    def update_existing_name(self, player_num, new_name):
        """
        Function 1: Update existing name
        For players with existing names
        """
        self.log_action(f"=== UPDATE EXISTING NAME ===")
        self.log_action(f"Player {player_num}: {new_name}")
        
        if player_num not in PLAYERS:
            self.log_action(f"ERROR: Invalid player number {player_num}")
            return False
        
        try:
            coords = PLAYERS[player_num]
            
            # Step 1: Click player
            self.log_action(f"Step 1: Click Player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speeds["screen_wait"])
            
            # Step 2: Click name field
            self.log_action(f"Step 2: Click name field at {SUB_NAME_FIELD}")
            pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
            time.sleep(self.speeds["mouse_click_delay"])
            
            # Step 3: Clear and type new name
            self.log_action(f"Step 3: Clear and type: {new_name}")
            pyautogui.tripleClick()  # Select all
            time.sleep(0.2)
            pyautogui.typewrite(new_name, interval=self.speeds["keyboard_type_interval"])
            time.sleep(self.speeds["action_delay"])
            
            # Step 4: Press Enter
            self.log_action("Step 4: Press Enter")
            pyautogui.press('enter')
            time.sleep(self.speeds["action_delay"])
            
            # Step 5: Click complete
            self.log_action(f"Step 5: Click complete at {COMPLETE_BUTTON}")
            pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
            time.sleep(self.speeds["screen_wait"])
            
            self.log_action(f"SUCCESS: Player {player_num} updated")
            return True
            
        except Exception as e:
            self.log_action(f"ERROR: {e}")
            return False
    
    def register_new_name(self, player_num, new_name):
        """
        Function 2: Register new name for empty seat
        For empty player positions
        """
        self.log_action(f"=== REGISTER NEW NAME ===")
        self.log_action(f"Player {player_num}: {new_name}")
        
        if player_num not in PLAYERS:
            self.log_action(f"ERROR: Invalid player number {player_num}")
            return False
        
        try:
            coords = PLAYERS[player_num]
            
            # Step 1: Click player
            self.log_action(f"Step 1: Click Player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speeds["mouse_click_delay"])
            
            # Step 2: Type name directly
            self.log_action(f"Step 2: Type name: {new_name}")
            pyautogui.typewrite(new_name, interval=self.speeds["keyboard_type_interval"])
            time.sleep(self.speeds["action_delay"])
            
            # Step 3: Press Enter
            self.log_action("Step 3: Press Enter")
            pyautogui.press('enter')
            time.sleep(self.speeds["action_delay"])
            
            self.log_action(f"SUCCESS: Player {player_num} registered")
            return True
            
        except Exception as e:
            self.log_action(f"ERROR: {e}")
            return False
    
    def delete_player(self, player_num):
        """
        Function 3: Delete player name
        Remove player from position
        """
        self.log_action(f"=== DELETE PLAYER ===")
        self.log_action(f"Player {player_num}")
        
        if player_num not in PLAYERS:
            self.log_action(f"ERROR: Invalid player number {player_num}")
            return False
        
        try:
            coords = PLAYERS[player_num]
            
            # Step 1: Click player
            self.log_action(f"Step 1: Click Player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.speeds["screen_wait"])
            
            # Step 2: Click delete button
            self.log_action(f"Step 2: Click Delete at {DELETE_BUTTON}")
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(self.speeds["screen_wait"])
            
            self.log_action(f"SUCCESS: Player {player_num} deleted")
            return True
            
        except Exception as e:
            self.log_action(f"ERROR: {e}")
            return False
    
    def batch_update(self, updates):
        """
        Batch update multiple players
        updates = [
            {"player": 1, "action": "update", "name": "John Doe"},
            {"player": 2, "action": "register", "name": "Jane Doe"},
            {"player": 3, "action": "delete"}
        ]
        """
        self.log_action("=== BATCH UPDATE START ===")
        self.take_screenshot("batch_before")
        
        success_count = 0
        total_count = len(updates)
        
        for update in updates:
            player = update.get("player")
            action = update.get("action")
            name = update.get("name", "")
            
            if action == "update":
                if self.update_existing_name(player, name):
                    success_count += 1
            elif action == "register":
                if self.register_new_name(player, name):
                    success_count += 1
            elif action == "delete":
                if self.delete_player(player):
                    success_count += 1
            else:
                self.log_action(f"Unknown action: {action}")
            
            time.sleep(self.speeds["action_delay"])
        
        self.take_screenshot("batch_after")
        self.log_action(f"=== BATCH UPDATE COMPLETE ===")
        self.log_action(f"Success: {success_count}/{total_count}")
        
        return success_count, total_count
    
    def show_speed_settings(self):
        """Display current speed settings"""
        print("\n=== CURRENT SPEED SETTINGS ===")
        for key, value in self.speeds.items():
            print(f"  {key}: {value} seconds")
        print("="*40)
    
    def update_speed_settings(self, new_speeds):
        """Update speed settings"""
        self.speeds.update(new_speeds)
        pyautogui.PAUSE = self.speeds["pyautogui_pause"]
        self.log_action("Speed settings updated")


def interactive_menu():
    """Interactive menu for the application"""
    manager = ActionTrackerManager()
    
    while True:
        print("\n" + "="*50)
        print("ACTION TRACKER MANAGER")
        print("="*50)
        print("1. Update existing name")
        print("2. Register new name (empty seat)")
        print("3. Delete player")
        print("4. Batch update")
        print("5. Speed settings")
        print("6. Take screenshot")
        print("7. Save log")
        print("0. Exit")
        print("-"*50)
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            player = int(input("Player number (1-10): "))
            name = input("New name: ").strip()
            print("\nStarting in 3 seconds...")
            time.sleep(3)
            manager.update_existing_name(player, name)
            
        elif choice == "2":
            player = int(input("Player number (1-10): "))
            name = input("New name: ").strip()
            print("\nStarting in 3 seconds...")
            time.sleep(3)
            manager.register_new_name(player, name)
            
        elif choice == "3":
            player = int(input("Player number to delete (1-10): "))
            print("\nStarting in 3 seconds...")
            time.sleep(3)
            manager.delete_player(player)
            
        elif choice == "4":
            print("\nBatch Update Instructions:")
            print("Enter updates in format: player,action,name")
            print("Actions: update, register, delete")
            print("Example: 1,update,John Doe")
            print("Enter empty line to finish")
            
            updates = []
            while True:
                line = input("> ").strip()
                if not line:
                    break
                
                parts = line.split(',')
                if len(parts) >= 2:
                    player = int(parts[0])
                    action = parts[1]
                    name = parts[2] if len(parts) > 2 else ""
                    updates.append({"player": player, "action": action, "name": name})
            
            if updates:
                print(f"\nProcessing {len(updates)} updates in 3 seconds...")
                time.sleep(3)
                manager.batch_update(updates)
            
        elif choice == "5":
            manager.show_speed_settings()
            print("\nSpeed Setting Options:")
            print("1. Use fast preset")
            print("2. Use normal preset")
            print("3. Use slow preset")
            print("4. Custom settings")
            
            speed_choice = input("Select: ").strip()
            
            if speed_choice == "1":  # Fast
                new_speeds = {
                    "mouse_click_delay": 0.1,
                    "keyboard_type_interval": 0.01,
                    "action_delay": 0.2,
                    "screen_wait": 0.5,
                    "pyautogui_pause": 0.1
                }
                manager.update_speed_settings(new_speeds)
                print("Fast preset applied")
                
            elif speed_choice == "2":  # Normal
                manager.update_speed_settings(DEFAULT_SPEEDS)
                print("Normal preset applied")
                
            elif speed_choice == "3":  # Slow
                new_speeds = {
                    "mouse_click_delay": 0.5,
                    "keyboard_type_interval": 0.05,
                    "action_delay": 1.0,
                    "screen_wait": 2.0,
                    "pyautogui_pause": 0.5
                }
                manager.update_speed_settings(new_speeds)
                print("Slow preset applied")
                
            elif speed_choice == "4":  # Custom
                print("\nEnter custom values (press Enter for default):")
                new_speeds = {}
                for key in DEFAULT_SPEEDS:
                    val = input(f"{key} (current: {manager.speeds[key]}): ").strip()
                    if val:
                        new_speeds[key] = float(val)
                if new_speeds:
                    manager.update_speed_settings(new_speeds)
                    print("Custom settings applied")
            
        elif choice == "6":
            manager.take_screenshot()
            
        elif choice == "7":
            manager.save_log()
            
        elif choice == "0":
            print("Exiting...")
            break
        
        else:
            print("Invalid option")


if __name__ == "__main__":
    print("ACTION TRACKER MANAGER")
    print("Integrated management for player names")
    print()
    
    interactive_menu()