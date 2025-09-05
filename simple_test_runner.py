"""
Simple Test Runner for Action Tracker Automation
간단한 테스트 실행 스크립트
"""

import json
import csv
import time
import pyautogui
from datetime import datetime

def load_test_data():
    """테스트 데이터 로드"""
    try:
        # JSON 파일에서 데이터 로드
        with open('test_players_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ JSON 데이터 로드 성공: {len(data['players'])}명의 플레이어")
            return data['players']
    except:
        print("❌ JSON 파일 로드 실패, CSV 시도 중...")
        
        # CSV 파일에서 데이터 로드
        try:
            players = []
            with open('test_players.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    players.append({
                        'num': int(row['player_num']),
                        'name': row['name'],
                        'chips': int(row['chips'])
                    })
            print(f"✅ CSV 데이터 로드 성공: {len(players)}명의 플레이어")
            return players
        except Exception as e:
            print(f"❌ 데이터 로드 실패: {e}")
            return []

def test_coordinates():
    """좌표 테스트 (클릭 없이)"""
    print("\n" + "="*60)
    print("좌표 테스트 모드 - 클릭 없이 위치만 확인")
    print("="*60)
    
    # 테스트용 좌표
    coordinates = {
        'player1': (215, 354),
        'player2': (386, 364),
        'player3': (560, 485),
        'player4': (559, 486),
        'player5': (557, 364),
        'player6': (721, 362),
        'player7': (737, 369),
        'player8': (890, 369),
        'player9': (860, 364),
        'player10': (1037, 357)
    }
    
    players = load_test_data()
    
    if not players:
        print("테스트 데이터가 없습니다!")
        return
    
    print(f"\n현재 화면 해상도: {pyautogui.size()}")
    print("3초 후 테스트 시작...\n")
    time.sleep(3)
    
    for player in players[:10]:  # 최대 10명만
        player_num = player['num']
        player_name = player['name']
        player_chips = player['chips']
        
        if player_num <= 10:
            coord_key = f'player{player_num}'
            x, y = coordinates[coord_key]
            
            print(f"Player {player_num}: {player_name}")
            print(f"  - 칩: {player_chips:,}")
            print(f"  - 좌표: ({x}, {y})")
            print(f"  - 마우스 이동 중...")
            
            # 마우스만 이동 (클릭 없음)
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.5)
            
    print("\n✅ 좌표 테스트 완료!")

def simulate_input():
    """입력 시뮬레이션 (실제 클릭 없이)"""
    print("\n" + "="*60)
    print("입력 시뮬레이션 모드 - 로직만 실행")
    print("="*60)
    
    players = load_test_data()
    
    if not players:
        print("테스트 데이터가 없습니다!")
        return
    
    print(f"\n총 {len(players)}명의 플레이어 처리 시뮬레이션")
    print("-" * 40)
    
    start_time = time.time()
    
    for i, player in enumerate(players, 1):
        print(f"\n[{i}/{len(players)}] 처리 중: {player['name']}")
        print(f"  1. 플레이어 {player['num']} 위치로 이동")
        print(f"  2. 더블클릭으로 편집 모드 진입")
        print(f"  3. 이름 입력: {player['name']}")
        print(f"  4. 칩 입력: {player['chips']:,}")
        print(f"  5. Enter 키로 확인")
        
        # 시뮬레이션 딜레이
        time.sleep(0.2)
    
    elapsed = time.time() - start_time
    print(f"\n✅ 시뮬레이션 완료!")
    print(f"총 소요 시간: {elapsed:.2f}초")
    print(f"플레이어당 평균: {elapsed/len(players):.2f}초")

def show_info():
    """정보 표시"""
    print("\n" + "="*60)
    print("Action Tracker 자동화 테스트 정보")
    print("="*60)
    
    print("\n📊 시스템 정보:")
    print(f"  - 화면 해상도: {pyautogui.size()}")
    print(f"  - 현재 마우스 위치: {pyautogui.position()}")
    print(f"  - 안전 모드: {pyautogui.FAILSAFE}")
    
    players = load_test_data()
    if players:
        print(f"\n📋 테스트 데이터:")
        print(f"  - 총 플레이어 수: {len(players)}")
        total_chips = sum(p['chips'] for p in players)
        print(f"  - 총 칩 합계: {total_chips:,}")
        print(f"  - 평균 칩: {total_chips//len(players):,}")
        
        print(f"\n👥 플레이어 목록:")
        for p in players[:5]:  # 처음 5명만 표시
            print(f"  {p['num']}. {p['name']}: {p['chips']:,} chips")
        if len(players) > 5:
            print(f"  ... 외 {len(players)-5}명")

def main_menu():
    """메인 메뉴"""
    while True:
        print("\n" + "="*60)
        print("Action Tracker 자동화 테스트 시스템")
        print("="*60)
        print("\n메뉴를 선택하세요:")
        print("1. 정보 표시")
        print("2. 좌표 테스트 (마우스 이동만)")
        print("3. 입력 시뮬레이션 (로직만)")
        print("4. GUI 테스트 앱 실행")
        print("5. 종료")
        print("-" * 40)
        
        choice = input("선택 (1-5): ")
        
        if choice == '1':
            show_info()
        elif choice == '2':
            test_coordinates()
        elif choice == '3':
            simulate_input()
        elif choice == '4':
            print("\nGUI 앱 실행 중...")
            try:
                import test_input_app
                app = test_input_app.TestInputApp()
                app.run()
            except Exception as e:
                print(f"GUI 앱 실행 실패: {e}")
        elif choice == '5':
            print("\n프로그램을 종료합니다.")
            break
        else:
            print("\n❌ 잘못된 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    print("=" * 60)
    print("Action Tracker Automation Test System")
    print("=" * 60)
    print("\n⚠️ 주의: ESC 키를 누르면 자동화가 중지됩니다.")
    
    # 안전 설정
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    main_menu()