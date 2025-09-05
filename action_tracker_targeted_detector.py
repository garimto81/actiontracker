"""
Targeted Position Detector for Action Tracker
Specifically designed for the visible Action Tracker interface
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import time
from datetime import datetime

class ActionTrackerTargetedDetector:
    def __init__(self):
        """Initialize the targeted detector"""
        self.player_positions = {}
        self.chip_positions = {}
        
    def capture_screenshot(self):
        """Capture current screen"""
        print("Capturing Action Tracker screenshot...")
        screenshot = pyautogui.screenshot()
        img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot, img_cv
    
    def detect_red_player_buttons(self, img_cv):
        """Detect red player name buttons specifically"""
        print("Detecting red player buttons...")
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        
        # Define red color range for player buttons
        # Red can appear in two ranges in HSV
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        # Create masks for both red ranges
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # Find contours in the red mask
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        player_buttons = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter for button-like dimensions
            if 80 < w < 150 and 25 < h < 50:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold
                    center_x = x + w // 2
                    center_y = y + h // 2
                    player_buttons.append({
                        'x': center_x,
                        'y': center_y,
                        'bounds': (x, y, w, h),
                        'area': area
                    })
        
        # Sort buttons by position (left to right)
        player_buttons.sort(key=lambda btn: btn['x'])
        
        return player_buttons
    
    def detect_chip_buttons(self, img_cv, player_buttons):
        """Detect golden/brown chip stack buttons below player buttons"""
        print("Detecting chip stack buttons...")
        
        # Convert to HSV
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        
        # Define golden/brown color range for chip buttons
        lower_gold = np.array([10, 100, 100])
        upper_gold = np.array([30, 255, 255])
        
        gold_mask = cv2.inRange(hsv, lower_gold, upper_gold)
        
        # Find contours
        contours, _ = cv2.findContours(gold_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        chip_buttons = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter for button-like dimensions
            if 80 < w < 150 and 25 < h < 50:
                area = cv2.contourArea(contour)
                if area > 1000:
                    center_x = x + w // 2
                    center_y = y + h // 2
                    chip_buttons.append({
                        'x': center_x,
                        'y': center_y,
                        'bounds': (x, y, w, h),
                        'area': area
                    })
        
        # Match chip buttons to player buttons
        matched_chips = []
        for player in player_buttons:
            # Look for chip button in the area below this player
            best_match = None
            min_distance = float('inf')
            
            for chip in chip_buttons:
                # Check if chip is below player and roughly aligned
                if (chip['y'] > player['y'] + 50 and  # Below player
                    abs(chip['x'] - player['x']) < 50):  # Horizontally aligned
                    
                    distance = abs(chip['x'] - player['x'])
                    if distance < min_distance:
                        min_distance = distance
                        best_match = chip
            
            if best_match:
                matched_chips.append(best_match)
            else:
                # If no match found, estimate position
                estimated_chip = {
                    'x': player['x'],
                    'y': player['y'] + 150,  # Estimate based on layout
                    'bounds': (player['x'] - 50, player['y'] + 130, 100, 40),
                    'estimated': True
                }
                matched_chips.append(estimated_chip)
        
        return matched_chips
    
    def create_position_mapping(self, player_buttons, chip_buttons):
        """Create final position mapping for automation"""
        print("Creating position mapping...")
        
        positions = {}
        
        for i, (player, chip) in enumerate(zip(player_buttons, chip_buttons), 1):
            positions[i] = {
                'name': {
                    'x': player['x'],
                    'y': player['y'],
                    'bounds': player['bounds']
                },
                'chips': {
                    'x': chip['x'],
                    'y': chip['y'],
                    'bounds': chip['bounds'],
                    'estimated': chip.get('estimated', False)
                }
            }
        
        return positions
    
    def visualize_detection(self, img_cv, positions):
        """Create visualization of detected positions"""
        print("Creating detection visualization...")
        
        # Convert to PIL for drawing
        img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'cyan', 'magenta', 'orange', 'pink', 'brown']
        
        for player_num, pos_data in positions.items():
            color = colors[(player_num - 1) % len(colors)]
            
            # Draw player name button
            name_data = pos_data['name']
            nx, ny = name_data['x'], name_data['y']
            if 'bounds' in name_data:
                bx, by, bw, bh = name_data['bounds']
                draw.rectangle([bx, by, bx + bw, by + bh], outline=color, width=3)
            
            # Draw crosshair on name button
            draw.line([(nx-15, ny), (nx+15, ny)], fill=color, width=2)
            draw.line([(nx, ny-15), (nx, ny+15)], fill=color, width=2)
            draw.text((nx + 20, ny - 20), f"P{player_num} Name", fill=color)
            
            # Draw chip button
            chip_data = pos_data['chips']
            cx, cy = chip_data['x'], chip_data['y']
            if 'bounds' in chip_data:
                bx, by, bw, bh = chip_data['bounds']
                outline_width = 2 if chip_data.get('estimated') else 3
                draw.rectangle([bx, by, bx + bw, by + bh], outline=color, width=outline_width)
            
            # Draw crosshair on chip button
            draw.line([(cx-15, cy), (cx+15, cy)], fill=color, width=2)
            draw.line([(cx, cy-15), (cx, cy+15)], fill=color, width=2)
            
            label = f"P{player_num} Chips"
            if chip_data.get('estimated'):
                label += " (Est.)"
            draw.text((cx + 20, cy - 20), label, fill=color)
            
            # Draw connection line
            draw.line([(nx, ny), (cx, cy)], fill=color, width=1)
        
        return img_pil
    
    def generate_automation_script(self, positions):
        """Generate automation script with detected positions"""
        print("Generating automation script...")
        
        script_content = f'''"""
