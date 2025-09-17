"""
플레이어 1-4 칩 입력 테스트
Action Tracker 칩 입력 기능 테스트 (좌석 1-4)
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
}

def test_chip_input(seat_number, chip_amount):
    """칩 입력 테스트 - Clear 로직 포함"""
    print(f"\n{'='*50}")
    print(f"[PLAYER {seat_number}] Testing chip input: {chip_amount:,} chips")
    print(f"{'='*50}")
    print(f"Coordinates: {CHIP_COORDS[seat_number]}")
    
    try:
        coords = CHIP_COORDS[seat_number]
        
        # Step 1: Click chip field
        print(f"Step 1: Clicking chip field at ({coords[0]}, {coords[1]})")
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)
        
        # Step 2: Clear existing value (triple click to select all)
        print(f"Step 2: Clearing existing value (triple click)")
        pyautogui.tripleClick()
        time.sleep(0.1)
        
        # Step 3: Type new chip amount
        chip_str = str(chip_amount)
        print(f"Step 3: Typing new chip amount: {chip_str}")
        
        for i, digit in enumerate(chip_str, 1):
            print(f"  - Digit {i}/{len(chip_str)}: '{digit}'")
            pyautogui.press(digit)
            time.sleep(0.1)  # Prevent overflow
        
        # Step 4: Complete
        time.sleep(0.2)
        print(f"[SUCCESS] PLAYER {seat_number}: Chip input successful!")
        return True
        
    except Exception as e:
        print(f"[FAILED] PLAYER {seat_number}: Failed - {e}")
        return False

def main():
    """메인 테스트"""
    print("\n" + "="*60)
    print("CHIP INPUT TEST - PLAYERS 1 TO 4")
    print("="*60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Screen Size: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    
    print("\nWARNING: ACTION TRACKER MUST BE OPEN AND ACTIVE!")
    print("This test will input chips for players 1-4")
    print("\nTest configurations:")
    print("  Player 1: 1,000,000 chips")
    print("  Player 2: 500,000 chips")
    print("  Player 3: 2,500,000 chips")
    print("  Player 4: 750,000 chips")
    
    print("\nStarting in 5 seconds...")
    print("(Move mouse to top-left corner to abort)")
    
    # Countdown
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n" + "="*60)
    print("STARTING CHIP INPUT TESTS")
    print("="*60)
    
    # Test cases for players 1-4
    test_cases = [
        (1, 1000000),    # Player 1: 1M
        (2, 500000),     # Player 2: 500K
        (3, 2500000),    # Player 3: 2.5M
        (4, 750000),     # Player 4: 750K
    ]
    
    success_count = 0
    fail_count = 0
    results = []
    
    for seat, chips in test_cases:
        result = test_chip_input(seat, chips)
        if result:
            success_count += 1
            results.append(f"Player {seat}: [SUCCESS] ({chips:,} chips)")
        else:
            fail_count += 1
            results.append(f"Player {seat}: [FAILED]")
        
        # Wait between inputs
        if seat < 4:  # Don't wait after last test
            print("\nWaiting 1 second before next player...")
            time.sleep(1)
    
    # Print results summary
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    for result in results:
        print(f"  {result}")
    
    print(f"\nTotal: {success_count} SUCCESS, {fail_count} FAILED")
    print(f"Success Rate: {success_count}/{len(test_cases)} ({success_count*100//len(test_cases)}%)")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if fail_count == 0:
        print("\nAll tests passed successfully!")
    else:
        print(f"\nWARNING: {fail_count} test(s) failed. Please check the errors above.")
    
    print("\nTest completed!")

if __name__ == "__main__":
    # Safety settings
    pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
    pyautogui.PAUSE = 0.1       # Default pause between commands
    
    # Run test
    main()