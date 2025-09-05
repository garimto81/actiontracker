"""
Test Both Name Update Processes
Demonstrates the difference between existing and new name processes
"""

import pyautogui
import time

# Player 1 coordinates
PLAYER1_X = 215
PLAYER1_Y = 354

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

print("="*60)
print("ACTION TRACKER NAME UPDATE PROCESS TEST")
print("="*60)
print()
print("This will demonstrate both update processes:")
print()
print("1. EXISTING NAME Process (4 steps):")
print("   - Click name field")
print("   - Click dropdown selection") 
print("   - Type new name")
print("   - Press Enter")
print("   - Click confirmation")
print()
print("2. NEW NAME Process (2 steps):")
print("   - Click name field")
print("   - Type new name")
print("   - Press Enter")
print()
print("-"*60)

choice = input("Which process to test? (1=Existing, 2=New, 3=Both): ")

def test_existing_name_process():
    """Test the existing name process"""
    print("\n" + "="*40)
    print("TESTING EXISTING NAME PROCESS")
    print("="*40)
    print("This simulates when a name already exists")
    print("and a dropdown appears")
    
    new_name = input("Enter name to update to: ") or "Mike"
    
    print(f"\nUpdating Player 1 to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Step 1
    print("[1/5] Clicking player name...")
    pyautogui.click(PLAYER1_X, PLAYER1_Y)
    time.sleep(0.3)
    
    # Step 2
    print("[2/5] Double-clicking to edit...")
    pyautogui.doubleClick()
    time.sleep(0.5)
    
    # Step 3 - Simulate dropdown selection
    print("[3/5] Selecting from dropdown...")
    pyautogui.click(PLAYER1_X, PLAYER1_Y + 25)
    time.sleep(0.3)
    
    # Step 4
    print("[4/5] Clearing and typing new name...")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.2)
    
    # Step 5
    print("[5/5] Pressing Enter and confirming...")
    pyautogui.press('enter')
    time.sleep(0.3)
    pyautogui.click(PLAYER1_X + 150, PLAYER1_Y)
    
    print("✓ Existing name process complete!")

def test_new_name_process():
    """Test the new name process"""
    print("\n" + "="*40)
    print("TESTING NEW NAME PROCESS")
    print("="*40)
    print("This simulates when a name is new")
    print("and no dropdown appears")
    
    new_name = input("Enter name to update to: ") or "NewPlayer"
    
    print(f"\nUpdating Player 1 to: {new_name}")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Step 1
    print("[1/3] Clicking player name...")
    pyautogui.click(PLAYER1_X, PLAYER1_Y)
    time.sleep(0.3)
    
    # Step 2
    print("[2/3] Double-clicking and typing...")
    pyautogui.doubleClick()
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.2)
    
    # Step 3
    print("[3/3] Pressing Enter...")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    print("✓ New name process complete!")

if choice == '1':
    test_existing_name_process()
elif choice == '2':
    test_new_name_process()
elif choice == '3':
    print("\nTesting both processes...")
    test_existing_name_process()
    print("\nWaiting 2 seconds before next test...")
    time.sleep(2)
    test_new_name_process()
    print("\n✓ Both processes tested!")
else:
    print("Invalid choice")

print("\nTest complete!")