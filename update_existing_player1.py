"""
기존 플레이어 1 이름 변경 자동화
이미 존재하는 이름을 변경하는 프로세스
"""

import pyautogui
import time
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# 플레이어 1 좌표
PLAYER1_X = 215
PLAYER1_Y = 354

def update_existing_name():
    """
    이미 존재하는 이름 변경 프로세스
    1. 이름 클릭
    2. 드롭다운에서 선택
    3. 텍스트 수정
    4. Enter
    5. 확인 클릭
    """
    
    print("="*60)
    print("기존 플레이어 1 이름 변경")
    print("="*60)
    print()
    print("프로세스: 이미 존재하는 이름 변경")
    print("단계:")
    print("  1. 플레이어 이름 클릭")
    print("  2. 더블클릭으로 편집 모드 진입")
    print("  3. 드롭다운 리스트에서 선택")
    print("  4. 새 이름 입력")
    print("  5. Enter 키 누르기")
    print("  6. 확인 클릭")
    print()
    
    new_name = "Daniel Negreanu"  # 변경할 새 이름
    
    print(f"플레이어 1을 '{new_name}'로 변경합니다")
    print("3초 후 시작...")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("\n실행 중...")
    print("-"*40)
    
    try:
        # 단계 1: 플레이어 이름 클릭
        print("[1/6] 플레이어 1 이름 클릭...")
        pyautogui.click(PLAYER1_X, PLAYER1_Y)
        time.sleep(0.3)
        
        # 단계 2: 더블클릭으로 편집 모드 진입
        print("[2/6] 더블클릭으로 편집 모드 진입...")
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # 단계 3: 드롭다운 리스트에서 선택 (아래쪽 클릭)
        print("[3/6] 드롭다운 리스트에서 선택...")
        pyautogui.click(PLAYER1_X, PLAYER1_Y + 30)  # 드롭다운 항목 클릭
        time.sleep(0.3)
        
        # 단계 4: 기존 텍스트 삭제 및 새 이름 입력
        print(f"[4/6] 새 이름 입력: {new_name}")
        pyautogui.hotkey('ctrl', 'a')  # 전체 선택
        time.sleep(0.1)
        pyautogui.press('delete')  # 삭제
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)  # 새 이름 입력
        time.sleep(0.2)
        
        # 단계 5: Enter 키 누르기
        print("[5/6] Enter 키로 적용...")
        pyautogui.press('enter')
        time.sleep(0.3)
        
        # 단계 6: 확인 클릭 (다른 곳 클릭 또는 확인 버튼)
        print("[6/6] 최종 확인...")
        pyautogui.click(PLAYER1_X + 200, PLAYER1_Y)  # 옆 영역 클릭으로 확인
        time.sleep(0.3)
        
        print("\n" + "="*60)
        print("✅ 성공적으로 완료!")
        print(f"플레이어 1 이름이 '{new_name}'로 변경되었습니다")
        print("="*60)
        
        # 스크린샷 저장
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"existing_name_update_{timestamp}.png"
        screenshot.save(filename)
        print(f"\n결과 스크린샷: {filename}")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("프로세스가 중단되었습니다")

if __name__ == "__main__":
    print("Action Tracker - 기존 이름 변경 프로세스")
    print("="*60)
    print()
    print("이 스크립트는 이미 등록된 이름을 변경할 때 사용하는")
    print("드롭다운 선택 프로세스를 실행합니다.")
    print()
    print("주의: Action Tracker가 활성화되어 있어야 합니다!")
    print()
    
    update_existing_name()