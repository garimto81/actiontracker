"""
Final Working Update with Correct Coordinates
Using user-provided exact coordinates
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# CORRECT COORDINATES (user provided)
MAIN_PLAYER1 = (233, 361)      # Main screen player1 select
SUB_NAME_FIELD = (785, 291)    # Sub screen name field
COMPLETE_BUTTON = (1720, 139)  # Complete registration button

def update_existing_name_process():
    """
    Process for existing names:
    1. Click Player1 on main screen
    2. Click name field on sub screen
    3. Select from dropdown
    4. Enter new name
    5. Press Enter
    6. Click complete button
    """
    
    print("="*60)
    print("EXISTING NAME UPDATE PROCESS")
    print("="*60)
    print()
    print("Coordinates to use:")
    print(f"  Main Player1: {MAIN_PLAYER1}")
    print(f"  Name field: {SUB_NAME_FIELD}")
    print(f"  Complete: {COMPLETE_BUTTON}")
    print()
    
    new_name = "Daniel Negreanu"
    
    # Before screenshot
    print("[BEFORE] Taking initial screenshot...")
    before = pyautogui.screenshot()
    before.save("working_before.png")
    
    print(f"\nChanging Player 1 to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click Player1 on main screen
        print(f"\n[Step 1] Click Player1 on main: {MAIN_PLAYER1}")
        pyautogui.click(MAIN_PLAYER1[0], MAIN_PLAYER1[1])
        time.sleep(1)  # Wait for sub screen
        
        # Step 2: Click name field on sub screen
        print(f"[Step 2] Click name field: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Select from dropdown (if exists)
        print("[Step 3] Select from dropdown")
        dropdown_y = SUB_NAME_FIELD[1] + 30
        pyautogui.click(SUB_NAME_FIELD[0], dropdown_y)
        time.sleep(0.3)
        
        # Step 4: Clear and enter new name
        print(f"[Step 4] Enter new name: {new_name}")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 5: Press Enter
        print("[Step 5] Press Enter")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 6: Click complete button
        print(f"[Step 6] Click complete: {COMPLETE_BUTTON}")
        pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
        time.sleep(1)
        
        # After screenshot
        print("\n[AFTER] Taking final screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"working_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("PROCESS COMPLETE - CHECK SCREENSHOTS!")
        print("="*60)
        print("1. working_before.png")
        print(f"2. {after_file}")
        print()
        print(f"Player 1 should now be: {new_name}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("working_error.png")

if __name__ == "__main__":
    update_existing_name_process()