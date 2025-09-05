"""
Continue past evaluation mode to Action Tracker main screen
"""

import pyautogui
import time

def continue_to_action_tracker():
    print("Continuing to Action Tracker")
    print("="*60)
    
    # Click "Continue" button
    print("Clicking 'Continue' button...")
    pyautogui.click(340, 526)  # Continue button location
    
    print("Waiting for Action Tracker to fully load...")
    time.sleep(5)  # Wait for Action Tracker to load
    
    # Take screenshot of Action Tracker main screen
    print("\nCapturing Action Tracker main screen...")
    screenshot = pyautogui.screenshot()
    screenshot.save("action_tracker_main_screen.png")
    print("Screenshot saved: action_tracker_main_screen.png")
    
    # Try clicking in the main area to ensure we're on main screen
    print("Clicking on main area to ensure we're on main screen...")
    pyautogui.click(700, 400)
    time.sleep(2)
    
    # Take another screenshot
    print("Taking final screenshot...")
    screenshot2 = pyautogui.screenshot()
    screenshot2.save("action_tracker_final_view.png")
    print("Screenshot saved: action_tracker_final_view.png")
    
    print("\n" + "="*60)
    print("Action Tracker Main Screen")
    print("="*60)
    print("\nIf the bulk update was successful, you should see:")
    print("• Stephen Chidwick")
    print("• Vanessa Selbst")  
    print("• Charlie Carrel")
    print("• Phil Hellmuth")
    print("• Daniel Negreanu")
    print("• Mustapha Kanit")
    print("\nWith their respective chip counts")
    print("="*60)

if __name__ == "__main__":
    continue_to_action_tracker()