"""
Launch Action Tracker from PokerGFX Server
"""

import pyautogui
import time

def launch_action_tracker():
    print("Launching Action Tracker from PokerGFX Server")
    print("="*60)
    
    # Click "Launch Action Tracker" button
    print("Clicking 'Launch Action Tracker' button...")
    pyautogui.click(600, 373)  # Button location from screenshot
    
    print("Waiting for Action Tracker to load...")
    time.sleep(5)  # Wait for window to open
    
    # Take screenshot after launch
    print("\nCapturing Action Tracker window...")
    screenshot = pyautogui.screenshot()
    screenshot.save("action_tracker_launched.png")
    print("Screenshot saved: action_tracker_launched.png")
    
    print("\n" + "="*60)
    print("Action Tracker should now be open")
    print("The main table view should show all 6 players")
    print("="*60)

if __name__ == "__main__":
    launch_action_tracker()