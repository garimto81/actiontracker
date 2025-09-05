"""
Action Tracker Test Input App
테스트용 자동 입력 로직 애플리케이션
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyautogui
import time
import json
import threading
from datetime import datetime
import os

class TestInputApp:
    def __init__(self):
        """테스트 입력 앱 초기화"""
        self.root = tk.Tk()
        self.root.title("Action Tracker Test Input App")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # 안전 모드 설정
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # 테스트 데이터
        self.test_players = [
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
        
        # 좌표 정보 (1920x1080 기준)
        self.coordinates = {
            'players': [
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
            ],
            'buttons': {
                'delete': (761, 108),
                'complete': (1733, 155),
                'close': (1745, 147),
                'edit': (815, 294)
            }
        }
        
        # 실행 상태
        self.is_running = False
        self.current_index = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI 구성"""
        # 헤더
        header_frame = tk.Frame(self.root, bg='#2d2d2d', height=80)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 Action Tracker Test Input System",
            font=("Arial", 20, "bold"),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        title_label.pack(pady=20)
        
        # 메인 컨테이너
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # 좌측 패널 - 플레이어 리스트
        left_panel = tk.Frame(main_container, bg='#2d2d2d', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=5)
        left_panel.pack_propagate(False)
        
        # 우측 패널 - 컨트롤 및 로그
        right_panel = tk.Frame(main_container, bg='#1e1e1e')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5)
        
        self.setup_player_list(left_panel)
        self.setup_control_panel(right_panel)
        self.setup_log_panel(right_panel)
        
    def setup_player_list(self, parent):
        """플레이어 리스트 설정"""
        tk.Label(
            parent,
            text="📋 테스트 플레이어 목록",
            font=("Arial", 14, "bold"),
            bg='#2d2d2d',
            fg='white'
        ).pack(pady=10)
        
        # 트리뷰 생성
        columns = ('번호', '이름', '칩')
        self.player_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # 컬럼 설정
        self.player_tree.heading('번호', text='#')
        self.player_tree.heading('이름', text='플레이어 이름')
        self.player_tree.heading('칩', text='칩 수량')
        
        self.player_tree.column('번호', width=50)
        self.player_tree.column('이름', width=150)
        self.player_tree.column('칩', width=150)
        
        # 데이터 삽입
        for player in self.test_players:
            self.player_tree.insert('', 'end', values=(
                player['num'],
                player['name'],
                f"{player['chips']:,}"
            ))
        
        self.player_tree.pack(padx=10, pady=5)
        
        # 플레이어 추가/삭제 버튼
        btn_frame = tk.Frame(parent, bg='#2d2d2d')
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ 플레이어 추가",
            command=self.add_player,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="➖ 선택 삭제",
            command=self.remove_player,
            bg='#f44336',
            fg='white',
            font=("Arial", 10),
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
    def setup_control_panel(self, parent):
        """컨트롤 패널 설정"""
        control_frame = tk.LabelFrame(
            parent,
            text="⚙️ 컨트롤 패널",
            bg='#2d2d2d',
            fg='white',
            font=("Arial", 12, "bold")
        )
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 모드 선택
        mode_frame = tk.Frame(control_frame, bg='#2d2d2d')
        mode_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            mode_frame,
            text="실행 모드:",
            bg='#2d2d2d',
            fg='white',
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="test")
        modes = [
            ("테스트 모드 (좌표만 표시)", "test"),
            ("시뮬레이션 모드 (마우스 이동)", "simulation"),
            ("실제 실행 모드 (클릭 실행)", "real")
        ]
        
        for text, value in modes:
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                bg='#2d2d2d',
                fg='white',
                selectcolor='#2d2d2d',
                activebackground='#2d2d2d',
                font=("Arial", 10)
            ).pack(side=tk.LEFT, padx=10)
        
        # 옵션 설정
        option_frame = tk.Frame(control_frame, bg='#2d2d2d')
        option_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            option_frame,
            text="입력 속도:",
            bg='#2d2d2d',
            fg='white',
            font=("Arial", 10)
        ).grid(row=0, column=0, padx=5, sticky='w')
        
        self.speed_var = tk.DoubleVar(value=0.5)
        speed_scale = tk.Scale(
            option_frame,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg='#2d2d2d',
            fg='white',
            troughcolor='#1e1e1e',
            highlightbackground='#2d2d2d',
            length=200
        )
        speed_scale.grid(row=0, column=1, padx=5)
        
        tk.Label(
            option_frame,
            text="초",
            bg='#2d2d2d',
            fg='white',
            font=("Arial", 10)
        ).grid(row=0, column=2, padx=5)
        
        # 실행 버튼들
        button_frame = tk.Frame(control_frame, bg='#2d2d2d')
        button_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶️ 테스트 시작",
            command=self.start_test,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹️ 중지",
            command=self.stop_test,
            bg='#f44336',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="📍 현재 좌표",
            command=self.show_current_position,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12, "bold"),
            width=15,
            height=2
        ).pack(side=tk.LEFT, padx=5)
        
        # 상태 표시
        self.status_label = tk.Label(
            control_frame,
            text="⏸️ 대기 중",
            bg='#2d2d2d',
            fg='yellow',
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(pady=10)
        
    def setup_log_panel(self, parent):
        """로그 패널 설정"""
        log_frame = tk.LabelFrame(
            parent,
            text="📝 실행 로그",
            bg='#2d2d2d',
            fg='white',
            font=("Arial", 12, "bold")
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 로그 텍스트 위젯
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            width=60,
            height=15,
            bg='#1e1e1e',
            fg='#00ff00',
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 로그 초기 메시지
        self.log("시스템 준비 완료")
        self.log(f"현재 화면 해상도: {pyautogui.size()}")
        self.log("테스트 모드를 선택하고 시작 버튼을 누르세요")
        
    def log(self, message):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
        
    def add_player(self):
        """플레이어 추가 대화상자"""
        dialog = tk.Toplevel(self.root)
        dialog.title("플레이어 추가")
        dialog.geometry("400x200")
        dialog.configure(bg='#2d2d2d')
        
        tk.Label(dialog, text="플레이어 이름:", bg='#2d2d2d', fg='white').grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="칩 수량:", bg='#2d2d2d', fg='white').grid(row=1, column=0, padx=10, pady=10)
        chip_entry = tk.Entry(dialog, width=30)
        chip_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def save_player():
            name = name_entry.get()
            chips = chip_entry.get()
            if name and chips:
                try:
                    chips = int(chips)
                    num = len(self.test_players) + 1
                    new_player = {"num": num, "name": name, "chips": chips}
                    self.test_players.append(new_player)
                    self.player_tree.insert('', 'end', values=(num, name, f"{chips:,}"))
                    self.log(f"플레이어 추가: {name} ({chips:,} chips)")
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("오류", "칩 수량은 숫자여야 합니다")
        
        tk.Button(
            dialog,
            text="추가",
            command=save_player,
            bg='#4CAF50',
            fg='white'
        ).grid(row=2, column=0, columnspan=2, pady=20)
        
    def remove_player(self):
        """선택된 플레이어 삭제"""
        selected = self.player_tree.selection()
        if selected:
            item = self.player_tree.item(selected)
            values = item['values']
            self.player_tree.delete(selected)
            
            # 테스트 데이터에서도 삭제
            self.test_players = [p for p in self.test_players if p['num'] != values[0]]
            self.log(f"플레이어 삭제: {values[1]}")
        
    def show_current_position(self):
        """현재 마우스 좌표 표시"""
        x, y = pyautogui.position()
        self.log(f"현재 마우스 좌표: ({x}, {y})")
        messagebox.showinfo("현재 좌표", f"X: {x}\nY: {y}")
        
    def start_test(self):
        """테스트 시작"""
        self.is_running = True
        self.current_index = 0
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="🔴 실행 중", fg='red')
        
        # 별도 스레드에서 실행
        self.test_thread = threading.Thread(target=self.run_test)
        self.test_thread.daemon = True
        self.test_thread.start()
        
    def stop_test(self):
        """테스트 중지"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="⏸️ 중지됨", fg='yellow')
        self.log("테스트 중지됨")
        
    def run_test(self):
        """테스트 실행 로직"""
        mode = self.mode_var.get()
        speed = self.speed_var.get()
        
        self.log(f"테스트 시작 - 모드: {mode}, 속도: {speed}초")
        
        # 초기 대기
        self.log("3초 후 시작...")
        time.sleep(3)
        
        for player in self.test_players:
            if not self.is_running:
                break
                
            player_num = player['num']
            player_name = player['name']
            player_chips = player['chips']
            
            # 플레이어 번호가 좌표 범위 내인지 확인
            if player_num <= len(self.coordinates['players']):
                x, y = self.coordinates['players'][player_num - 1]
                
                if mode == "test":
                    # 테스트 모드 - 좌표만 표시
                    self.log(f"Player {player_num} ({player_name}): 좌표 ({x}, {y})")
                    
                elif mode == "simulation":
                    # 시뮬레이션 모드 - 마우스 이동만
                    self.log(f"Player {player_num} ({player_name}): 마우스 이동 ({x}, {y})")
                    pyautogui.moveTo(x, y, duration=0.5)
                    
                elif mode == "real":
                    # 실제 실행 모드 - 클릭 및 입력
                    self.log(f"Player {player_num} ({player_name}): 클릭 및 입력")
                    
                    # 플레이어 위치 클릭
                    pyautogui.click(x, y)
                    time.sleep(speed)
                    
                    # 더블클릭으로 편집 모드
                    pyautogui.doubleClick()
                    time.sleep(speed)
                    
                    # 기존 텍스트 삭제
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.press('delete')
                    time.sleep(0.2)
                    
                    # 이름 입력
                    pyautogui.typewrite(player_name)
                    time.sleep(speed)
                    pyautogui.press('tab')
                    
                    # 칩 입력
                    pyautogui.typewrite(str(player_chips))
                    time.sleep(speed)
                    
                    # 확인
                    pyautogui.press('enter')
                    self.log(f"✅ Player {player_num} 업데이트 완료")
                
                time.sleep(speed)
            else:
                self.log(f"⚠️ Player {player_num}: 좌표 범위 초과")
        
        self.log("테스트 완료")
        self.stop_test()
        
    def run(self):
        """앱 실행"""
        self.root.mainloop()


def main():
    """메인 함수"""
    print("=" * 60)
    print("Action Tracker Test Input App 시작")
    print("=" * 60)
    
    app = TestInputApp()
    app.run()


if __name__ == "__main__":
    main()