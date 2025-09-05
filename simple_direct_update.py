"""
Simple Direct Update on Main Screen
Based on working execute_10_players.py coordinates
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# These coordinates WORKED in execute_10_players.py
PLAYER1_COORDS = (215, 354)

def simple_direct_update():
    """
    Simple process like execute_10_players.py:
    1. Click player
    2. Double-click to edit
    3. Clear and type
    4. Enter
    """
    
    print("="*60)
    print("SIMPLE DIRECT UPDATE (LIKE EXECUTE_10_PLAYERS.PY)")
    print("="*60)
    print()
    print(f"Using coords that worked before: {PLAYER1_COORDS}")
    print()
    
    new_name = "Daniel Negreanu"
    
    # Before screenshot
    print("[1] Taking BEFORE screenshot...")
    before = pyautogui.screenshot()
    before.save("simple_before.png")
    
    print(f"\nChanging to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Exactly like execute_10_players.py
        print(f"\n[1] Clicking Player 1 at {PLAYER1_COORDS}")
        pyautogui.click(PLAYER1_COORDS[0], PLAYER1_COORDS[1])
        time.sleep(0.3)
        
        print("[2] Double-clicking to edit...")
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        print("[3] Selecting all and deleting...")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        
        print(f"[4] Typing: {new_name}")
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.2)
        
        print("[5] Pressing Enter...")
        pyautogui.press('enter')
        time.sleep(0.3)
        
        # After screenshot
        print("\n[6] Taking AFTER screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"simple_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("COMPLETE - CHECK SCREENSHOTS!")
        print("="*60)
        print("1. simple_before.png")
        print(f"2. {after_file}")
        print()
        print("Player 1 should be 'Daniel Negreanu'")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    simple_direct_update()