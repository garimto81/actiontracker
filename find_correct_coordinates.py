"""
Find correct coordinates for Player 1 button
"""

import pyautogui
import time
from datetime import datetime

print("="*60)
print("FINDING CORRECT PLAYER 1 COORDINATES")
print("="*60)
print()
print("Based on the screenshot analysis:")
print("The red 'Alice Johnson' button appears to be at:")
print()

# Looking at the screenshot more carefully:
# The red button with "Alice Johnson" is in the second row
# It's the leftmost button in the player name row
# Estimated coordinates based on visual analysis:

POSSIBLE_COORDS = [
    (152, 260),  # Previous attempt - didn't work
    (215, 354),  # Original coordinate from earlier scripts
    (152, 258),  # Slightly adjusted
    (150, 260),  # Left edge of button
    (180, 260),  # Center of button
]

print("Testing multiple possible coordinates...")
print("This will click different positions and take screenshots")
print()
print("Starting in 3 seconds...")
time.sleep(3)

for i, (x, y) in enumerate(POSSIBLE_COORDS, 1):
    print(f"\n[Test {i}] Clicking at ({x}, {y})")
    
    # Click the position
    pyautogui.click(x, y)
    time.sleep(0.5)
    
    # Try double-click
    pyautogui.doubleClick()
    time.sleep(1)
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    filename = f"test_coord_{i}_{x}_{y}.png"
    screenshot.save(filename)
    print(f"  Screenshot saved: {filename}")
    
    # Press ESC to cancel any dialog
    pyautogui.press('esc')
    time.sleep(0.5)

print("\n" + "="*60)
print("TESTING COMPLETE")
print("="*60)
print("Check the screenshots to see which coordinate opened the edit dialog")
print()

# Also show current mouse position for manual checking
print("Move your mouse over the Player 1 button and note the coordinates")
print("Press Ctrl+C to stop...")
try:
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nStopped")