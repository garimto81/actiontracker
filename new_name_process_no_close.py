"""
New Name Registration Process - Without Closing Action Tracker
이름이 없는 경우 등록 프로세스 - Action Tracker 닫지 않음
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# Coordinates
SUB_NAME_FIELD = (785, 291)    # Sub screen name field
COMPLETE_BUTTON = (1720, 139)  # Complete button (CLOSES Action Tracker!)

# Player coordinates on main screen
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

def register_new_name_without_closing(player_num, new_name):
    """
    Register new name WITHOUT closing Action Tracker
    
    Process for empty name slot:
    1. Click player on main screen
    2. Click name field on sub screen
    3. Type new name directly (no clear needed)
    4. Press Enter to save
    5. Press ESC to close sub screen (instead of complete button)
    """
    
    print(f"\n{'='*60}")
    print(f"PLAYER {player_num} - NEW NAME REGISTRATION")
    print(f"{'='*60}")
    
    if player_num not in PLAYERS:
        print(f"Invalid player number: {player_num}")
        return False
    
    player_coords = PLAYERS[player_num]
    
    print(f"Registering Player {player_num} as: {new_name}")
    print(f"Player coordinates: {player_coords}")
    print()
    
    try:
        # Step 1: Click player on main screen
        print(f"[Step 1] Click Player {player_num} on main screen")
        pyautogui.click(player_coords[0], player_coords[1])
        time.sleep(1)  # Wait for sub screen
        
        # Step 2: Click name field
        print(f"[Step 2] Click name field: {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(0.5)
        
        # Step 3: Type new name (no clear needed for empty field)
        print(f"[Step 3] Type new name: {new_name}")
        pyautogui.typewrite(new_name, interval=0.02)
        time.sleep(0.3)
        
        # Step 4: Press Enter to save
        print("[Step 4] Press Enter to save")
        pyautogui.press('enter')
        time.sleep(0.5)
        
        # Step 5: Press ESC to close sub screen (NOT complete button!)
        print("[Step 5] Press ESC to close sub screen (keeps Action Tracker open)")
        pyautogui.press('esc')
        time.sleep(0.5)
        
        print(f"✓ Player {player_num} registered as '{new_name}'")
        print("✓ Action Tracker remains open")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def register_multiple_new_names():
    """Register multiple players with new names"""
    
    print("="*60)
    print("MULTIPLE PLAYER REGISTRATION")
    print("Process: Register without closing Action Tracker")
    print("="*60)
    
    # Example: Register players 2-5
    new_players = {
        2: "Phil Ivey",
        3: "Doyle Brunson",
        4: "Tom Dwan",
        5: "Phil Hellmuth"
    }
    
    print("\nPlayers to register:")
    for num, name in new_players.items():
        print(f"  Player {num}: {name}")
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    # Take before screenshot
    before = pyautogui.screenshot()
    before.save("multi_before.png")
    
    # Register each player
    success_count = 0
    for player_num, name in new_players.items():
        if register_new_name_without_closing(player_num, name):
            success_count += 1
        time.sleep(0.5)  # Brief pause between players
    
    # Take after screenshot
    after = pyautogui.screenshot()
    timestamp = datetime.now().strftime("%H%M%S")
    after_file = f"multi_after_{timestamp}.png"
    after.save(after_file)
    
    print("\n" + "="*60)
    print("REGISTRATION COMPLETE")
    print("="*60)
    print(f"Success: {success_count}/{len(new_players)} players")
    print(f"Screenshot: {after_file}")
    print("Action Tracker should still be open!")
    print("="*60)

if __name__ == "__main__":
    print("NEW NAME REGISTRATION PROCESS")
    print("This will NOT close Action Tracker")
    print()
    print("Options:")
    print("1. Register single player")
    print("2. Register multiple players (2-5)")
    print()
    
    choice = input("Select (1-2): ").strip()
    
    if choice == "1":
        player = int(input("Player number (1-10): "))
        name = input("New name: ").strip()
        
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        register_new_name_without_closing(player, name)
        
    elif choice == "2":
        register_multiple_new_names()
    
    else:
        print("Invalid choice")