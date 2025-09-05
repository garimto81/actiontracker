"""
Final Action Tracker Position Detector
Uses analyzed color values for accurate detection
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json
import time
from datetime import datetime

class ActionTrackerFinalDetector:
    def __init__(self):
        """Initialize the final detector with analyzed color ranges"""
        self.player_positions = {}
        self.chip_positions = {}
        
        # Color ranges based on actual analysis
        # Player buttons are teal/cyan: HSV H=30, S=125, V=184
        self.player_color_range = {
            'lower': np.array([20, 100, 150]),  # Lower bound
            'upper': np.array([40, 255, 255])   # Upper bound
        }
        
        # Chip buttons: HSV H=0, S=79, V=149 (brownish)
        self.chip_color_range = {
            'lower': np.array([0, 60, 120]),
            'upper': np.array([15, 150, 180])
        }
    
    def capture_screenshot(self):
        """Capture current screen"""
        print("Capturing Action Tracker screenshot...")
        screenshot = pyautogui.screenshot()
        img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot, img_cv
    
    def detect_player_buttons(self, img_cv):
        """Detect teal player name buttons"""
        print("Detecting teal player name buttons...")
        
        # Convert to HSV
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        
        # Create mask for player button colors
        mask = cv2.inRange(hsv, self.player_color_range['lower'], self.player_color_range['upper'])
        
        # Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        player_buttons = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter for button-like dimensions
            if 60 < w < 200 and 20 < h < 60:
                area = cv2.contourArea(contour)
                if area > 800:  # Minimum area threshold
                    center_x = x + w // 2
                    center_y = y + h // 2
                    player_buttons.append({
                        'x': center_x,
                        'y': center_y,
                        'bounds': (x, y, w, h),
                        'area': area
                    })
        
        # Sort buttons by position (left to right, then top to bottom)
        player_buttons.sort(key=lambda btn: (btn['y'] // 50, btn['x']))
        
        # Debug: save mask for inspection
        cv2.imwrite("player_mask_debug.png", mask)
        
        return player_buttons
    
    def detect_chip_buttons(self, img_cv):
        """Detect brown/gold chip stack buttons"""
        print("Detecting chip stack buttons...")
        
        # Convert to HSV
        hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
        
        # Create mask for chip button colors
        mask = cv2.inRange(hsv, self.chip_color_range['lower'], self.chip_color_range['upper'])
        
        # Morphological operations
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        chip_buttons = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter for button-like dimensions
            if 60 < w < 200 and 20 < h < 60:
                area = cv2.contourArea(contour)
                if area > 800:
                    center_x = x + w // 2
                    center_y = y + h // 2
                    chip_buttons.append({
                        'x': center_x,
                        'y': center_y,
                        'bounds': (x, y, w, h),
                        'area': area
                    })
        
        # Sort by position
        chip_buttons.sort(key=lambda btn: (btn['y'] // 50, btn['x']))
        
        # Debug: save mask
        cv2.imwrite("chip_mask_debug.png", mask)
        
        return chip_buttons
    
    def match_buttons(self, player_buttons, chip_buttons):
        """Match player buttons with their corresponding chip buttons"""
        print("Matching player and chip buttons...")
        
        matched_pairs = []
        used_chip_indices = set()
        
        for player in player_buttons:
            best_chip = None
            best_distance = float('inf')
            best_chip_index = -1
            
            for i, chip in enumerate(chip_buttons):
                if i in used_chip_indices:
                    continue
                
                # Calculate distance
                dx = abs(chip['x'] - player['x'])
                dy = abs(chip['y'] - player['y'])
                distance = np.sqrt(dx*dx + dy*dy)
                
                # Check if chip is roughly below player and aligned
                if (chip['y'] > player['y'] + 50 and  # Below player
                    dx < 100 and  # Horizontally aligned
                    distance < best_distance):
                    best_distance = distance
                    best_chip = chip
                    best_chip_index = i
            
            if best_chip:
                matched_pairs.append((player, best_chip))
                used_chip_indices.add(best_chip_index)
            else:
                # Create estimated chip position
                estimated_chip = {
                    'x': player['x'],
                    'y': player['y'] + 130,  # Estimate based on typical layout
                    'bounds': (player['x'] - 50, player['y'] + 110, 100, 40),
                    'estimated': True,
                    'area': 0
                }
                matched_pairs.append((player, estimated_chip))
        
        return matched_pairs
    
    def create_position_mapping(self, matched_pairs):
        """Create final position mapping"""
        print("Creating position mapping...")
        
        positions = {}
        
        for i, (player, chip) in enumerate(matched_pairs, 1):
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
        """Create detailed visualization"""
        print("Creating detection visualization...")
        
        # Convert to PIL
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
            
            # Draw crosshair and label
            draw.line([(nx-20, ny), (nx+20, ny)], fill=color, width=3)
            draw.line([(nx, ny-20), (nx, ny+20)], fill=color, width=3)
            draw.text((nx + 25, ny - 25), f"P{player_num}", fill=color)
            
            # Draw chip button
            chip_data = pos_data['chips']
            cx, cy = chip_data['x'], chip_data['y']
            
            if 'bounds' in chip_data:
                bx, by, bw, bh = chip_data['bounds']
                outline_style = 2 if chip_data.get('estimated') else 3
                draw.rectangle([bx, by, bx + bw, by + bh], outline=color, width=outline_style)
            
            # Draw crosshair and label
            draw.line([(cx-20, cy), (cx+20, cy)], fill=color, width=3)
            draw.line([(cx, cy-20), (cx, cy+20)], fill=color, width=3)
            
            chip_label = f"${player_num}"
            if chip_data.get('estimated'):
                chip_label += " (est)"
            draw.text((cx + 25, cy - 25), chip_label, fill=color)
            
            # Connect player to chip with line
            draw.line([(nx, ny), (cx, cy)], fill=color, width=2)
        
        return img_pil
    
    def generate_automation_script(self, positions):
        """Generate comprehensive automation script"""
        print("Generating automation script...")
        
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        script = f'''"""
Action Tracker Automation Script
Generated: {timestamp_str}
Detected positions: {len(positions)} players

