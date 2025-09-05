"""
Ultra Fast Player1 Name Updater - Mike Version
최고속 처리: Enter 키 포함 + 완료 버튼
"""

import pyautogui
import time

# 사용자 클릭 좌표
COORDS = {
    'player1': (215, 354),      # Player1 버튼
    'edit': (815, 294),         # 편집 필드  
    'complete': (1733, 155)     # 완료 버튼
}

def ultra_fast_click(x, y, delay=0.15):
    """초고속 클릭"""
    pyautogui.click(x, y)
    time.sleep(delay)

def ultra_fast_type(text):
    """초고속 타이핑 + Enter"""
    pyautogui.hotkey('ctrl', 'a')  # 전체 선택
    time.sleep(0.05)
    pyautogui.typewrite(text)      # 텍스트 입력
    time.sleep(0.05)
    pyautogui.press('enter')       # Enter로 등록
    time.sleep(0.1)

def update_to_mike():
    """Mike로 초고속 업데이트"""
    print("ULTRA FAST UPDATE: Player1 -> Mike")
    print("=" * 40)
    
    start_time = time.time()
    
    # 1단계: Player1 클릭
    print("[1] Player1 click")
    ultra_fast_click(COORDS['player1'][0], COORDS['player1'][1], 0.4)
    
    # 2단계: 편집 필드 클릭
    print("[2] Edit field click") 
    ultra_fast_click(COORDS['edit'][0], COORDS['edit'][1], 0.2)
    
    # 3단계: Mike 입력 + Enter
    print("[3] Type 'Mike' + Enter")
    ultra_fast_type("Mike")
    
    # 4단계: 완료 버튼
    print("[4] Complete button")
    ultra_fast_click(COORDS['complete'][0], COORDS['complete'][1], 0.2)
    
    elapsed = time.time() - start_time
    
    print("=" * 40)
    print(f"SUCCESS: Mike updated in {elapsed:.1f}s")
    print("=" * 40)

def main():
    """메인 실행"""
    print("Ultra Fast Mike Updater")
    print("=" * 25)
    print("Ready to change Player1 -> Mike")
    print("Starting in 2 seconds...")
    
    time.sleep(2)
    update_to_mike()

if __name__ == "__main__":
    main()