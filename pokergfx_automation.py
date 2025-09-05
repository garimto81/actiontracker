"""
PokerGFX Action Tracker Automation
실제 작동하는 자동화 스크립트
"""

import pyautogui
import pygetwindow as gw
import time
import sys
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def find_pokergfx_action_tracker():
    """PokerGFX Action Tracker 윈도우 찾기"""
    print("\n[STEP 1] Finding PokerGFX Action Tracker...")
    
    # 모든 윈도우 확인
    all_windows = gw.getAllTitles()
    
    # PokerGFX Action Tracker 찾기
    target_window = None
    for title in all_windows:
        if 'PokerGFX Action Tracker' in title:
            target_window = title
            break
    
    if not target_window:
        print("   [ERROR] PokerGFX Action Tracker not found!")
        print("   Available windows:")
        for title in all_windows:
            if 'poker' in title.lower() or 'gfx' in title.lower():
                print(f"     - {title}")
        return None
    
    window = gw.getWindowsWithTitle(target_window)[0]
    print(f"   [OK] Found: {target_window}")
    print(f"   Position: ({window.left}, {window.top})")
    print(f"   Size: {window.width}x{window.height}")
    
    return window

def activate_and_position_window(window):
    """윈도우 활성화 및 위치 조정"""
    print("\n[STEP 2] Activating window...")
    
    try:
        # 최소화된 경우 복원
        if window.isMinimized:
            window.restore()
            time.sleep(0.5)
        
        # 윈도우를 화면 중앙으로 이동
        screen_width, screen_height = pyautogui.size()
        window_width = 1200  # 적절한 크기로 설정
        window_height = 800
        
        # 중앙 위치 계산
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        
        # 윈도우 이동 및 크기 조정
        window.moveTo(center_x, center_y)
        time.sleep(0.5)
        window.resizeTo(window_width, window_height)
        time.sleep(0.5)
        
        # 활성화
        window.activate()
        time.sleep(0.5)
        
        print(f"   [OK] Window positioned at ({center_x}, {center_y})")
        print(f"   Size: {window_width}x{window_height}")
        return True
        
    except Exception as e:
        print(f"   [ERROR] Failed to activate window: {e}")
        return False

