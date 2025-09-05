"""
Activate Action Tracker and Register Player 2
Action Tracker 활성화 후 Player 2 등록
"""

import pyautogui
import time
from datetime import datetime
import pygetwindow as gw

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Coordinates
MAIN_PLAYER2 = (374, 359)      # Player 2 on main screen
SUB_NAME_FIELD = (785, 291)    # Sub screen name field
COMPLETE_BUTTON = (1720, 139)  # Complete registration button

def activate_action_tracker():
    """Activate Action Tracker window"""
    try:
        # Find Action Tracker window
        windows = gw.getWindowsWithTitle('Action Tracker')
        if windows:
            window = windows[0]
            window.activate()  # Bring to front
            window.maximize()  # Maximize if needed
            time.sleep(1)
            print("Action Tracker activated")
            return True
        else:
            print("Action Tracker window not found!")
            # Try clicking on taskbar
            pyautogui.click(1000, 850)  # Approximate taskbar position
            time.sleep(1)
            return False
    except:
        print("Could not activate window, continuing anyway...")
        return False

def register_player2():
    """Register Player 2 with new name"""
    
    print("="*60)
    print("PLAYER 2 REGISTRATION (WITH WINDOW ACTIVATION)")
    print("="*60)
    
    # First activate Action Tracker
    print("\n[0] Activating Action Tracker window...")
    activate_action_tracker()
    
    new_name = "Phil Ivey"
    
    # Before screenshot
    print("\n[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("player2_activated_before.png")
    
    # Check if screen is black
    import numpy as np
    img_array = np.array(before)
    if np.mean(img_array) < 10:  # Very dark image
        print("WARNING: Screen appears to be black!")
        print("Trying to click on screen to activate...")
        pyautogui.click(694, 400)  # Center of screen
        time.sleep(1)
        before = pyautogui.screenshot()
        before.save("player2_activated_before2.png")
    
    print(f"\nRegistering Player 2 as: {new_name}")
    print("Starting process...")
    
    try:
        # Step 1: Click Player2
        print(f"\n[Step 1] Click Player2: {MAIN_PLAYER2}")
        pyautogui.click(MAIN_PLAYER2[0], MAIN_PLAYER2[1])
        time.sleep(1)
        
        # Take screenshot to check if sub screen opened
        check = pyautogui.screenshot()
        check.save("player2_check.png")
        
        # Step 2: Click name field
        print(f"[Step 2] Click name field: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Type new name
        print(f"[Step 3] Type: {new_name}")
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 4: Enter
        print("[Step 4] Press Enter")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 5: Complete
        print(f"[Step 5] Click complete: {COMPLETE_BUTTON}")
        pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
        time.sleep(1)
        
        # After screenshot
        print("\n[AFTER] Taking final screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"player2_activated_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("PROCESS COMPLETE!")
        print("="*60)
        print("Check screenshots:")
        print("1. player2_activated_before.png")
        print("2. player2_check.png (sub screen)")
        print(f"3. {after_file}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("player2_activated_error.png")

if __name__ == "__main__":
    register_player2()