"""
Direct update of Action Tracker players - simplified version
"""

import pyautogui
import time
import random

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def update_all_players():
    print("\n" + "="*60)
    print(" ACTION TRACKER - PLAYER UPDATE")
    print("="*60)
    
    # Generate random player data
    players = [
        {"name": "Tom Dwan", "chips": random.randint(100000, 500000)},
        {"name": "Phil Ivey", "chips": random.randint(100000, 500000)},
        {"name": "Daniel Negreanu", "chips": random.randint(100000, 500000)},
        {"name": "Vanessa Selbst", "chips": random.randint(100000, 500000)},
        {"name": "Phil Hellmuth", "chips": random.randint(100000, 500000)},
        {"name": "Antonio Esfandiari", "chips": random.randint(100000, 500000)}
    ]
    
    # Player button positions (from previous analysis)
    positions = [
        (150, 260),  # Mike/Player 1
        (275, 260),  # Hunter/Player 2
        (390, 260),  # Jayden/Player 3
        (510, 260),  # JUN/Player 4
        (635, 260),  # Richie/Player 5
        (755, 260),  # Ray/Player 6
    ]
    
    print("\nPlayers to update:")
    for i, p in enumerate(players):
        print(f"  Seat {i+1}: {p['name']} - {p['chips']:,} chips")
    
    print("\nStarting update in 3 seconds...")
    print("Move mouse to top-left corner to abort")
    time.sleep(3)
    
    # Close any open dialogs first
    print("\nClosing any open dialogs...")
    pyautogui.press('escape')
    time.sleep(0.5)
    pyautogui.press('escape')
    time.sleep(0.5)
    
    # Update each player
    for i, (player, pos) in enumerate(zip(players, positions)):
        print(f"\nUpdating Seat {i+1}: {player['name']}")
        
        try:
            # Click on player button
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.5)
            
            # Clear and type name
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(player['name'])
            time.sleep(0.3)
            
            # Tab to chip field
            pyautogui.press('tab')
            time.sleep(0.3)
            
            # Clear and type chips
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.write(str(player['chips']))
            time.sleep(0.3)
            
            # Confirm with Enter
            pyautogui.press('enter')
            time.sleep(0.5)
            
            print(f"  [OK] Updated: {player['name']} ({player['chips']:,})")
            
        except Exception as e:
            print(f"  [ERROR] Error updating seat {i+1}: {e}")
    
    # Take final screenshot
    print("\nTaking final screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save("players_updated.png")
    
    print("\n" + "="*60)
    print(" UPDATE COMPLETE")
    print("="*60)
    
    # Summary
    total = sum(p['chips'] for p in players)
    print(f"\nTotal chips in play: {total:,}")
    print("Screenshot saved: players_updated.png")

if __name__ == "__main__":
    update_all_players()