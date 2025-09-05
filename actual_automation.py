"""
Action Tracker REAL Automation Script
실제로 작동하는 자동 입력 스크립트
"""

import pyautogui
import pygetwindow as gw
import time
import sys
import json
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def find_action_tracker():
    """Action Tracker 윈도우 찾기"""
    print("[1] Searching for Action Tracker window...")
    
    # 모든 윈도우 확인
    all_windows = gw.getAllTitles()
    print(f"   Found {len(all_windows)} windows")
    
    # Action Tracker 관련 윈도우 찾기
    action_tracker_windows = []
    for title in all_windows:
        if 'action' in title.lower() or 'tracker' in title.lower() or 'poker' in title.lower():
            action_tracker_windows.append(title)
            print(f"   - Possible match: {title}")
    
    if not action_tracker_windows:
        print("   [ERROR] No Action Tracker window found!")
        print("   Please make sure Action Tracker is running")
        return None
    
    # 첫 번째 매칭 윈도우 사용
    target_window = action_tracker_windows[0]
    window = gw.getWindowsWithTitle(target_window)[0]
    
    print(f"   [OK] Found: {target_window}")
    return window

def activate_window(window):
    """윈도우 활성화"""
    print("[2] Activating window...")
    
    try:
        # 최소화된 경우 복원
        if window.isMinimized:
            window.restore()
            time.sleep(0.5)
        
        # 윈도우 활성화
        window.activate()
        time.sleep(0.5)
        
        # 최상위로 가져오기
        window.maximize()
        time.sleep(0.5)
        
        print(f"   [OK] Window activated at position ({window.left}, {window.top})")
        print(f"   Size: {window.width}x{window.height}")
        return True
        
    except Exception as e:
        print(f"   [ERROR] Failed to activate window: {e}")
        return False

def click_player_position(player_num):
    """플레이어 위치 클릭"""
    # 플레이어 좌표 (1920x1080 기준)
    player_coords = [
        (215, 354),   # Player 1
        (386, 364),   # Player 2
        (560, 485),   # Player 3
        (559, 486),   # Player 4
        (557, 364),   # Player 5
        (721, 362),   # Player 6
        (737, 369),   # Player 7
        (890, 369),   # Player 8
        (860, 364),   # Player 9
        (1037, 357),  # Player 10
    ]
    
    if player_num < 1 or player_num > 10:
        print(f"   [ERROR] Invalid player number: {player_num}")
        return False
    
    x, y = player_coords[player_num - 1]
    
    # 현재 해상도에 맞게 조정
    screen_width, screen_height = pyautogui.size()
    if screen_width != 1920 or screen_height != 1080:
        # 비율 조정
        x = int(x * screen_width / 1920)
        y = int(y * screen_height / 1080)
        print(f"   Adjusted coordinates for {screen_width}x{screen_height}")
    
    print(f"   Clicking Player {player_num} at ({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(0.5)
    return True

def input_player_data(name, chips):
    """플레이어 데이터 입력"""
    print(f"   Inputting: {name} with {chips} chips")
    
    # 더블클릭으로 편집 모드 진입
    pyautogui.doubleClick()
    time.sleep(1)
    
    # 기존 텍스트 전체 선택 및 삭제
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    pyautogui.press('delete')
    time.sleep(0.2)
    
    # 이름 입력
    pyautogui.typewrite(name)
    time.sleep(0.5)
    
    # Tab 키로 다음 필드로 이동
    pyautogui.press('tab')
    time.sleep(0.3)
    
    # 칩 수량 입력
    pyautogui.typewrite(str(chips))
    time.sleep(0.5)
    
    # Enter로 확인
    pyautogui.press('enter')
    time.sleep(1)
    
    print(f"   [OK] Data input complete")
    return True

def automated_input_test():
    """자동 입력 테스트"""
    print("\n" + "="*60)
    print("ACTION TRACKER AUTOMATED INPUT TEST")
    print("="*60)
    
    # 테스트 데이터
    test_players = [
        {"num": 1, "name": "Test Player 1", "chips": 1000000},
        {"num": 2, "name": "Test Player 2", "chips": 2000000},
        {"num": 3, "name": "Test Player 3", "chips": 1500000},
    ]
    
    # Action Tracker 찾기
    window = find_action_tracker()
    if not window:
        print("\n[FAILED] Cannot proceed without Action Tracker window")
        return False
    
    # 윈도우 활성화
    if not activate_window(window):
        print("\n[FAILED] Cannot activate window")
        return False
    
    print("\n[3] Starting automated input in 3 seconds...")
    print("   Press ESC to stop at any time")
    time.sleep(3)
    
    # 각 플레이어 처리
    success_count = 0
    for player in test_players:
        print(f"\n[4] Processing Player {player['num']}...")
        
        try:
            # 플레이어 위치 클릭
            if not click_player_position(player['num']):
                continue
            
            # 데이터 입력
            if not input_player_data(player['name'], player['chips']):
                continue
            
            success_count += 1
            
        except Exception as e:
            print(f"   [ERROR] Failed to process player {player['num']}: {e}")
            continue
    
    # 결과 출력
    print("\n" + "="*60)
    print(f"RESULTS: {success_count}/{len(test_players)} players processed successfully")
    print("="*60)
    
    return success_count > 0

def mouse_position_test():
    """마우스 위치 테스트"""
    print("\n" + "="*60)
    print("MOUSE POSITION TEST")
    print("="*60)
    print("Move your mouse to see coordinates")
    print("Press Ctrl+C to stop")
    print("-"*60)
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: ({x}, {y})", end='\r')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nTest stopped")

def screenshot_test():
    """스크린샷 테스트"""
    print("\n[5] Taking screenshot...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    
    screenshot = pyautogui.screenshot()
    screenshot.save(f"c:\\claude02\\ActionTracker_Automation\\{filename}")
    
    print(f"   [OK] Screenshot saved: {filename}")
    return filename

def main():
    """메인 함수"""
    print("="*60)
    print("ACTION TRACKER REAL AUTOMATION")
    print("="*60)
    print("\nOptions:")
    print("1. Automated Input Test (REAL)")
    print("2. Mouse Position Test")
    print("3. Screenshot Test")
    print("4. Find Windows Test")
    print("5. Exit")
    print("-"*60)
    
    choice = input("Select (1-5): ")
    
    if choice == '1':
        automated_input_test()
    elif choice == '2':
        mouse_position_test()
    elif choice == '3':
        screenshot_test()
    elif choice == '4':
        window = find_action_tracker()
        if window:
            print(f"\nWindow found: {window.title}")
            print(f"Position: ({window.left}, {window.top})")
            print(f"Size: {window.width}x{window.height}")
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    # 경고 메시지
    print("\nWARNING: This script will control your mouse and keyboard!")
    print("Make sure Action Tracker is running before starting.")
    print("Press ESC to emergency stop.\n")
    
    confirm = input("Continue? (y/n): ")
    if confirm.lower() == 'y':
        main()
    else:
        print("Cancelled")