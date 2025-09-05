"""
Verify and Update with Screenshot Confirmation
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def update_player1_with_verification():
    """Update player 1 and verify with screenshots"""
    
    print("="*60)
    print("UPDATE PLAYER 1 WITH VERIFICATION")
    print("="*60)
    
    # Take initial screenshot
    print("\n[1] Taking BEFORE screenshot...")
    before_screenshot = pyautogui.screenshot()
    before_filename = f"before_{datetime.now().strftime('%H%M%S')}.png"
    before_screenshot.save(before_filename)
    print(f"   Saved: {before_filename}")
    
    # Main screen player 1 coordinates (red button)
    # Based on the screenshot, player 1 is at approximately:
    PLAYER1_BUTTON = (152, 260)  # The red "Alice Johnson" button
    
    print(f"\n[2] Clicking Player 1 button at {PLAYER1_BUTTON}")
    pyautogui.click(PLAYER1_BUTTON[0], PLAYER1_BUTTON[1])
    time.sleep(0.5)
    
    # Double-click to enter edit mode
    print("[3] Double-clicking to enter edit mode...")
    pyautogui.doubleClick()
    time.sleep(1)
    
    # Take screenshot of edit dialog
    print("[4] Taking EDIT DIALOG screenshot...")
    edit_screenshot = pyautogui.screenshot()
    edit_filename = f"edit_dialog_{datetime.now().strftime('%H%M%S')}.png"
    edit_screenshot.save(edit_filename)
    print(f"   Saved: {edit_filename}")
    
    # Type new name (assuming edit field is active)
    new_name = "Daniel Negreanu"
    print(f"\n[5] Typing new name: {new_name}")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.typewrite(new_name, interval=0.03)
    time.sleep(0.3)
    
    # Press Enter to confirm
    print("[6] Pressing Enter to confirm...")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Press Escape to close any dialog
    print("[7] Pressing ESC to close dialog...")
    pyautogui.press('esc')
    time.sleep(0.5)
    
    # Take final screenshot
    print("\n[8] Taking AFTER screenshot...")
    after_screenshot = pyautogui.screenshot()
    after_filename = f"after_{datetime.now().strftime('%H%M%S')}.png"
    after_screenshot.save(after_filename)
    print(f"   Saved: {after_filename}")
    
    print("\n" + "="*60)
    print("VERIFICATION REQUIRED!")
    print("="*60)
    print("Please check these screenshots:")
    print(f"1. BEFORE: {before_filename}")
    print(f"2. EDIT DIALOG: {edit_filename}")
    print(f"3. AFTER: {after_filename}")
    print("\nCheck if the name changed from 'Alice Johnson' to 'Daniel Negreanu'")
    print("="*60)

if __name__ == "__main__":
    print("Starting in 3 seconds...")
    print("Make sure Action Tracker is visible!")
    time.sleep(3)
    
    try:
        update_player1_with_verification()
    except Exception as e:
        print(f"\nERROR: {e}")
        # Take error screenshot
        error_screenshot = pyautogui.screenshot()
        error_filename = f"error_{datetime.now().strftime('%H%M%S')}.png"
        error_screenshot.save(error_filename)
        print(f"Error screenshot: {error_filename}")