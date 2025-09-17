"""
마우스 좌표 추출 도구
실시간으로 마우스 위치를 추적하고 클릭 시 좌표를 저장
"""

import pyautogui
import time
import keyboard
from datetime import datetime

def get_current_position():
    """현재 마우스 위치 반환"""
    return pyautogui.position()

def track_mouse_position():
    """실시간 마우스 위치 추적"""
    print("=" * 60)
    print("MOUSE COORDINATE TRACKER")
    print("=" * 60)
    print("Instructions:")
    print("  - Move mouse to see coordinates")
    print("  - Press 'C' to capture current position")
    print("  - Press 'P' to capture player positions (1-10)")
    print("  - Press 'H' to capture chip positions (1-10)")
    print("  - Press 'S' to save all captured coordinates")
    print("  - Press 'ESC' to exit")
    print("=" * 60)
    print("\nTracking mouse position...\n")
    
    captured_coords = {
        "player_coords": {},
        "chip_coords": {},
        "other_coords": []
    }
    
    player_count = 0
    chip_count = 0
    
    try:
        while True:
            # Show current position
            x, y = get_current_position()
            print(f"\rMouse Position: ({x}, {y})    ", end="", flush=True)
            
            # Check for key presses
            if keyboard.is_pressed('c'):
                # Capture general coordinate
                captured_coords["other_coords"].append((x, y))
                print(f"\n[CAPTURED] General coordinate: ({x}, {y})")
                time.sleep(0.3)  # Prevent multiple captures
                
            elif keyboard.is_pressed('p'):
                # Capture player coordinate
                player_count += 1
                if player_count <= 10:
                    captured_coords["player_coords"][player_count] = (x, y)
                    print(f"\n[PLAYER {player_count}] Captured: ({x}, {y})")
                else:
                    print(f"\n[WARNING] Already captured 10 player positions")
                time.sleep(0.3)
                
            elif keyboard.is_pressed('h'):
                # Capture chip coordinate
                chip_count += 1
                if chip_count <= 10:
                    captured_coords["chip_coords"][chip_count] = (x, y)
                    print(f"\n[CHIP {chip_count}] Captured: ({x}, {y})")
                else:
                    print(f"\n[WARNING] Already captured 10 chip positions")
                time.sleep(0.3)
                
            elif keyboard.is_pressed('s'):
                # Save captured coordinates
                save_coordinates(captured_coords)
                time.sleep(0.3)
                
            elif keyboard.is_pressed('esc'):
                # Exit
                print("\n\nExiting coordinate tracker...")
                break
                
            time.sleep(0.01)  # Small delay to prevent high CPU usage
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    # Show summary
    print("\n" + "=" * 60)
    print("CAPTURED COORDINATES SUMMARY")
    print("=" * 60)
    
    if captured_coords["player_coords"]:
        print("\nPlayer Coordinates:")
        for seat, coord in captured_coords["player_coords"].items():
            print(f"  Player {seat}: {coord}")
    
    if captured_coords["chip_coords"]:
        print("\nChip Coordinates:")
        for seat, coord in captured_coords["chip_coords"].items():
            print(f"  Chip {seat}: {coord}")
    
    if captured_coords["other_coords"]:
        print("\nOther Coordinates:")
        for i, coord in enumerate(captured_coords["other_coords"], 1):
            print(f"  {i}. {coord}")
    
    return captured_coords

def save_coordinates(coords):
    """Save coordinates to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"captured_coordinates_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("CAPTURED COORDINATES\n")
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write("=" * 60 + "\n\n")
        
        if coords["player_coords"]:
            f.write("PLAYER_COORDS = {\n")
            for seat, coord in coords["player_coords"].items():
                f.write(f"    {seat}: {coord},\n")
            f.write("}\n\n")
        
        if coords["chip_coords"]:
            f.write("CHIP_COORDS = {\n")
            for seat, coord in coords["chip_coords"].items():
                f.write(f"    {seat}: {coord},\n")
            f.write("}\n\n")
        
        if coords["other_coords"]:
            f.write("OTHER_COORDS = [\n")
            for coord in coords["other_coords"]:
                f.write(f"    {coord},\n")
            f.write("]\n")
    
    print(f"\n[SAVED] Coordinates saved to {filename}")

def click_and_capture():
    """Click to capture mode"""
    print("=" * 60)
    print("CLICK TO CAPTURE MODE")
    print("=" * 60)
    print("Instructions:")
    print("  - Click anywhere to capture that position")
    print("  - Press 'Q' to quit")
    print("=" * 60)
    print("\nReady to capture clicks...\n")
    
    captured = []
    
    try:
        while True:
            if keyboard.is_pressed('q'):
                break
            
            # Check for mouse click
            if pyautogui.mouseDown():
                x, y = get_current_position()
                captured.append((x, y))
                print(f"[CLICK {len(captured)}] Captured: ({x}, {y})")
                time.sleep(0.3)  # Prevent multiple captures from one click
    
    except KeyboardInterrupt:
        pass
    
    print("\n" + "=" * 60)
    print("CAPTURED CLICKS")
    print("=" * 60)
    for i, coord in enumerate(captured, 1):
        print(f"  {i}. {coord}")
    
    return captured

def automated_capture():
    """Automated capture with countdown"""
    print("=" * 60)
    print("AUTOMATED COORDINATE CAPTURE")
    print("=" * 60)
    print("This will capture 10 player positions and 10 chip positions")
    print("Position your mouse and press ENTER when ready for each capture")
    print("=" * 60)
    
    coords = {
        "player_coords": {},
        "chip_coords": {}
    }
    
    # Capture player coordinates
    print("\n--- CAPTURING PLAYER COORDINATES ---")
    for i in range(1, 11):
        input(f"\nMove mouse to PLAYER {i} position and press ENTER: ")
        x, y = get_current_position()
        coords["player_coords"][i] = (x, y)
        print(f"  Player {i}: ({x}, {y}) - CAPTURED!")
    
    # Capture chip coordinates
    print("\n--- CAPTURING CHIP COORDINATES ---")
    for i in range(1, 11):
        input(f"\nMove mouse to CHIP {i} position and press ENTER: ")
        x, y = get_current_position()
        coords["chip_coords"][i] = (x, y)
        print(f"  Chip {i}: ({x}, {y}) - CAPTURED!")
    
    # Display results
    print("\n" + "=" * 60)
    print("CAPTURE COMPLETE")
    print("=" * 60)
    
    print("\n# Copy and paste these into your code:\n")
    
    print("PLAYER_COORDS = {")
    for seat, coord in coords["player_coords"].items():
        print(f"    {seat}: {coord},")
    print("}\n")
    
    print("CHIP_COORDS = {")
    for seat, coord in coords["chip_coords"].items():
        print(f"    {seat}: {coord},")
    print("}")
    
    # Save to file
    save_coordinates(coords)
    
    return coords

def main():
    """Main menu"""
    print("\n" + "=" * 60)
    print("ACTION TRACKER COORDINATE TOOL")
    print("=" * 60)
    print("1. Real-time tracking (keyboard capture)")
    print("2. Click to capture mode")
    print("3. Automated capture (step by step)")
    print("4. Exit")
    print("=" * 60)
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        track_mouse_position()
    elif choice == "2":
        click_and_capture()
    elif choice == "3":
        automated_capture()
    elif choice == "4":
        print("Exiting...")
    else:
        print("Invalid option")

if __name__ == "__main__":
    print(f"Screen Size: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    main()