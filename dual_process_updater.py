"""
Dual Process Name Updater
Handles both existing and new player names with different update processes
"""

import pyautogui
import time
from datetime import datetime

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# Player coordinates
PLAYER_COORDS = {
    1: (215, 354),
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

# Known existing names in the system (for testing)
EXISTING_NAMES = [
    "Johnny Chan",
    "Chris Ferguson", 
    "Stu Ungar",
    "Vanessa Selbst",
    "Jason Koon",
    "Mike",
    "Alice",
    "Bob"
]

def update_existing_name_process(player_num, new_name):
    """
    Process for EXISTING names (이름이 이미 존재하는 경우):
    1. Click player name
    2. Click dropdown selection
    3. Modify text
    4. Press Enter
    5. Click confirmation
    """
    print(f"\n[EXISTING NAME PROCESS] Player {player_num} → {new_name}")
    print("Steps: Click → Select → Modify → Enter → Confirm")
    
    x, y = PLAYER_COORDS[player_num]
    
    # Step 1: Click player name
    print(f"  1. Click player at ({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(0.3)
    
    # Step 2: Double-click to open edit
    print(f"  2. Double-click to open edit mode")
    pyautogui.doubleClick()
    time.sleep(0.5)
    
    # Step 3: Click dropdown selection (click below for dropdown item)
    print(f"  3. Click dropdown selection")
    pyautogui.click(x, y + 25)  # Click slightly below for dropdown
    time.sleep(0.3)
    
    # Step 4: Clear and enter new text
    print(f"  4. Clear and type: {new_name}")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.2)
    
    # Step 5: Press Enter
    print(f"  5. Press Enter")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    # Step 6: Click confirmation (click away or confirm button)
    print(f"  6. Click confirmation")
    pyautogui.click(x + 150, y)  # Click away to confirm
    time.sleep(0.3)
    
    print(f"  ✓ Completed (Existing Name Process)")

def update_new_name_process(player_num, new_name):
    """
    Process for NEW names (이름이 등록되지 않은 경우):
    1. Click player name
    2. Modify text
    3. Press Enter
    """
    print(f"\n[NEW NAME PROCESS] Player {player_num} → {new_name}")
    print("Steps: Click → Modify → Enter")
    
    x, y = PLAYER_COORDS[player_num]
    
    # Step 1: Click player name
    print(f"  1. Click player at ({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(0.3)
    
    # Step 2: Double-click to edit
    print(f"  2. Double-click to edit")
    pyautogui.doubleClick()
    time.sleep(0.5)
    
    # Step 3: Clear and type new name
    print(f"  3. Clear and type: {new_name}")
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.typewrite(new_name, interval=0.02)
    time.sleep(0.2)
    
    # Step 4: Press Enter
    print(f"  4. Press Enter")
    pyautogui.press('enter')
    time.sleep(0.3)
    
    print(f"  ✓ Completed (New Name Process)")

def is_existing_name(name):
    """Check if name exists in the system (simulation)"""
    # In real implementation, this would detect dropdown
    # For now, we simulate with a known list
    return any(existing in name for existing in EXISTING_NAMES)

def smart_update_player(player_num, new_name):
    """Automatically choose correct process based on name"""
    if is_existing_name(new_name):
        update_existing_name_process(player_num, new_name)
    else:
        update_new_name_process(player_num, new_name)

def update_all_players_mixed():
    """Update all 10 players with mixed existing/new names"""
    print("="*60)
    print("DUAL PROCESS UPDATE - ALL 10 PLAYERS")
    print("="*60)
    
    # Mix of existing and new names
    updates = {
        1: "Johnny Chan",      # Existing
        2: "NewPlayer001",     # New
        3: "Mike",            # Existing
        4: "TestPlayer123",   # New
        5: "Alice",           # Existing
        6: "RandomName456",   # New
        7: "Bob",             # Existing
        8: "UniquePlayer789", # New
        9: "Chris Ferguson",  # Existing
        10: "FinalPlayer999"  # New
    }
    
    print("\nPlayer Updates:")
    for num, name in updates.items():
        status = "EXISTING" if is_existing_name(name) else "NEW"
        print(f"  Player {num:2}: {name:20} [{status}]")
    
    confirm = input("\nStart update? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    start_time = time.time()
    
    for player_num, new_name in updates.items():
        try:
            smart_update_player(player_num, new_name)
        except Exception as e:
            print(f"Error updating player {player_num}: {e}")
    
    elapsed = time.time() - start_time
    
    print("\n" + "="*60)
    print(f"COMPLETE! Time: {elapsed:.1f} seconds")
    print("="*60)
    
    # Screenshot
    screenshot = pyautogui.screenshot()
    filename = f"dual_process_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot.save(filename)
    print(f"Screenshot: {filename}")

def manual_test():
    """Manual test for specific process"""
    print("MANUAL PROCESS TEST")
    print("="*40)
    print("\nSelect process type:")
    print("1. Existing Name Process (dropdown + confirm)")
    print("2. New Name Process (simple)")
    print("3. Auto-detect (smart)")
    
    choice = input("Choice (1-3): ").strip()
    
    if choice not in ['1', '2', '3']:
        print("Invalid choice")
        return
    
    player_num = int(input("Player number (1-10): "))
    if player_num not in PLAYER_COORDS:
        print("Invalid player number")
        return
    
    new_name = input("New name: ").strip()
    
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    if choice == '1':
        update_existing_name_process(player_num, new_name)
    elif choice == '2':
        update_new_name_process(player_num, new_name)
    else:
        smart_update_player(player_num, new_name)
    
    print("\nComplete!")

def main():
    print("DUAL PROCESS NAME UPDATER")
    print("="*40)
    print("\nThis handles both:")
    print("• Existing names (dropdown process)")
    print("• New names (simple process)")
    print("\nOptions:")
    print("1. Update all 10 players (mixed)")
    print("2. Manual test single player")
    print("3. Quick test Player 1")
    
    choice = input("\nSelect (1-3): ").strip()
    
    if choice == '1':
        update_all_players_mixed()
    elif choice == '2':
        manual_test()
    elif choice == '3':
        print("\nQuick test on Player 1")
        print("Starting in 3 seconds...")
        time.sleep(3)
        
        # Test with existing name
        print("\nTest 1: Existing name")
        update_existing_name_process(1, "Mike")
        
        time.sleep(2)
        
        # Test with new name
        print("\nTest 2: New name")
        update_new_name_process(1, "TestPlayer2024")
        
        print("\nTests complete!")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()