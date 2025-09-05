"""
좌표 검증 및 스크린샷 분석 도구
Action Tracker 현재 상태 확인
"""

import pyautogui
import time
from PIL import Image, ImageDraw
import os

# 현재 사용 중인 좌표들
COORDS = {
    'player1': (215, 354),        # Player1 버튼
    'delete': (761, 108),         # 삭제 버튼
    'complete': (1733, 155),      # 완료 버튼
    'edit': (815, 294)            # 편집 필드 (이전에 사용된 좌표)
}

def take_screenshot_with_markers():
    """현재 화면 스크린샷과 좌표 마커 표시"""
    print("현재 화면 스크린샷 촬영 중...")
    
    try:
        # 스크린샷 촬영
        screenshot = pyautogui.screenshot()
        draw = ImageDraw.Draw(screenshot)
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        print("\n=== 좌표 검증 ===")
        for i, (name, (x, y)) in enumerate(COORDS.items()):
            color = colors[i % len(colors)]
            
            # 십자 마커 그리기
            draw.line([(x-40, y), (x+40, y)], fill=color, width=6)
            draw.line([(x, y-40), (x, y+40)], fill=color, width=6)
            
            # 좌표 텍스트
            draw.text((x+45, y-25), f"{name}: ({x},{y})", fill=color)
            
            print(f"{i+1}. {name}: ({x}, {y}) - {color}")
        
        # 파일 저장
        timestamp = int(time.time())
        filename = f"coordinate_check_{timestamp}.png"
        filepath = os.path.join(os.getcwd(), filename)
        screenshot.save(filepath)
        
        print(f"\n스크린샷 저장: {filepath}")
        print("\n이 이미지를 확인하여 좌표가 올바른 위치에 있는지 검증하세요.")
        
        return filepath
        
    except Exception as e:
        print(f"스크린샷 오류: {e}")
        return None

def test_click_sequence():
    """실제 클릭 시퀀스 테스트 (실행하지 않고 로직만 출력)"""
    print("\n=== 예상 클릭 시퀀스 ===")
    print("1. Player1 탭 클릭: (215, 354)")
    print("2. 대기: 0.3초")
    print("3. 이름 입력 + Enter")
    print("4. 완료 버튼 클릭: (1733, 155)")
    print("5. 대기: 0.2초")
    
    print("\n주의사항:")
    print("- Action Tracker가 화면에 표시되어 있어야 합니다")
    print("- 좌표가 정확한 버튼 위치에 있는지 확인하세요")
    print("- 화면 해상도나 창 위치가 변경되면 좌표도 변경됩니다")

def analyze_screen_region():
    """화면 영역 분석"""
    try:
        screen_size = pyautogui.size()
        print(f"\n=== 화면 정보 ===")
        print(f"화면 해상도: {screen_size.width} x {screen_size.height}")
        
        print(f"\n=== 좌표 유효성 검사 ===")
        for name, (x, y) in COORDS.items():
            if 0 <= x < screen_size.width and 0 <= y < screen_size.height:
                print(f"✅ {name}: ({x}, {y}) - 유효")
            else:
                print(f"❌ {name}: ({x}, {y}) - 화면 범위 벗어남")
                
    except Exception as e:
        print(f"화면 분석 오류: {e}")

def main():
    """Main execution"""
    print("Action Tracker Coordinate Validation Tool")
    print("=" * 40)
    
    # 화면 분석
    analyze_screen_region()
    
    # 스크린샷 촬영
    screenshot_path = take_screenshot_with_markers()
    
    # 클릭 시퀀스 표시
    test_click_sequence()
    
    print("\n" + "=" * 40)
    print("검증 완료!")
    
    if screenshot_path:
        print(f"스크린샷을 확인하여 좌표 정확성을 검증하세요:")
        print(f"파일: {screenshot_path}")

if __name__ == "__main__":
    main()