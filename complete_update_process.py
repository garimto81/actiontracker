"""
Complete Update Process - Main Screen to Edit Dialog
"""

import pyautogui
import time
from datetime import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def complete_update_process():
    """Complete process: Main screen → Edit dialog → Update name → Close"""
    
    print("="*60)
    print("COMPLETE UPDATE PROCESS")
    print("="*60)
    
    # Coordinates
    PLAYER1_MAIN = (215, 354)      # Player 1 on main screen
    NAME_FIELD = (582, 196)         # Golden NAME button in edit dialog
    X_BUTTON = (1232, 73)           # X button to close dialog
    
    new_name = "Daniel Negreanu"
    
    print(f"\nTarget: Change Player 1 to '{new_name}'")
    print("\nSteps:")
    print("1. Click Player 1 on main screen")
    print("2. Click NAME field in edit dialog")
    print("3. Enter new name")
    print("4. Close dialog")
    print()
    
    # Initial screenshot
    print("[BEFORE] Taking initial screenshot...")
    before = pyautogui.screenshot()
    before.save("process_before.png")
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    try:
        # Step 1: Click player on main screen
        print("\n[1] Clicking Player 1 on main screen...")
        pyautogui.click(PLAYER1_MAIN[0], PLAYER1_MAIN[1])
        time.sleep(1)  # Wait for dialog to open
        
        # Step 2: Click NAME field in edit dialog
        print("[2] Clicking NAME field in edit dialog...")
        pyautogui.click(NAME_FIELD[0], NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Clear and type new name
        print(f"[3] Entering new name: {new_name}")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.5)
        
        # Step 4: Press Enter to save
        print("[4] Pressing Enter to save...")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Take screenshot of edit dialog with new name
        print("[5] Taking screenshot of updated dialog...")
        dialog = pyautogui.screenshot()
        dialog.save("process_dialog_updated.png")
        
        # Step 5: Close dialog
        print("[6] Closing edit dialog...")
        pyautogui.click(X_BUTTON[0], X_BUTTON[1])
        time.sleep(1)
        
        # Final screenshot
        print("\n[AFTER] Taking final screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"process_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("PROCESS COMPLETE - CHECK SCREENSHOTS!")
        print("="*60)
        print("1. process_before.png - Initial state")
        print("2. process_dialog_updated.png - Dialog with new name")
        print(f"3. {after_file} - Final main screen")
        print()
        print("Player 1 should now show 'Daniel Negreanu'")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("process_error.png")

if __name__ == "__main__":
    complete_update_process()