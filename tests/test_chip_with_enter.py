"""
칩 입력 테스트 - 플레이어 이름 좌표 클릭 + 숫자 입력 + 엔터
올바른 프로세스로 수정된 버전
"""

import pyautogui
import time
from datetime import datetime

# 플레이어 이름 좌표 (칩 입력 시 클릭할 위치)
PLAYER_COORDS = {
    1: (233, 361),
    2: (374, 359),
    3: (544, 362),
    4: (722, 359),
    5: (886, 356),
    6: (1051, 354),
    7: (1213, 355),
    8: (1385, 383),
    9: (1549, 367),
    10: (1705, 356)
}

def input_chips_correct(seat_number, chip_amount):
    """올바른 칩 입력 프로세스"""
    print(f"\n{'='*50}")
    print(f"[SEAT {seat_number}] Inputting {chip_amount:,} chips")
    print(f"{'='*50}")
    
    try:
        # 플레이어 이름 좌표 사용
        coords = PLAYER_COORDS[seat_number]
        print(f"Player name coordinates: {coords}")
        
        # Step 1: Click player name field
        print(f"Step 1: Click player name field at ({coords[0]}, {coords[1]})")
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)
        
        # Step 2: Clear existing value
        print(f"Step 2: Clear field (triple click)")
        pyautogui.tripleClick()
        time.sleep(0.1)
        
        # Step 3: Type chip amount
        chip_str = str(chip_amount)
        print(f"Step 3: Type chip amount: {chip_str}")
        
        for i, digit in enumerate(chip_str, 1):
            print(f"  - Typing digit {i}/{len(chip_str)}: '{digit}'")
            pyautogui.press(digit)
            time.sleep(0.1)  # Prevent overflow
        
        # Step 4: Press Enter to confirm
        print(f"Step 4: Press ENTER to confirm")
        time.sleep(0.2)
        pyautogui.press('enter')
        time.sleep(0.3)
        
        print(f"[SUCCESS] Chips input complete for seat {seat_number}!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        return False

def test_seats_1_to_4():
    """좌석 1-4 테스트"""
    print("\n" + "="*60)
    print("CHIP INPUT TEST - SEATS 1-4")
    print("Using PLAYER NAME coordinates + ENTER key")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Screen: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    
    print("\nCoordinates being used:")
    for seat in range(1, 5):
        print(f"  Seat {seat}: {PLAYER_COORDS[seat]}")
    
    print("\nProcess: Click name -> Clear -> Type chips -> Press ENTER")
    print("\nStarting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Test data
    test_chips = {
        1: 1000000,   # 1M
        2: 500000,    # 500K
        3: 2500000,   # 2.5M
        4: 750000     # 750K
    }
    
    results = []
    
    for seat, chips in test_chips.items():
        success = input_chips_correct(seat, chips)
        results.append((seat, chips, success))
        
        if seat < 4:
            print("\nWaiting 1 second before next seat...")
            time.sleep(1)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for seat, chips, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"  Seat {seat}: {status} - {chips:,} chips")
    
    success_count = sum(1 for _, _, success in results if success)
    print(f"\nSuccess Rate: {success_count}/4 ({success_count*25}%)")
    print(f"End Time: {datetime.now().strftime('%H:%M:%S')}")

def test_single_seat():
    """단일 좌석 테스트"""
    print("\n" + "="*60)
    print("SINGLE SEAT TEST")
    print("="*60)
    
    seat = int(input("Enter seat number (1-10): "))
    if seat not in PLAYER_COORDS:
        print("Invalid seat number!")
        return
    
    chips = int(input("Enter chip amount: "))
    
    print(f"\nTesting seat {seat} with {chips:,} chips")
    print(f"Using player coordinates: {PLAYER_COORDS[seat]}")
    print("\nStarting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    input_chips_correct(seat, chips)

def test_all_10_seats():
    """모든 10개 좌석 테스트"""
    print("\n" + "="*60)
    print("ALL 10 SEATS TEST")
    print("="*60)
    
    print("This will test all 10 seats")
    print("Starting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    test_amounts = {
        1: 1000000, 2: 500000, 3: 2500000, 4: 750000, 5: 1500000,
        6: 300000, 7: 2000000, 8: 800000, 9: 1200000, 10: 600000
    }
    
    results = []
    
    for seat in range(1, 11):
        chips = test_amounts[seat]
        success = input_chips_correct(seat, chips)
        results.append((seat, chips, success))
        
        if seat < 10:
            time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print("RESULTS - ALL 10 SEATS")
    print("="*60)
    
    for seat, chips, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"  Seat {seat:2}: {status} - {chips:,} chips")
    
    success_count = sum(1 for _, _, success in results if success)
    print(f"\nTotal Success: {success_count}/10 ({success_count*10}%)")

def main():
    """메인 메뉴"""
    print("\n" + "="*60)
    print("CHIP INPUT TESTER - CORRECTED VERSION")
    print("Process: Click PLAYER NAME -> Type CHIPS -> Press ENTER")
    print("="*60)
    print("1. Test seats 1-4")
    print("2. Test single seat")
    print("3. Test all 10 seats")
    print("4. Exit")
    print("="*60)
    
    choice = input("\nSelect (1-4): ").strip()
    
    if choice == "1":
        test_seats_1_to_4()
    elif choice == "2":
        test_single_seat()
    elif choice == "3":
        test_all_10_seats()
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    print("ACTION TRACKER must be open!")
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    main()