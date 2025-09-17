"""
새로운 칩 좌표 테스트
플레이어 1-10 칩 입력 테스트
"""

import pyautogui
import time
from datetime import datetime

# 새로운 칩 입력 좌표
CHIP_COORDS = {
    1: (211, 480),
    2: (377, 480),
    3: (547, 480),
    4: (719, 480),
    5: (913, 480),
    6: (1031, 480),
    7: (1211, 480),
    8: (1378, 480),
    9: (1546, 480),
    10: (1696, 480)
}

def test_chip_input(seat_number, chip_amount):
    """칩 입력 테스트"""
    print(f"\n{'='*50}")
    print(f"[SEAT {seat_number}] Testing chip input: {chip_amount:,} chips")
    print(f"Coordinates: {CHIP_COORDS[seat_number]}")
    
    try:
        coords = CHIP_COORDS[seat_number]
        
        # Step 1: Click chip field
        print(f"  1. Click: ({coords[0]}, {coords[1]})")
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.3)
        
        # Step 2: Clear existing value
        print(f"  2. Clear: Triple click")
        pyautogui.tripleClick()
        time.sleep(0.1)
        
        # Step 3: Type new amount
        chip_str = str(chip_amount)
        print(f"  3. Type: {chip_str}")
        
        for i, digit in enumerate(chip_str, 1):
            print(f"     [{i}/{len(chip_str)}] '{digit}'")
            pyautogui.press(digit)
            time.sleep(0.1)
        
        time.sleep(0.2)
        print(f"  [SUCCESS]")
        return True
        
    except Exception as e:
        print(f"  [FAILED]: {e}")
        return False

def test_all_seats():
    """모든 좌석 테스트"""
    print("\n" + "="*60)
    print("CHIP INPUT TEST - ALL 10 SEATS")
    print("="*60)
    print(f"Start: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Screen: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    
    print("\nNEW COORDINATES:")
    for seat, coord in CHIP_COORDS.items():
        print(f"  Seat {seat:2}: {coord}")
    
    print("\nStarting in 5 seconds...")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Test amounts for each seat
    test_amounts = {
        1: 1000000,   # 1M
        2: 500000,    # 500K
        3: 2500000,   # 2.5M
        4: 750000,    # 750K
        5: 1500000,   # 1.5M
        6: 300000,    # 300K
        7: 2000000,   # 2M
        8: 800000,    # 800K
        9: 1200000,   # 1.2M
        10: 600000    # 600K
    }
    
    results = []
    
    for seat in range(1, 11):
        chips = test_amounts[seat]
        success = test_chip_input(seat, chips)
        results.append((seat, chips, success))
        
        if seat < 10:
            time.sleep(1)
    
    # Results summary
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    
    success_count = 0
    for seat, chips, success in results:
        status = "[OK]" if success else "[FAIL]"
        print(f"  Seat {seat:2}: {status} {chips:,} chips")
        if success:
            success_count += 1
    
    print(f"\nSuccess Rate: {success_count}/10 ({success_count*10}%)")
    print(f"End: {datetime.now().strftime('%H:%M:%S')}")

def test_specific_seats():
    """특정 좌석만 테스트"""
    print("\n" + "="*60)
    print("CHIP INPUT TEST - SPECIFIC SEATS")
    print("="*60)
    
    seats_to_test = input("Enter seat numbers (comma separated, e.g., 1,2,3): ")
    seats = [int(s.strip()) for s in seats_to_test.split(",")]
    
    print(f"\nTesting seats: {seats}")
    print("Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    for seat in seats:
        if seat in CHIP_COORDS:
            amount = int(input(f"\nChip amount for seat {seat}: "))
            test_chip_input(seat, amount)
            time.sleep(1)
        else:
            print(f"Invalid seat number: {seat}")

def main():
    """메인 메뉴"""
    print("\n" + "="*60)
    print("CHIP INPUT TESTER - NEW COORDINATES")
    print("="*60)
    print("1. Test all 10 seats")
    print("2. Test seats 1-4 only")
    print("3. Test specific seats")
    print("4. Exit")
    print("="*60)
    
    choice = input("\nSelect (1-4): ").strip()
    
    if choice == "1":
        test_all_seats()
    elif choice == "2":
        # Test seats 1-4
        print("\n" + "="*60)
        print("TESTING SEATS 1-4")
        print("="*60)
        print("Starting in 3 seconds...")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        
        test_amounts = [1000000, 500000, 2500000, 750000]
        for seat, amount in zip(range(1, 5), test_amounts):
            test_chip_input(seat, amount)
            if seat < 4:
                time.sleep(1)
    elif choice == "3":
        test_specific_seats()
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    main()