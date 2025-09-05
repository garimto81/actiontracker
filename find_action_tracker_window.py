"""
Find and activate Action Tracker window if it's already open
"""

import pyautogui
import time

def find_and_activate_action_tracker():
    print("Finding Action Tracker Window")
    print("="*60)
    
    # First, close the evaluation popup
    print("Closing evaluation popup...")
    pyautogui.press('escape')
    time.sleep(1)
    
    # Try Alt+Tab to switch windows
    print("Switching between windows to find Action Tracker...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(2)
    
    # Take screenshot of current window
    print("Capturing current window...")
    screenshot = pyautogui.screenshot()
    screenshot.save("current_window.png")
    
    # Get all windows
    try:
        windows = pyautogui.getAllWindows()
        print("\nAll open windows:")
        for window in windows:
            print(f"  - {window.title}")
            if "action tracker" in window.title.lower():
                print(f"    [FOUND] Activating: {window.title}")
                window.activate()
                time.sleep(2)
                
                # Take screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save("action_tracker_found.png")
                print("    Screenshot saved: action_tracker_found.png")
                break
    except Exception as e:
        print(f"Could not enumerate windows: {e}")
    
    # Alternative: Try keyboard shortcuts to navigate
    print("\nTrying keyboard navigation...")
    
    # ESC to close any dialogs
    for i in range(3):
        pyautogui.press('escape')
        time.sleep(0.5)
    
    # Click in center to ensure focus
    pyautogui.click(700, 400)
    time.sleep(1)
    
    # Final screenshot
    print("\nTaking final screenshot...")
    final_screenshot = pyautogui.screenshot()
    final_screenshot.save("final_window_state.png")
    print("Screenshot saved: final_window_state.png")
    
    print("\n" + "="*60)
    print("Window search complete")
    print("Check screenshots to see current state")
    print("="*60)

if __name__ == "__main__":
    find_and_activate_action_tracker()