"""
Wait for user to activate Action Tracker, then register Player 2
사용자가 Action Tracker를 활성화한 후 Player 2 등록
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Coordinates
MAIN_PLAYER2 = (374, 359)      # Player 2 on main screen
SUB_NAME_FIELD = (785, 291)    # Sub screen name field
COMPLETE_BUTTON = (1720, 139)  # Complete registration button

def register_player2_simple():
    """Simple Player 2 registration"""
    
    print("="*60)
    print("PLAYER 2 - NEW NAME REGISTRATION")
    print("="*60)
    print()
    print("!!! IMPORTANT !!!")
    print("Please make sure Action Tracker is visible on screen!")
    print("!!! IMPORTANT !!!")
    print()
    
    new_name = "Phil Ivey"
    
    print(f"Will register Player 2 as: {new_name}")
    print("\nYou have 5 seconds to activate Action Tracker window...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\nStarting registration process...")
    
    # Before screenshot
    print("[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("p2_before.png")
    
    try:
        # Step 1: Click Player2
        print(f"\n[1] Click Player2: {MAIN_PLAYER2}")
        pyautogui.click(MAIN_PLAYER2[0], MAIN_PLAYER2[1])
        time.sleep(1)
        
        # Step 2: Click name field
        print(f"[2] Click name field: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Type name
        print(f"[3] Type: {new_name}")
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 4: Enter
        print("[4] Press Enter")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 5: Complete
        print(f"[5] Click complete: {COMPLETE_BUTTON}")
        pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
        time.sleep(1)
        
        # After screenshot
        print("\n[AFTER] Taking screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"p2_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("COMPLETE!")
        print("="*60)
        print(f"Check: {after_file}")
        print(f"Player 2 should be: {new_name}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    register_player2_simple()