def take_screenshot(name="pokergfx"):
    """스크린샷 촬영"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    path = f"c:\\claude02\\ActionTracker_Automation\\{filename}"
    
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    
    print(f"   Screenshot saved: {filename}")
    return path

def click_at_position(x, y, description=""):
    """특정 위치 클릭"""
    print(f"   Clicking {description} at ({x}, {y})")
    pyautogui.moveTo(x, y, duration=0.5)
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(0.5)

def input_text(text, clear_first=True):
    """텍스트 입력"""
    if clear_first:
        # 기존 텍스트 전체 선택 및 삭제
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
    
    # 텍스트 입력
    pyautogui.typewrite(text, interval=0.05)
    time.sleep(0.3)

def automated_player_update():
    """플레이어 자동 업데이트"""
    print("\n" + "="*60)
    print("POKERGFX ACTION TRACKER AUTOMATION")
    print("="*60)
    
    # 테스트 데이터
    test_data = [
        {"position": 1, "name": "Daniel N.", "chips": "1.5M"},
        {"position": 2, "name": "Phil I.", "chips": "2.0M"},
        {"position": 3, "name": "Tom D.", "chips": "3.0M"},
    ]
    
    # Action Tracker 찾기
    window = find_pokergfx_action_tracker()
    if not window:
        return False
    
    # 윈도우 활성화
    if not activate_and_position_window(window):
        return False
    
    # 스크린샷 (현재 상태)
    print("\n[STEP 3] Taking initial screenshot...")
    take_screenshot("before_update")
    
    print("\n[STEP 4] Starting automation in 3 seconds...")
    print("         Press ESC to stop at any time!")
    for i in range(3, 0, -1):
        print(f"         {i}...")
        time.sleep(1)
    
    # 윈도우 기준점 (왼쪽 상단)
    base_x = window.left
    base_y = window.top
    
    # 플레이어 위치 (윈도우 내 상대 좌표)
    player_positions = [
        (100, 150),  # Player 1
        (100, 200),  # Player 2
        (100, 250),  # Player 3
        (100, 300),  # Player 4
        (100, 350),  # Player 5
    ]
    
    print("\n[STEP 5] Updating players...")
    
    for data in test_data:
        pos = data["position"]
        name = data["name"]
        chips = data["chips"]
        
        print(f"\n   Player {pos}: {name} ({chips})")
        
        # 플레이어 위치 클릭 (절대 좌표)
        if pos <= len(player_positions):
            rel_x, rel_y = player_positions[pos - 1]
            abs_x = base_x + rel_x
            abs_y = base_y + rel_y
            
            # 클릭
            click_at_position(abs_x, abs_y, f"Player {pos}")
            
            # 더블클릭으로 편집 모드
            pyautogui.doubleClick()
            time.sleep(1)
            
            # 이름 입력
            input_text(name)
            
            # Tab으로 다음 필드
            pyautogui.press('tab')
            time.sleep(0.3)
            
            # 칩 입력
            input_text(chips)
            
            # Enter로 확인
            pyautogui.press('enter')
            time.sleep(1)
            
            print(f"   [OK] Player {pos} updated")
    
    # 최종 스크린샷
    print("\n[STEP 6] Taking final screenshot...")
    take_screenshot("after_update")
    
    print("\n" + "="*60)
    print("AUTOMATION COMPLETE!")
    print("="*60)
    
    return True

def scan_window_elements():
    """윈도우 요소 스캔"""
    print("\n[SCAN] Scanning window elements...")
    
    window = find_pokergfx_action_tracker()
    if not window:
        return
    
    activate_and_position_window(window)
    
    print("\n[SCAN] Taking screenshot for analysis...")
    screenshot_path = take_screenshot("window_scan")
    
    # 윈도우 내 주요 영역 표시
    base_x = window.left
    base_y = window.top
    
    print("\n[SCAN] Key areas (relative to window):")
    print(f"   Top Menu Bar: ({base_x}, {base_y}) to ({base_x + window.width}, {base_y + 30})")
    print(f"   Player List: ({base_x}, {base_y + 100}) to ({base_x + 400}, {base_y + 600})")
    print(f"   Control Panel: ({base_x + 500}, {base_y + 100}) to ({base_x + 800}, {base_y + 400})")
    
    # 마우스 위치 추적 (5초간)
    print("\n[SCAN] Move mouse over window elements (5 seconds)...")
    start_time = time.time()
    positions = []
    
    while time.time() - start_time < 5:
        x, y = pyautogui.position()
        # 윈도우 내부인지 확인
        if base_x <= x <= base_x + window.width and base_y <= y <= base_y + window.height:
            rel_x = x - base_x
            rel_y = y - base_y
            positions.append((rel_x, rel_y))
            print(f"   Window position: ({rel_x}, {rel_y})", end='\r')
        time.sleep(0.1)
    
    print("\n[SCAN] Scan complete!")

def main_menu():
    """메인 메뉴"""
    while True:
        print("\n" + "="*60)
        print("POKERGFX ACTION TRACKER AUTOMATION")
        print("="*60)
        print("\n1. Find PokerGFX Windows")
        print("2. Scan Window Elements")
        print("3. Automated Player Update (TEST)")
        print("4. Take Screenshot")
        print("5. Exit")
        print("-"*60)
        
        choice = input("Select (1-5): ")
        
        if choice == '1':
            window = find_pokergfx_action_tracker()
            if window:
                print("\n[INFO] Window is ready for automation")
        
        elif choice == '2':
            scan_window_elements()
        
        elif choice == '3':
            automated_player_update()
        
        elif choice == '4':
            window = find_pokergfx_action_tracker()
            if window:
                activate_and_position_window(window)
                take_screenshot("manual")
        
        elif choice == '5':
            print("\nExiting...")
            break
        
        else:
            print("\n[ERROR] Invalid choice")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("POKERGFX ACTION TRACKER AUTOMATION SYSTEM")
    print("="*60)
    print("\nThis will control your mouse and keyboard!")
    print("Make sure PokerGFX Action Tracker is running.")
    print("Press ESC to emergency stop.")
    
    main_menu()