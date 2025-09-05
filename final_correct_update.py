"""
Final Correct Player 1 Update with Accurate Coordinates
정확한 좌표값으로 플레이어 1 이름 변경
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 정확한 좌표값 (사용자 제공)
MAIN_PLAYER1 = (233, 361)      # 메인 화면 player1 선택 좌표
SUB_NAME_FIELD = (785, 291)    # 서브 화면 player 이름 선택 좌표
COMPLETE_BUTTON = (1720, 139)  # 플레이어 이름 등록 완료 좌표

def update_player1_existing_name():
    """
    기존 이름이 존재하는 경우의 업데이트 프로세스
    1. 메인 화면에서 Player1 클릭
    2. 서브 화면에서 이름 필드 클릭
    3. 드롭다운에서 선택
    4. 새 이름 입력
    5. Enter
    6. 완료 버튼 클릭
    """
    
    print("="*60)
    print("PLAYER 1 UPDATE - CORRECT COORDINATES")
    print("="*60)
    print()
    print("Using coordinates:")
    print(f"  1. Main screen Player1: {MAIN_PLAYER1}")
    print(f"  2. Sub screen name field: {SUB_NAME_FIELD}")
    print(f"  3. Complete button: {COMPLETE_BUTTON}")
    print()
    
    new_name = "Daniel Negreanu"
    
    # Before screenshot
    print("[BEFORE] 초기 스크린샷 저장...")
    before = pyautogui.screenshot()
    before.save("final_before.png")
    
    print(f"\nPlayer 1을 '{new_name}'로 변경합니다")
    print("3초 후 시작...")
    time.sleep(3)
    
    try:
        # Step 1: 메인 화면에서 Player1 클릭
        print(f"\n[1단계] 메인 화면 Player1 클릭: {MAIN_PLAYER1}")
        pyautogui.click(MAIN_PLAYER1[0], MAIN_PLAYER1[1])
        time.sleep(1)  # 서브 화면이 열릴 때까지 대기
        
        # Step 2: 서브 화면에서 이름 필드 클릭
        print(f"[2단계] 서브 화면 이름 필드 클릭: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: 드롭다운이 나타나면 선택 (기존 이름인 경우)
        print("[3단계] 드롭다운에서 선택 (있는 경우)")
        dropdown_y = SUB_NAME_FIELD[1] + 30  # 드롭다운 첫 항목
        pyautogui.click(SUB_NAME_FIELD[0], dropdown_y)
        time.sleep(0.3)
        
        # Step 4: 기존 텍스트 삭제 및 새 이름 입력
        print(f"[4단계] 새 이름 입력: {new_name}")
        pyautogui.hotkey('ctrl', 'a')  # 전체 선택
        time.sleep(0.1)
        pyautogui.press('delete')  # 삭제
        time.sleep(0.1)
        pyautogui.typewrite(new_name, interval=0.02)  # 새 이름 입력
        time.sleep(0.3)
        
        # Step 5: Enter 키로 확정
        print("[5단계] Enter 키로 확정")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 6: 완료 버튼 클릭
        print(f"[6단계] 완료 버튼 클릭: {COMPLETE_BUTTON}")
        pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
        time.sleep(1)
        
        # After screenshot
        print("\n[AFTER] 최종 스크린샷 저장...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"final_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("프로세스 완료 - 스크린샷 확인!")
        print("="*60)
        print("1. final_before.png - 변경 전")
        print(f"2. {after_file} - 변경 후")
        print()
        print(f"Player 1이 '{new_name}'로 변경되었는지 확인하세요")
        print("="*60)
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("final_error.png")
        print("오류 스크린샷: final_error.png")

def update_player1_new_name():
    """
    새로운 이름인 경우의 간단한 프로세스
    1. 메인 화면에서 Player1 클릭
    2. 서브 화면에서 이름 필드 클릭
    3. 새 이름 입력
    4. Enter
    5. 완료 버튼 클릭
    """
    
    print("="*60)
    print("NEW NAME UPDATE PROCESS")
    print("="*60)
    
    new_name = "NewPlayer2024"
    
    print("3초 후 시작...")
    time.sleep(3)
    
    # Step 1: 메인 화면에서 Player1 클릭
    print(f"[1] 메인 화면 Player1 클릭: {MAIN_PLAYER1}")
    pyautogui.click(MAIN_PLAYER1[0], MAIN_PLAYER1[1])
    time.sleep(1)
    
    # Step 2: 서브 화면 이름 필드 클릭
    print(f"[2] 이름 필드 클릭: {SUB_NAME_FIELD}")
    pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
    time.sleep(0.5)
    
    # Step 3: 새 이름 입력
    print(f"[3] 새 이름 입력: {new_name}")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.3)
    
    # Step 4: Enter
    print("[4] Enter 키")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Step 5: 완료 버튼
    print(f"[5] 완료 버튼: {COMPLETE_BUTTON}")
    pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
    time.sleep(1)
    
    print("완료!")

if __name__ == "__main__":
    print("Action Tracker Player 1 Name Update")
    print("="*60)
    print("\nOptions:")
    print("1. Update existing name (dropdown process)")
    print("2. Enter new name (simple process)")
    print("3. Auto (run existing name process)")
    print()
    
    choice = input("Select (1-3, default 3): ").strip() or "3"
    
    if choice == "1" or choice == "3":
        update_player1_existing_name()
    elif choice == "2":
        update_player1_new_name()
    else:
        print("Invalid choice")