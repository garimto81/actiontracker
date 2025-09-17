"""
Test 10 Players Coordinates
10명 플레이어 좌표 테스트
"""

import pyautogui
import time

# 10명의 플레이어 좌표
COORDS = {
    1: (215, 354),
    2: (374, 359),
    3: (544, 362),
    4: (722, 359),
    5: (886, 356),
    6: (1051, 354),
    7: (1213, 355),
    8: (1385, 383),
    9: (1549, 367),
    10: (1705, 356),
}

def test_coordinates():
    """좌표 테스트 - 마우스만 이동"""
    print("="*50)
    print("10 PLAYERS COORDINATE TEST")
    print("="*50)
    print("\nMoving mouse to each player position...")
    print("Starting in 3 seconds...\n")
    
    time.sleep(3)
    
    for num, (x, y) in COORDS.items():
        print(f"Player {num:2d}: Moving to ({x:4d}, {y:4d})")
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(0.5)
    
    print("\nTest complete!")

def quick_update():
    """빠른 업데이트 테스트"""
    print("="*50)
    print("QUICK UPDATE TEST")
    print("="*50)
    
    # 테스트 데이터
    players = [
        (1, "Test1"),
        (2, "Test2"),
        (3, "Test3")
    ]
    
    print("\nUpdating first 3 players...")
    print("Starting in 3 seconds...\n")
    
    time.sleep(3)
    
    for num, name in players:
        x, y = COORDS[num]
        
        print(f"Player {num}: {name}")
        
        # 클릭
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        # 더블클릭
        pyautogui.doubleClick()
        time.sleep(0.8)
        
        # 텍스트 입력
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(name)
        time.sleep(0.3)
        
        # Enter
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print(f"  [OK] Updated\n")
    
    print("Quick update complete!")

if __name__ == "__main__":
    print("1. Test coordinates (mouse move only)")
    print("2. Quick update (first 3 players)")
    
    choice = input("\nSelect (1 or 2): ")
    
    if choice == "1":
        test_coordinates()
    elif choice == "2":
        quick_update()
    else:
        print("Invalid choice")