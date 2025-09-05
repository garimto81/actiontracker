"""
Final Test - Action Tracker Automation
최종 실행 테스트
"""

import pyautogui
import time
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

def test_automation():
    """간단한 자동화 테스트"""
    
    print("="*50)
    print("ACTION TRACKER AUTOMATION TEST")
    print("="*50)
    print()
    
    # 테스트 좌표 (검증된 좌표)
    coords = {
        'player1': (215, 354),
        'edit': (815, 294),
        'complete': (1733, 155)
    }
    
    print("Test will:")
    print("1. Click Player1 position")
    print("2. Click edit field")
    print("3. Type 'AutoTest'")
    print("4. Click complete")
    print()
    print("Starting in 3 seconds...")
    
    # 카운트다운
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    try:
        # Step 1: Player1 클릭
        print("\n[1/4] Clicking Player1...")
        pyautogui.click(coords['player1'][0], coords['player1'][1])
        time.sleep(0.5)
        
        # Step 2: Edit 필드 클릭
        print("[2/4] Clicking edit field...")
        pyautogui.click(coords['edit'][0], coords['edit'][1])
        time.sleep(0.5)
        
        # Step 3: 텍스트 입력
        print("[3/4] Typing 'AutoTest'...")
        pyautogui.hotkey('ctrl', 'a')  # 전체 선택
        time.sleep(0.2)
        pyautogui.typewrite('AutoTest')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 4: Complete 버튼
        print("[4/4] Clicking complete...")
        pyautogui.click(coords['complete'][0], coords['complete'][1])
        time.sleep(0.5)
        
        print("\n" + "="*50)
        print("TEST COMPLETE - SUCCESS!")
        print("="*50)
        
        # 스크린샷 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot = pyautogui.screenshot()
        filename = f"test_complete_{timestamp}.png"
        screenshot.save(filename)
        print(f"\nScreenshot saved: {filename}")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_automation()