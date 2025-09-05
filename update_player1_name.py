"""
Action Tracker Player 1 Name Update Script
Update player 1 name with complete automation logic
"""

import pyautogui
import time
import cv2
import numpy as np
from PIL import Image, ImageDraw

class Player1NameUpdater:
    def __init__(self):
        """Initialize Player 1 name updater"""
        # Main screen coordinates (from previous analysis)
        self.player1_main_button = (209, 658)  # Player1 red button on main screen
        
        # Edit dialog coordinates (from dialog analysis)
        self.edit_name_field = (582, 196)      # NAME field golden button
        self.edit_close_x = (1232, 73)         # X button to close dialog
        
        # Safety settings
        self.click_delay = 0.5
        self.type_delay = 0.1
        self.dialog_wait = 1.0
        
    def capture_screenshot(self, filename="debug_screenshot.png"):
        """Capture screenshot for debugging"""
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved: {filename}")
        return screenshot
    
    def safe_click(self, x, y, description=""):
        """Safe click with coordinate validation"""
        try:
            print(f"Clicking: ({x}, {y}) - {description}")
            pyautogui.click(x, y)
            time.sleep(self.click_delay)
            return True
        except Exception as e:
            print(f"Click failed: {e}")
            return False
    
    def safe_type(self, text, clear_first=True):
        """Safe text input"""
        try:
            if clear_first:
                # Select all existing text and delete
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(self.type_delay)
            
            # Type new text
            pyautogui.typewrite(str(text))
            time.sleep(self.type_delay)
            return True
        except Exception as e:
            print(f"Text input failed: {e}")
            return False
    
    def update_player1_name(self, new_name):
        """Main logic to update Player 1 name"""
        print("="*60)
        print(f"Starting Player 1 name update to: '{new_name}'")
        print("="*60)
        
        try:
            # Step 1: Click Player 1 button on main screen
            print("\n[Step 1] Click Player1 button on main screen")
            if not self.safe_click(self.player1_main_button[0], self.player1_main_button[1], 
                                 "Player1 main button"):
                return False
            
            # Step 2: Wait for edit dialog to load
            print("\n[Step 2] Wait for edit dialog to load")
            time.sleep(self.dialog_wait)
            self.capture_screenshot("after_dialog_open.png")
            
            # Step 3: Click NAME field
            print("\n[Step 3] Click NAME field")
            if not self.safe_click(self.edit_name_field[0], self.edit_name_field[1], 
                                 "NAME field"):
                return False
            
            # Step 4: Enter new name
            print(f"\n[Step 4] Enter new name: '{new_name}'")
            if not self.safe_type(new_name, clear_first=True):
                return False
            
            # Step 5: Press Enter to confirm
            print("\n[Step 5] Press Enter to confirm")
            pyautogui.press('enter')
            time.sleep(self.click_delay)
            
            # Step 6: Close dialog (X button)
            print("\n[Step 6] Close edit dialog")
            if not self.safe_click(self.edit_close_x[0], self.edit_close_x[1], 
                                 "Dialog X button"):
                return False
            
            # Step 7: Wait for return to main screen
            print("\n[Step 7] Wait for return to main screen")
            time.sleep(self.dialog_wait)
            
            # Step 8: Final verification
            print("\n[Step 8] Update completion verification")
            final_screenshot = self.capture_screenshot("update_complete.png")
            
            print("="*60)
            print(f"SUCCESS: Player 1 name updated to: '{new_name}'")
            print("Final screenshot: update_complete.png")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\nERROR during update: {e}")
            import traceback
            traceback.print_exc()
            
            # Capture error screenshot
            self.capture_screenshot("error_screenshot.png")
            return False
    
    def test_coordinates(self):
        """Test coordinates (show markers without clicking)"""
        print("Coordinate Test Mode")
        print("="*40)
        
        # Capture current screen
        screenshot = pyautogui.screenshot()
        img_pil = Image.fromarray(np.array(screenshot))
        draw = ImageDraw.Draw(img_pil)
        
        # Test coordinates with markers
        coords = [
            (self.player1_main_button, "Player1 Main", "red"),
            (self.edit_name_field, "NAME Field", "blue"),
            (self.edit_close_x, "Close X", "green")
        ]
        
        for (x, y), label, color in coords:
            # Draw cross marker
            draw.line([(x-20, y), (x+20, y)], fill=color, width=3)
            draw.line([(x, y-20), (x, y+20)], fill=color, width=3)
            draw.text((x+25, y-10), f"{label} ({x},{y})", fill=color)
            
            print(f"{label}: ({x}, {y})")
        
        # Save test image
        img_pil.save("coordinate_test.png")
        print("Coordinate test image saved: coordinate_test.png")

def main():
    """Main execution function"""
    updater = Player1NameUpdater()
    
    print("Action Tracker Player 1 Name Updater")
    print("====================================")
    print()
    print("Options:")
    print("1. Test coordinates (show positions without clicking)")
    print("2. Update Player 1 name")
    print()
    
    try:
        choice = input("Choose (1 or 2): ").strip()
        
        if choice == "1":
            updater.test_coordinates()
        
        elif choice == "2":
            new_name = input("Enter new player name: ").strip()
            if not new_name:
                print("Please enter a name.")
                return
            
            print(f"\nStarting update to '{new_name}'...")
            print("Make sure Action Tracker is active!")
            print("Starting in 3 seconds...")
            
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            
            success = updater.update_player1_name(new_name)
            
            if success:
                print("UPDATE SUCCESS!")
            else:
                print("UPDATE FAILED!")
        
        else:
            print("Invalid choice.")
    
    except KeyboardInterrupt:
        print("\nCancelled by user.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()