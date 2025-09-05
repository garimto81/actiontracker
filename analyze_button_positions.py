"""
Analyze Action Tracker button positions
Find exact coordinates for player name buttons and chip buttons
"""

import pyautogui
import time
from PIL import Image, ImageDraw, ImageFont

def capture_and_analyze():
    print("\n" + "="*70)
    print(" ACTION TRACKER - BUTTON POSITION ANALYSIS")
    print("="*70)
    
    # Take screenshot
    print("\n[1] Taking screenshot of current Action Tracker...")
    time.sleep(2)  # Give time to ensure Action Tracker is visible
    screenshot = pyautogui.screenshot()
    screenshot.save("action_tracker_current.png")
    print("    Saved: action_tracker_current.png")
    
    # Get screen size
    width, height = pyautogui.size()
    print(f"\n[2] Screen Resolution: {width} x {height}")
    
    # Based on the visible buttons in the screenshot:
    # Player name buttons are in the row with Mike, Hunter, Jayden, etc.
    # Chip buttons appear to be in the row below with the orange circles
    
    print("\n[3] Analyzing button positions based on visible layout...")
    
    # Player name buttons (approximate positions based on screenshot)
    # These are in the second row of buttons
    name_button_y = 260  # Y coordinate for name buttons row
    name_button_spacing = 120  # Approximate spacing between buttons
    name_button_start_x = 150  # Starting X position
    
    print("\n[4] Estimated Player Name Button Positions:")
    print("-" * 50)
    name_positions = []
    for i in range(10):
        x = name_button_start_x + (i * name_button_spacing)
        name_positions.append((x, name_button_y))
        if i < 6:  # First 6 are visible
            names = ["Mike", "Hunter", "Jayden", "JUN", "Richie", "Ray"]
            print(f"    Player {i+1} ({names[i]}): ({x}, {name_button_y})")
        else:
            print(f"    Player {i+1}: ({x}, {name_button_y})")
    
    # Chip buttons (the orange circular buttons below)
    chip_button_y = 450  # Y coordinate for chip buttons row
    
    print("\n[5] Estimated Chip Button Positions:")
    print("-" * 50)
    chip_positions = []
    for i in range(10):
        x = name_button_start_x + (i * name_button_spacing)
        chip_positions.append((x, chip_button_y))
        print(f"    Player {i+1} Chips: ({x}, {chip_button_y})")
    
    # Create annotated screenshot showing button positions
    print("\n[6] Creating annotated screenshot...")
    img = screenshot.copy()
    draw = ImageDraw.Draw(img)
    
    # Draw markers for name buttons
    for i, (x, y) in enumerate(name_positions[:6]):
        # Draw crosshair
        draw.line([(x-10, y), (x+10, y)], fill="red", width=2)
        draw.line([(x, y-10), (x, y+10)], fill="red", width=2)
        # Draw label
        draw.text((x-10, y-25), f"P{i+1}", fill="red")
    
    # Draw markers for chip buttons
    for i, (x, y) in enumerate(chip_positions[:6]):
        # Draw crosshair
        draw.line([(x-10, y), (x+10, y)], fill="blue", width=2)
        draw.line([(x, y-10), (x, y+10)], fill="blue", width=2)
        # Draw label
        draw.text((x-10, y+15), f"C{i+1}", fill="blue")
    
    img.save("action_tracker_annotated.png")
    print("    Saved: action_tracker_annotated.png")
    
    # Generate update code with correct positions
    print("\n[7] Generating updated logic...")
    
    code = '''
# Corrected positions for Action Tracker buttons
PLAYER_NAME_POSITIONS = [
'''
    for i in range(6):
        code += f'    ({name_positions[i][0]}, {name_positions[i][1]}),  # Player {i+1}\n'
    
    code += ''']

PLAYER_CHIP_POSITIONS = [
'''
    for i in range(6):
        code += f'    ({chip_positions[i][0]}, {chip_positions[i][1]}),  # Player {i+1} chips\n'
    
    code += ''']

# Update logic:
# 1. Click on player name button to select player
# 2. Type new name
# 3. Click on chip button
# 4. Type new chip amount
'''
    
    print(code)
    
    # Save the corrected positions to a file
    with open("corrected_positions.py", "w") as f:
        f.write(code)
    
    print("\n[8] Saved corrected positions to: corrected_positions.py")
    
    print("\n" + "="*70)
    print(" ANALYSIS COMPLETE")
    print("="*70)
    print("\nCheck 'action_tracker_annotated.png' to verify button positions")
    print("Red markers = Player name buttons")
    print("Blue markers = Chip buttons")
    print("="*70)

if __name__ == "__main__":
    capture_and_analyze()