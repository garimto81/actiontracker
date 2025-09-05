"""
Smart Name Updater for Action Tracker
Handles both existing and non-existing player names with different processes
"""

import pyautogui
import time
import cv2
import numpy as np
from PIL import Image
from datetime import datetime

class SmartNameUpdater:
    def __init__(self):
        """Initialize smart name updater with both update processes"""
        # Safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.2
        
        # 10 player coordinates (confirmed working)
        self.player_coords = {
            1: (215, 354),
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
        
        # Timing settings
        self.click_delay = 0.3
        self.type_delay = 0.02
        self.dropdown_wait = 0.5  # Wait for dropdown to appear
        self.detection_wait = 0.8  # Wait before detecting dropdown
        
    def capture_screenshot(self, filename=None):
        """Capture screenshot for debugging"""
        screenshot = pyautogui.screenshot()
        if filename:
            screenshot.save(filename)
            print(f"Screenshot saved: {filename}")
        return screenshot
    
    def detect_dropdown_list(self, region=None):
        """
        Detect if a dropdown list appeared after clicking name field
        Returns True if dropdown detected, False otherwise
        """
        print("Checking for dropdown list...")
        time.sleep(self.detection_wait)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Look for dropdown indicators (typically darker background or list items)
        # Check for characteristic dropdown features:
        # 1. Darker rectangular area below the input field
        # 2. Multiple selectable items in a list
        
        if region:
            # Focus on specific region if provided
            x, y, w, h = region
            img_cv = img_cv[y:y+h, x:x+w]
        
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Look for rectangular shapes (dropdown borders)
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check for large rectangular contours (potential dropdown)
        dropdown_detected = False
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 5000:  # Significant area
                x, y, w, h = cv2.boundingRect(contour)
                if w > 100 and h > 50:  # Dropdown-like dimensions
                    dropdown_detected = True
                    break
        
        # Alternative: Check for color changes indicating dropdown
        # Dropdowns often have different background colors
        if not dropdown_detected:
            # Check for significant dark areas (common dropdown background)
            dark_pixels = np.sum(gray < 80)
            total_pixels = gray.size
            dark_ratio = dark_pixels / total_pixels
            
            if dark_ratio > 0.15:  # More than 15% dark pixels might indicate dropdown
                dropdown_detected = True
        
        if dropdown_detected:
            print("✓ Dropdown list detected - Name exists!")
            self.capture_screenshot(f"dropdown_detected_{datetime.now().strftime('%H%M%S')}.png")
        else:
            print("✗ No dropdown detected - Name is new!")
            
        return dropdown_detected
    
    def update_existing_name(self, player_num, new_name):
        """
        Process for updating when name already exists in the system
        Process: Click name → Select from dropdown → Modify → Enter → Confirm
        """
        print(f"[Existing Name Process] Player {player_num}: {new_name}")
        
        coords = self.player_coords[player_num]
        
        try:
            # Step 1: Click player name field
            print(f"  1. Clicking player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.click_delay)
            
            # Step 2: Double-click to open edit mode
            print(f"  2. Double-clicking to enter edit mode")
            pyautogui.doubleClick()
            time.sleep(self.dropdown_wait)
            
            # Step 3: Wait for dropdown and select first item (or click again)
            print(f"  3. Selecting from dropdown list")
            # Click slightly below to select from dropdown
            pyautogui.click(coords[0], coords[1] + 30)
            time.sleep(self.click_delay)
            
            # Step 4: Clear and type new name
            print(f"  4. Clearing and entering new name: {new_name}")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.typewrite(new_name, interval=self.type_delay)
            time.sleep(0.2)
            
            # Step 5: Press Enter
            print(f"  5. Pressing Enter to confirm")
            pyautogui.press('enter')
            time.sleep(self.click_delay)
            
            # Step 6: Click confirmation if needed (click elsewhere or specific confirm button)
            print(f"  6. Final confirmation")
            # Click somewhere else to confirm (or specific confirm button if exists)
            pyautogui.click(coords[0] + 200, coords[1])
            time.sleep(self.click_delay)
            
            print(f"  ✓ Player {player_num} updated (existing name process)")
            return True
            
        except Exception as e:
            print(f"  ✗ Error updating player {player_num}: {e}")
            return False
    
    def update_new_name(self, player_num, new_name):
        """
        Process for updating when name doesn't exist in the system
        Process: Click name → Modify → Enter
        """
        print(f"[New Name Process] Player {player_num}: {new_name}")
        
        coords = self.player_coords[player_num]
        
        try:
            # Step 1: Click player name field
            print(f"  1. Clicking player {player_num} at {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.click_delay)
            
            # Step 2: Double-click to enter edit mode
            print(f"  2. Double-clicking to enter edit mode")
            pyautogui.doubleClick()
            time.sleep(0.5)
            
            # Step 3: Clear and type new name
            print(f"  3. Entering new name: {new_name}")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.typewrite(new_name, interval=self.type_delay)
            time.sleep(0.2)
            
            # Step 4: Press Enter
            print(f"  4. Pressing Enter to confirm")
            pyautogui.press('enter')
            time.sleep(self.click_delay)
            
            print(f"  ✓ Player {player_num} updated (new name process)")
            return True
            
        except Exception as e:
            print(f"  ✗ Error updating player {player_num}: {e}")
            return False
    
    def smart_update_player(self, player_num, new_name):
        """
        Smart update that detects whether name exists and uses appropriate process
        """
        print(f"\nSmart Update - Player {player_num}: {new_name}")
        print("-" * 50)
        
        coords = self.player_coords[player_num]
        
        try:
            # Initial click to test for dropdown
            print("Testing for existing name...")
            pyautogui.click(coords[0], coords[1])
            time.sleep(self.click_delay)
            pyautogui.doubleClick()
            
            # Detect if dropdown appears
            dropdown_region = (coords[0] - 50, coords[1] - 20, 300, 200)
            has_dropdown = self.detect_dropdown_list(dropdown_region)
            
            # Press ESC to cancel current action
            pyautogui.press('esc')
            time.sleep(0.3)
            
            # Use appropriate update process
            if has_dropdown:
                return self.update_existing_name(player_num, new_name)
            else:
                return self.update_new_name(player_num, new_name)
                
        except Exception as e:
            print(f"Error in smart update: {e}")
            return False
    
    def update_multiple_players(self, player_updates):
        """
        Update multiple players with smart detection
        player_updates: dict of {player_num: new_name}
        """
        print("="*60)
        print("SMART MULTI-PLAYER UPDATE")
        print("="*60)
        
        results = {}
        start_time = time.time()
        
        for player_num, new_name in player_updates.items():
            if player_num in self.player_coords:
                success = self.smart_update_player(player_num, new_name)
                results[player_num] = success
            else:
                print(f"Invalid player number: {player_num}")
                results[player_num] = False
        
        # Summary
        elapsed = time.time() - start_time
        success_count = sum(1 for s in results.values() if s)
        
        print("\n" + "="*60)
        print("UPDATE SUMMARY")
        print("="*60)
        print(f"Success: {success_count}/{len(player_updates)} players")
        print(f"Time: {elapsed:.1f} seconds")
        
        # Final screenshot
        self.capture_screenshot(f"smart_update_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        return results

def test_detection_only():
    """Test dropdown detection without updating"""
    updater = SmartNameUpdater()
    
    print("DETECTION TEST MODE")
    print("="*40)
    print("Click on a player name and I'll detect if dropdown appears")
    print("Starting in 3 seconds...")
    
    time.sleep(3)
    
    # Test player 1
    coords = updater.player_coords[1]
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.3)
    pyautogui.doubleClick()
    
    has_dropdown = updater.detect_dropdown_list()
    
    pyautogui.press('esc')
    
    print(f"\nDetection Result: {'Existing name' if has_dropdown else 'New name'}")

def main():
    """Main execution"""
    updater = SmartNameUpdater()
    
    print("Smart Name Updater for Action Tracker")
    print("====================================")
    print("\nOptions:")
    print("1. Test detection only")
    print("2. Update single player (smart)")
    print("3. Update all 10 players")
    print("4. Custom update list")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        test_detection_only()
        
    elif choice == "2":
        player_num = int(input("Player number (1-10): "))
        new_name = input("New name: ").strip()
        
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        success = updater.smart_update_player(player_num, new_name)
        print(f"\nResult: {'Success' if success else 'Failed'}")
        
    elif choice == "3":
        # Test with mix of potentially existing and new names
        test_names = {
            1: "Alice Johnson",
            2: "Bob Smith",
            3: "Charlie Brown",
            4: "David Lee",
            5: "Emma Wilson",
            6: "Frank Miller",
            7: "Grace Chen",
            8: "Henry Taylor",
            9: "Ivy Anderson",
            10: "Jack Robinson"
        }
        
        print("\nUpdating all 10 players...")
        print("Starting in 3 seconds...")
        time.sleep(3)
        
        updater.update_multiple_players(test_names)
        
    elif choice == "4":
        players = {}
        print("\nEnter player updates (empty name to finish):")
        while True:
            try:
                num = input("Player number (1-10): ").strip()
                if not num:
                    break
                num = int(num)
                if num < 1 or num > 10:
                    print("Invalid player number")
                    continue
                name = input(f"New name for player {num}: ").strip()
                if name:
                    players[num] = name
            except ValueError:
                print("Invalid input")
                continue
        
        if players:
            print(f"\nUpdating {len(players)} players...")
            print("Starting in 3 seconds...")
            time.sleep(3)
            
            updater.update_multiple_players(players)
        else:
            print("No players to update")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()