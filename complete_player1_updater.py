"""
Complete Player1 Name Updater - Fast Version
Uses all user-clicked coordinates for complete automation
"""

import pyautogui
import time
from PIL import Image, ImageDraw

# Complete set of user-clicked coordinates
COORDINATES = {
    'player1_button': (215, 354),        # Click recorded: (215, 354) - player1
    'player_edit_field': (815, 294),     # Click recorded: (815, 294) player edit
    'edit_complete_button': (1733, 155)  # Click recorded: (1733, 155) - player edit complete
}

def fast_click(x, y, description="", delay=0.3):
    """Fast click with minimal delay"""
    print(f"Click: ({x}, {y}) - {description}")
    pyautogui.click(x, y)
    time.sleep(delay)

def fast_type(text):
    """Fast text input"""
    print(f"Type: '{text}'")
    pyautogui.hotkey('ctrl', 'a')  # Select all
    time.sleep(0.1)
    pyautogui.typewrite(str(text))
    time.sleep(0.1)

def test_all_coordinates():
    """Test all coordinates with markers"""
    print("Testing all coordinates...")
    
    try:
        screenshot = pyautogui.screenshot()
        draw = ImageDraw.Draw(screenshot)
        
        colors = ['red', 'blue', 'green']
        
        for i, (name, (x, y)) in enumerate(COORDINATES.items()):
            color = colors[i % len(colors)]
            
            # Draw cross marker
            draw.line([(x-30, y), (x+30, y)], fill=color, width=5)
            draw.line([(x, y-30), (x, y+30)], fill=color, width=5)
            
            # Draw label
            draw.text((x+35, y-20), f"{name}: ({x},{y})", fill=color)
            
            print(f"{i+1}. {name}: ({x}, {y})")
        
        screenshot.save("complete_coordinates_test.png")
        print("Complete coordinate test saved: complete_coordinates_test.png")
        
    except Exception as e:
        print(f"Test failed: {e}")

def update_player1_complete(new_name):
    """Complete Player1 name update with finish button"""
    print("=" * 60)
    print(f"FAST UPDATE: Player1 -> '{new_name}'")
    print("=" * 60)
    
    try:
        # Step 1: Click Player1 button (fast)
        print("[1/4] Player1 button")
        fast_click(COORDINATES['player1_button'][0], 
                  COORDINATES['player1_button'][1], 
                  "Player1", 0.5)
        
        # Step 2: Click edit field (fast)  
        print("[2/4] Edit field")
        fast_click(COORDINATES['player_edit_field'][0], 
                  COORDINATES['player_edit_field'][1], 
                  "Edit field", 0.3)
        
        # Step 3: Type new name (fast)
        print("[3/4] Enter name")
        fast_type(new_name)
        
        # Step 4: Click complete button (NEW!)
        print("[4/4] Complete button")
        fast_click(COORDINATES['edit_complete_button'][0], 
                  COORDINATES['edit_complete_button'][1], 
                  "Complete", 0.3)
        
        print("\n" + "=" * 60)
        print(f"COMPLETE SUCCESS: '{new_name}' - FAST MODE")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"Update failed: {e}")
        return False

def quick_test():
    """Quick test function"""
    test_name = "QuickTest"
    
    print("QUICK TEST MODE")
    print("=" * 30)
    print(f"Testing with name: '{test_name}'")
    print("Make sure Action Tracker is ready!")
    
    # Quick countdown
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.8)
    
    print("GO!")
    success = update_player1_complete(test_name)
    
    if success:
        print("\nQUICK TEST SUCCESS!")
    else:
        print("\nQUICK TEST FAILED!")
    
    return success

def main():
    """Main function with fast options"""
    print("Complete Player1 Updater - FAST VERSION")
    print("=" * 45)
    print("Coordinates collected:")
    for i, (name, (x, y)) in enumerate(COORDINATES.items(), 1):
        print(f"  {i}. {name}: ({x}, {y})")
    
    print("\nFAST OPTIONS:")
    print("1. Test coordinates")
    print("2. Custom name update")  
    print("3. Quick test (QuickTest)")
    
    try:
        choice = input("\nChoose (1/2/3): ").strip()
        
        if choice == "1":
            test_all_coordinates()
            
        elif choice == "2":
            new_name = input("Enter name: ").strip()
            if not new_name:
                print("No name entered.")
                return
                
            print(f"\nUPDATING TO: '{new_name}'")
            print("Ready? Starting in 2 seconds...")
            time.sleep(2)
            
            success = update_player1_complete(new_name)
            print("DONE!" if success else "FAILED!")
            
        elif choice == "3":
            quick_test()
        
        else:
            print("Invalid choice.")
            
    except KeyboardInterrupt:
        print("\nCancelled.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()