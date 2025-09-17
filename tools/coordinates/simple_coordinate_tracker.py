"""
간단한 마우스 좌표 추적기
실시간으로 마우스 좌표를 표시
"""

import pyautogui
import time

def simple_tracker():
    """간단한 실시간 좌표 추적"""
    print("=" * 60)
    print("SIMPLE MOUSE COORDINATE TRACKER")
    print("=" * 60)
    print("Move your mouse to see coordinates")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        while True:
            # Get current mouse position
            x, y = pyautogui.position()
            
            # Get pixel color at current position
            try:
                r, g, b = pyautogui.pixel(x, y)
                color_info = f"RGB({r}, {g}, {b})"
            except:
                color_info = "RGB(?, ?, ?)"
            
            # Display position and color
            position_str = f"Position: ({x:4}, {y:4})"
            print(f"\r{position_str} | Color: {color_info}     ", end="", flush=True)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nStopped by user")
        print("\nLast position: ({}, {})".format(x, y))

if __name__ == "__main__":
    print(f"Screen Size: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    print()
    simple_tracker()