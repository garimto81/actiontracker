"""
Automatic Bulk Update for Action Tracker
Updates all 6 players with random names and chips
"""

import pyautogui
import time
import random
from datetime import datetime

# Player positions in Action Tracker
PLAYER_POSITIONS = {
    1: {"x": 320, "y": 400},
    2: {"x": 960, "y": 200},
    3: {"x": 1400, "y": 400},
    4: {"x": 1400, "y": 800},
    5: {"x": 860, "y": 950},
    6: {"x": 320, "y": 800}
}

# Random player names pool
PLAYER_NAMES = [
    "Daniel Negreanu", "Phil Ivey", "Doyle Brunson", "Phil Hellmuth",
    "Vanessa Selbst", "Antonio Esfandiari", "Tom Dwan", "Viktor Blom",
    "Patrik Antonius", "Doug Polk", "Dan Smith", "Fedor Holz",
    "Jason Koon", "Bryn Kenney", "Stephen Chidwick", "David Peters",
    "Michael Addamo", "Justin Bonomo", "Steve O'Dwyer", "Sam Greenwood",
    "Mikita Badziakouski", "Timothy Adams", "Seth Davies", "Ali Imsirovic",
    "Mustapha Kanit", "Rainer Kempe", "Igor Kurganov", "Charlie Carrel"
]

def activate_action_tracker():
    """Try to activate Action Tracker window"""
    try:
        windows = pyautogui.getAllWindows()
        for window in windows:
            if "action tracker" in window.title.lower():
                window.activate()
                time.sleep(0.5)
                print("[OK] Action Tracker window activated")
                return True
    except Exception as e:
        print(f"[Info] Could not auto-activate window: {e}")
    return False

def update_player(seat, name, chips):
    """Update single player in Action Tracker"""
    try:
        pos = PLAYER_POSITIONS[seat]
        
        print(f"Updating Seat {seat}: {name} ({chips:,} chips)")
        
        # Click on player position
        pyautogui.click(pos["x"], pos["y"])
        time.sleep(0.3)
        
        # Move to name field (Tab key)
        pyautogui.press('tab')
        time.sleep(0.2)
        
        # Select all and delete existing text
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        
        # Type new name
        pyautogui.write(name)
        time.sleep(0.2)
        
        # Move to chip field
        pyautogui.press('tab')
        time.sleep(0.2)
        
        # Select all and delete existing text
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        
        # Type new chip count
        pyautogui.write(str(chips))
        time.sleep(0.2)
        
        # Confirm with Enter
        pyautogui.press('enter')
        time.sleep(0.3)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to update seat {seat}: {e}")
        return False

def main():
    print("\n" + "="*60)
    print(" AUTOMATIC BULK UPDATE - ACTION TRACKER")
    print("="*60)
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Activate Action Tracker
    if not activate_action_tracker():
        print("\n[Warning] Please make sure Action Tracker is running")
        print("[Info] Continuing anyway in 3 seconds...")
        time.sleep(3)
    
    # Generate random players
    selected_names = random.sample(PLAYER_NAMES, 6)
    players = []
    
    print("\n[Players to Update]")
    print("-" * 40)
    
    for i in range(6):
        player = {
            'seat': i + 1,
            'name': selected_names[i],
            'chips': random.randint(50000, 500000)
        }
        players.append(player)
        print(f"  Seat {player['seat']}: {player['name']}")
        print(f"         Chips: {player['chips']:,}")
    
    print("-" * 40)
    
    # Countdown
    print("\n[Starting in 5 seconds...]")
    print("[Move mouse to top-left corner to abort]")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    # Take screenshot before
    print("\n[Taking screenshot: before_update.png]")
    before_shot = pyautogui.screenshot()
    before_shot.save("before_update.png")
    
    # Update all players
    print("\n[Updating Players...]")
    print("="*40)
    
    success_count = 0
    for player in players:
        if update_player(player['seat'], player['name'], player['chips']):
            success_count += 1
            print(f"  [OK] Seat {player['seat']} updated successfully")
        else:
            print(f"  [FAIL] Seat {player['seat']} update failed")
        time.sleep(0.5)
    
    # Take screenshot after
    print("\n[Taking screenshot: after_update.png]")
    after_shot = pyautogui.screenshot()
    after_shot.save("after_update.png")
    
    # Summary
    print("\n" + "="*60)
    print(f" UPDATE COMPLETE: {success_count}/6 players updated")
    print("="*60)
    print("\n[Screenshots saved:]")
    print("  - before_update.png")
    print("  - after_update.png")
    
    # Show final player list
    print("\n[Final Player List]")
    print("-" * 40)
    total_chips = 0
    for p in players:
        print(f"  Seat {p['seat']}: {p['name']}")
        print(f"         Chips: {p['chips']:,}")
        total_chips += p['chips']
    print("-" * 40)
    print(f"  Total Chips in Play: {total_chips:,}")
    print("="*60)

if __name__ == "__main__":
    # Set safety features
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n[ABORTED] User cancelled operation")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")