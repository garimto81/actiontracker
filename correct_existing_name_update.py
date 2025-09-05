"""
Correct Existing Name Update Process
With proper coordinates for Player 1
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# CORRECT COORDINATES (from previous analysis)
PLAYER1_MAIN_BUTTON = (209, 658)    # Red button on main screen
NAME_FIELD_GOLDEN = (582, 196)      # Golden NAME button in edit dialog
DIALOG_CLOSE_X = (1232, 73)         # X button to close dialog

def update_existing_name():
    """
    Process for updating existing names with dropdown:
    1. Click player on main screen
    2. Click NAME field in dialog
    3. Select from dropdown
    4. Enter new name
    5. Press Enter
    6. Close dialog
    """
    
    print("="*60)
    print("EXISTING NAME UPDATE - CORRECT COORDINATES")
    print("="*60)
    print()
    print("Coordinates being used:")
    print(f"  Main screen Player 1: {PLAYER1_MAIN_BUTTON}")
    print(f"  Dialog NAME field: {NAME_FIELD_GOLDEN}")
    print(f"  Dialog X button: {DIALOG_CLOSE_X}")
    print()
    
    new_name = "Daniel Negreanu"
    
    # Take before screenshot
    print("[BEFORE] Taking initial screenshot...")
    before = pyautogui.screenshot()
    before.save("correct_before.png")
    
    print(f"\nChanging Player 1 to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click Player 1 on MAIN screen
        print(f"\n[1] Clicking Player 1 on main screen at {PLAYER1_MAIN_BUTTON}")
        pyautogui.click(PLAYER1_MAIN_BUTTON[0], PLAYER1_MAIN_BUTTON[1])
        time.sleep(1)  # Wait for dialog to open
        
        # Take screenshot of opened dialog
        print("[2] Dialog opened - taking screenshot...")
        dialog_opened = pyautogui.screenshot()
        dialog_opened.save("dialog_opened.png")
        
        # Step 2: Click NAME field (golden button) in dialog
        print(f"[3] Clicking NAME field at {NAME_FIELD_GOLDEN}")
        pyautogui.click(NAME_FIELD_GOLDEN[0], NAME_FIELD_GOLDEN[1])
        time.sleep(0.5)
        
        # Step 3: If dropdown appears, select first item
        print("[4] Selecting from dropdown (if exists)...")
        dropdown_y = NAME_FIELD_GOLDEN[1] + 30
        pyautogui.click(NAME_FIELD_GOLDEN[0], dropdown_y)
        time.sleep(0.3)
        
        # Step 4: Clear and type new name
        print(f"[5] Clearing and typing: {new_name}")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.5)
        
        # Step 5: Press Enter to save
        print("[6] Pressing Enter to save...")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Take screenshot before closing
        print("[7] Taking screenshot of updated dialog...")
        updated = pyautogui.screenshot()
        updated.save("dialog_updated_correct.png")
        
        # Step 6: Close dialog with X button
        print(f"[8] Closing dialog with X button at {DIALOG_CLOSE_X}")
        pyautogui.click(DIALOG_CLOSE_X[0], DIALOG_CLOSE_X[1])
        time.sleep(1)
        
        # Take final screenshot
        print("\n[AFTER] Taking final screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"correct_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("PROCESS COMPLETE - VERIFY SCREENSHOTS!")
        print("="*60)
        print("Screenshots to check:")
        print("1. correct_before.png - Initial state")
        print("2. dialog_opened.png - Dialog opened")
        print("3. dialog_updated_correct.png - After name change")
        print(f"4. {after_file} - Final main screen")
        print()
        print("Expected: Player 1 should show 'Daniel Negreanu'")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("error_correct.png")

if __name__ == "__main__":
    # First, close any open dialog
    print("Closing any open dialog first...")
    pyautogui.press('esc')
    time.sleep(0.5)
    pyautogui.click(DIALOG_CLOSE_X[0], DIALOG_CLOSE_X[1])
    time.sleep(1)
    
    # Now run the update
    update_existing_name()