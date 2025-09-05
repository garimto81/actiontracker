"""
Close the player edit dialog and verify the main Action Tracker screen
"""

import pyautogui
import time

def close_dialog_and_verify():
    print("Action Tracker - Closing Edit Dialog and Verifying Changes")
    print("="*60)
    
    # Method 1: Click X button on the dialog
    print("Clicking X button to close dialog...")
    pyautogui.click(1235, 75)  # X button location from screenshot
    time.sleep(1)
    
    # Method 2: Press ESC key as backup
    print("Pressing ESC to ensure dialog is closed...")
    pyautogui.press('escape')
    time.sleep(1)
    
    # Method 3: Click outside the dialog
    print("Clicking on main area...")
    pyautogui.click(100, 400)  # Click on left side of screen
    time.sleep(2)
    
    # Take screenshot of main screen
    print("\nCapturing main Action Tracker screen...")
    screenshot = pyautogui.screenshot()
    screenshot.save("action_tracker_verified.png")
    print("Screenshot saved: action_tracker_verified.png")
    
    # Also capture with a different name for comparison
    time.sleep(1)
    screenshot2 = pyautogui.screenshot()
    screenshot2.save("final_result.png")
    print("Screenshot saved: final_result.png")
    
    print("\n" + "="*60)
    print("Verification complete!")
    print("Check 'action_tracker_verified.png' to see the updated players")
    print("="*60)

if __name__ == "__main__":
    close_dialog_and_verify()