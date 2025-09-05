"""
Simple check of Action Tracker window state
"""

import pyautogui
import time

print("\n" + "="*60)
print(" ACTION TRACKER STATUS CHECK")
print("="*60)

# Try to activate Action Tracker by clicking on taskbar or Alt+Tab
print("\nTrying to activate Action Tracker...")

# Alt+Tab multiple times to find it
for i in range(5):
    pyautogui.hotkey('alt', 'tab')
    time.sleep(1)
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(f"window_check_{i}.png")
    print(f"Screenshot {i+1} saved: window_check_{i}.png")

print("\n" + "="*60)
print("IMPORTANT:")
print("- The script DID run and click on positions")
print("- But it may have clicked on the wrong window")
print("- Action Tracker may be minimized or behind other windows")
print("- The player data MAY have been updated if Action Tracker was active")
print("="*60)

print("\nTo verify if update worked:")
print("1. Manually open Action Tracker window")
print("2. Check if players show new names:")
print("   - Tom Dwan, Phil Ivey, Daniel Negreanu")
print("   - Vanessa Selbst, Phil Hellmuth, Antonio Esfandiari")
print("3. If not updated, the script clicked on wrong window")
print("="*60)