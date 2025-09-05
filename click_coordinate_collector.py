"""
Real-time Click Coordinate Collector
마우스 클릭으로 정확한 좌표 수집
"""

import pyautogui
import time
import threading
from pynput import mouse
import sys

class CoordinateCollector:
    def __init__(self):
        self.coordinates = {}
        self.current_label = ""
        self.collecting = True
        
    def on_click(self, x, y, button, pressed):
        """마우스 클릭 이벤트 처리"""
        if pressed and button == mouse.Button.left and self.current_label:
            print(f"\n✅ {self.current_label}: ({x}, {y}) recorded!")
            self.coordinates[self.current_label] = (x, y)
            self.current_label = ""
            return False  # 리스너 중지
    
    def collect_coordinate(self, label, instruction):
        """특정 좌표 수집"""
        print(f"\n📍 {label} 좌표 수집")
        print(f"   {instruction}")
        print("   마우스 클릭으로 위치를 지정하세요...")
        
        self.current_label = label
        
        # 마우스 리스너 시작
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
    
    def generate_code(self):
        """수집된 좌표로 코드 생성"""
        if not self.coordinates:
            print("수집된 좌표가 없습니다.")
            return
            
        print("\n" + "="*50)
        print("📋 수집된 좌표 정보")
        print("="*50)
        
        for label, (x, y) in self.coordinates.items():
            print(f"{label}: ({x}, {y})")
        
        print("\n" + "="*50)
        print("🔧 업데이트된 좌표 코드")
        print("="*50)
        
        print("COORDS = {")
        for label, (x, y) in self.coordinates.items():
            print(f"    '{label.lower()}': ({x}, {y}),")
        print("}")
        
        # 파일로 저장
        with open("collected_coordinates.txt", "w") as f:
            f.write("Collected Coordinates:\n")
            f.write("="*30 + "\n")
            for label, (x, y) in self.coordinates.items():
                f.write(f"{label}: ({x}, {y})\n")
            
            f.write("\nCode:\n")
            f.write("COORDS = {\n")
            for label, (x, y) in self.coordinates.items():
                f.write(f"    '{label.lower()}': ({x}, {y}),\n")
            f.write("}\n")
        
        print("\n📁 좌표 정보가 'collected_coordinates.txt'에 저장되었습니다.")

def main():
    print("🎯 Action Tracker 좌표 수집 도구")
    print("="*40)
    print("정확한 좌표를 마우스 클릭으로 수집합니다.")
    print("각 단계에서 해당 버튼을 클릭하세요.")
    
    collector = CoordinateCollector()
    
    # 좌표 수집 순서
    coordinates_to_collect = [
        ("ALICE_BUTTON", "Alice 플레이어 버튼을 클릭하세요"),
        ("PLAYER2_BUTTON", "Player2 버튼을 클릭하세요"), 
        ("PLAYER3_BUTTON", "Player3 버튼을 클릭하세요"),
        ("EDIT_FIELD", "플레이어 이름 편집 필드를 클릭하세요"),
        ("COMPLETE_BUTTON", "완료 버튼을 클릭하세요"),
        ("DELETE_BUTTON", "삭제 버튼을 클릭하세요 (있다면)")
    ]
    
    try:
        for label, instruction in coordinates_to_collect:
            collector.collect_coordinate(label, instruction)
            time.sleep(0.5)  # 잠시 대기
        
        # 결과 생성
        collector.generate_code()
        
    except KeyboardInterrupt:
        print("\n⏹️ 수집이 중단되었습니다.")
        collector.generate_code()
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")

if __name__ == "__main__":
    # pyautogui 안전 설정
    pyautogui.FAILSAFE = True
    main()