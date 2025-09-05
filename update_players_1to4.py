"""
Update Players 1-4 with Different Processes
1~3번: 이름 수정 (이미 존재)
4번: 새 이름 등록 (비어있음)
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Coordinates
MAIN_PLAYER1 = (233, 361)
MAIN_PLAYER2 = (374, 359)
MAIN_PLAYER3 = (544, 362)
MAIN_PLAYER4 = (722, 359)

SUB_NAME_FIELD = (785, 291)    # Sub screen name field (for existing names)
COMPLETE_BUTTON = (1720, 139)  # Complete button (closes Action Tracker)

def update_existing_name(player_num, coords, new_name):
    """
    Update existing name (Players 1-3)
    Process: Click player → Click name field → Clear → Type → Enter → Complete
    """
    print(f"\n[Player {player_num}] Updating existing name to: {new_name}")
    
    # Step 1: Click player on main screen
    print(f"  1. Click Player {player_num}: {coords}")
    pyautogui.click(coords[0], coords[1])
    time.sleep(1)  # Wait for sub screen
    
    # Step 2: Click name field in sub screen
    print(f"  2. Click name field: {SUB_NAME_FIELD}")
    pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
    time.sleep(0.5)
    
    # Step 3: Clear and type new name
    print(f"  3. Clear and type: {new_name}")
    pyautogui.tripleClick()  # Select all
    time.sleep(0.2)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.3)
    
    # Step 4: Press Enter
    print("  4. Press Enter")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    # Step 5: Click complete button
    print(f"  5. Click complete: {COMPLETE_BUTTON}")
    pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
    time.sleep(1)
    
    print(f"  [OK] Player {player_num} updated")

def register_new_name(player_num, coords, new_name):
    """
    Register new name (Player 4)
    Simple process: Click player → Type → Enter
    """
    print(f"\n[Player {player_num}] Registering new name: {new_name}")
    
    # Step 1: Click player on main screen
    print(f"  1. Click Player {player_num}: {coords}")
    pyautogui.click(coords[0], coords[1])
    time.sleep(0.5)
    
    # Step 2: Type new name directly
    print(f"  2. Type name: {new_name}")
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.3)
    
    # Step 3: Press Enter
    print("  3. Press Enter")
    pyautogui.press('enter')
    time.sleep(0.5)
    
    print(f"  [OK] Player {player_num} registered")

def update_all_four_players():
    """
    Update all 4 players with appropriate processes
    """
    print("="*60)
    print("UPDATE PLAYERS 1-4")
    print("="*60)
    print("\nPlayer Status:")
    print("  Players 1-3: Have existing names (update process)")
    print("  Player 4: Empty slot (register process)")
    print()
    
    # New names for each player
    new_names = {
        1: "Johnny Chan",      # Update existing
        2: "Chris Moneymaker", # Update existing  
        3: "Antonio Esfandiari", # Update existing
        4: "Tom Dwan"          # Register new
    }
    
    print("New Names:")
    for num, name in new_names.items():
        status = "Update" if num <= 3 else "Register"
        print(f"  Player {num}: {name} [{status}]")
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    # Take before screenshot
    print("\n[BEFORE] Taking initial screenshot...")
    before = pyautogui.screenshot()
    before.save("players_1to4_before.png")
    
    try:
        # Update Player 1 (existing name)
        update_existing_name(1, MAIN_PLAYER1, new_names[1])
        
        # Update Player 2 (existing name)
        update_existing_name(2, MAIN_PLAYER2, new_names[2])
        
        # Update Player 3 (existing name)
        update_existing_name(3, MAIN_PLAYER3, new_names[3])
        
        # Register Player 4 (new name - simple process)
        register_new_name(4, MAIN_PLAYER4, new_names[4])
        
        # Take after screenshot
        print("\n[AFTER] Taking final screenshot...")
        after = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%H%M%S")
        after_file = f"players_1to4_after_{timestamp}.png"
        after.save(after_file)
        
        print("\n" + "="*60)
        print("SUCCESS - ALL 4 PLAYERS UPDATED!")
        print("="*60)
        print("Results:")
        for num, name in new_names.items():
            print(f"  Player {num}: {name}")
        print()
        print(f"Before: players_1to4_before.png")
        print(f"After: {after_file}")
        print("="*60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        error_shot = pyautogui.screenshot()
        error_shot.save("players_1to4_error.png")
        print("Error screenshot: players_1to4_error.png")

if __name__ == "__main__":
    update_all_four_players()