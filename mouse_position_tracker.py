"""
실시간 마우스 좌표 확인 도구
간단하고 바로 사용 가능한 버전
"""

import pyautogui
import time
import keyboard

def track_mouse_position():
    """실시간 마우스 좌표 추적"""
    print("="*60)
    print("REAL-TIME MOUSE POSITION TRACKER")
    print("="*60)
    print("\nInstructions:")
    print("- Move your mouse to see coordinates")
    print("- Press SPACE to save current position")
    print("- Press ESC to exit")
    print("-"*60)
    print()
    
    saved_positions = []
    
    try:
        while True:
            # 현재 마우스 좌표
            x, y = pyautogui.position()
            
            # 화면에 표시 (같은 줄에 업데이트)
            print(f"Mouse Position: ({x:4d}, {y:4d})", end='\r')
            
            # 스페이스바 누르면 좌표 저장
            if keyboard.is_pressed('space'):
                saved_positions.append((x, y))
                print(f"\n[SAVED] Position #{len(saved_positions)}: ({x}, {y})")
                time.sleep(0.3)  # 중복 저장 방지
            
            # ESC 누르면 종료
            if keyboard.is_pressed('esc'):
                break
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        pass
    
    # 저장된 좌표 출력
    print("\n\n" + "="*60)
    print("SAVED POSITIONS:")
    print("="*60)
    
    if saved_positions:
        for i, (x, y) in enumerate(saved_positions, 1):
            print(f"{i}. ({x}, {y})")
        
        # Python 코드로 출력
        print("\n" + "-"*60)
        print("Python code format:")
        print("-"*60)
        print("coordinates = {")
        for i, (x, y) in enumerate(saved_positions, 1):
            print(f"    'position_{i}': ({x}, {y}),")
        print("}")
    else:
        print("No positions saved")
    
    print("\nDone!")

if __name__ == "__main__":
    track_mouse_position()