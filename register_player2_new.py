"""
Register Player 2 - New Name (No existing name)
2번 플레이어 새 이름 등록 (기존 이름 없음)
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Player 2 coordinates on main screen
MAIN_PLAYER2 = (374, 359)      # Player 2 on main screen
SUB_NAME_FIELD = (785, 291)    # Sub screen name field (same for all players)
COMPLETE_BUTTON = (1720, 139)  # Complete registration button

def register_player2_new_name():
    """
    Register new name for Player 2 (no existing name):
    1. Click Player2 on main screen
    2. Click name field on sub screen
    3. Type new name (no need to clear)
    4. Press Enter
    5. Click complete button
    """
    
    print("="*60)
    print("PLAYER 2 - NEW NAME REGISTRATION")
    print("="*60)
    print()
    print("Process for empty name slot:")
    print("1. Click Player2 on main screen")
    print("2. Click name field")
    print("3. Type new name directly")
    print("4. Press Enter")
    print("5. Click complete")
    print()
    
    new_name = "Phil Ivey"  # Famous poker player
    
    # Before screenshot
    print("[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("player2_before.png")
    
    print(f"\nRegistering Player 2 as: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click Player2 on main screen
        print(f"\n[Step 1] Click Player2: {MAIN_PLAYER2}")
        pyautogui.click(MAIN_PLAYER2[0], MAIN_PLAYER2[1])
        time.sleep(1)  # Wait for sub screen
        
        # Step 2: Click name field on sub screen
        print(f"[Step 2] Click name field: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Type new name directly (no clear needed for empty field)
        print(f"[Step 3] Type new name: {new_name}")
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
        after_file = f"player2_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("SUCCESS - PLAYER 2 REGISTERED!")
        print("="*60)
        print(f"Screenshot: {after_file}")
        print(f"Player 2 is now: {new_name}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("player2_error.png")
        print("Error screenshot: player2_error.png")

if __name__ == "__main__":
    print("Action Tracker - Player 2 Registration")
    print("This will register a NEW name for Player 2")
    print()
    register_player2_new_name()