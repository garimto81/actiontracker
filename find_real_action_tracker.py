"""
Find and activate the real Action Tracker window
"""

import pyautogui
import time

def find_real_action_tracker():
    print("Searching for Action Tracker window...")
    print("="*60)
    
    # Get all windows and find Action Tracker
    try:
        windows = pyautogui.getAllWindows()
        action_tracker_found = False
        
        print("\nAll open windows:")
        for window in windows:
            print(f"  - {window.title}")
            
            # Look for Action Tracker window
            if "action tracker" in window.title.lower() or "pokergfx" in window.title.lower():
                print(f"\n[FOUND] Action Tracker: {window.title}")
                window.activate()
                time.sleep(2)
                action_tracker_found = True
                
                # Take screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save("real_action_tracker.png")
                print("Screenshot saved: real_action_tracker.png")
                break
        
        if not action_tracker_found:
            print("\n[WARNING] Action Tracker window not found!")
            print("Action Tracker may not be running or may have a different window title")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60)
    print("Window search complete")
    
    # Take current screenshot anyway
    current = pyautogui.screenshot()
    current.save("current_active_window.png")
    print("Current window saved: current_active_window.png")

if __name__ == "__main__":
    find_real_action_tracker()