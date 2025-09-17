"""
10개 좌표 캡처 도구
플레이어 1-10과 칩 1-10 좌표를 순서대로 캡처
"""

import pyautogui
import time

def capture_player_and_chip_coords():
    """플레이어와 칩 좌표 캡처"""
    print("=" * 60)
    print("CAPTURE 10 PLAYER & CHIP COORDINATES")
    print("=" * 60)
    print("This tool will help you capture coordinates for:")
    print("  - 10 Player positions")
    print("  - 10 Chip input positions")
    print("\nInstructions:")
    print("  1. Position Action Tracker window properly")
    print("  2. Follow the prompts")
    print("  3. Move mouse to position and press ENTER")
    print("=" * 60)
    
    input("\nPress ENTER when ready to start...")
    
    # Capture player coordinates
    print("\n" + "=" * 60)
    print("CAPTURING PLAYER COORDINATES")
    print("=" * 60)
    
    player_coords = {}
    for i in range(1, 11):
        input(f"\nMove mouse to PLAYER {i} name area and press ENTER: ")
        x, y = pyautogui.position()
        player_coords[i] = (x, y)
        print(f"  ✓ Player {i}: ({x}, {y})")
    
    # Capture chip coordinates
    print("\n" + "=" * 60)
    print("CAPTURING CHIP COORDINATES")
    print("=" * 60)
    
    chip_coords = {}
    for i in range(1, 11):
        input(f"\nMove mouse to CHIP INPUT {i} field and press ENTER: ")
        x, y = pyautogui.position()
        chip_coords[i] = (x, y)
        print(f"  ✓ Chip {i}: ({x}, {y})")
    
    # Display results
    print("\n" + "=" * 60)
    print("CAPTURE COMPLETE - COPY THIS CODE:")
    print("=" * 60)
    
    # Format for Python code
    print("\n# Player name click coordinates")
    print("PLAYER_COORDS = {")
    for i in range(1, 11):
        print(f"    {i}: {player_coords[i]},")
    print("}")
    
    print("\n# Chip input field coordinates")
    print("CHIP_COORDS = {")
    for i in range(1, 11):
        print(f"    {i}: {chip_coords[i]},")
    print("}")
    
    # Save to file
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"coordinates_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("# Captured coordinates\n")
        f.write(f"# Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Screen size: {pyautogui.size()[0]} x {pyautogui.size()[1]}\n\n")
        
        f.write("PLAYER_COORDS = {\n")
        for i in range(1, 11):
            f.write(f"    {i}: {player_coords[i]},\n")
        f.write("}\n\n")
        
        f.write("CHIP_COORDS = {\n")
        for i in range(1, 11):
            f.write(f"    {i}: {chip_coords[i]},\n")
        f.write("}\n")
    
    print(f"\n✓ Coordinates saved to: {filename}")
    
    # Also create code snippet
    code_filename = f"coordinates_code_{timestamp}.py"
    with open(code_filename, 'w') as f:
        f.write('"""\nAction Tracker Coordinates\n')
        f.write(f"Captured: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Screen: {pyautogui.size()[0]} x {pyautogui.size()[1]}\n")
        f.write('"""\n\n')
        
        f.write("PLAYER_COORDS = {\n")
        for i in range(1, 11):
            f.write(f"    {i}: {player_coords[i]},\n")
        f.write("}\n\n")
        
        f.write("CHIP_COORDS = {\n")
        for i in range(1, 11):
            f.write(f"    {i}: {chip_coords[i]},\n")
        f.write("}\n\n")
        
        f.write("# Other important coordinates\n")
        f.write("SUB_NAME_FIELD = (785, 291)  # Name input field in sub dialog\n")
        f.write("COMPLETE_BUTTON = (1720, 139)  # Complete button\n")
        f.write("DELETE_BUTTON = (721, 112)  # Delete button\n")
    
    print(f"✓ Python code saved to: {code_filename}")
    
    return player_coords, chip_coords

if __name__ == "__main__":
    print(f"Current Screen Size: {pyautogui.size()[0]} x {pyautogui.size()[1]}")
    capture_player_and_chip_coords()