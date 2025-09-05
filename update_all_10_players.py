"""
Update All 10 Players with Mixed Processes
1~4번: 이름 수정 (이미 존재)
5~10번: 새 이름 등록 (비어있음)
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Coordinates for all 10 players
PLAYERS = {
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

SUB_NAME_FIELD = (785, 291)    # Sub screen name field (for existing names)
COMPLETE_BUTTON = (1720, 139)  # Complete button (closes Action Tracker)

def update_existing_name(player_num, coords, new_name):
    """
    Update existing name (Players 1-4)
    Process: Click player → Click name field → Clear → Type → Enter → Complete
    """
    print(f"\n[Player {player_num}] Updating existing: {new_name}")
    
    try:
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
        
        print(f"  [SUCCESS] Player {player_num} updated")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Player {player_num} error: {e}")
        return False

def register_new_name(player_num, coords, new_name):
    """
    Register new name (Players 5-10)
    Simple process: Click player → Type → Enter
    """
    print(f"\n[Player {player_num}] Registering new: {new_name}")
    
    try:
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
        
        print(f"  [SUCCESS] Player {player_num} registered")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Player {player_num} error: {e}")
        return False

def update_all_ten_players():
    """
    Update all 10 players with appropriate processes
    """
    print("="*60)
    print("UPDATE ALL 10 PLAYERS")
    print("="*60)
    print("\nPlayer Status:")
    print("  Players 1-4: Update existing names")
    print("  Players 5-10: Register new names (empty)")
    print()
    
    # New names for each player - using famous poker players
    new_names = {
        1: "Phil Ivey",           # Update existing
        2: "Daniel Negreanu",     # Update existing  
        3: "Doyle Brunson",       # Update existing
        4: "Phil Hellmuth",       # Update existing
        5: "Tom Dwan",            # Register new
        6: "Patrik Antonius",     # Register new
        7: "Gus Hansen",          # Register new
        8: "Vanessa Selbst",      # Register new
        9: "Erik Seidel",         # Register new
        10: "Johnny Chan"         # Register new
    }
    
    # Track which players have existing names
    existing_players = [1, 2, 3, 4]
    empty_players = [5, 6, 7, 8, 9, 10]
    
    print("New names for each player:")
    for num, name in new_names.items():
        status = "Update" if num in existing_players else "Register"
        print(f"  Player {num}: {name} [{status}]")
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    # Take before screenshot
    print("\n[BEFORE] Taking screenshot...")
    before = pyautogui.screenshot()
    before.save("all_players_before.png")
    
    success_count = 0
    failed_players = []
    
    # Process each player
    for player_num in range(1, 11):
        if player_num in existing_players:
            # Update existing name
            if update_existing_name(player_num, PLAYERS[player_num], new_names[player_num]):
                success_count += 1
            else:
                failed_players.append(player_num)
                # If update fails, might be because it's actually empty
                print(f"  [RETRY] Trying to register Player {player_num} as new...")
                if register_new_name(player_num, PLAYERS[player_num], new_names[player_num]):
                    success_count += 1
                    existing_players.remove(player_num)
                    empty_players.append(player_num)
                    print(f"  [CORRECTED] Player {player_num} was actually empty")
        else:
            # Register new name
            if register_new_name(player_num, PLAYERS[player_num], new_names[player_num]):
                success_count += 1
            else:
                failed_players.append(player_num)
                # If registration fails, might be because it actually has a name
                print(f"  [RETRY] Trying to update Player {player_num} as existing...")
                if update_existing_name(player_num, PLAYERS[player_num], new_names[player_num]):
                    success_count += 1
                    empty_players.remove(player_num)
                    existing_players.append(player_num)
                    print(f"  [CORRECTED] Player {player_num} actually had a name")
        
        time.sleep(0.5)  # Brief pause between players
    
    # Take after screenshot
    print("\n[AFTER] Taking screenshot...")
    after = pyautogui.screenshot()
    timestamp = datetime.now().strftime("%H%M%S")
    after_file = f"all_players_after_{timestamp}.png"
    after.save(after_file)
    
    print("\n" + "="*60)
    if success_count == 10:
        print("SUCCESS - ALL 10 PLAYERS UPDATED!")
    else:
        print(f"PARTIAL SUCCESS - {success_count}/10 players updated")
    print("="*60)
    
    print("\nResults:")
    for num, name in new_names.items():
        status = "SUCCESS" if num not in failed_players else "FAILED"
        print(f"  Player {num}: {name} [{status}]")
    
    if failed_players:
        print(f"\nFailed players: {failed_players}")
        print("Failed players need manual verification.")
    
    print(f"\nScreenshots:")
    print(f"  Before: all_players_before.png")
    print(f"  After: {after_file}")
    print("="*60)

if __name__ == "__main__":
    update_all_ten_players()