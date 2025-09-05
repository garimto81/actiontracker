"""
Correct Player 1 Update with Verified Coordinates
Using the coordinates that actually worked before
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# CORRECT coordinates from execute_10_players.py that worked!
# These are the coordinates on the MAIN screen
PLAYER1_COORDS = (215, 354)

def update_player1_correctly():
    """Update Player 1 with the correct coordinates"""
    
    print("="*60)
    print("CORRECT PLAYER 1 UPDATE")
    print("="*60)
    print()
    print("Using verified coordinates from working scripts")
    print(f"Player 1 coordinates: {PLAYER1_COORDS}")
    print()
    
    # Take initial screenshot
    print("[1] Taking BEFORE screenshot...")
    before = pyautogui.screenshot()
    before.save("correct_before.png")
    print("    Saved: correct_before.png")
    
    new_name = "Daniel Negreanu"
    print(f"\nUpdating to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    print("\nExecuting update process...")
    print("-"*40)
    
    try:
        # Step 1: Click Player 1
        print(f"[1] Clicking Player 1 at {PLAYER1_COORDS}")
        pyautogui.click(PLAYER1_COORDS[0], PLAYER1_COORDS[1])
        time.sleep(0.3)
        
        # Step 2: Double-click to edit
        print("[2] Double-clicking to enter edit mode")
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # Step 3: Clear and type new name
        print(f"[3] Clearing and typing: {new_name}")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 4: Press Enter
        print("[4] Pressing Enter to confirm")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Take final screenshot
        print("\n[5] Taking AFTER screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_filename = f"correct_after_{timestamp}.png"
        after.save(after_filename)
        print(f"    Saved: {after_filename}")
        
        print("\n" + "="*60)
        print("PROCESS COMPLETE")
        print("="*60)
        print("CHECK THE SCREENSHOTS:")
        print("1. BEFORE: correct_before.png")
        print(f"2. AFTER: {after_filename}")
        print()
        print("The name should have changed from 'Alice Johnson'")
        print(f"to '{new_name}'")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("error_state.png")
        print("Error screenshot: error_state.png")

if __name__ == "__main__":
    update_player1_correctly()