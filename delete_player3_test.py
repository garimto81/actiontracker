"""
Delete Player 3 Test
3번 플레이어 삭제 테스트
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Coordinates
PLAYER3_MAIN = (544, 362)      # Player 3 on main screen
DELETE_BUTTON = (721, 112)     # Delete button coordinate

def delete_player3():
    """
    Delete Player 3
    Process: Click Player 3 → Click Delete button
    """
    
    print("="*60)
    print("DELETE PLAYER 3 TEST")
    print("="*60)
    print()
    print("Process:")
    print("1. Click Player 3 to select")
    print("2. Click Delete button")
    print()
    
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Take before screenshot
    print("\n[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("delete_player3_before.png")
    print("Screenshot saved: delete_player3_before.png")
    
    try:
        # Step 1: Click Player 3 to select
        print(f"\n[Step 1] Click Player 3: {PLAYER3_MAIN}")
        pyautogui.click(PLAYER3_MAIN[0], PLAYER3_MAIN[1])
        time.sleep(1)  # Wait for selection
        
        # Step 2: Click Delete button
        print(f"[Step 2] Click Delete button: {DELETE_BUTTON}")
        pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
        time.sleep(1)  # Wait for deletion
        
        # Take after screenshot
        print("\n[AFTER] Taking screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"delete_player3_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("DELETE COMPLETE!")
        print("="*60)
        print("Player 3 (Doyle Brunson) has been deleted")
        print(f"Before: delete_player3_before.png")
        print(f"After: {after_file}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("delete_player3_error.png")
        print("Error screenshot saved: delete_player3_error.png")

if __name__ == "__main__":
    delete_player3()