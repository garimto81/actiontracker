"""
칩 입력 디버깅 스크립트
문제를 단계별로 확인
"""

import pyautogui
import time
from datetime import datetime

# 새로운 칩 좌표
CHIP_COORDS = {
    1: (211, 480),
    2: (377, 480),
    3: (547, 480),
    4: (719, 480),
    5: (913, 480),
}

def test_methods():
    """다양한 입력 방법 테스트"""
    print("=" * 60)
    print("CHIP INPUT DEBUG TEST")
    print("=" * 60)
    print("Testing different input methods...")
    
    seat = 1
    coords = CHIP_COORDS[seat]
    test_amount = "100000"
    
    print(f"\nTesting Seat {seat} at {coords}")
    print("Amount to input: " + test_amount)
    
    print("\n1. Testing different clear methods...")
    print("Starting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Method 1: Click only
    print("\n[METHOD 1] Click only")
    pyautogui.click(coords[0], coords[1])
    time.sleep(2)
    
    # Method 2: Click + Select All (Ctrl+A)
    print("\n[METHOD 2] Click + Ctrl+A")
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(2)
    
    # Method 3: Click + Triple Click
    print("\n[METHOD 3] Click + Triple Click")
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.5)
    pyautogui.tripleClick()
    time.sleep(2)
    
    # Method 4: Click + Backspace multiple times
    print("\n[METHOD 4] Click + Multiple Backspace")
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.5)
    for _ in range(10):
        pyautogui.press('backspace')
        time.sleep(0.05)
    time.sleep(2)
    
    # Method 5: Double click to select
    print("\n[METHOD 5] Double Click to select")
    pyautogui.doubleClick(coords[0], coords[1])
    time.sleep(2)

def test_typing_methods():
    """다양한 타이핑 방법 테스트"""
    print("\n" + "=" * 60)
    print("TYPING METHOD TEST")
    print("=" * 60)
    
    seat = 1
    coords = CHIP_COORDS[seat]
    
    print(f"Testing typing at Seat {seat}: {coords}")
    print("Starting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Click field
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.5)
    
    # Clear first
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    
    print("\n[TEST 1] Using typewrite")
    pyautogui.typewrite("111111", interval=0.1)
    time.sleep(2)
    
    # Clear again
    pyautogui.click(coords[0], coords[1])
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    
    print("\n[TEST 2] Using individual press")
    for digit in "222222":
        pyautogui.press(digit)
        time.sleep(0.1)
    time.sleep(2)
    
    # Clear again
    pyautogui.click(coords[0], coords[1])
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.2)
    
    print("\n[TEST 3] Using write (faster)")
    pyautogui.write("333333")
    time.sleep(2)

def test_focus():
    """포커스 문제 테스트"""
    print("\n" + "=" * 60)
    print("FOCUS TEST")
    print("=" * 60)
    
    seat = 1
    coords = CHIP_COORDS[seat]
    
    print("Testing if field gets proper focus...")
    print("Starting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Method 1: Single click with longer wait
    print("\n[FOCUS 1] Single click + wait")
    pyautogui.click(coords[0], coords[1])
    time.sleep(1)  # Longer wait for focus
    pyautogui.typewrite("444444", interval=0.1)
    time.sleep(2)
    
    # Method 2: Click multiple times
    print("\n[FOCUS 2] Multiple clicks")
    for _ in range(3):
        pyautogui.click(coords[0], coords[1])
        time.sleep(0.2)
    pyautogui.typewrite("555555", interval=0.1)
    time.sleep(2)
    
    # Method 3: Click and hold
    print("\n[FOCUS 3] Click and hold")
    pyautogui.mouseDown(coords[0], coords[1])
    time.sleep(0.5)
    pyautogui.mouseUp()
    time.sleep(0.5)
    pyautogui.typewrite("666666", interval=0.1)

def test_single_seat_detailed():
    """단일 좌석 상세 테스트"""
    print("\n" + "=" * 60)
    print("DETAILED SINGLE SEAT TEST")
    print("=" * 60)
    
    seat = int(input("Enter seat number to test (1-5): "))
    if seat not in CHIP_COORDS:
        print("Invalid seat number")
        return
    
    coords = CHIP_COORDS[seat]
    amount = input("Enter chip amount: ")
    
    print(f"\nTesting Seat {seat} at {coords}")
    print(f"Amount: {amount}")
    print("\nStarting in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\nStep by step execution:")
    
    # Step 1: Move mouse
    print(f"1. Moving mouse to {coords}")
    pyautogui.moveTo(coords[0], coords[1], duration=0.5)
    time.sleep(1)
    
    # Step 2: Click
    print("2. Clicking field")
    pyautogui.click()
    time.sleep(1)
    
    # Step 3: Select all
    print("3. Selecting all (Ctrl+A)")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.5)
    
    # Step 4: Type each digit
    print("4. Typing digits:")
    for i, digit in enumerate(amount, 1):
        print(f"   Digit {i}: '{digit}'")
        pyautogui.press(digit)
        time.sleep(0.15)  # Slower typing
    
    print("\nComplete!")

def main():
    """메인 메뉴"""
    print("\n" + "=" * 60)
    print("CHIP INPUT DEBUGGER")
    print("=" * 60)
    print("1. Test different clear methods")
    print("2. Test typing methods")
    print("3. Test focus issues")
    print("4. Detailed single seat test")
    print("5. Exit")
    print("=" * 60)
    
    choice = input("\nSelect (1-5): ").strip()
    
    if choice == "1":
        test_methods()
    elif choice == "2":
        test_typing_methods()
    elif choice == "3":
        test_focus()
    elif choice == "4":
        test_single_seat_detailed()
    elif choice == "5":
        print("Exiting...")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    print(f"Screen: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    print("\nMAKE SURE ACTION TRACKER IS OPEN!")
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    main()