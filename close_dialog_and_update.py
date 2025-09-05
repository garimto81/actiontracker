"""
Close Edit Dialog and Update Player 1 Correctly
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

def close_edit_dialog_and_update():
    """Close current dialog and update from main screen"""
    
    print("="*60)
    print("FIXING: Close Dialog and Update Correctly")
    print("="*60)
    
    # Step 1: Close current edit dialog (X button)
    print("\n[1] Closing current edit dialog...")
    # X button is typically at top-right of dialog
    pyautogui.click(1232, 73)  # X button position from previous analysis
    time.sleep(1)
    
    print("[2] Taking screenshot of main screen...")
    screenshot = pyautogui.screenshot()
    screenshot.save("main_screen_check.png")
    print("   Saved: main_screen_check.png")
    
    # Step 2: Now click the actual player 1 button on main screen
    print("\n[3] Clicking Player 1 on MAIN screen...")
    print("   Position: (215, 658)")  # Main screen player 1 position
    
    # The correct coordinates for main screen player buttons
    PLAYER1_MAIN = (209, 658)  # Red button on main screen
    
    pyautogui.click(PLAYER1_MAIN[0], PLAYER1_MAIN[1])
    time.sleep(1)
    
    print("[4] Edit dialog should now be open...")
    
    # Step 3: Click on NAME field in edit dialog
    NAME_FIELD = (582, 196)  # Golden NAME button in edit dialog
    
    print("[5] Clicking NAME field in edit dialog...")
    pyautogui.click(NAME_FIELD[0], NAME_FIELD[1])
    time.sleep(0.5)
    
    # Step 4: Clear and enter new name
    new_name = "Daniel Negreanu"
    print(f"[6] Entering new name: {new_name}")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.3)
    
    # Step 5: Press Enter
    print("[7] Pressing Enter...")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Step 6: Close dialog with X button
    print("[8] Closing edit dialog...")
    pyautogui.click(1232, 73)  # X button
    time.sleep(1)
    
    # Final screenshot
    print("\n[9] Taking final screenshot...")
    final_screenshot = pyautogui.screenshot()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"correct_update_{timestamp}.png"
    final_screenshot.save(filename)
    
    print("="*60)
    print("COMPLETE!")
    print(f"Final screenshot: {filename}")
    print("="*60)

if __name__ == "__main__":
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    try:
        close_edit_dialog_and_update()
    except Exception as e:
        print(f"Error: {e}")
        # Take error screenshot
        error_screenshot = pyautogui.screenshot()
        error_screenshot.save("error_state.png")
        print("Error screenshot saved: error_state.png")