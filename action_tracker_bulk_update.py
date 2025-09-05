"""
Action Tracker 일괄 업데이트 프로그램
모든 플레이어의 이름과 칩을 한번에 변경
"""

import pyautogui
import time
import json
import random
from datetime import datetime

class ActionTrackerBulkUpdater:
    def __init__(self):
        # Action Tracker 플레이어 위치 (이전 분석 데이터)
        self.player_positions = {
            1: {"x": 320, "y": 400},
            2: {"x": 960, "y": 200},
            3: {"x": 1400, "y": 400},
            4: {"x": 1400, "y": 800},
            5: {"x": 860, "y": 950},
            6: {"x": 320, "y": 800}
        }
        
        # 액션 버튼 위치
        self.action_buttons = {
            "fold": (810, 980),
            "check": (885, 980),
            "call": (960, 980),
            "raise": (1035, 980),
            "allin": (1110, 980)
        }
        
        # 안전 설정
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.3
        
    def activate_action_tracker(self):
        """Action Tracker 창 활성화"""
        try:
            windows = pyautogui.getAllWindows()
            for window in windows:
                if "action tracker" in window.title.lower():
                    window.activate()
                    time.sleep(0.5)
                    print("[OK] Action Tracker window activated")
                    return True
        except Exception as e:
            print(f"[Warning] Could not activate window: {e}")
        return False
    
    def bulk_update_players(self, players_data):
        """모든 플레이어 일괄 업데이트"""
        print("\n" + "="*60)
        print(" BULK UPDATE - ACTION TRACKER")
        print("="*60)
        
        # Action Tracker 활성화
        if not self.activate_action_tracker():
            print("[Info] Please make sure Action Tracker is running")
        
        # 스크린샷 (업데이트 전)
        before_shot = pyautogui.screenshot()
        before_shot.save("before_bulk_update.png")
        print("[Screenshot] Before: before_bulk_update.png")
        
        success_count = 0
        
        # 각 플레이어 업데이트
        for player in players_data:
            seat = player.get('seat', 1)
            name = player.get('name', f'Player{seat}')
            chips = player.get('chips', 100000)
            
            if seat in self.player_positions:
                if self.update_single_player(seat, name, chips):
                    success_count += 1
                time.sleep(0.5)  # 각 플레이어 간 대기
        
        # 스크린샷 (업데이트 후)
        after_shot = pyautogui.screenshot()
        after_shot.save("after_bulk_update.png")
        print("[Screenshot] After: after_bulk_update.png")
        
        print("\n" + "="*60)
        print(f" UPDATE COMPLETE: {success_count}/{len(players_data)} players")
        print("="*60)
        
        return success_count
    
    def update_single_player(self, seat, name, chips):
        """단일 플레이어 업데이트"""
        try:
            pos = self.player_positions[seat]
            
            print(f"\n[Seat {seat}] Updating...")
            
            # 플레이어 위치 클릭
            pyautogui.click(pos["x"], pos["y"])
            time.sleep(0.3)
            
            # 이름 필드로 이동 (Tab 또는 직접 클릭)
            pyautogui.press('tab')
            time.sleep(0.2)
            
            # 기존 텍스트 선택 및 삭제
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # 새 이름 입력
            pyautogui.write(name)
            time.sleep(0.2)
            print(f"  Name: {name}")
            
            # 칩 필드로 이동
            pyautogui.press('tab')
            time.sleep(0.2)
            
            # 기존 값 선택 및 삭제
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            
            # 새 칩 수량 입력
            pyautogui.write(str(chips))
            time.sleep(0.2)
            print(f"  Chips: {chips:,}")
            
            # 확인 (Enter)
            pyautogui.press('enter')
            time.sleep(0.3)
            
            print(f"  [SUCCESS] Seat {seat} updated")
            return True
            
        except Exception as e:
            print(f"  [ERROR] Failed to update seat {seat}: {e}")
            return False
    
    def clear_all_players(self):
        """모든 플레이어 초기화"""
        print("\n[CLEAR] Clearing all players...")
        
        for seat in range(1, 7):
            if seat in self.player_positions:
                pos = self.player_positions[seat]
                
                # 좌석 클릭
                pyautogui.click(pos["x"], pos["y"])
                time.sleep(0.2)
                
                # Clear 또는 Delete 키
                pyautogui.press('delete')
                time.sleep(0.2)
        
        print("[CLEAR] All players cleared")
    
    def load_from_json(self, filename):
        """JSON 파일에서 플레이어 데이터 로드"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 다양한 JSON 형식 지원
            if 'Data' in data and 'Players' in data['Data']:
                # Frame Poker 형식
                players = []
                for p in data['Data']['Players']:
                    players.append({
                        'seat': p.get('seat', 1),
                        'name': p.get('name', 'Unknown'),
                        'chips': p.get('stack', 100000)
                    })
                return players
            
            elif 'players' in data:
                # 일반 형식
                return data['players']
            
            elif isinstance(data, list):
                # 리스트 형식
                return data
            
            else:
                print("[Error] Unknown JSON format")
                return []
                
        except Exception as e:
            print(f"[Error] Could not load JSON: {e}")
            return []
    
    def create_sample_players(self, num_players=6):
        """샘플 플레이어 데이터 생성"""
        names = [
            "Daniel Negreanu", "Phil Ivey", "Doyle Brunson",
            "Phil Hellmuth", "Vanessa Selbst", "Antonio Esfandiari",
            "Tom Dwan", "Viktor Blom", "Patrik Antonius",
            "Doug Polk", "Dan Smith", "Fedor Holz"
        ]
        
        random.shuffle(names)
        
        players = []
        for i in range(min(num_players, 6)):
            players.append({
                'seat': i + 1,
                'name': names[i] if i < len(names) else f"Player {i+1}",
                'chips': random.randint(50000, 500000)
            })
        
        return players
    
    def save_current_setup(self, filename="current_setup.json"):
        """현재 설정 저장"""
        # 스크린샷으로 현재 상태 캡처
        screenshot = pyautogui.screenshot()
        screenshot.save(f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        print(f"[Save] Setup saved to screenshot")

def print_menu():
    """메뉴 출력"""
    print("\n" + "="*60)
    print(" ACTION TRACKER BULK UPDATE TOOL")
    print("="*60)
    print("1. Quick Update (6 random players)")
    print("2. Custom Update (enter manually)")
    print("3. Load from JSON file")
    print("4. Tournament Setup (specific players)")
    print("5. Clear all players")
    print("6. Test single seat")
    print("7. Exit")
    print("="*60)

def manual_input():
    """수동 입력"""
    players = []
    num = int(input("How many players? (1-6): "))
    
    for i in range(min(num, 6)):
        print(f"\n[Player {i+1}]")
        name = input("Name: ")
        chips = int(input("Chips: "))
        players.append({
            'seat': i + 1,
            'name': name,
            'chips': chips
        })
    
    return players

def tournament_setups():
    """토너먼트 프리셋"""
    setups = {
        '1': {  # WSOP Main Event Style
            'name': 'WSOP Main Event Final Table',
            'players': [
                {'seat': 1, 'name': 'Koray Aldemir', 'chips': 177000000},
                {'seat': 2, 'name': 'George Holmes', 'chips': 107000000},
                {'seat': 3, 'name': 'Jack Oliver', 'chips': 33400000},
                {'seat': 4, 'name': 'Hye Park', 'chips': 14300000},
                {'seat': 5, 'name': 'Joshua Remitio', 'chips': 10100000},
                {'seat': 6, 'name': 'Alejandro Lococo', 'chips': 8200000}
            ]
        },
        '2': {  # High Roller Style
            'name': 'High Roller Final',
            'players': [
                {'seat': 1, 'name': 'Jason Koon', 'chips': 5000000},
                {'seat': 2, 'name': 'Stephen Chidwick', 'chips': 4500000},
                {'seat': 3, 'name': 'Bryn Kenney', 'chips': 4000000},
                {'seat': 4, 'name': 'Dan Smith', 'chips': 3500000},
                {'seat': 5, 'name': 'David Peters', 'chips': 3000000},
                {'seat': 6, 'name': 'Seth Davies', 'chips': 2500000}
            ]
        },
        '3': {  # Cash Game Style
            'name': 'Cash Game Session',
            'players': [
                {'seat': 1, 'name': 'Tom Dwan', 'chips': 1000000},
                {'seat': 2, 'name': 'Phil Ivey', 'chips': 1000000},
                {'seat': 3, 'name': 'Patrik Antonius', 'chips': 1000000},
                {'seat': 4, 'name': 'Doug Polk', 'chips': 1000000},
                {'seat': 5, 'name': 'Daniel Negreanu', 'chips': 1000000},
                {'seat': 6, 'name': 'Phil Hellmuth', 'chips': 1000000}
            ]
        }
    }
    
    print("\nTournament Presets:")
    for key, setup in setups.items():
        print(f"{key}. {setup['name']}")
    
    choice = input("\nSelect preset (1-3): ")
    
    if choice in setups:
        print(f"\nLoading: {setups[choice]['name']}")
        return setups[choice]['players']
    
    return []

def main():
    updater = ActionTrackerBulkUpdater()
    
    while True:
        print_menu()
        choice = input("\nChoice (1-7): ").strip()
        
        if choice == '1':
            # Quick Update
            print("\n[Quick Update] Generating 6 random players...")
            players = updater.create_sample_players(6)
            
            print("\nPlayers to update:")
            for p in players:
                print(f"  Seat {p['seat']}: {p['name']} - {p['chips']:,} chips")
            
            confirm = input("\nProceed? (y/n): ")
            if confirm.lower() == 'y':
                updater.bulk_update_players(players)
                
        elif choice == '2':
            # Custom Update
            players = manual_input()
            if players:
                updater.bulk_update_players(players)
                
        elif choice == '3':
            # Load from JSON
            filename = input("JSON filename (or press Enter for 'sample_data.json'): ").strip()
            if not filename:
                filename = "sample_data.json"
            
            players = updater.load_from_json(filename)
            if players:
                print(f"\nLoaded {len(players)} players")
                updater.bulk_update_players(players)
            else:
                print("No players loaded")
                
        elif choice == '4':
            # Tournament Setup
            players = tournament_setups()
            if players:
                updater.bulk_update_players(players)
                
        elif choice == '5':
            # Clear all
            confirm = input("Clear all players? (y/n): ")
            if confirm.lower() == 'y':
                updater.clear_all_players()
                
        elif choice == '6':
            # Test single seat
            seat = int(input("Seat number (1-6): "))
            name = input("Name: ")
            chips = int(input("Chips: "))
            
            updater.update_single_player(seat, name, chips)
            
        elif choice == '7':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice")

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" ACTION TRACKER BULK UPDATE SYSTEM")
    print("="*60)
    print("\nThis tool allows you to update all players at once")
    print("in the Action Tracker application.")
    print("\n[IMPORTANT] Make sure Action Tracker is running!")
    print("Move mouse to top-left corner to abort at any time.")
    
    input("\nPress Enter to continue...")
    
    main()