Auto-generated Action Tracker Automation Script
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Detected {len(positions)} player positions
"""

import pyautogui
import time

# Detected player positions
PLAYER_POSITIONS = {{
'''
        
        for player_num, pos_data in positions.items():
            name_pos = (pos_data['name']['x'], pos_data['name']['y'])
            chip_pos = (pos_data['chips']['x'], pos_data['chips']['y'])
            estimated_note = " # Estimated position" if pos_data['chips'].get('estimated') else ""
            
            script_content += f'''    {player_num}: {{
        'name': {name_pos},
        'chips': {chip_pos}{estimated_note}
    }},
'''
        
        script_content += '''}}

def click_and_type(x, y, text, delay=0.2):
    """Click at position and type text"""
    pyautogui.click(x, y)
    time.sleep(delay)
    pyautogui.hotkey('ctrl', 'a')  # Select all
    time.sleep(0.1)
    pyautogui.typewrite(str(text))
    time.sleep(delay)

def update_player(player_num, name=None, chips=None):
    """Update a specific player's information"""
    if player_num not in PLAYER_POSITIONS:
        print(f"Player {player_num} not found in positions")
        return False
    
    pos = PLAYER_POSITIONS[player_num]
    
    try:
        if name is not None:
            print(f"Updating Player {player_num} name to: {name}")
            click_and_type(pos['name'][0], pos['name'][1], name)
        
        if chips is not None:
            print(f"Updating Player {player_num} chips to: {chips}")
            click_and_type(pos['chips'][0], pos['chips'][1], chips)
        
        return True
    except Exception as e:
        print(f"Error updating Player {player_num}: {e}")
        return False

def update_all_players(player_data, delay=0.5):
    """Update multiple players from dictionary"""
    success_count = 0
    
    for player_num, data in player_data.items():
        if player_num in PLAYER_POSITIONS:
            name = data.get('name')
            chips = data.get('chips')
            
            if update_player(player_num, name, chips):
                success_count += 1
            
            time.sleep(delay)  # Delay between players
        else:
            print(f"Player {player_num} position not detected")
    
    print(f"Successfully updated {success_count}/{len(player_data)} players")
    return success_count

def test_positions():
    """Test by clicking each detected position"""
    print("Testing detected positions...")
    print("This will click each player name and chip position")
    print("Press Ctrl+C to cancel within 5 seconds")
    
    try:
        time.sleep(5)
        
        for player_num, pos in PLAYER_POSITIONS.items():
            print(f"Testing Player {player_num}...")
            
            # Click name position
            pyautogui.click(pos['name'][0], pos['name'][1])
            time.sleep(0.5)
            
            # Click chip position
            pyautogui.click(pos['chips'][0], pos['chips'][1])
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("Test cancelled by user")

