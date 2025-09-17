"""
Simple Coordinate Checker
아주 간단한 좌표 확인 도구
"""

import pyautogui
import time

def show_mouse_position():
    """5초 동안 마우스 좌표 표시"""
    print("\n" + "="*50)
    print("MOUSE COORDINATE CHECKER")
    print("="*50)
    print("\nMove your mouse around...")
    print("Position will update every 0.5 seconds")
    print("(5 seconds duration)\n")
    
    for i in range(10):
        x, y = pyautogui.position()
        screen_width, screen_height = pyautogui.size()
        
        print(f"Position: ({x:4d}, {y:4d}) | Screen: {screen_width}x{screen_height}", end='\r')
        time.sleep(0.5)
    
    print("\n\nDone!")

def check_specific_positions():
    """특정 위치 확인"""
    print("\n" + "="*50)
    print("CHECKING KNOWN POSITIONS")
    print("="*50)
    
    positions = {
        'Player1': (215, 354),
        'Player2': (386, 364),
        'Delete Button': (761, 108),
        'Edit Field': (815, 294),
        'Complete Button': (1733, 155),
    }
    
    print("\nMoving mouse to each position...")
    print("(2 seconds per position)\n")
    
    for name, (x, y) in positions.items():
        print(f"Moving to {name}: ({x}, {y})")
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(1.5)
    
    print("\nAll positions checked!")

def main():
    print("Simple Coordinate Checker")
    print("1. Show current mouse position (5 seconds)")
    print("2. Check known positions (auto move)")
    print("3. Exit")
    
    choice = input("\nSelect (1-3): ")
    
    if choice == '1':
        show_mouse_position()
    elif choice == '2':
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        check_specific_positions()
    elif choice == '3':
        print("Bye!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()