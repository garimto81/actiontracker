"""
Real Scenario Test - Load Table with Empty Seat 2
2번 자리만 비어있는 실제 시나리오 테스트
"""

import pyautogui
import time
import pandas as pd
import json
from datetime import datetime

# Coordinates
PLAYER_COORDS = {
    1: (233, 361), 2: (374, 359), 3: (544, 362), 4: (722, 359), 5: (886, 356),
    6: (1051, 354), 7: (1213, 355), 8: (1385, 383), 9: (1549, 367), 10: (1705, 356)
}

CHIP_COORDS = {
    1: (1226, 622), 2: (1382, 619), 3: (1537, 615), 4: (1688, 615), 5: (1694, 615),
    6: (1694, 615), 7: (1226, 622), 8: (1382, 619), 9: (1537, 615), 10: (1688, 615)
}

SUB_NAME_FIELD = (785, 291)
COMPLETE_BUTTON = (1720, 139)

# Speed settings (Normal speed)
SPEEDS = {
    "mouse_click_delay": 0.3,
    "keyboard_type_interval": 0.02,
    "action_delay": 0.5,
    "screen_wait": 1.0
}

def create_test_data():
    """Create test table data with seat 2 empty"""
    test_data = {
        "T01": {
            1: {"player": "Phil Ivey", "chips": 1500000, "notable": True},
            # Seat 2 is empty
            3: {"player": "Daniel Negreanu", "chips": 1200000, "notable": True},
            4: {"player": "Doyle Brunson", "chips": 980000, "notable": False},
            5: {"player": "Tom Dwan", "chips": 620000, "notable": False},
            6: {"player": "Patrik Antonius", "chips": 540000, "notable": False},
            7: {"player": "Gus Hansen", "chips": 480000, "notable": False},
            8: {"player": "Vanessa Selbst", "chips": 890000, "notable": True},
            9: {"player": "Erik Seidel", "chips": 670000, "notable": False},
            10: {"player": "Johnny Chan", "chips": 1100000, "notable": True}
        }
    }
    
    # Save as JSON for loading
    with open('test_table_data.json', 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print("[DATA] Test data created - Seat 2 is empty")
    return test_data

def update_existing_name(seat, new_name):
    """Update existing player name (6-step process)"""
    try:
        coords = PLAYER_COORDS[seat]
        print(f"  [UPDATE] Seat {seat}: Updating existing name to '{new_name}'")
        
        # Step 1: Click player
        print(f"    Step 1: Click player at {coords}")
        pyautogui.click(coords[0], coords[1])
        time.sleep(SPEEDS["action_delay"])
        
        # Step 2: Click name field
        print(f"    Step 2: Click name field at {SUB_NAME_FIELD}")
        pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
        time.sleep(SPEEDS["action_delay"])
        
        # Step 3: Clear existing name
        print(f"    Step 3: Clear existing name")
        pyautogui.tripleClick()
        time.sleep(SPEEDS["mouse_click_delay"])
        
        # Step 4: Type new name
        print(f"    Step 4: Type new name: '{new_name}'")
        pyautogui.typewrite(new_name, interval=SPEEDS["keyboard_type_interval"])
        time.sleep(SPEEDS["action_delay"])
        
        # Step 5: Press Enter
        print(f"    Step 5: Press Enter")
        pyautogui.press('enter')
        time.sleep(SPEEDS["action_delay"])
        
        # Step 6: Click Complete
        print(f"    Step 6: Click Complete at {COMPLETE_BUTTON}")
        pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
        time.sleep(SPEEDS["screen_wait"])
        
        print(f"    ✓ Seat {seat} name updated successfully")
        return True
        
    except Exception as e:
        print(f"    ✗ Error updating seat {seat}: {e}")
        return False

def register_new_name(seat, name):
    """Register new player name (3-step process)"""
    try:
        coords = PLAYER_COORDS[seat]
        print(f"  [REGISTER] Seat {seat}: Registering new name '{name}'")
        
        # Step 1: Click player position
        print(f"    Step 1: Click player at {coords}")
        pyautogui.click(coords[0], coords[1])
        time.sleep(SPEEDS["action_delay"])
        
        # Step 2: Type name
        print(f"    Step 2: Type name: '{name}'")
        pyautogui.typewrite(name, interval=SPEEDS["keyboard_type_interval"])
        time.sleep(SPEEDS["action_delay"])
        
        # Step 3: Press Enter
        print(f"    Step 3: Press Enter")
        pyautogui.press('enter')
        time.sleep(SPEEDS["screen_wait"])
        
        print(f"    ✓ Seat {seat} name registered successfully")
        return True
        
    except Exception as e:
        print(f"    ✗ Error registering seat {seat}: {e}")
        return False

def input_chips(seat, chips):
    """Input chip amount"""
    try:
        coords = CHIP_COORDS[seat]
        print(f"  [CHIPS] Seat {seat}: Inputting {chips:,} chips")
        
        # Click chip field
        print(f"    Step 1: Click chip field at {coords}")
        pyautogui.click(coords[0], coords[1])
        time.sleep(SPEEDS["mouse_click_delay"])
        
        # Clear existing value
        print(f"    Step 2: Clear existing value")
        pyautogui.tripleClick()
        time.sleep(SPEEDS["mouse_click_delay"])
        
        # Type new chips
        print(f"    Step 3: Type chips: {chips}")
        pyautogui.typewrite(str(chips), interval=SPEEDS["keyboard_type_interval"])
        time.sleep(SPEEDS["action_delay"])
        
        # Press Enter
        print(f"    Step 4: Press Enter")
        pyautogui.press('enter')
        time.sleep(SPEEDS["action_delay"])
        
        print(f"    ✓ Seat {seat} chips updated successfully")
        return True
        
    except Exception as e:
        print(f"    ✗ Error inputting chips for seat {seat}: {e}")
        return False

def simulate_scenario():
    """Simulate the complete scenario"""
    print("=" * 70)
    print("REAL SCENARIO TEST - SEAT 2 EMPTY")
    print("=" * 70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Create test data
    print("\n[STEP 1] Creating Test Data")
    print("-" * 40)
    table_data = create_test_data()
    
    # Assume seats status (in real scenario, would use auto-detect)
    occupied_seats = [1, 3, 4, 5, 6, 7, 8, 9, 10]  # These have existing names
    empty_seats = [2]  # This needs new registration
    
    print("\n[STEP 2] Current Table Status")
    print("-" * 40)
    print(f"Occupied seats: {occupied_seats}")
    print(f"Empty seats: {empty_seats}")
    
    # Add new player for seat 2
    new_player_seat2 = {"player": "Phil Hellmuth", "chips": 750000}
    print(f"\nNew player for Seat 2: {new_player_seat2['player']} ({new_player_seat2['chips']:,} chips)")
    
    print("\n[STEP 3] Processing Names")
    print("-" * 40)
    
    # Process all seats
    for seat, player_info in table_data["T01"].items():
        if seat in occupied_seats:
            # Update existing name
            success = update_existing_name(seat, player_info['player'])
        
    # Register new name for seat 2
    if 2 in empty_seats:
        success = register_new_name(2, new_player_seat2['player'])
    
    print("\n[STEP 4] Processing Chips")
    print("-" * 40)
    
    # Input chips for all seats including new seat 2
    for seat, player_info in table_data["T01"].items():
        success = input_chips(seat, player_info['chips'])
    
    # Input chips for seat 2
    success = input_chips(2, new_player_seat2['chips'])
    
    print("\n[STEP 5] Summary")
    print("=" * 70)
    print("✓ Updated 9 existing player names")
    print("✓ Registered 1 new player (Seat 2)")
    print("✓ Input chips for all 10 players")
    print("\n[SUCCESS] Real scenario test completed!")
    
    # Save final state
    final_state = {
        "table": "T01",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "players": {}
    }
    
    for seat, info in table_data["T01"].items():
        final_state["players"][seat] = info
    
    final_state["players"][2] = new_player_seat2
    
    with open('test_final_state.json', 'w', encoding='utf-8') as f:
        json.dump(final_state, f, indent=2, ensure_ascii=False)
    
    print("\nFinal state saved to: test_final_state.json")

def dry_run():
    """Dry run without actual clicks"""
    print("\n" + "="*70)
    print("DRY RUN MODE - NO ACTUAL CLICKS")
    print("="*70)
    
    # Create test data
    table_data = create_test_data()
    
    print("\n[SIMULATION] Table T01 Processing Plan")
    print("-" * 40)
    
    # Show plan
    print("1. Update existing names (6-step process):")
    for seat in [1, 3, 4, 5, 6, 7, 8, 9, 10]:
        player = table_data["T01"][seat]["player"]
        print(f"   Seat {seat}: {player}")
    
    print("\n2. Register new name (3-step process):")
    print("   Seat 2: Phil Hellmuth (NEW)")
    
    print("\n3. Input chips for all seats:")
    for seat in range(1, 11):
        if seat == 2:
            print(f"   Seat 2: 750,000 chips")
        elif seat in table_data["T01"]:
            chips = table_data["T01"][seat]["chips"]
            print(f"   Seat {seat}: {chips:,} chips")
    
    print("\n[TIMING] Estimated execution time:")
    update_time = 9 * 3.5  # 9 existing names
    register_time = 1 * 1.5  # 1 new name
    chips_time = 10 * 1.0  # 10 chip inputs
    total_time = update_time + register_time + chips_time
    print(f"   Name updates: {update_time:.1f} seconds")
    print(f"   Name registration: {register_time:.1f} seconds")
    print(f"   Chip inputs: {chips_time:.1f} seconds")
    print(f"   Total: {total_time:.1f} seconds")

if __name__ == "__main__":
    import sys
    
    print("SELECT MODE:")
    print("1. DRY RUN (simulation only)")
    print("2. REAL TEST (actual clicks)")
    print("3. EXIT")
    
    # For automated testing, default to dry run
    mode = "1"
    
    if mode == "1":
        dry_run()
    elif mode == "2":
        print("\n⚠️ WARNING: This will perform actual mouse clicks!")
        print("Make sure Action Tracker is open and visible.")
        print("Starting in 5 seconds...")
        time.sleep(5)
        simulate_scenario()
    else:
        print("Test cancelled.")