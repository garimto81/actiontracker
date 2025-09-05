"""
Capture Action Tracker main screen after closing any open dialogs
"""

import pyautogui
import time

def capture_main_screen():
    print("Closing any open dialogs...")
    
    # Press ESC multiple times to close any open dialogs
    for i in range(3):
        pyautogui.press('escape')
        time.sleep(0.5)
    
    print("Waiting for main screen...")
    time.sleep(2)
    
    # Take screenshot of main screen
    print("Taking screenshot: action_tracker_main.png")
    screenshot = pyautogui.screenshot()
    screenshot.save("action_tracker_main.png")
    print("Screenshot saved!")
    
    # Also click on a neutral area to ensure we're on main screen
    pyautogui.click(500, 500)  # Click in middle of screen
    time.sleep(1)
    
    # Take another screenshot
    print("Taking screenshot: action_tracker_final.png")
    screenshot2 = pyautogui.screenshot()
    screenshot2.save("action_tracker_final.png")
    print("Final screenshot saved!")

if __name__ == "__main__":
    capture_main_screen()