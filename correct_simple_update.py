"""
Correct Simple Update - No Dropdown Process
드롭다운 없는 간단한 프로세스
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# CORRECT COORDINATES
MAIN_PLAYER1 = (233, 361)      # Main screen player1 select
SUB_NAME_FIELD = (785, 291)    # Sub screen name field
COMPLETE_BUTTON = (1720, 139)  # Complete registration button

def simple_name_update():
    """
    Simple process WITHOUT dropdown:
    1. Click Player1 on main screen
    2. Click name field on sub screen
    3. Clear and enter new name (NO DROPDOWN STEP)
    4. Press Enter
    5. Click complete button
    """
    
    print("="*60)
    print("SIMPLE NAME UPDATE - NO DROPDOWN")
    print("="*60)
    print()
    print("Process:")
    print("1. Click Player1 on main screen")
    print("2. Click name field")
    print("3. Clear and type new name")
    print("4. Press Enter")
    print("5. Click complete")
    print()
    
    new_name = "Daniel Negreanu"
    
    # Before screenshot
    print("[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("simple_before.png")
    
    print(f"\nChanging Player 1 to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click Player1 on main screen
        print(f"\n[Step 1] Click Player1: {MAIN_PLAYER1}")
        pyautogui.click(MAIN_PLAYER1[0], MAIN_PLAYER1[1])
        time.sleep(1)  # Wait for sub screen
        
        # Step 2: Click name field on sub screen
        print(f"[Step 2] Click name field: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Clear and enter new name (NO DROPDOWN CLICK)
        print(f"[Step 3] Clear and type: {new_name}")
        # Triple-click to select all
        pyautogui.tripleClick()
        time.sleep(0.2)
        # Type new name (replaces selected text)
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 4: Press Enter
        print("[Step 4] Press Enter")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 5: Click complete button
        print(f"[Step 5] Click complete: {COMPLETE_BUTTON}")
        pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
        time.sleep(1)
        
        # After screenshot
        print("\n[AFTER] Taking final screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"simple_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("SUCCESS - CHECK SCREENSHOT!")
        print("="*60)
        print(f"Result: {after_file}")
        print(f"Player 1 should be: {new_name}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("simple_error.png")

if __name__ == "__main__":
    simple_name_update()