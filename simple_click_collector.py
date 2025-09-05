"""
Simple Click Collector
간단한 클릭 좌표 수집기
"""

from pynput import mouse
import time

class SimpleClickCollector:
    def __init__(self):
        self.clicks = []
        self.running = True
        
    def on_click(self, x, y, button, pressed):
        """클릭 이벤트 처리"""
        if pressed and button == mouse.Button.left:
            click_num = len(self.clicks) + 1
            self.clicks.append((x, y))
            print(f"Click {click_num}: ({x}, {y})")
            
            # 10번 클릭하면 자동 종료
            if click_num >= 10:
                return False
    
    def start_collection(self):
        """좌표 수집 시작"""
        print("="*50)
        print("SIMPLE CLICK COLLECTOR")
        print("="*50)
        print("\nClick anywhere to record coordinates")
        print("(Max 10 clicks or press Ctrl+C to stop)\n")
        
        # 마우스 리스너 시작
        with mouse.Listener(on_click=self.on_click) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                pass
        
        # 결과 출력
        self.show_results()
    
    def show_results(self):
        """수집된 좌표 표시"""
        print("\n" + "="*50)
        print("COLLECTED COORDINATES")
        print("="*50)
        
        if self.clicks:
            for i, (x, y) in enumerate(self.clicks, 1):
                print(f"{i}. ({x}, {y})")
            
            # Python 코드 형식으로 출력
            print("\n" + "-"*50)
            print("Python code:")
            print("-"*50)
            print("coordinates = [")
            for x, y in self.clicks:
                print(f"    ({x}, {y}),")
            print("]")
            
            # 딕셔너리 형식
            print("\n" + "-"*50)
            print("Dictionary format:")
            print("-"*50)
            print("coords = {")
            for i, (x, y) in enumerate(self.clicks, 1):
                print(f"    'click_{i}': ({x}, {y}),")
            print("}")
        else:
            print("No clicks recorded")

def main():
    collector = SimpleClickCollector()
    collector.start_collection()

if __name__ == "__main__":
    main()