# Example usage
if __name__ == "__main__":
    # Example 1: Update specific players
    update_player(1, "Alice", 15000)
    update_player(2, "Bob", 12500)
    
    # Example 2: Batch update
    players_data = {{
        1: {{'name': 'Alice', 'chips': 15000}},
        2: {{'name': 'Bob', 'chips': 12500}},
        3: {{'name': 'Charlie', 'chips': 18000}},
        4: {{'name': 'David', 'chips': 9500}},
        5: {{'name': 'Eve', 'chips': 22000}}
    }}
    
    print("Starting batch update in 3 seconds...")
    print("Make sure Action Tracker window is active!")
    time.sleep(3)
    
    update_all_players(players_data)
    print("Batch update complete!")
'''
        
        return script_content
    
    def save_results(self, positions, script_content):
        """Save detection results and generated script"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save positions as JSON
        json_data = {
            'detection_timestamp': datetime.now().isoformat(),
            'player_count': len(positions),
            'positions': {}
        }
        
        for player_num, pos_data in positions.items():
            json_data['positions'][str(player_num)] = {
                'name_x': pos_data['name']['x'],
                'name_y': pos_data['name']['y'],
                'chip_x': pos_data['chips']['x'],
                'chip_y': pos_data['chips']['y'],
                'chip_estimated': pos_data['chips'].get('estimated', False)
            }
        
        json_filename = f"action_tracker_positions_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Save automation script
        script_filename = f"action_tracker_automation_{timestamp}.py"
        with open(script_filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return json_filename, script_filename
    
    def run(self):
        """Main detection workflow"""
        print("="*60)
        print("Action Tracker Targeted Position Detector")
        print("="*60)
        
        try:
            # Capture screenshot
            screenshot_pil, img_cv = self.capture_screenshot()
            
            # Detect player buttons (red)
            player_buttons = self.detect_red_player_buttons(img_cv)
            print(f"Detected {len(player_buttons)} player name buttons")
            
            if not player_buttons:
                print("No player buttons detected. Make sure Action Tracker is visible.")
                return None
            
            # Detect chip buttons (golden/brown)
            chip_buttons = self.detect_chip_buttons(img_cv, player_buttons)
            print(f"Detected/estimated {len(chip_buttons)} chip positions")
            
            # Create position mapping
            positions = self.create_position_mapping(player_buttons, chip_buttons)
            
            # Create visualization
            viz_image = self.visualize_detection(img_cv, positions)
            
            # Generate automation script
            script_content = self.generate_automation_script(positions)
            
            # Save results
            json_file, script_file = self.save_results(positions, script_content)
            
            # Save visualization
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            viz_filename = f"action_tracker_detection_{timestamp}.png"
            viz_image.save(viz_filename)
            
            print("\n" + "="*60)
            print("DETECTION COMPLETE!")
            print("="*60)
            print(f"✅ Detected {len(positions)} player positions")
            print(f"📊 Positions saved: {json_file}")
            print(f"🤖 Automation script: {script_file}")
            print(f"🖼️  Visualization: {viz_filename}")
            print("\nTo use the automation:")
            print(f"1. Make sure Action Tracker is active")
            print(f"2. Run: python {script_file}")
            print("="*60)
            
            return positions
            
        except Exception as e:
            print(f"Error during detection: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Main entry point"""
    detector = ActionTrackerTargetedDetector()
    positions = detector.run()
    
    if positions:
        print("\nDetected Positions Summary:")
        for player_num, pos_data in positions.items():
            name_pos = (pos_data['name']['x'], pos_data['name']['y'])
            chip_pos = (pos_data['chips']['x'], pos_data['chips']['y'])
            estimated = " (estimated)" if pos_data['chips'].get('estimated') else ""
            print(f"  Player {player_num}: Name{name_pos}, Chips{chip_pos}{estimated}")

if __name__ == "__main__":
    main()