"""
Action Tracker Automation Test Runner (English Version)
"""

import json
import csv
import time
import pyautogui
from datetime import datetime
import os

def load_test_data():
    """Load test data"""
    try:
        # Load from JSON
        with open('test_players_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"[OK] JSON data loaded: {len(data['players'])} players")
            return data['players']
    except:
        print("[ERROR] JSON load failed, trying CSV...")
        
        # Load from CSV
        try:
            players = []
            with open('test_players.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    players.append({
                        'num': int(row['player_num']),
                        'name': row['name'],
                        'chips': int(row['chips'])
                    })
            print(f"[OK] CSV data loaded: {len(players)} players")
            return players
        except Exception as e:
            print(f"[ERROR] Data load failed: {e}")
            return []

def test_coordinates():
    """Test coordinates without clicking"""
    print("\n" + "="*60)
    print("COORDINATE TEST MODE - Position check only (no clicks)")
    print("="*60)
    
    # Test coordinates
    coordinates = [
        (215, 354),   # Player 1
        (386, 364),   # Player 2
        (560, 485),   # Player 3
        (559, 486),   # Player 4
        (557, 364),   # Player 5
        (721, 362),   # Player 6
        (737, 369),   # Player 7
        (890, 369),   # Player 8
        (860, 364),   # Player 9
        (1037, 357),  # Player 10
    ]
    
    players = load_test_data()
    
    if not players:
        print("No test data available!")
        return
    
    screen_width, screen_height = pyautogui.size()
    print(f"\nScreen resolution: {screen_width}x{screen_height}")
    print("Starting in 3 seconds...\n")
    time.sleep(3)
    
    for player in players[:10]:  # Max 10 players
        player_num = player['num']
        player_name = player['name']
        player_chips = player['chips']
        
        if player_num <= 10:
            x, y = coordinates[player_num - 1]
            
            print(f"Player {player_num}: {player_name}")
            print(f"  - Chips: {player_chips:,}")
            print(f"  - Coordinates: ({x}, {y})")
            print(f"  - Moving mouse...")
            
            # Move mouse only (no click)
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.5)
            
    print("\n[COMPLETE] Coordinate test finished!")

def simulate_input():
    """Input simulation (logic only, no actual clicks)"""
    print("\n" + "="*60)
    print("INPUT SIMULATION MODE - Logic execution only")
    print("="*60)
    
    players = load_test_data()
    
    if not players:
        print("No test data available!")
        return
    
    print(f"\nProcessing {len(players)} players (simulation)")
    print("-" * 40)
    
    start_time = time.time()
    
    for i, player in enumerate(players, 1):
        print(f"\n[{i}/{len(players)}] Processing: {player['name']}")
        print(f"  1. Move to Player {player['num']} position")
        print(f"  2. Double-click to enter edit mode")
        print(f"  3. Enter name: {player['name']}")
        print(f"  4. Enter chips: {player['chips']:,}")
        print(f"  5. Press Enter to confirm")
        
        # Simulation delay
        time.sleep(0.2)
    
    elapsed = time.time() - start_time
    print(f"\n[COMPLETE] Simulation finished!")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Average per player: {elapsed/len(players):.2f} seconds")

def show_info():
    """Display system and data information"""
    print("\n" + "="*60)
    print("ACTION TRACKER AUTOMATION TEST INFORMATION")
    print("="*60)
    
    print("\nSYSTEM INFO:")
    width, height = pyautogui.size()
    x, y = pyautogui.position()
    print(f"  - Screen resolution: {width}x{height}")
    print(f"  - Current mouse position: ({x}, {y})")
    print(f"  - Failsafe mode: {pyautogui.FAILSAFE}")
    print(f"  - Pause between actions: {pyautogui.PAUSE} seconds")
    
    players = load_test_data()
    if players:
        print(f"\nTEST DATA:")
        print(f"  - Total players: {len(players)}")
        total_chips = sum(p['chips'] for p in players)
        print(f"  - Total chips: {total_chips:,}")
        print(f"  - Average chips: {total_chips//len(players):,}")
        
        print(f"\nPLAYER LIST:")
        for p in players[:5]:  # Show first 5
            print(f"  {p['num']}. {p['name']}: {p['chips']:,} chips")
        if len(players) > 5:
            print(f"  ... and {len(players)-5} more players")

def demo_automation():
    """Demonstration of automation logic"""
    print("\n" + "="*60)
    print("AUTOMATION DEMONSTRATION")
    print("="*60)
    
    print("\nThis demonstrates the automation logic:")
    print("1. Find Action Tracker window")
    print("2. Load player data from JSON/CSV")
    print("3. For each player:")
    print("   - Click on player position")
    print("   - Open edit dialog")
    print("   - Clear existing data")
    print("   - Enter new name and chips")
    print("   - Confirm and save")
    print("4. Log results and statistics")
    
    print("\nKEY FEATURES:")
    print("- Coordinate-based clicking system")
    print("- Automatic error recovery")
    print("- Progress tracking and logging")
    print("- Multiple input modes (test/simulation/real)")
    print("- Emergency stop with ESC key")

def main_menu():
    """Main menu"""
    while True:
        print("\n" + "="*60)
        print("ACTION TRACKER AUTOMATION TEST SYSTEM")
        print("="*60)
        print("\nSelect an option:")
        print("1. Show Information")
        print("2. Test Coordinates (mouse movement only)")
        print("3. Simulate Input (logic only)")
        print("4. Automation Demo (explanation)")
        print("5. Exit")
        print("-" * 40)
        
        choice = input("Choice (1-5): ")
        
        if choice == '1':
            show_info()
        elif choice == '2':
            test_coordinates()
        elif choice == '3':
            simulate_input()
        elif choice == '4':
            demo_automation()
        elif choice == '5':
            print("\nExiting program.")
            break
        else:
            print("\n[ERROR] Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("=" * 60)
    print("ACTION TRACKER AUTOMATION TEST SYSTEM")
    print("=" * 60)
    print("\nNOTE: Press ESC key to stop automation at any time")
    
    # Safety settings
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
    
    # Check if data files exist
    if not os.path.exists('test_players_data.json') and not os.path.exists('test_players.csv'):
        print("\n[WARNING] No test data files found!")
        print("Creating sample data...")
        
        # Create sample JSON data
        sample_data = {
            "players": [
                {"num": 1, "name": "Player 1", "chips": 1000000},
                {"num": 2, "name": "Player 2", "chips": 1500000},
                {"num": 3, "name": "Player 3", "chips": 2000000}
            ]
        }
        
        with open('test_players_data.json', 'w') as f:
            json.dump(sample_data, f, indent=2)
        print("[OK] Sample data created: test_players_data.json")
    
    main_menu()