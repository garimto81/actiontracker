"""
Action Tracker Automation Script
Generated: 2025-09-04 17:56:27
Detected positions: 12 players

This script provides functions to automatically update Action Tracker
player names and chip stacks using the detected UI positions.
"""

import pyautogui
import time
import json
from datetime import datetime

# Detected player positions
PLAYER_POSITIONS = {
    1: {
        'name': (209, 658),
        'chips': (209, 788)  # Estimated position
    },
    2: {
        'name': (376, 658),
        'chips': (376, 788)  # Estimated position
    },
    3: {
        'name': (543, 658),
        'chips': (543, 788)  # Estimated position
    },
    4: {
        'name': (710, 658),
        'chips': (710, 788)  # Estimated position
    },
    5: {
        'name': (878, 658),
        'chips': (878, 788)  # Estimated position
    },
    6: {
        'name': (1045, 658),
        'chips': (1045, 788)  # Estimated position
    },
    7: {
        'name': (1212, 658),
        'chips': (1212, 788)  # Estimated position
    },
    8: {
        'name': (1379, 658),
        'chips': (1379, 788)  # Estimated position
    },
    9: {
        'name': (1546, 658),
        'chips': (1546, 788)  # Estimated position
    },
    10: {
        'name': (1713, 658),
        'chips': (1713, 788)  # Estimated position
    },
    11: {
        'name': (710, 1112),
        'chips': (710, 1242)  # Estimated position
    },
    12: {
        'name': (1392, 1116),
        'chips': (1392, 1246)  # Estimated position
    },
}}

def safe_click_and_type(x, y, text, click_delay=0.3, type_delay=0.1):
    """Safely click and type with error handling"""
    try:
        # Click at position
        pyautogui.click(x, y)
        time.sleep(click_delay)
        
        # Select all existing text
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(type_delay)
        
        # Type new text
        pyautogui.typewrite(str(text))
        time.sleep(type_delay)
        
        return True
    except Exception as e:
        print(f"Error clicking/typing at ({x}, {y}): {e}")
        return False

def update_player_name(player_num, name):
    """Update a specific player's name"""
    if player_num not in PLAYER_POSITIONS:
        print(f"Player {player_num} not found")
        return False
    
    pos = PLAYER_POSITIONS[player_num]['name']
    print(f"Updating Player {player_num} name to: {name}")
    return safe_click_and_type(pos[0], pos[1], name)

def update_player_chips(player_num, chips):
    """Update a specific player's chip stack"""
    if player_num not in PLAYER_POSITIONS:
        print(f"Player {player_num} not found")
        return False
    
    pos = PLAYER_POSITIONS[player_num]['chips']
    print(f"Updating Player {player_num} chips to: {chips}")
    return safe_click_and_type(pos[0], pos[1], chips)

def update_player(player_num, name=None, chips=None):
    """Update both name and chips for a player"""
    success = True
    
    if name is not None:
        if not update_player_name(player_num, name):
            success = False
    
    if chips is not None:
        if not update_player_chips(player_num, chips):
            success = False
    
    return success

def batch_update(player_data, delay_between_players=0.5):
    """Update multiple players from dictionary"""
    results = {{}}
    
    print(f"Starting batch update of {len(player_data)} players...")
    print("Make sure Action Tracker window is active!")
    
    for player_num, data in player_data.items():
        if player_num not in PLAYER_POSITIONS:
            print(f"Warning: Player {player_num} position not detected, skipping")
            results[player_num] = False
            continue
        
        name = data.get('name')
        chips = data.get('chips')
        
        success = update_player(player_num, name, chips)
        results[player_num] = success
        
        if success:
            print(f"✅ Player {player_num} updated successfully")
        else:
            print(f"❌ Player {player_num} update failed")
        
        time.sleep(delay_between_players)
    
    # Summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    print(f"\nBatch update complete: {successful}/{total} players updated successfully")
    
    return results

def test_positions():
    """Test all detected positions by clicking them"""
    print("Testing all detected positions...")
    print("This will click each player name and chip position")
    print("Make sure Action Tracker is active and visible!")
    print("Starting in 3 seconds... Press Ctrl+C to cancel")
    
    try:
        time.sleep(3)
        
        for player_num in PLAYER_POSITIONS:
            print(f"Testing Player {player_num} positions...")
            
            # Test name position
            name_pos = PLAYER_POSITIONS[player_num]['name']
            pyautogui.click(name_pos[0], name_pos[1])
            time.sleep(0.5)
            
            # Test chip position
            chip_pos = PLAYER_POSITIONS[player_num]['chips']
            pyautougui.click(chip_pos[0], chip_pos[1])
            time.sleep(0.5)
            
        print("Position testing complete!")
        
    except KeyboardInterrupt:
        print("\nPosition testing cancelled by user")
    except Exception as e:
        print(f"\nError during position testing: {e}")

def load_player_data_from_json(filename):
    """Load player data from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return {{}}

def save_update_log(results, filename=None):
    """Save update results to log file"""
    if filename is None:
        filename = f"update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    log_data = {{
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'successful_updates': sum(1 for success in results.values() if success),
        'total_attempts': len(results)
    }}
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        print(f"Update log saved to: {filename}")
    except Exception as e:
        print(f"Error saving log: {e}")

# Example usage and test data
EXAMPLE_PLAYERS = {{
    1: {{'name': 'Alice', 'chips': 15000}},
    2: {{'name': 'Bob', 'chips': 12500}},
    3: {{'name': 'Charlie', 'chips': 18000}},
    4: {{'name': 'Diana', 'chips': 9500}},
    5: {{'name': 'Eve', 'chips': 22000}},
    6: {{'name': 'Frank', 'chips': 11000}},
    7: {{'name': 'Grace', 'chips': 16500}},
    8: {{'name': 'Henry', 'chips': 13000}},
    9: {{'name': 'Ivy', 'chips': 19500}},
    10: {{'name': 'Jack', 'chips': 14000}}
}}

if __name__ == "__main__":
    print("Action Tracker Automation Script")
    print("================================")
    print(f"Detected {len(PLAYER_POSITIONS)} player positions")
    print()
    print("Available functions:")
    print("- update_player(num, name, chips)")
    print("- batch_update(player_data)")
    print("- test_positions()")
    print()
    
    # Example: Update first 3 players
    test_data = {{k: v for k, v in EXAMPLE_PLAYERS.items() if k <= 3}}
    
    print("Example usage:")
    print("batch_update(EXAMPLE_PLAYERS)")
    print()
    print("Running example update in 5 seconds...")
    print("Make sure Action Tracker is active!")
    
    try:
        time.sleep(5)
        results = batch_update(test_data)
        save_update_log(results)
    except KeyboardInterrupt:
        print("\nExample cancelled by user")
