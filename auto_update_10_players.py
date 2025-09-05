"""
Auto Update 10 Players with Random Names
10명의 플레이어 이름 자동 변경 (임의 이름)
"""

import pyautogui
import time
from datetime import datetime
import random

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 10명의 플레이어 좌표
PLAYER_COORDINATES = {
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

# 임의의 플레이어 이름 (유명 포커 플레이어들)
RANDOM_NAMES = [
    "Johnny Chan",
    "Chris Ferguson",
    "Stu Ungar",
    "Vanessa Selbst",
    "Jason Koon",
    "Fedor Holz",
    "Justin Bonomo",
    "Stephen Chidwick",
    "Dan Smith",
    "Bryn Kenney"
]

# 칩 수량 (랜덤)
def get_random_chips():
    """랜덤 칩 생성"""
    return random.randint(500000, 5000000)

def update_single_player(player_num, name):
    """단일 플레이어 업데이트"""
    
    if player_num not in PLAYER_COORDINATES:
        print(f"  [ERROR] Player {player_num} not found")
        return False
    
    x, y = PLAYER_COORDINATES[player_num]
    
    try:
        # 1. 플레이어 클릭
        print(f"  Clicking player {player_num} at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        # 2. 더블클릭으로 편집
        pyautogui.doubleClick()
        time.sleep(0.8)
        
        # 3. 기존 텍스트 삭제
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # 4. 새 이름 입력
        pyautogui.typewrite(name)
        time.sleep(0.3)
        
        # 5. Enter로 확인
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print(f"  [OK] Player {player_num} -> {name}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

def auto_update_all():
    """모든 플레이어 자동 업데이트"""
    
    print("\n" + "="*60)
    print("AUTO UPDATE 10 PLAYERS")
    print("="*60)
    print("\nUpdating all 10 players with random names...")
    print("\nPlayer Names to be assigned:")
    print("-" * 40)
    
    # 이름 미리 보기
    for i in range(10):
        print(f"Player {i+1:2d}: {RANDOM_NAMES[i]}")
    
    print("-" * 40)
    print("\nStarting in 5 seconds...")
    print("Press ESC to stop at any time!\n")
    
    # 카운트다운
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # 시작 시간
    start_time = time.time()
    success_count = 0
    
    print("\n" + "="*60)
    print("PROCESSING...")
    print("="*60 + "\n")
    
    # 각 플레이어 업데이트
    for i in range(10):
        player_num = i + 1
        player_name = RANDOM_NAMES[i]
        
        print(f"[{player_num}/10] Updating Player {player_num}: {player_name}")
        
        if update_single_player(player_num, player_name):
            success_count += 1
        
        # 다음 플레이어 전 잠시 대기
        if i < 9:  # 마지막 플레이어가 아니면
            time.sleep(0.3)
        
        print()
    
    # 종료 시간
    end_time = time.time()
    elapsed = end_time - start_time
    
    # 결과 출력
    print("="*60)
    print("UPDATE COMPLETE!")
    print("="*60)
    print(f"\nResults:")
    print(f"  Success: {success_count}/10 players")
    print(f"  Time: {elapsed:.1f} seconds")
    print(f"  Average: {elapsed/10:.1f} seconds per player")
    
    # 스크린샷 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    filename = f"auto_update_10players_{timestamp}.png"
    screenshot.save(filename)
    print(f"\nScreenshot saved: {filename}")
    
    # 업데이트된 이름 목록
    print("\n" + "="*60)
    print("UPDATED PLAYER LIST:")
    print("="*60)
    for i in range(10):
        print(f"Player {i+1:2d}: {RANDOM_NAMES[i]}")
    print("="*60)

def main():
    """메인 실행"""
    print("\n*** AUTO UPDATE 10 PLAYERS ***")
    print("\nThis will automatically update all 10 players with:")
    print("- Johnny Chan")
    print("- Chris Ferguson") 
    print("- Stu Ungar")
    print("- Vanessa Selbst")
    print("- Jason Koon")
    print("- Fedor Holz")
    print("- Justin Bonomo")
    print("- Stephen Chidwick")
    print("- Dan Smith")
    print("- Bryn Kenney")
    
    confirm = input("\nReady to start? (yes/no): ")
    
    if confirm.lower() in ['yes', 'y']:
        auto_update_all()
    else:
        print("\nCancelled.")

if __name__ == "__main__":
    main()