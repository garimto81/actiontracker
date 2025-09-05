"""
Auto Detect Player Status in GFX Action Tracker
플레이어 이름 등록 상태 자동 감지
"""

import pyautogui
import time
import cv2
import numpy as np
from PIL import Image
import pytesseract
import json

# Player coordinates
PLAYER_COORDS = {
    1: (233, 361),
    2: (374, 359),
    3: (544, 362),
    4: (722, 359),
    5: (886, 356),
    6: (1051, 354),
    7: (1213, 355),
    8: (1385, 383),
    9: (1549, 367),
    10: (1705, 356)
}

# Detection areas for player names (relative to player position)
NAME_REGION_OFFSET = {
    'x_offset': -50,
    'y_offset': -30,
    'width': 150,
    'height': 60
}

class PlayerDetector:
    def __init__(self):
        self.player_status = {}
        self.detected_names = {}
        
    def capture_screen_region(self, x, y, width, height):
        """Capture specific region of screen"""
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        return screenshot
    
    def detect_by_color(self, player_num):
        """
        Method 1: Color-based detection
        빈 자리는 회색, 이름 있는 자리는 빨간색 배경
        """
        coords = PLAYER_COORDS[player_num]
        
        # Capture small region around player position
        region_x = coords[0] - 50
        region_y = coords[1] - 20
        region = self.capture_screen_region(region_x, region_y, 100, 40)
        
        # Convert to numpy array
        img_array = np.array(region)
        
        # Check for red color (player with name) vs gray (empty)
        # Red background RGB approximately (180-220, 40-80, 40-80)
        red_pixels = np.sum((img_array[:,:,0] > 180) & 
                           (img_array[:,:,0] < 220) & 
                           (img_array[:,:,1] < 80) & 
                           (img_array[:,:,2] < 80))
        
        # Gray background RGB approximately (100-150, 100-150, 100-150)
        gray_pixels = np.sum((img_array[:,:,0] > 100) & 
                            (img_array[:,:,0] < 150) & 
                            (img_array[:,:,1] > 100) & 
                            (img_array[:,:,1] < 150) & 
                            (img_array[:,:,2] > 100) & 
                            (img_array[:,:,2] < 150))
        
        # Determine status based on color dominance
        if red_pixels > gray_pixels * 2:
            return "occupied"
        else:
            return "empty"
    
    def detect_by_ocr(self, player_num):
        """
        Method 2: OCR-based detection
        텍스트 인식으로 이름 유무 확인
        """
        coords = PLAYER_COORDS[player_num]
        
        # Capture name region
        region_x = coords[0] + NAME_REGION_OFFSET['x_offset']
        region_y = coords[1] + NAME_REGION_OFFSET['y_offset']
        width = NAME_REGION_OFFSET['width']
        height = NAME_REGION_OFFSET['height']
        
        region = self.capture_screen_region(region_x, region_y, width, height)
        
        # Convert to grayscale for better OCR
        gray = cv2.cvtColor(np.array(region), cv2.COLOR_RGB2GRAY)
        
        # Apply threshold for better text recognition
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        # Use OCR to detect text
        try:
            text = pytesseract.image_to_string(thresh, config='--psm 8').strip()
            
            # Check if it's a number (empty seat) or name
            if text.isdigit() or text == "" or len(text) <= 2:
                return "empty", ""
            else:
                return "occupied", text
        except:
            return "unknown", ""
    
    def detect_by_pixel_pattern(self, player_num):
        """
        Method 3: Pixel pattern detection
        특정 픽셀 패턴으로 빈자리/이름 구분
        """
        coords = PLAYER_COORDS[player_num]
        
        # Check specific pixel that differs between empty and occupied
        check_points = [
            (coords[0], coords[1]),  # Center
            (coords[0] - 30, coords[1]),  # Left
            (coords[0] + 30, coords[1]),  # Right
        ]
        
        colors = []
        for x, y in check_points:
            pixel = pyautogui.pixel(x, y)
            colors.append(pixel)
        
        # Analyze color pattern
        avg_red = sum(c[0] for c in colors) / len(colors)
        avg_green = sum(c[1] for c in colors) / len(colors)
        avg_blue = sum(c[2] for c in colors) / len(colors)
        
        # Red dominant = occupied, Gray = empty
        if avg_red > avg_green + 50 and avg_red > avg_blue + 50:
            return "occupied"
        else:
            return "empty"
    
    def detect_all_players(self, method="color"):
        """
        Detect status of all 10 players
        """
        results = {}
        
        print("Detecting player status...")
        print("-" * 50)
        
        for player_num in range(1, 11):
            if method == "color":
                status = self.detect_by_color(player_num)
                results[player_num] = {"status": status}
                
            elif method == "ocr":
                status, name = self.detect_by_ocr(player_num)
                results[player_num] = {"status": status, "name": name}
                
            elif method == "pixel":
                status = self.detect_by_pixel_pattern(player_num)
                results[player_num] = {"status": status}
            
            print(f"Player {player_num}: {results[player_num]}")
            time.sleep(0.1)  # Small delay between detections
        
        return results
    
    def smart_detect(self):
        """
        Smart detection using multiple methods
        여러 방법을 조합하여 정확도 향상
        """
        print("Starting smart detection...")
        print("=" * 60)
        
        # First try color detection (fastest)
        color_results = {}
        for player_num in range(1, 11):
            color_results[player_num] = self.detect_by_color(player_num)
        
        # Then verify with pixel pattern for uncertain cases
        final_results = {}
        for player_num in range(1, 11):
            color_status = color_results[player_num]
            
            # Double-check with pixel pattern
            pixel_status = self.detect_by_pixel_pattern(player_num)
            
            # If both agree, we're confident
            if color_status == pixel_status:
                final_results[player_num] = {
                    "status": color_status,
                    "confidence": "high"
                }
            else:
                # If they disagree, use OCR as tiebreaker
                ocr_status, name = self.detect_by_ocr(player_num)
                final_results[player_num] = {
                    "status": ocr_status,
                    "name": name if name else "",
                    "confidence": "medium"
                }
            
            status_icon = "✓" if final_results[player_num]["status"] == "occupied" else "○"
            print(f"Player {player_num:2}: {status_icon} {final_results[player_num]['status']:10} "
                  f"[{final_results[player_num]['confidence']}]")
        
        return final_results
    
    def save_detection_results(self, results, filename="player_status.json"):
        """Save detection results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {filename}")
    
    def generate_gui_config(self, results):
        """
        Generate configuration for GUI based on detection
        GUI에서 사용할 설정 생성
        """
        config = {
            "empty_seats": [],
            "occupied_seats": [],
            "detected_names": {},
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for player_num, data in results.items():
            if data["status"] == "empty":
                config["empty_seats"].append(player_num)
            else:
                config["occupied_seats"].append(player_num)
                if "name" in data and data["name"]:
                    config["detected_names"][player_num] = data["name"]
        
        return config


def test_detection():
    """Test detection methods"""
    detector = PlayerDetector()
    
    print("=" * 60)
    print("ACTION TRACKER PLAYER DETECTION")
    print("=" * 60)
    print()
    
    print("Detection Methods:")
    print("1. Color-based (Fast)")
    print("2. OCR-based (Accurate for names)")
    print("3. Pixel pattern (Medium)")
    print("4. Smart detection (Combined)")
    print()
    
    choice = input("Select method (1-4): ").strip()
    
    print("\nStarting detection in 3 seconds...")
    print("Make sure Action Tracker is visible!")
    time.sleep(3)
    
    if choice == "1":
        results = detector.detect_all_players("color")
    elif choice == "2":
        results = detector.detect_all_players("ocr")
    elif choice == "3":
        results = detector.detect_all_players("pixel")
    elif choice == "4":
        results = detector.smart_detect()
    else:
        print("Invalid choice")
        return
    
    # Save results
    detector.save_detection_results(results)
    
    # Generate GUI config
    config = detector.generate_gui_config(results)
    with open("gui_auto_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "=" * 60)
    print("DETECTION COMPLETE")
    print("=" * 60)
    print(f"Empty seats: {config['empty_seats']}")
    print(f"Occupied seats: {config['occupied_seats']}")
    if config['detected_names']:
        print(f"Detected names: {config['detected_names']}")
    print("\nConfiguration saved to gui_auto_config.json")
    print("You can load this in the GUI for automatic setup!")


if __name__ == "__main__":
    test_detection()