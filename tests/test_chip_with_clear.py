"""
칩 입력 테스트 - Clear 로직 포함 버전
기존 값을 지우고 새로운 값 입력
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
    """칩 입력 테스트 - Clear 로직 포함"""
    print(f"\n[TEST] Seat {seat_number}: Input {chip_amount} chips")
    print(f"  Coordinates: {CHIP_COORDS[seat_number]}")
    
    try:
        coords = CHIP_COORDS[seat_number]
        
        # Step 1: Click chip field
        print(f"  Step 1: Click chip field at ({coords[0]}, {coords[1]})")
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)
        
        # Step 2: Clear existing value (triple click to select all)
        print(f"  Step 2: Clear existing value (triple click)")
        pyautogui.tripleClick()
        time.sleep(0.1)
        
        # Step 3: Type new chip amount
        chip_str = str(chip_amount)
        print(f"  Step 3: Type new chip amount: {chip_str}")
        
        for i, digit in enumerate(chip_str, 1):
            print(f"    - Typing digit {i}/{len(chip_str)}: '{digit}'")
            pyautogui.press(digit)
            time.sleep(0.1)  # Prevent overflow
        
        # Step 4: Complete
        time.sleep(0.2)
        print(f"  [SUCCESS] Seat {seat_number} chip input complete!")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return False

def main():
    """메인 테스트"""
    print("=" * 60)
    print("CHIP INPUT TEST WITH CLEAR")
    print("=" * 60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Screen Size: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    
    print("\nWARNING: Make sure Action Tracker is open!")
    print("Test includes CLEAR logic for existing values")
    print("\nStarting in 5 seconds...")
    print("Move mouse to top-left corner to abort")
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("STARTING TESTS")
    print("=" * 60)
    
    # Test cases
    test_cases = [
        (1, 1000000),    # Seat 1: 1M
        (2, 500000),     # Seat 2: 500K
        (3, 2500000),    # Seat 3: 2.5M
    ]
    
    success_count = 0
    fail_count = 0
    
    for seat, chips in test_cases:
        result = test_chip_input(seat, chips)
        if result:
            success_count += 1
        else:
            fail_count += 1
        
        print("  Waiting 1 second...")
        time.sleep(1)
    
    # Results
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"SUCCESS: {success_count}/{len(test_cases)}")
    print(f"FAILED: {fail_count}/{len(test_cases)}")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if fail_count == 0:
        print("\nAll tests passed!")
    else:
        print(f"\n{fail_count} test(s) failed.")
    
    print("\nTest completed!")

if __name__ == "__main__":
    # Safety settings
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    # Run test
    main()