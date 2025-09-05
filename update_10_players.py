"""
10 Players Name Update Automation
10명의 플레이어 이름을 자동으로 변경
"""

import pyautogui
import time
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 10명의 플레이어 좌표 (제공받은 좌표)
PLAYER_COORDINATES = {
    'player1': (215, 354),      # 기존 좌표
    'player2': (374, 359),
    'player3': (544, 362),
    'player4': (722, 359),
    'player5': (886, 356),
    'player6': (1051, 354),
    'player7': (1213, 355),
    'player8': (1385, 383),
    'player9': (1549, 367),
    'player10': (1705, 356),
}

# 테스트용 플레이어 이름 데이터
TEST_PLAYERS = [
    {"num": 1, "name": "Daniel Negreanu", "chips": 1500000},
    {"num": 2, "name": "Phil Ivey", "chips": 2000000},
    {"num": 3, "name": "Phil Hellmuth", "chips": 1800000},
    {"num": 4, "name": "Doyle Brunson", "chips": 1200000},
    {"num": 5, "name": "Antonio Esfandiari", "chips": 2500000},
    {"num": 6, "name": "Mike Matusow", "chips": 900000},
    {"num": 7, "name": "Tom Dwan", "chips": 3000000},
    {"num": 8, "name": "Viktor Blom", "chips": 1600000},
    {"num": 9, "name": "Patrik Antonius", "chips": 2200000},
    {"num": 10, "name": "Gus Hansen", "chips": 1100000}
]

def update_player(player_num, name, chips=None):
    """단일 플레이어 업데이트"""
    
    # 플레이어 좌표 가져오기
    coord_key = f'player{player_num}'
    if coord_key not in PLAYER_COORDINATES:
        print(f"  [ERROR] Player {player_num} coordinates not found")
        return False
    
    x, y = PLAYER_COORDINATES[coord_key]
    
    try:
        # 1. 플레이어 위치 클릭
        print(f"  - Clicking Player {player_num} at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.5)
        
        # 2. 더블클릭으로 편집 모드 진입
        print(f"  - Double-clicking to edit")
        pyautogui.doubleClick()
        time.sleep(0.8)
        
        # 3. 기존 텍스트 전체 선택 및 삭제
        print(f"  - Clearing existing text")
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.press('delete')
        time.sleep(0.2)
        
        # 4. 새 이름 입력
        print(f"  - Typing: {name}")
        pyautogui.typewrite(name)
        time.sleep(0.3)
        
        # 5. 칩 입력 (옵션)
        if chips:
            pyautogui.press('tab')
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.2)
            pyautogui.typewrite(str(chips))
            time.sleep(0.3)
        
        # 6. Enter로 확인
        print(f"  - Confirming with Enter")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        print(f"  [OK] Player {player_num} updated successfully!")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to update Player {player_num}: {e}")
        return False

def update_all_players(players_data=None):
    """모든 플레이어 업데이트"""
    
    if players_data is None:
        players_data = TEST_PLAYERS
    
    print("\n" + "="*60)
    print("10 PLAYERS UPDATE AUTOMATION")
    print("="*60)
    
    print(f"\nUpdating {len(players_data)} players...")
    print("Starting in 3 seconds...\n")
    
    # 카운트다운
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # 통계
    success_count = 0
    failed_players = []
    
    # 각 플레이어 업데이트
    for player in players_data:
        player_num = player['num']
        player_name = player['name']
        player_chips = player.get('chips', None)
        
        print(f"\n[Player {player_num}] {player_name}")
        
        if update_player(player_num, player_name, player_chips):
            success_count += 1
        else:
            failed_players.append(player_num)
        
        # 다음 플레이어 전 잠시 대기
        time.sleep(0.5)
    
    # 결과 출력
    print("\n" + "="*60)
    print("UPDATE COMPLETE")
    print("="*60)
    print(f"Success: {success_count}/{len(players_data)}")
    
    if failed_players:
        print(f"Failed players: {failed_players}")
    
    # 스크린샷 저장
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    filename = f"10players_update_{timestamp}.png"
    screenshot.save(filename)
    print(f"\nScreenshot saved: {filename}")
    
    return success_count == len(players_data)

def quick_test():
    """빠른 테스트 (처음 3명만)"""
    print("\n" + "="*60)
    print("QUICK TEST - First 3 Players")
    print("="*60)
    
    test_data = TEST_PLAYERS[:3]  # 처음 3명만
    update_all_players(test_data)

def show_coordinates():
    """좌표 확인"""
    print("\n" + "="*60)
    print("PLAYER COORDINATES")
    print("="*60)
    
    for player, (x, y) in PLAYER_COORDINATES.items():
        print(f"{player:10s}: ({x:4d}, {y:4d})")

def main():
    """메인 메뉴"""
    print("\n" + "="*60)
    print("10 PLAYERS AUTOMATION SYSTEM")
    print("="*60)
    
    print("\nOptions:")
    print("1. Update ALL 10 players")
    print("2. Quick test (first 3 players)")
    print("3. Update single player")
    print("4. Show coordinates")
    print("5. Exit")
    
    choice = input("\nSelect (1-5): ")
    
    if choice == '1':
        update_all_players()
    
    elif choice == '2':
        quick_test()
    
    elif choice == '3':
        player_num = int(input("Player number (1-10): "))
        name = input("Player name: ")
        chips = input("Chips (or press Enter to skip): ")
        
        if 1 <= player_num <= 10:
            update_player(player_num, name, chips if chips else None)
        else:
            print("Invalid player number")
    
    elif choice == '4':
        show_coordinates()
    
    elif choice == '5':
        print("Exiting...")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()