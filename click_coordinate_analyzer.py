"""
Click Coordinate Analyzer
사용자가 클릭한 좌표를 실시간으로 분석하고 저장하는 도구
"""

import pyautogui
import time
import json
from datetime import datetime
from pynput import mouse
import threading
import os

class ClickCoordinateAnalyzer:
    def __init__(self):
        """좌표 분석기 초기화"""
        self.clicks = []
        self.is_recording = False
        self.current_label = "unknown"
        
    def on_click(self, x, y, button, pressed):
        """마우스 클릭 이벤트 처리"""
        if pressed and self.is_recording:
            # 현재 시간 기록
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # 클릭 정보 저장
            click_info = {
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'button': str(button),
                'label': self.current_label
            }
            
            self.clicks.append(click_info)
            print(f"[{timestamp}] Click recorded: ({x}, {y}) - {self.current_label}")
            
            # 스크린샷 저장 (선택사항)
            if len(self.clicks) <= 10:  # 처음 10개만 스크린샷 저장
                self.save_click_screenshot(x, y, len(self.clicks))
    
    def save_click_screenshot(self, x, y, click_number):
        """클릭 위치 스크린샷 저장"""
        try:
            screenshot = pyautogui.screenshot()
            
            # PIL로 마커 추가
            from PIL import ImageDraw
            draw = ImageDraw.Draw(screenshot)
            
            # 클릭 위치에 빨간 십자 표시
            draw.line([(x-20, y), (x+20, y)], fill="red", width=3)
            draw.line([(x, y-20), (x, y+20)], fill="red", width=3)
            draw.text((x+25, y-15), f"Click {click_number}", fill="red")
            
            filename = f"click_{click_number}_{x}_{y}.png"
            screenshot.save(filename)
            print(f"  Screenshot saved: {filename}")
            
        except Exception as e:
            print(f"  Screenshot error: {e}")
    
    def start_recording(self, label="click"):
        """좌표 기록 시작"""
        self.current_label = label
        self.is_recording = True
        print(f"\n=== 좌표 기록 시작: '{label}' ===")
        print("마우스를 클릭하면 좌표가 기록됩니다.")
        print("'s'를 눌러 기록 중단, 'q'를 눌러 종료")
    
    def stop_recording(self):
        """좌표 기록 중단"""
        self.is_recording = False
        print("\n=== 좌표 기록 중단 ===")
    
    def save_coordinates(self, filename=None):
        """좌표 데이터를 JSON 파일로 저장"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"click_coordinates_{timestamp}.json"
        
        data = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_clicks': len(self.clicks),
            'coordinates': self.clicks
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"좌표 데이터 저장: {filename}")
        return filename
    
    def print_summary(self):
        """기록된 좌표 요약 출력"""
        if not self.clicks:
            print("기록된 클릭이 없습니다.")
            return
        
        print(f"\n=== 기록된 좌표 요약 ({len(self.clicks)}개) ===")
        for i, click in enumerate(self.clicks, 1):
            print(f"{i:2d}. [{click['timestamp']}] ({click['x']:4d}, {click['y']:4d}) - {click['label']}")
    
    def generate_code_template(self):
        """기록된 좌표로 코드 템플릿 생성"""
        if not self.clicks:
            print("기록된 클릭이 없습니다.")
            return
        
        print("\n=== 생성된 코드 템플릿 ===")
        print("# 기록된 좌표들")
        
        # 좌표 딕셔너리 생성
        coordinates = {}
        for i, click in enumerate(self.clicks, 1):
            key = f"{click['label']}_{i}" if click['label'] != 'unknown' else f"click_{i}"
            coordinates[key] = (click['x'], click['y'])
        
        print("COORDINATES = {")
        for key, (x, y) in coordinates.items():
            print(f"    '{key}': ({x}, {y}),")
        print("}")
        
        print("\n# 사용 예제")
        print("import pyautogui")
        print("import time")
        print()
        for key, (x, y) in coordinates.items():
            print(f"# {key} 클릭")
            print(f"pyautogui.click({x}, {y})")
            print("time.sleep(0.5)")
            print()
    
    def interactive_mode(self):
        """대화형 모드 실행"""
        print("Click Coordinate Analyzer")
        print("=" * 50)
        print("명령어:")
        print("  r <label>  - 좌표 기록 시작 (예: r player1)")
        print("  s          - 기록 중단")
        print("  p          - 기록된 좌표 출력")
        print("  c          - 코드 템플릿 생성")
        print("  save       - 좌표 파일 저장")
        print("  clear      - 기록된 좌표 지우기")
        print("  q          - 종료")
        print()
        
        # 마우스 리스너 시작
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        
        try:
            while True:
                command = input("> ").strip().lower()
                
                if command.startswith('r '):
                    label = command[2:].strip()
                    if label:
                        self.start_recording(label)
                    else:
                        print("라벨을 입력해주세요. 예: r player1")
                
                elif command == 'r':
                    label = input("라벨 입력: ").strip()
                    self.start_recording(label if label else "click")
                
                elif command == 's':
                    self.stop_recording()
                
                elif command == 'p':
                    self.print_summary()
                
                elif command == 'c':
                    self.generate_code_template()
                
                elif command == 'save':
                    self.save_coordinates()
                
                elif command == 'clear':
                    self.clicks = []
                    print("기록된 좌표를 모두 지웠습니다.")
                
                elif command == 'q':
                    break
                
                else:
                    print("알 수 없는 명령어입니다.")
        
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
        
        finally:
            self.stop_recording()
            listener.stop()

def main():
    """메인 실행 함수"""
    analyzer = ClickCoordinateAnalyzer()
    
    print("좌표 분석 모드를 선택하세요:")
    print("1. 대화형 모드 (추천)")
    print("2. 자동 기록 모드 (10초간 모든 클릭 기록)")
    
    try:
        choice = input("선택 (1 또는 2): ").strip()
        
        if choice == "1":
            analyzer.interactive_mode()
        
        elif choice == "2":
            print("\n10초간 모든 클릭을 기록합니다...")
            print("시작!")
            
            # 마우스 리스너 시작
            listener = mouse.Listener(on_click=analyzer.on_click)
            listener.start()
            
            analyzer.start_recording("auto_click")
            time.sleep(10)
            analyzer.stop_recording()
            
            listener.stop()
            
            # 결과 출력
            analyzer.print_summary()
            analyzer.generate_code_template()
            analyzer.save_coordinates()
        
        else:
            print("잘못된 선택입니다.")
    
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()