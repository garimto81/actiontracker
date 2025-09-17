"""
칩 입력 테스트 스크립트
Action Tracker 칩 입력 기능 테스트
"""

import pyautogui
import time
from datetime import datetime

# 칩 입력 좌표 (integrated_gui_final_FINAL.py에서 가져옴)
CHIP_COORDS = {
    1: (1226, 622),
    2: (1382, 619),
    3: (1537, 615),
    4: (1688, 615),
    5: (1694, 615),
    6: (1694, 615),
    7: (1226, 622),
    8: (1382, 619),
    9: (1537, 615),
    10: (1688, 615)
}

def test_chip_input(seat_number, chip_amount):
    """단일 좌석 칩 입력 테스트"""
    print(f"\n[TEST] Seat {seat_number}: Input {chip_amount} chips")
    print(f"Coordinates: {CHIP_COORDS[seat_number]}")
    
    try:
        # 1. 칩 입력 필드 클릭
        coords = CHIP_COORDS[seat_number]
        print(f"  1. Click chip field: ({coords[0]}, {coords[1]})")
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)
        
        # 2. 칩 금액 입력 (한 자리씩)
        chip_str = str(chip_amount)
        print(f"  2. Input chip amount: {chip_str}")
        for i, digit in enumerate(chip_str):
            print(f"     - Typing digit '{digit}'...")
            pyautogui.press(digit)
            time.sleep(0.1)  # 오버플로우 방지
        
        # 3. 입력 완료
        time.sleep(0.2)
        print(f"  [OK] Seat {seat_number} chip input complete!")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

def run_test_sequence():
    """테스트 시퀀스 실행"""
    print("=" * 60)
    print("Starting Chip Input Test")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nWARNING: Make sure Action Tracker is open and active!")
    print("Test will start in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    # 테스트 케이스
    test_cases = [
        (1, 1000000),    # 좌석 1: 100만
        (2, 500000),     # 좌석 2: 50만
        (3, 2500000),    # 좌석 3: 250만
        (4, 750000),     # 좌석 4: 75만
        (5, 1500000),    # 좌석 5: 150만
    ]
    
    success_count = 0
    fail_count = 0
    
    for seat, chips in test_cases:
        result = test_chip_input(seat, chips)
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        # 각 입력 사이 대기
        time.sleep(1)
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    print(f"[SUCCESS]: {success_count}")
    print(f"[FAILED]: {fail_count}")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success_count, fail_count

def test_single_seat():
    """단일 좌석 테스트 (디버깅용)"""
    print("\nSingle Seat Test Mode")
    print("=" * 60)
    
    seat = int(input("Enter seat number to test (1-10): "))
    chips = input("Enter chip amount: ")
    
    print(f"\nInputting {chips} chips to seat {seat}.")
    print("Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    test_chip_input(seat, chips)

def main():
    """메인 함수"""
    print("\nAction Tracker Chip Input Test")
    print("=" * 60)
    print("1. Run full test sequence (5 seats)")
    print("2. Test single seat")
    print("3. Exit")
    print("=" * 60)
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == "1":
        run_test_sequence()
    elif choice == "2":
        test_single_seat()
    elif choice == "3":
        print("Exiting test.")
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    # 안전 장치 설정
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    # 현재 화면 크기 출력
    screen_width, screen_height = pyautogui.size()
    print(f"\nScreen Size: {screen_width} x {screen_height}")
    
    # 메인 실행
    main()