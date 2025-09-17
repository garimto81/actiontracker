"""
플레이어 이름 변경 화면 분석 도구
NAME 옆 player1 버튼 클릭 시 나타나는 편집 화면 분석
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time
import json
from datetime import datetime

def capture_name_edit_screen():
    """플레이어 이름 편집 화면 캡처 및 분석"""
    print("플레이어 이름 편집 화면을 분석합니다...")
    print("Action Tracker에서 플레이어 이름 버튼을 클릭한 후 3초 후 스크린샷을 찍습니다.")
    
    # 사용자가 클릭할 시간 제공
    time.sleep(3)
    
    # 스크린샷 캡처
    screenshot = pyautogui.screenshot()
    screenshot.save("name_edit_screen.png")
    print("스크린샷 저장: name_edit_screen.png")
    
    # OpenCV 형식으로 변환
    img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    return screenshot, img_cv

def analyze_edit_elements(img_cv):
    """편집 화면의 UI 요소들 분석"""
    print("편집 화면 UI 요소 분석 중...")
    
    # 그레이스케일 변환
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # 텍스트 입력 필드 감지 (흰색 배경의 사각형 영역)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    input_fields = []
    buttons = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        # 텍스트 입력 필드 같은 영역 (큰 사각형)
        if 100 < w < 400 and 20 < h < 60 and area > 1000:
            input_fields.append({
                'type': 'input_field',
                'x': x + w//2,
                'y': y + h//2,
                'bounds': (x, y, w, h),
                'area': area
            })
        
        # 버튼 같은 영역 (작은 사각형)
        elif 50 < w < 150 and 20 < h < 50 and area > 500:
            buttons.append({
                'type': 'button',
                'x': x + w//2,
                'y': y + h//2,
                'bounds': (x, y, w, h),
                'area': area
            })
    
    return input_fields, buttons

def detect_text_areas(img_cv):
    """텍스트 영역 감지"""
    print("텍스트 영역 감지 중...")
    
    # HSV 변환
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    
    # 어두운 텍스트 감지 (검은색 텍스트)
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 100])
    dark_mask = cv2.inRange(hsv, lower_dark, upper_dark)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(dark_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_areas = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 10 < w < 200 and 10 < h < 40:
            text_areas.append({
                'type': 'text',
                'x': x + w//2,
                'y': y + h//2,
                'bounds': (x, y, w, h)
            })
    
    return text_areas

def create_analysis_visualization(img_cv, input_fields, buttons, text_areas):
    """분석 결과 시각화"""
    print("분석 결과 시각화 생성 중...")
    
    # PIL 형식으로 변환
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # 입력 필드 표시 (빨간색)
    for i, field in enumerate(input_fields):
        x, y, w, h = field['bounds']
        draw.rectangle([x, y, x+w, y+h], outline="red", width=3)
        draw.text((x, y-20), f"Input {i+1}", fill="red")
        
        # 중앙점 표시
        cx, cy = field['x'], field['y']
        draw.line([(cx-15, cy), (cx+15, cy)], fill="red", width=2)
        draw.line([(cx, cy-15), (cx, cy+15)], fill="red", width=2)
    
    # 버튼 표시 (파란색)
    for i, button in enumerate(buttons):
        x, y, w, h = button['bounds']
        draw.rectangle([x, y, x+w, y+h], outline="blue", width=2)
        draw.text((x, y-20), f"Btn {i+1}", fill="blue")
        
        # 중앙점 표시
        cx, cy = button['x'], button['y']
        draw.line([(cx-10, cy), (cx+10, cy)], fill="blue", width=1)
        draw.line([(cx, cy-10), (cx, cy+10)], fill="blue", width=1)
    
    # 텍스트 영역 표시 (녹색)
    for i, text in enumerate(text_areas[:10]):  # 상위 10개만 표시
        x, y, w, h = text['bounds']
        draw.rectangle([x, y, x+w, y+h], outline="green", width=1)
    
    return img_pil

def save_analysis_results(input_fields, buttons, text_areas):
    """분석 결과를 JSON으로 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    analysis_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'screen_type': 'player_name_edit',
        'detected_elements': {
            'input_fields': [
                {
                    'id': i+1,
                    'center_x': field['x'],
                    'center_y': field['y'],
                    'bounds': field['bounds'],
                    'area': field['area']
                }
                for i, field in enumerate(input_fields)
            ],
            'buttons': [
                {
                    'id': i+1,
                    'center_x': button['x'],
                    'center_y': button['y'],
                    'bounds': button['bounds'],
                    'area': button['area']
                }
                for i, button in enumerate(buttons)
            ],
            'text_areas_count': len(text_areas)
        }
    }
    
    filename = f"name_edit_analysis_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    return filename

def main():
    """메인 분석 함수"""
    print("="*60)
    print("플레이어 이름 편집 화면 분석 도구")
    print("="*60)
    print()
    print("사용 방법:")
    print("1. Action Tracker가 실행되어 있는지 확인")
    print("2. 플레이어 이름 버튼(예: player1) 클릭")
    print("3. 편집 화면이 나타나면 이 스크립트 실행")
    print()
    print("3초 후 스크린샷을 찍습니다...")
    
    try:
        # 스크린샷 캡처
        screenshot_pil, img_cv = capture_name_edit_screen()
        
        # UI 요소 분석
        input_fields, buttons = analyze_edit_elements(img_cv)
        text_areas = detect_text_areas(img_cv)
        
        print(f"감지된 요소들:")
        print(f"  - 입력 필드: {len(input_fields)}개")
        print(f"  - 버튼: {len(buttons)}개")
        print(f"  - 텍스트 영역: {len(text_areas)}개")
        
        # 시각화 생성
        viz_image = create_analysis_visualization(img_cv, input_fields, buttons, text_areas)
        
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        viz_filename = f"name_edit_analysis_{timestamp}.png"
        viz_image.save(viz_filename)
        
        json_filename = save_analysis_results(input_fields, buttons, text_areas)
        
        print(f"\n분석 완료!")
        print(f"시각화 이미지: {viz_filename}")
        print(f"분석 데이터: {json_filename}")
        print(f"원본 스크린샷: name_edit_screen.png")
        
        # 결과 요약 출력
        if input_fields:
            print(f"\n입력 필드 좌표:")
            for i, field in enumerate(input_fields, 1):
                print(f"  필드 {i}: ({field['x']}, {field['y']})")
        
        if buttons:
            print(f"\n버튼 좌표:")
            for i, button in enumerate(buttons, 1):
                print(f"  버튼 {i}: ({button['x']}, {button['y']})")
        
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()