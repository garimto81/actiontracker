"""
Player1 Name Changer - Simple Version
Uses user-clicked coordinates: (215, 354) and (815, 294)
"""

import pyautogui
import time
from PIL import Image, ImageDraw

# User-clicked coordinates
COORDINATES = {
    'player1_button': (215, 354),     # Click recorded: (215, 354) - player1
    'player_edit_field': (815, 294)   # Click recorded: (815, 294) player edit
}

def safe_click(x, y, description=""):
    """Safe click with description"""
    try:
        print(f"Clicking: ({x}, {y}) - {description}")
        pyautogui.click(x, y)
        time.sleep(0.8)  # Wait after click
        return True
    except Exception as e:
        print(f"Click failed: {e}")
        return False

def safe_type(text, clear_first=True):
    """Safe text input"""
    try:
        if clear_first:
            print("Clearing existing text...")
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
        print(f"Typing: '{text}'")
        pyautogui.typewrite(str(text))
        time.sleep(0.2)
        return True
    except Exception as e:
        print(f"Typing failed: {e}")
        return False

def test_coordinates():
    """Test coordinates by showing markers"""
    print("Testing coordinates...")
    
    try:
        screenshot = pyautogui.screenshot()
        draw = ImageDraw.Draw(screenshot)
        
        # Draw markers for each coordinate
        colors = ['red', 'blue']
        names = list(COORDINATES.keys())
        
        for i, (name, (x, y)) in enumerate(COORDINATES.items()):
            color = colors[i]
            
            # Draw cross marker
            draw.line([(x-25, y), (x+25, y)], fill=color, width=4)
            draw.line([(x, y-25), (x, y+25)], fill=color, width=4)
            
            # Draw label
            draw.text((x+30, y-15), f"{name}: ({x},{y})", fill=color)
            
            print(f"{name}: ({x}, {y})")
        
        screenshot.save("test_coordinates.png")
        print("Coordinate test image saved: test_coordinates.png")
        
    except Exception as e:
        print(f"Test failed: {e}")

def update_player1_name(new_name):
    """Update Player1 name using clicked coordinates"""
    print("=" * 50)
    print(f"Updating Player1 name to: '{new_name}'")
    print("=" * 50)
    
    try:
        # Step 1: Click Player1 button
        print("\n[Step 1] Click Player1 button")
        if not safe_click(COORDINATES['player1_button'][0], 
                          COORDINATES['player1_button'][1], 
                          "Player1 button"):
            return False
        
        # Step 2: Click edit field and enter name
        print("\n[Step 2] Click edit field")
        if not safe_click(COORDINATES['player_edit_field'][0], 
                          COORDINATES['player_edit_field'][1], 
                          "Edit field"):
            return False
        
        # Step 3: Type new name
        print(f"\n[Step 3] Enter new name")
        if not safe_type(new_name, clear_first=True):
            return False
        
        # Step 4: Press Enter to confirm
        print(f"\n[Step 4] Press Enter to confirm")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print("\n" + "=" * 50)
        print(f"SUCCESS: Player1 name updated to '{new_name}'")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"Update failed: {e}")
        return False

def main():
    """Main function"""
    print("Player1 Name Changer")
    print("=" * 30)
    print("Collected coordinates:")
    for name, (x, y) in COORDINATES.items():
        print(f"  {name}: ({x}, {y})")
    print()
    print("Options:")
    print("1. Test coordinates (show markers)")
    print("2. Update Player1 name")
    
    try:
        choice = input("\nChoose (1 or 2): ").strip()
        
        if choice == "1":
            test_coordinates()
            
        elif choice == "2":
            new_name = input("Enter new player name: ").strip()
            if not new_name:
                print("Please enter a name.")
                return
                
            print(f"\nStarting update to '{new_name}'...")
            print("Make sure Action Tracker is active!")
            
            # Countdown
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            
            print("\nStarting!")
            success = update_player1_name(new_name)
            
            if success:
                print("\nUPDATE SUCCESS!")
                print("Check Player1 button in Action Tracker to verify.")
            else:
                print("\nUPDATE FAILED!")
                print("Please check if coordinates are correct.")
        
        else:
            print("Invalid choice.")
            
    except KeyboardInterrupt:
        print("\nCancelled by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()