"""
Coordinate Validation and Screenshot Analysis Tool
Action Tracker Current State Checker
"""

import pyautogui
import time
from PIL import Image, ImageDraw
import os

# Current coordinates in use
COORDS = {
    'player1': (215, 354),        # Player1 button
    'delete': (761, 108),         # Delete button  
    'complete': (1733, 155),      # Complete button
    'edit': (815, 294)            # Edit field (previously used coordinate)
}

def take_screenshot_with_markers():
    """Take screenshot with coordinate markers"""
    print("Taking current screen screenshot...")
    
    try:
        # Take screenshot
        screenshot = pyautogui.screenshot()
        draw = ImageDraw.Draw(screenshot)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        print("\n=== Coordinate Verification ===")
        for i, (name, (x, y)) in enumerate(COORDS.items()):
            color = colors[i % len(colors)]
            
            # Draw cross marker
            draw.line([(x-40, y), (x+40, y)], fill=color, width=6)
            draw.line([(x, y-40), (x, y+40)], fill=color, width=6)
            
            # Coordinate text
            draw.text((x+45, y-25), f"{name}: ({x},{y})", fill=color)
            
            print(f"{i+1}. {name}: ({x}, {y}) - {color}")
        
        # Save file
        timestamp = int(time.time())
        filename = f"coordinate_check_{timestamp}.png"
        filepath = os.path.join(os.getcwd(), filename)
        screenshot.save(filepath)
        
        print(f"\nScreenshot saved: {filepath}")
        print("\nCheck this image to verify coordinates are at correct positions.")
        
        return filepath
        
    except Exception as e:
        print(f"Screenshot error: {e}")
        return None

def test_click_sequence():
    """Test actual click sequence (logic only, not executed)"""
    print("\n=== Expected Click Sequence ===")
    print("1. Click Player1 tab: (215, 354)")
    print("2. Wait: 0.3 seconds")
    print("3. Type name + Enter")
    print("4. Click complete button: (1733, 155)")
    print("5. Wait: 0.2 seconds")
    
    print("\nImportant notes:")
    print("- Action Tracker must be visible on screen")
    print("- Verify coordinates are at correct button positions")
    print("- Coordinates change if screen resolution or window position changes")

def analyze_screen_region():
    """Analyze screen region"""
    try:
        screen_size = pyautogui.size()
        print(f"\n=== Screen Information ===")
        print(f"Screen resolution: {screen_size.width} x {screen_size.height}")
        
        print(f"\n=== Coordinate Validity Check ===")
        for name, (x, y) in COORDS.items():
            if 0 <= x < screen_size.width and 0 <= y < screen_size.height:
                print(f"✅ {name}: ({x}, {y}) - Valid")
            else:
                print(f"❌ {name}: ({x}, {y}) - Out of screen bounds")
                
    except Exception as e:
        print(f"Screen analysis error: {e}")

def main():
    """Main execution"""
    print("Action Tracker Coordinate Validation Tool")
    print("=" * 40)
    
    # Screen analysis
    analyze_screen_region()
    
    # Take screenshot
    screenshot_path = take_screenshot_with_markers()
    
    # Show click sequence
    test_click_sequence()
    
    print("\n" + "=" * 40)
    print("Validation complete!")
    
    if screenshot_path:
        print(f"Check screenshot to verify coordinate accuracy:")
        print(f"File: {screenshot_path}")

if __name__ == "__main__":
    main()