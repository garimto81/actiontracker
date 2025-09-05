"""
Action Tracker Automation App
GUI 기반 플레이어 관리 자동화 도구
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyautogui
import time
import threading
from datetime import datetime

class ActionTrackerAutomationApp:
    def __init__(self):
        """앱 초기화"""
        self.root = tk.Tk()
        self.root.title("Action Tracker Automation App v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # 좌표 정보
        self.coordinates = {
            'player1': (215, 354),
            'delete': (761, 108),
            'complete': (1733, 155)
        }
        
        # 실행 상태
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 제목
        title_label = tk.Label(
            main_frame,
            text="🎮 Action Tracker Automation",
            font=("Arial", 18, "bold"),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 20))
        
        # 좌측 패널 (컨트롤)
        left_frame = tk.Frame(main_frame, bg='#3c3c3c', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # 우측 패널 (로그)
        right_frame = tk.Frame(main_frame, bg='#3c3c3c', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.setup_control_panel(left_frame)
        self.setup_log_panel(right_frame)
        
    def setup_control_panel(self, parent):
        """컨트롤 패널 구성"""
        # 컨트롤 패널 제목
        control_title = tk.Label(
            parent,
            text="🎯 Player Controls",
            font=("Arial", 14, "bold"),
            bg='#3c3c3c',
            fg='#ffffff'
        )
        control_title.pack(pady=10)
        
        # 이름 변경 섹션
        name_frame = tk.LabelFrame(
            parent,
            text="Name Update",
            font=("Arial", 10, "bold"),
            bg='#3c3c3c',
            fg='#ffffff',
            bd=2,
            relief=tk.GROOVE
        )
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 이름 입력
        tk.Label(
            name_frame,
            text="Player Name:",
            bg='#3c3c3c',
            fg='#ffffff'
        ).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        self.name_entry = tk.Entry(
            name_frame,
            font=("Arial", 12),
            width=20
        )
        self.name_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # 이름 변경 버튼
        self.update_button = tk.Button(
            name_frame,
            text="⚡ Update Name (Fast)",
            command=self.update_name_clicked,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.update_button.pack(fill=tk.X, padx=5, pady=5)
        
        # 빠른 이름 버튼들
        quick_frame = tk.LabelFrame(
            parent,
            text="Quick Names",
            font=("Arial", 10, "bold"),
            bg='#3c3c3c',
            fg='#ffffff',
            bd=2,
            relief=tk.GROOVE
        )
        quick_frame.pack(fill=tk.X, padx=10, pady=5)
        
        quick_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        for i, name in enumerate(quick_names):
            if i % 2 == 0:
                row_frame = tk.Frame(quick_frame, bg='#3c3c3c')
                row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            btn = tk.Button(
                row_frame,
                text=name,
                command=lambda n=name: self.quick_name_update(n),
                bg='#2196F3',
                fg='white',
                font=("Arial", 9),
                width=8
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # 삭제 섹션
        delete_frame = tk.LabelFrame(
            parent,
            text="Player Management",
            font=("Arial", 10, "bold"),
            bg='#3c3c3c',
            fg='#ffffff',
            bd=2,
            relief=tk.GROOVE
        )
        delete_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.delete_button = tk.Button(
            delete_frame,
            text="🗑️ Delete Player1",
            command=self.delete_player_clicked,
            bg='#f44336',
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2
        )
        self.delete_button.pack(fill=tk.X, padx=5, pady=5)
        
        # 좌표 정보
        coords_frame = tk.LabelFrame(
            parent,
            text="Coordinates Info",
            font=("Arial", 10, "bold"),
            bg='#3c3c3c',
            fg='#ffffff',
            bd=2,
            relief=tk.GROOVE
        )
        coords_frame.pack(fill=tk.X, padx=10, pady=5)
        
        coords_text = tk.Text(
            coords_frame,
            height=4,
            width=25,
            font=("Consolas", 9),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        coords_text.pack(padx=5, pady=5)
        
        coords_info = "Player1: (215, 354)\nDelete: (761, 108)\nComplete: (1733, 155)\nStatus: Ready"
        coords_text.insert(tk.END, coords_info)
        coords_text.config(state=tk.DISABLED)
        
    def setup_log_panel(self, parent):
        """로그 패널 구성"""
        # 로그 패널 제목
        log_title = tk.Label(
            parent,
            text="📋 Activity Log",
            font=("Arial", 14, "bold"),
            bg='#3c3c3c',
            fg='#ffffff'
        )
        log_title.pack(pady=10)
        
        # 로그 텍스트 영역
        self.log_text = scrolledtext.ScrolledText(
            parent,
            font=("Consolas", 10),
            bg='#1e1e1e',
            fg='#00ff00',
            insertbackground='#00ff00',
            selectbackground='#404040'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 초기 로그 메시지
        self.add_log("=== Action Tracker Automation App Started ===")
        self.add_log("Ready for automation tasks")
        
        # 로그 제어 버튼
        log_control_frame = tk.Frame(parent, bg='#3c3c3c')
        log_control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        clear_log_btn = tk.Button(
            log_control_frame,
            text="Clear Log",
            command=self.clear_log,
            bg='#ff9800',
            fg='white',
            font=("Arial", 9)
        )
        clear_log_btn.pack(side=tk.RIGHT)
        
    def add_log(self, message):
        """로그 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
        
    def clear_log(self):
        """로그 지우기"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("Log cleared")
        
    def simple_name_update(self, name):
        """간단한 이름 업데이트 (0.7초 버전)"""
        try:
            self.add_log(f"Starting name update: Player1 -> {name}")
            start_time = time.time()
            
            # 이름 탭 클릭
            self.add_log("Clicking Player1 name tab...")
            pyautogui.click(self.coordinates['player1'][0], self.coordinates['player1'][1])
            time.sleep(0.3)
            
            # 이름 입력 + Enter
            self.add_log(f"Typing '{name}' and pressing Enter...")
            pyautogui.typewrite(name)
            time.sleep(0.1)
            pyautogui.press('enter')
            
            elapsed = time.time() - start_time
            self.add_log(f"SUCCESS: {name} updated in {elapsed:.1f}s")
            self.add_log("=" * 40)
            
            return True
            
        except Exception as e:
            self.add_log(f"ERROR: {str(e)}")
            return False
    
    def delete_player(self):
        """플레이어 삭제"""
        try:
            self.add_log("Starting Player1 deletion...")
            start_time = time.time()
            
            # Player1 클릭
            self.add_log("Clicking Player1...")
            pyautogui.click(self.coordinates['player1'][0], self.coordinates['player1'][1])
            time.sleep(0.4)
            
            # 삭제 버튼 클릭
            self.add_log("Clicking delete button...")
            pyautogui.click(self.coordinates['delete'][0], self.coordinates['delete'][1])
            time.sleep(0.3)
            
            # 완료 버튼 클릭
            self.add_log("Clicking complete button...")
            pyautogui.click(self.coordinates['complete'][0], self.coordinates['complete'][1])
            time.sleep(0.2)
            
            elapsed = time.time() - start_time
            self.add_log(f"SUCCESS: Player1 deleted in {elapsed:.1f}s")
            self.add_log("=" * 40)
            
            return True
            
        except Exception as e:
            self.add_log(f"ERROR: {str(e)}")
            return False
    
    def update_name_clicked(self):
        """이름 업데이트 버튼 클릭"""
        if self.is_running:
            messagebox.showwarning("Warning", "Already running an operation!")
            return
            
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter a name!")
            return
        
        self.run_in_thread(lambda: self.simple_name_update(name))
    
    def quick_name_update(self, name):
        """빠른 이름 업데이트"""
        if self.is_running:
            messagebox.showwarning("Warning", "Already running an operation!")
            return
            
        self.run_in_thread(lambda: self.simple_name_update(name))
    
    def delete_player_clicked(self):
        """삭제 버튼 클릭"""
        if self.is_running:
            messagebox.showwarning("Warning", "Already running an operation!")
            return
            
        result = messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete Player1?"
        )
        
        if result:
            self.run_in_thread(self.delete_player)
    
    def run_in_thread(self, func):
        """별도 스레드에서 실행"""
        self.is_running = True
        self.update_button_states(False)
        
        def wrapper():
            try:
                func()
            finally:
                self.is_running = False
                self.root.after(0, lambda: self.update_button_states(True))
        
        thread = threading.Thread(target=wrapper)
        thread.daemon = True
        thread.start()
    
    def update_button_states(self, enabled):
        """버튼 상태 업데이트"""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.update_button.config(state=state)
        self.delete_button.config(state=state)
    
    def run(self):
        """앱 실행"""
        # 창 중앙 정렬
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # 종료 이벤트 바인딩
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.add_log("App ready! Make sure Action Tracker is visible.")
        self.root.mainloop()
    
    def on_closing(self):
        """앱 종료 시"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Operation in progress. Force quit?"):
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """메인 실행"""
    try:
        app = ActionTrackerAutomationApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {str(e)}")

if __name__ == "__main__":
    main()