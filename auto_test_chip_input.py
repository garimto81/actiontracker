"""
자동 칩 입력 테스트 스크립트
입력 없이 자동으로 테스트 실행
"""

import pyautogui
import time
from datetime import datetime

# 칩 입력 좌표
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
    print(f"  Coordinates: {CHIP_COORDS[seat_number]}")
    
    try:
        # 1. 칩 입력 필드 클릭
        coords = CHIP_COORDS[seat_number]
        print(f"  Step 1: Click chip field at ({coords[0]}, {coords[1]})")
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)
        
        # 2. 칩 금액 입력 (한 자리씩)
        chip_str = str(chip_amount)
        print(f"  Step 2: Input chip amount: {chip_str}")
        
        for i, digit in enumerate(chip_str, 1):
            print(f"    - Typing digit {i}/{len(chip_str)}: '{digit}'")
            pyautogui.press(digit)
            time.sleep(0.1)  # 오버플로우 방지
        
        # 3. 입력 완료
        time.sleep(0.2)
        print(f"  [SUCCESS] Seat {seat_number} chip input complete!")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

def main():
    """메인 테스트 실행"""
    print("=" * 60)
    print("AUTO CHIP INPUT TEST")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Screen Size: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    
    print("\nWARNING: Make sure Action Tracker is open and active!")
    print("Test will start automatically in 5 seconds...")
    print("Move mouse to top-left corner to abort (PyAutoGUI failsafe)")
    
    # 카운트다운
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("STARTING TESTS")
    print("=" * 60)
    
    # 테스트 케이스
    test_cases = [
        (1, 1000000),    # 좌석 1: 100만
        (2, 500000),     # 좌석 2: 50만
        (3, 2500000),    # 좌석 3: 250만
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
        print("  Waiting 1 second before next test...")
        time.sleep(1)
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"SUCCESS: {success_count}/{len(test_cases)}")
    print(f"FAILED: {fail_count}/{len(test_cases)}")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if fail_count == 0:
        print("\nAll tests passed successfully!")
    else:
        print(f"\n{fail_count} test(s) failed. Please check the errors above.")
    
    print("\nTest completed!")

if __name__ == "__main__":
    # 안전 장치 설정
    pyautogui.FAILSAFE = True  # 마우스를 좌상단으로 이동시 중단
    pyautogui.PAUSE = 0.1      # 각 명령 사이 기본 대기 시간
    
    # 메인 실행
    main()