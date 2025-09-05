"""
PokerGFX Action Tracker - 실제 실행 스크립트
간단하고 직접적인 자동화
"""

import pyautogui
import pygetwindow as gw
import time
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def main():
    print("\n" + "="*60)
    print("POKERGFX ACTION TRACKER - AUTOMATED INPUT")
    print("="*60)
    
    # 1. PokerGFX Action Tracker 찾기
    print("\n[1] Finding PokerGFX Action Tracker...")
    
    windows = gw.getWindowsWithTitle('PokerGFX Action Tracker')
    if not windows:
        print("   ERROR: PokerGFX Action Tracker not found!")
        print("   Please start the program first.")
        return
    
    window = windows[0]
    print(f"   FOUND: {window.title}")
    
    # 2. 윈도우 활성화
    print("\n[2] Activating window...")
    
    if window.isMinimized:
        window.restore()
    
    window.activate()
    time.sleep(1)
    
    # 화면 중앙으로 이동
    screen_w, screen_h = pyautogui.size()
    window.moveTo(100, 100)
    window.resizeTo(1200, 800)
    time.sleep(1)
    
    print(f"   Window positioned at (100, 100)")
    print(f"   Size: 1200x800")
    
    # 3. 스크린샷
    print("\n[3] Taking screenshot...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    screenshot.save(f"pokergfx_ready_{timestamp}.png")
    print(f"   Saved: pokergfx_ready_{timestamp}.png")
    
    # 4. 자동 입력 시작
    print("\n[4] Starting automated input in 3 seconds...")
    print("    PRESS ESC TO STOP!")
    
    for i in range(3, 0, -1):
        print(f"    {i}...")
        time.sleep(1)
    
    # 테스트 데이터
    players = [
        {"name": "Mike Test", "chips": "1000000"},
        {"name": "John Demo", "chips": "2000000"},
        {"name": "Test Player", "chips": "1500000"}
    ]
    
    # 윈도우 내 플레이어 위치 (상대 좌표)
    # 실제 좌표는 Action Tracker UI에 맞게 조정 필요
    base_x = window.left
    base_y = window.top
    
    # 첫 번째 플레이어 위치 (예시)
    player_x = base_x + 200
    player_y = base_y + 200
    
    print(f"\n[5] Processing {len(players)} players...")
    
    for i, player in enumerate(players):
        print(f"\n   Player {i+1}: {player['name']}")
        
        # 플레이어 위치 클릭
        click_x = player_x
        click_y = player_y + (i * 50)  # 50픽셀씩 아래로
        
        print(f"   - Moving to ({click_x}, {click_y})")
        pyautogui.moveTo(click_x, click_y, duration=0.5)
        
        print(f"   - Clicking...")
        pyautogui.click()
        time.sleep(0.5)
        
        print(f"   - Double-clicking to edit...")
        pyautogui.doubleClick()
        time.sleep(1)
        
        print(f"   - Clearing field...")
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        time.sleep(0.3)
        
        print(f"   - Typing name: {player['name']}")
        pyautogui.typewrite(player['name'])
        time.sleep(0.5)
        
        print(f"   - Moving to next field...")
        pyautogui.press('tab')
        time.sleep(0.3)
        
        print(f"   - Typing chips: {player['chips']}")
        pyautogui.typewrite(player['chips'])
        time.sleep(0.5)
        
        print(f"   - Confirming...")
        pyautogui.press('enter')
        time.sleep(1)
        
        print(f"   [OK] Player {i+1} updated!")
    
    # 6. 완료
    print("\n" + "="*60)
    print("AUTOMATION COMPLETE!")
    print("="*60)
    
    # 최종 스크린샷
    screenshot = pyautogui.screenshot()
    screenshot.save(f"pokergfx_complete_{timestamp}.png")
    print(f"\nFinal screenshot: pokergfx_complete_{timestamp}.png")

if __name__ == "__main__":
    print("\n*** POKERGFX ACTION TRACKER AUTOMATION ***")
    print("\nThis script will:")
    print("1. Find and activate PokerGFX Action Tracker")
    print("2. Automatically input player data")
    print("3. Use mouse clicks and keyboard typing")
    print("\nMAKE SURE:")
    print("- PokerGFX Action Tracker is running")
    print("- You have saved any important data")
    print("- Press ESC to emergency stop\n")
    
    confirm = input("Ready to start? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\n[STOPPED] User interrupted")
        except Exception as e:
            print(f"\n\n[ERROR] {e}")
    else:
        print("\nCancelled.")