This script provides functions to automatically update Action Tracker
player names and chip stacks using the detected UI positions.
"""

import pyautogui
import time
import json
from datetime import datetime

# Detected player positions
PLAYER_POSITIONS = {{'''
        
        for player_num, pos_data in positions.items():
            name_x, name_y = pos_data['name']['x'], pos_data['name']['y']
            chip_x, chip_y = pos_data['chips']['x'], pos_data['chips']['y']
            estimated_note = "  # Estimated position" if pos_data['chips'].get('estimated') else ""
            
            script += f'''
    {player_num}: {{
        'name': ({name_x}, {name_y}),
        'chips': ({chip_x}, {chip_y}){estimated_note}
    }},'''
        
        script += '''
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
    print(f"\\nBatch update complete: {successful}/{total} players updated successfully")
    
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
        print("\\nPosition testing cancelled by user")
    except Exception as e:
        print(f"\\nError during position testing: {e}")

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
        print("\\nExample cancelled by user")
'''
        
        return script
    
    def save_results(self, positions, script_content):
        """Save all results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save positions JSON
        json_data = {
            'detection_timestamp': datetime.now().isoformat(),
            'detection_method': 'color_based_hsv',
            'player_count': len(positions),
            'color_ranges': {
                'player_buttons': {
                    'lower_hsv': self.player_color_range['lower'].tolist(),
                    'upper_hsv': self.player_color_range['upper'].tolist()
                },
                'chip_buttons': {
                    'lower_hsv': self.chip_color_range['lower'].tolist(),
                    'upper_hsv': self.chip_color_range['upper'].tolist()
                }
            },
            'positions': {}
        }
        
        for player_num, pos_data in positions.items():
            json_data['positions'][str(player_num)] = {
                'name_x': pos_data['name']['x'],
                'name_y': pos_data['name']['y'],
                'name_bounds': pos_data['name']['bounds'],
                'chip_x': pos_data['chips']['x'],
                'chip_y': pos_data['chips']['y'],
                'chip_bounds': pos_data['chips']['bounds'],
                'chip_estimated': pos_data['chips'].get('estimated', False)
            }
        
        json_filename = f"action_tracker_final_positions_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Save automation script
        script_filename = f"action_tracker_final_automation_{timestamp}.py"
        with open(script_filename, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return json_filename, script_filename
    
    def run(self):
        """Main detection workflow"""
        print("="*70)
        print("ACTION TRACKER FINAL POSITION DETECTOR")
        print("="*70)
        
        try:
            # Capture screenshot
            screenshot_pil, img_cv = self.capture_screenshot()
            
            # Detect player buttons using color analysis
            player_buttons = self.detect_player_buttons(img_cv)
            print(f"[OK] Detected {len(player_buttons)} player name buttons")
            
            if not player_buttons:
                print("[ERROR] No player buttons detected!")
                print("[INFO] Check the debug masks: player_mask_debug.png")
                return None
            
            # Detect chip buttons
            chip_buttons = self.detect_chip_buttons(img_cv)
            print(f"[OK] Detected {len(chip_buttons)} chip buttons")
            
            # Match players with chips
            matched_pairs = self.match_buttons(player_buttons, chip_buttons)
            print(f"[OK] Matched {len(matched_pairs)} player-chip pairs")
            
            # Create position mapping
            positions = self.create_position_mapping(matched_pairs)
            
            # Create visualization
            viz_image = self.visualize_detection(img_cv, positions)
            
            # Generate automation script
            script_content = self.generate_automation_script(positions)
            
            # Save all results
            json_file, script_file = self.save_results(positions, script_content)
            
            # Save visualization
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            viz_filename = f"action_tracker_final_detection_{timestamp}.png"
            viz_image.save(viz_filename)
            
            print("\n" + "="*70)
            print("DETECTION COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"Detected {len(positions)} player positions")
            print(f"Positions data: {json_file}")
            print(f"Automation script: {script_file}")
            print(f"Detection visualization: {viz_filename}")
            print(f"Debug masks: player_mask_debug.png, chip_mask_debug.png")
            print("\nTO USE THE AUTOMATION:")
            print(f"   1. Make sure Action Tracker is active and visible")
            print(f"   2. Run: python {script_file}")
            print(f"   3. Or import the script and use the functions")
            print("="*70)
            
            return positions
            
        except Exception as e:
            print(f"[ERROR] Error during detection: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Main execution"""
    detector = ActionTrackerFinalDetector()
    positions = detector.run()
    
    if positions:
        print(f"\nDETECTED POSITIONS SUMMARY:")
        print("-" * 50)
        for player_num, pos_data in positions.items():
            name_pos = (pos_data['name']['x'], pos_data['name']['y'])
            chip_pos = (pos_data['chips']['x'], pos_data['chips']['y'])
            status = " (estimated)" if pos_data['chips'].get('estimated') else ""
            print(f"  Player {player_num:2d}: Name{name_pos} -> Chips{chip_pos}{status}")

if __name__ == "__main__":
    main()