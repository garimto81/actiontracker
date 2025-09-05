"""
Frame Poker → Action Tracker Reverse Bridge
Frame Poker의 데이터를 Action Tracker로 전송하는 역방향 브릿지
"""

import socket
import json
import time
import requests
import pyautogui
import threading
from datetime import datetime

class FramePokerToActionTracker:
    def __init__(self):
        # Frame Poker 서버 설정
        self.fp_host = '127.0.0.1'
        self.fp_port = 8088  # HTTP API
        
        # Action Tracker 설정
        self.at_host = '127.0.0.1'
        self.at_tcp_port = 8080  # TCP 포트 (추정)
        
        # Action Tracker 좌표 (이전 분석 데이터)
        self.at_positions = {
            1: {"x": 320, "y": 400},
            2: {"x": 960, "y": 200},
            3: {"x": 1400, "y": 400},
            4: {"x": 1400, "y": 800},
            5: {"x": 860, "y": 950},
            6: {"x": 320, "y": 800}
        }
        
        # Action buttons 좌표
        self.action_buttons = {
            "fold": (810, 980),
            "check": (885, 980),
            "call": (960, 980),
            "raise": (1035, 980),
            "allin": (1110, 980)
        }
        
        self.running = False
        self.last_data = None
        
    def start(self):
        """역방향 브릿지 시작"""
        self.running = True
        
        print("="*60)
        print(" Frame Poker → Action Tracker Bridge")
        print("="*60)
        print(f"Frame Poker Source: http://{self.fp_host}:{self.fp_port}/data")
        print(f"Action Tracker Target: {self.at_host}:{self.at_tcp_port}")
        print("="*60)
        
        # 스레드 시작
        threads = [
            threading.Thread(target=self.poll_frame_poker, daemon=True),
            threading.Thread(target=self.send_to_action_tracker_tcp, daemon=True),
            threading.Thread(target=self.monitor_changes, daemon=True)
        ]
        
        for t in threads:
            t.start()
        
        print("\n[Bridge] Started reverse sync!")
        print("[Bridge] Monitoring Frame Poker data...")
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[Bridge] Shutting down...")
            self.running = False
    
    def poll_frame_poker(self):
        """Frame Poker 데이터 주기적 확인"""
        while self.running:
            try:
                # Frame Poker에서 데이터 가져오기
                response = requests.get(f"http://{self.fp_host}:{self.fp_port}/data", timeout=2)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 데이터 변경 감지
                    if self.last_data != data:
                        print(f"\n[Frame Poker] Data changed at {datetime.now().strftime('%H:%M:%S')}")
                        self.process_frame_poker_data(data)
                        self.last_data = data
                        
            except Exception as e:
                print(f"[Poll Error] {e}")
            
            time.sleep(2)  # 2초마다 확인
    
    def process_frame_poker_data(self, data):
        """Frame Poker 데이터 처리"""
        if 'Data' in data and 'Players' in data['Data']:
            players = data['Data']['Players']
            
            print(f"[Process] Found {len(players)} players")
            
            for player in players:
                print(f"  - Seat {player['seat']}: {player['name']} ({player['stack']} chips)")
            
            # Action Tracker로 전송 준비
            self.prepare_for_action_tracker(players)
    
    def prepare_for_action_tracker(self, players):
        """Action Tracker 형식으로 데이터 준비"""
        # 방법 1: TCP 전송용 데이터
        self.tcp_data = []
        
        for player in players:
            # Action Tracker 프로토콜 (추정)
            at_command = f"REGISTER_PLAYER:{player['seat']},{player['name']},{player['stack']}\n"
            self.tcp_data.append(at_command)
            
            # 칩 업데이트 명령
            if 'stackChangeValue' in player and player['stackChangeValue'] != 0:
                at_update = f"UPDATE_STACK:{player['seat']},{player['stack']}\n"
                self.tcp_data.append(at_update)
            
            # 액션 처리
            if player.get('busted', False):
                at_bust = f"PLAYER_BUSTED:{player['seat']}\n"
                self.tcp_data.append(at_bust)
    
    def send_to_action_tracker_tcp(self):
        """TCP를 통해 Action Tracker로 전송"""
        while self.running:
            if hasattr(self, 'tcp_data') and self.tcp_data:
                try:
                    # TCP 연결
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.settimeout(2)
                    client.connect((self.at_host, self.at_tcp_port))
                    
                    print(f"\n[TCP] Connected to Action Tracker")
                    
                    # 명령 전송
                    for command in self.tcp_data:
                        client.send(command.encode())
                        print(f"[TCP Sent] {command.strip()}")
                        time.sleep(0.1)
                    
                    # 응답 확인
                    try:
                        response = client.recv(1024)
                        print(f"[TCP Response] {response.decode()}")
                    except:
                        pass
                    
                    client.close()
                    self.tcp_data = []  # 전송 완료 후 초기화
                    
                except Exception as e:
                    print(f"[TCP Error] Could not connect to Action Tracker: {e}")
                    print("[TCP] Action Tracker may not be running on port 8080")
            
            time.sleep(5)
    
    def send_to_action_tracker_ui(self, players):
        """UI 자동화를 통해 Action Tracker에 입력 (대안)"""
        print("\n[UI Automation] Updating Action Tracker UI...")
        
        # Action Tracker 창 활성화
        try:
            windows = pyautogui.getAllWindows()
            for window in windows:
                if "action tracker" in window.title.lower():
                    window.activate()
                    time.sleep(0.5)
                    break
        except:
            pass
        
        # 각 플레이어 정보 입력
        for player in players:
            if player['seat'] in self.at_positions:
                pos = self.at_positions[player['seat']]
                
                # 좌석 클릭
                pyautogui.click(pos['x'], pos['y'])
                time.sleep(0.3)
                
                # 이름 입력 (Tab으로 필드 이동)
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.write(player['name'])
                
                # 칩 입력
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.write(str(player['stack']))
                
                # 확인
                pyautogui.press('enter')
                time.sleep(0.5)
                
                print(f"[UI] Updated Seat {player['seat']}: {player['name']}")
    
    def monitor_changes(self):
        """변경사항 모니터링"""
        while self.running:
            time.sleep(30)
            
            if self.last_data:
                players = self.last_data.get('Data', {}).get('Players', [])
                if players:
                    total = sum(p['stack'] for p in players)
                    print(f"\n[Monitor] {len(players)} players, Total: {total:,} chips")
    
    def simulate_action(self, seat, action, amount=0):
        """액션 시뮬레이션 (Frame Poker → Action Tracker)"""
        print(f"\n[Action] Simulating {action} for seat {seat}")
        
        # TCP로 액션 전송
        action_command = f"ACTION:{seat},{action},{amount}\n"
        
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2)
            client.connect((self.at_host, self.at_tcp_port))
            client.send(action_command.encode())
            client.close()
            print(f"[Action] Sent to Action Tracker")
        except:
            print(f"[Action] Could not send via TCP, trying UI...")
            
            # UI 자동화 대안
            if action.lower() in self.action_buttons:
                button_pos = self.action_buttons[action.lower()]
                pyautogui.click(button_pos[0], button_pos[1])
                print(f"[UI] Clicked {action} button")

