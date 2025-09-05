"""
Fix Current Edit Dialog - Direct Update
"""

import pyautogui
import time
from datetime import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def fix_current_dialog():
    """Fix the currently open edit dialog"""
    
    print("="*60)
    print("FIXING CURRENT EDIT DIALOG")
    print("="*60)
    print()
    print("Current state: Edit dialog is open with 'Alice Johnson'")
    print("Goal: Change to 'Daniel Negreanu' and close dialog")
    print()
    
    new_name = "Daniel Negreanu"
    
    # The golden NAME field button coordinates
    NAME_FIELD = (582, 196)
    
    # X button to close
    X_BUTTON = (1232, 73)
    
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click on the NAME field (golden button)
        print("[1] Clicking NAME field (golden button)...")
        pyautogui.click(NAME_FIELD[0], NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 2: Triple-click to select all text
        print("[2] Triple-clicking to select all text...")
        pyautogui.tripleClick()
        time.sleep(0.3)
        
        # Step 3: Type new name (replaces selected text)
        print(f"[3] Typing: {new_name}")
        pyautogui.typewrite(new_name, interval=0.03)
        time.sleep(0.5)
        
        # Step 4: Press Tab to move to next field (saves the name)
        print("[4] Pressing Tab to save...")
        pyautogui.press('tab')
        time.sleep(0.5)
        
        # Take screenshot to verify change
        print("[5] Taking screenshot of updated dialog...")
        updated = pyautogui.screenshot()
        updated.save("dialog_updated.png")
        
        # Step 5: Close dialog with X button
        print("[6] Closing dialog with X button...")
        pyautogui.click(X_BUTTON[0], X_BUTTON[1])
        time.sleep(1)
        
        # Final screenshot
        print("[7] Taking final screenshot...")
        final = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        final_file = f"fixed_result_{timestamp}.png"
        final.save(final_file)
        
        print("\n" + "="*60)
        print("FIX COMPLETE - CHECK SCREENSHOTS!")
        print("="*60)
        print("1. dialog_updated.png - Dialog after name change")
        print(f"2. {final_file} - Main screen after closing")
        print()
        print("NAME field should show 'Daniel Negreanu'")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("fix_error.png")

if __name__ == "__main__":
    fix_current_dialog()