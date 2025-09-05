"""
Update Action Tracker with CORRECT button positions
Based on actual screenshot analysis
"""

import pyautogui
import time
import random

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# CORRECT button positions from screenshot analysis
PLAYER_NAME_POSITIONS = [
    (150, 260),  # player1
    (270, 260),  # player2
    (390, 260),  # player3
    (510, 260),  # player4
    (630, 260),  # player5
    (750, 260),  # player6
]

PLAYER_CHIP_POSITIONS = [
    (150, 450),  # player1 chips (10,000 button)
    (270, 450),  # player2 chips
    (390, 450),  # player3 chips
    (510, 450),  # player4 chips
    (630, 450),  # player5 chips
    (750, 450),  # player6 chips
]

def update_all_players():
    print("\n" + "="*70)
    print(" ACTION TRACKER - CORRECT POSITIONS UPDATE")
    print("="*70)
    
    # Generate random poker players
    poker_pros = [
        "Phil Ivey", "Daniel Negreanu", "Doyle Brunson", "Phil Hellmuth",
        "Vanessa Selbst", "Antonio Esfandiari", "Tom Dwan", "Viktor Blom",
        "Patrik Antonius", "Doug Polk", "Dan Smith", "Fedor Holz",
        "Jason Koon", "Bryn Kenney", "Stephen Chidwick", "David Peters"
    ]
    
    # Select 6 random players
    selected_players = random.sample(poker_pros, 6)
    players = []
    for name in selected_players:
        players.append({
            "name": name,
            "chips": random.randint(50000, 500000)
        })
    
    # Take before screenshot
    print("\n[1] Taking before screenshot...")
    before = pyautogui.screenshot()
    before.save("before_correct_update.png")
    
    # Display update plan
    print("\n[2] Players to update:")
    print("-" * 50)
    for i, p in enumerate(players):
        print(f"    Player {i+1}: {p['name']} - {p['chips']:,} chips")
    print("-" * 50)
    
    print("\n[3] Starting in 3 seconds...")
    print("    (Move mouse to top-left corner to abort)")
    for i in range(3, 0, -1):
        print(f"    {i}...")
        time.sleep(1)
    
    # Update each player
    print("\n[4] Updating players...")
    print("=" * 50)
    
    for i, player in enumerate(players):
        try:
            print(f"\nPlayer {i+1}: {player['name']}")
            
            # Step 1: Click on player NAME button
            name_x, name_y = PLAYER_NAME_POSITIONS[i]
            print(f"  - Clicking name button at ({name_x}, {name_y})")
            pyautogui.click(name_x, name_y)
            time.sleep(0.3)
            
            # Clear and type name
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.write(player['name'])
            time.sleep(0.2)
            
            # Step 2: Click on player CHIP button
            chip_x, chip_y = PLAYER_CHIP_POSITIONS[i]
            print(f"  - Clicking chip button at ({chip_x}, {chip_y})")
            pyautogui.click(chip_x, chip_y)
            time.sleep(0.3)
            
            # Clear and type chips
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.write(str(player['chips']))
            time.sleep(0.2)
            
            # Press Enter or Tab to confirm
            pyautogui.press('enter')
            time.sleep(0.3)
            
            print(f"  [OK] Updated: {player['name']} with {player['chips']:,} chips")
            
        except Exception as e:
            print(f"  [ERROR] Failed to update player {i+1}: {e}")
    
    # Take after screenshot
    print("\n[5] Taking after screenshot...")
    time.sleep(1)  # Wait a moment for UI to update
    after = pyautogui.screenshot()
    after.save("after_correct_update.png")
    
    # Summary
    print("\n" + "="*70)
    print(" UPDATE COMPLETE")
    print("="*70)
    
    total_chips = sum(p['chips'] for p in players)
    print(f"\nTotal chips in play: {total_chips:,}")
    
    print("\nScreenshots saved:")
    print("  - before_correct_update.png")
    print("  - after_correct_update.png")
    
    print("\nPlease check the screenshots to verify the update!")
    print("="*70)

if __name__ == "__main__":
    update_all_players()