def test_reverse_sync():
    """역방향 동기화 테스트"""
    print("\n[Test] Testing Frame Poker -> Action Tracker sync")
    
    # Frame Poker에서 데이터 가져오기
    try:
        response = requests.get("http://127.0.0.1:8088/data")
        if response.status_code == 200:
            data = response.json()
            
            if 'Data' in data and 'Players' in data['Data']:
                players = data['Data']['Players']
                
                print(f"\n[Test] Current Frame Poker data:")
                for p in players:
                    print(f"  Seat {p['seat']}: {p['name']} - {p['stack']} chips")
                
                # Action Tracker 형식으로 변환
                print(f"\n[Test] Converting to Action Tracker format:")
                for p in players:
                    at_cmd = f"REGISTER_PLAYER:{p['seat']},{p['name']},{p['stack']}"
                    print(f"  {at_cmd}")
                
                return True
        else:
            print("[Test] Frame Poker server not responding")
            return False
            
    except Exception as e:
        print(f"[Test Error] {e}")
        return False

def main():
    print("\n" + "="*60)
    print(" Frame Poker to Action Tracker Reverse Bridge")
    print("="*60)
    print("\nThis bridge syncs data FROM Frame Poker TO Action Tracker")
    print("(Opposite direction of normal flow)")
    print("\nOptions:")
    print("1. Start reverse bridge")
    print("2. Test current data")
    print("3. Send test action")
    print("4. UI automation mode")
    print("5. Exit")
    
    bridge = FramePokerToActionTracker()
    
    while True:
        choice = input("\nChoice (1-5): ").strip()
        
        if choice == '1':
            print("\nStarting reverse bridge...")
            bridge.start()
            
        elif choice == '2':
            test_reverse_sync()
            
        elif choice == '3':
            seat = int(input("Seat number (1-6): "))
            action = input("Action (fold/check/call/raise/allin): ")
            amount = 0
            if action.lower() in ['raise', 'call']:
                amount = int(input("Amount: "))
            bridge.simulate_action(seat, action, amount)
            
        elif choice == '4':
            print("\nUI Automation Mode")
            print("Getting current Frame Poker data...")
            
            response = requests.get(f"http://127.0.0.1:8088/data")
            if response.status_code == 200:
                data = response.json()
                players = data.get('Data', {}).get('Players', [])
                
                if players:
                    bridge.send_to_action_tracker_ui(players)
                    print("\nUI automation completed!")
                else:
                    print("No players found")
                    
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    # 먼저 테스트
    if test_reverse_sync():
        print("\n[OK] Test successful, ready for reverse sync")
    else:
        print("\n[Warning] Test failed, check server connections")
    
    # 메인 메뉴
    main()