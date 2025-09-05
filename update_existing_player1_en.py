"""
Update Existing Player 1 Name
Process for updating names that already exist in the system
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# Player 1 coordinates
PLAYER1_X = 215
PLAYER1_Y = 354

def update_existing_name():
    """
    Process for existing names (with dropdown):
    1. Click name
    2. Select from dropdown
    3. Modify text
    4. Press Enter
    5. Click confirmation
    """
    
    print("="*60)
    print("UPDATE EXISTING PLAYER 1 NAME")
    print("="*60)
    print()
    print("Process Type: EXISTING NAME (Dropdown Process)")
    print("Steps:")
    print("  1. Click player name")
    print("  2. Double-click to edit")
    print("  3. Select from dropdown list")
    print("  4. Enter new name")
    print("  5. Press Enter key")
    print("  6. Click confirmation")
    print()
    
    new_name = "Daniel Negreanu"  # New name to set
    
    print(f"Updating Player 1 to: '{new_name}'")
    print("Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\nExecuting...")
    print("-"*40)
    
    try:
        # Step 1: Click player name
        print("[1/6] Clicking Player 1 name...")
        pyautogui.click(PLAYER1_X, PLAYER1_Y)
        time.sleep(0.3)
        
        # Step 2: Double-click to enter edit mode
        print("[2/6] Double-clicking to enter edit mode...")
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # Step 3: Select from dropdown (click below for dropdown item)
        print("[3/6] Selecting from dropdown list...")
        pyautogui.click(PLAYER1_X, PLAYER1_Y + 30)  # Click dropdown item
        time.sleep(0.3)
        
        # Step 4: Clear and enter new name
        print(f"[4/6] Entering new name: {new_name}")
        pyautogui.hotkey('ctrl', 'a')  # Select all
        time.sleep(0.1)
        pyautogui.press('delete')  # Delete
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)  # Type new name
        time.sleep(0.2)
        
        # Step 5: Press Enter
        print("[5/6] Pressing Enter to apply...")
        pyautogui.press('enter')
        time.sleep(0.3)
        
        # Step 6: Click confirmation (click away or confirm button)
        print("[6/6] Final confirmation...")
        pyautogui.click(PLAYER1_X + 200, PLAYER1_Y)  # Click away to confirm
        time.sleep(0.3)
        
        print("\n" + "="*60)
        print("SUCCESS! Process completed!")
        print(f"Player 1 name updated to: '{new_name}'")
        print("="*60)
        
        # Save screenshot
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"existing_name_update_{timestamp}.png"
        screenshot.save(filename)
        print(f"\nResult screenshot saved: {filename}")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        print("Process interrupted")

if __name__ == "__main__":
    print("Action Tracker - Existing Name Update Process")
    print("="*60)
    print()
    print("This script demonstrates the process for updating")
    print("names that already exist in the system (with dropdown).")
    print()
    print("NOTE: Action Tracker must be active and visible!")
    print()
    
    update_existing_name()