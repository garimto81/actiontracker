"""
Register Player 3 - Simple 3 Steps Only
3번 플레이어 등록 - 간단한 3단계만
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Player 3 coordinate
PLAYER3_MAIN = (544, 362)

def register_player3():
    """
    Register Player 3 with only 3 steps:
    1. Click Player 3 on main screen
    2. Type new name directly
    3. Press Enter
    """
    
    print("="*60)
    print("PLAYER 3 - SIMPLE 3-STEP REGISTRATION")
    print("="*60)
    print()
    print("Process (3 steps only):")
    print("1. Click Player 3")
    print("2. Type name")
    print("3. Press Enter")
    print()
    
    new_name = "Doyle Brunson"
    
    # Before screenshot
    print("[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("player3_before.png")
    
    print(f"\nRegistering Player 3 as: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click Player 3 on main screen
        print(f"\n[Step 1] Click Player 3: {PLAYER3_MAIN}")
        pyautogui.click(PLAYER3_MAIN[0], PLAYER3_MAIN[1])
        time.sleep(0.5)
        
        # Step 2: Type new name directly
        print(f"[Step 2] Type name: {new_name}")
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 3: Press Enter
        print("[Step 3] Press Enter")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # After screenshot
        print("\n[AFTER] Taking screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"player3_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("SUCCESS - 3 STEPS COMPLETE!")
        print("="*60)
        print(f"Player 3 registered as: {new_name}")
        print(f"Screenshot: {after_file}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("player3_error.png")

if __name__ == "__main__":
    register_player3()