"""
Update Action Tracker players - Full screen version
Adjusted coordinates for full screen mode
"""

import pyautogui
import time
import random

# Safety settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def update_players_fullscreen():
    print("\n" + "="*70)
    print(" ACTION TRACKER - FULL SCREEN UPDATE")
    print("="*70)
    
    # Generate 6 random players with poker pro names
    players = [
        {"name": "Doyle Brunson", "chips": random.randint(100000, 500000)},
        {"name": "Johnny Chan", "chips": random.randint(100000, 500000)},
        {"name": "Stu Ungar", "chips": random.randint(100000, 500000)},
        {"name": "Chris Moneymaker", "chips": random.randint(100000, 500000)},
        {"name": "Sam Farha", "chips": random.randint(100000, 500000)},
        {"name": "Gus Hansen", "chips": random.randint(100000, 500000)}
    ]
    
    # Take screenshot before update
    print("\n[1] Taking screenshot before update...")
    before = pyautogui.screenshot()
    before.save("before_fullscreen_update.png")
    print("    Saved: before_fullscreen_update.png")
    
    # Display players to update
    print("\n[2] Players to update:")
    print("-" * 50)
    for i, p in enumerate(players):
        print(f"    Seat {i+1}: {p['name']} - {p['chips']:,} chips")
    print("-" * 50)
    
    print("\n[3] Starting update in 3 seconds...")
    print("    (Move mouse to top-left corner to abort)")
    time.sleep(3)
    
    # For full screen, need to find the actual button positions
    # First, let's click on the main area to ensure focus
    print("\n[4] Ensuring Action Tracker has focus...")
    pyautogui.click(960, 540)  # Center of screen
    time.sleep(0.5)
    
    # Try to find and click player buttons
    # These coordinates need to be adjusted based on full screen resolution
    # Assuming 1920x1080 resolution
    
    print("\n[5] Looking for player buttons...")
    
    # Method 1: Try clicking on the first visible button area
    # Based on the original screenshot, buttons were in a row
    
    # Estimated positions for full screen (adjust based on your resolution)
    button_positions = [
        (300, 500),   # Player 1
        (500, 500),   # Player 2  
        (700, 500),   # Player 3
        (900, 500),   # Player 4
        (1100, 500),  # Player 5
        (1300, 500),  # Player 6
    ]
    
    print("\n[6] Attempting to update players...")
    
    for i, (player, pos) in enumerate(zip(players, button_positions)):
        try:
            print(f"\n    Updating Seat {i+1}: {player['name']}")
            
            # Click on player button position
            pyautogui.click(pos[0], pos[1])
            time.sleep(0.5)
            
            # Try double-click in case single click doesn't work
            pyautogui.doubleClick(pos[0], pos[1])
            time.sleep(0.5)
            
            # Clear and type name
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.write(player['name'])
            time.sleep(0.3)
            
            # Tab to chip field
            pyautogui.press('tab')
            time.sleep(0.3)
            
            # Clear and type chips
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            pyautogui.write(str(player['chips']))
            time.sleep(0.3)
            
            # Confirm with Enter
            pyautogui.press('enter')
            time.sleep(0.5)
            
            print(f"      [OK] Updated with {player['chips']:,} chips")
            
        except Exception as e:
            print(f"      [ERROR] Failed: {e}")
    
    # Take screenshot after update
    print("\n[7] Taking screenshot after update...")
    after = pyautogui.screenshot()
    after.save("after_fullscreen_update.png")
    print("    Saved: after_fullscreen_update.png")
    
    print("\n" + "="*70)
    print(" UPDATE ATTEMPT COMPLETE")
    print("="*70)
    print("\nPlease check the screenshots to verify if update was successful:")
    print("  - before_fullscreen_update.png")
    print("  - after_fullscreen_update.png")
    print("\nIf buttons weren't found, we may need to adjust coordinates")
    print("="*70)

if __name__ == "__main__":
    update_players_fullscreen()