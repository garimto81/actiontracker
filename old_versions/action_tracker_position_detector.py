"""
Action Tracker Position Detector using Computer Vision
Automatically detects UI element positions through screenshot analysis
"""

import cv2
import numpy as np
import pytesseract
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime
import re

class ActionTrackerPositionDetector:
    def __init__(self):
        """Initialize the position detector"""
        self.detected_positions = {
            'player_names': [],
            'chip_inputs': [],
            'buttons': {},
            'other_elements': {}
        }
        
    def capture_screenshot(self):
        """Capture current screen"""
        print("Capturing screenshot...")
        screenshot = pyautogui.screenshot()
        # Convert PIL image to OpenCV format
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot, screenshot_cv
    
    def detect_text_regions(self, image):
        """Detect text regions using OCR"""
        print("Detecting text regions...")
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Use pytesseract to get bounding boxes of text
        try:
            data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
            text_regions = []
            
            for i in range(len(data['text'])):
                text = str(data['text'][i]).strip()
                if text:
                    x = data['left'][i]
                    y = data['top'][i]
                    w = data['width'][i]
                    h = data['height'][i]
                    conf = data['conf'][i]
                    
                    if conf > 30:  # Confidence threshold
                        text_regions.append({
                            'text': text,
                            'x': x,
                            'y': y,
                            'width': w,
                            'height': h,
                            'confidence': conf,
                            'center': (x + w//2, y + h//2)
                        })
            
            return text_regions
        except Exception as e:
            print(f"OCR Error: {e}")
            return []
    
    def detect_buttons(self, image):
        """Detect button-like elements using edge detection"""
        print("Detecting button elements...")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        buttons = []
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size and aspect ratio (typical button dimensions)
            if 80 < w < 200 and 20 < h < 60:
                aspect_ratio = w / h
                if 1.5 < aspect_ratio < 5:
                    buttons.append({
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h,
                        'center': (x + w//2, y + h//2)
                    })
        
        return buttons
    
    def find_player_positions(self, text_regions):
        """Identify player name positions"""
        print("Identifying player positions...")
        player_positions = []
        
        # Look for "Player" patterns
        player_pattern = re.compile(r'player\s*\d+|p\d+', re.IGNORECASE)
        
        for region in text_regions:
            if player_pattern.match(region['text'].lower()):
                player_positions.append({
                    'label': region['text'],
                    'x': region['center'][0],
                    'y': region['center'][1],
                    'bounds': (region['x'], region['y'], region['width'], region['height'])
                })
        
        # Sort by position (left to right, top to bottom)
        player_positions.sort(key=lambda p: (p['y'], p['x']))
        
        return player_positions
    
    def find_chip_input_positions(self, image, player_positions):
        """Find chip input fields based on player positions"""
        print("Finding chip input positions...")
        chip_positions = []
        
        # For each player, look for input field below
        for player in player_positions:
            # Search region below player name
            search_y_start = player['y'] + 50
            search_y_end = player['y'] + 250
            search_x_start = player['x'] - 50
            search_x_end = player['x'] + 50
            
            # Look for numeric text or input field patterns
            roi = image[max(0, search_y_start):min(image.shape[0], search_y_end),
                       max(0, search_x_start):min(image.shape[1], search_x_end)]
            
            if roi.size > 0:
                # Detect edges in ROI
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray_roi, 30, 100)
                
                # Find contours that might be input fields
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    # Check if it looks like an input field
                    if 40 < w < 150 and 15 < h < 40:
                        chip_positions.append({
                            'player': player['label'],
                            'x': search_x_start + x + w//2,
                            'y': search_y_start + y + h//2,
                            'bounds': (search_x_start + x, search_y_start + y, w, h)
                        })
                        break
        
        return chip_positions
    
    def analyze_layout(self, image):
        """Comprehensive layout analysis"""
        print("Performing comprehensive layout analysis...")
        
        # Detect all text regions
        text_regions = self.detect_text_regions(image)
        
        # Detect button-like elements
        buttons = self.detect_buttons(image)
        
        # Find player positions
        player_positions = self.find_player_positions(text_regions)
        
        # Find chip input positions
        chip_positions = self.find_chip_input_positions(image, player_positions)
        
        # Store detected positions
        self.detected_positions['player_names'] = player_positions
        self.detected_positions['chip_inputs'] = chip_positions
        self.detected_positions['buttons'] = buttons
        self.detected_positions['text_regions'] = text_regions
        
        return self.detected_positions
    
    def visualize_detection(self, image, positions):
        """Create annotated image showing detected positions"""
        print("Creating visualization...")
        
        # Convert to PIL for drawing
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # Draw player positions
        for i, player in enumerate(positions.get('player_names', [])):
            x, y = player['x'], player['y']
            # Draw crosshair
            draw.line([(x-15, y), (x+15, y)], fill="red", width=2)
            draw.line([(x, y-15), (x, y+15)], fill="red", width=2)
            # Draw label
            draw.text((x+20, y-10), f"P{i+1}", fill="red")
            # Draw bounding box
            if 'bounds' in player:
                bx, by, bw, bh = player['bounds']
                draw.rectangle([bx, by, bx+bw, by+bh], outline="red", width=2)
        
        # Draw chip positions
        for chip in positions.get('chip_inputs', []):
            x, y = chip['x'], chip['y']
            # Draw crosshair
            draw.line([(x-15, y), (x+15, y)], fill="blue", width=2)
            draw.line([(x, y-15), (x, y+15)], fill="blue", width=2)
            # Draw label
            draw.text((x+20, y-10), "Chip", fill="blue")
            # Draw bounding box
            if 'bounds' in chip:
                bx, by, bw, bh = chip['bounds']
                draw.rectangle([bx, by, bx+bw, by+bh], outline="blue", width=2)
        
        # Draw detected buttons
        for button in positions.get('buttons', [])[:20]:  # Limit to 20 to avoid clutter
            x, y, w, h = button['x'], button['y'], button['width'], button['height']
            draw.rectangle([x, y, x+w, y+h], outline="green", width=1)
        
        return img_pil
    
    def save_positions(self, filename="detected_positions.json"):
        """Save detected positions to JSON file"""
        # Convert to serializable format
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'player_names': [
                {
                    'label': p['label'],
                    'x': p['x'],
                    'y': p['y']
                } for p in self.detected_positions.get('player_names', [])
            ],
            'chip_inputs': [
                {
                    'player': c['player'],
                    'x': c['x'],
                    'y': c['y']
                } for c in self.detected_positions.get('chip_inputs', [])
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"Positions saved to {filename}")
    
    def detect_by_template_matching(self, image, template_path):
        """Alternative method using template matching"""
        print("Attempting template matching...")
        
        try:
            # Load template
            template = cv2.imread(template_path, 0)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Perform template matching
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            
            # Find locations with high correlation
            threshold = 0.7
            locations = np.where(result >= threshold)
            
            matches = []
            for pt in zip(*locations[::-1]):
                matches.append({
                    'x': pt[0] + template.shape[1]//2,
                    'y': pt[1] + template.shape[0]//2,
                    'confidence': result[pt[1], pt[0]]
                })
            
            return matches
        except Exception as e:
            print(f"Template matching error: {e}")
            return []
    
    def run_detection(self):
        """Main detection workflow"""
        print("Starting Action Tracker position detection...")
        
        # Capture screenshot
        screenshot_pil, screenshot_cv = self.capture_screenshot()
        
        # Analyze layout
        positions = self.analyze_layout(screenshot_cv)
        
        # Create visualization
        annotated_image = self.visualize_detection(screenshot_cv, positions)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save annotated image
        annotated_filename = f"action_tracker_detected_{timestamp}.png"
        annotated_image.save(annotated_filename)
        print(f"Annotated image saved: {annotated_filename}")
        
        # Save positions JSON
        json_filename = f"positions_{timestamp}.json"
        self.save_positions(json_filename)
        
        # Print summary
        print("\n=== Detection Summary ===")
        print(f"Player positions found: {len(positions.get('player_names', []))}")
        print(f"Chip input positions found: {len(positions.get('chip_inputs', []))}")
        print(f"Button elements found: {len(positions.get('buttons', []))}")
        print(f"Text regions found: {len(positions.get('text_regions', []))}")
        
        if positions.get('player_names'):
            print("\nDetected Player Positions:")
            for i, player in enumerate(positions['player_names'], 1):
                print(f"  Player {i}: ({player['x']}, {player['y']}) - {player['label']}")
        
        if positions.get('chip_inputs'):
            print("\nDetected Chip Input Positions:")
            for chip in positions['chip_inputs']:
                print(f"  {chip['player']}: ({chip['x']}, {chip['y']})")
        
        return positions

def main():
    """Main execution"""
    detector = ActionTrackerPositionDetector()
    
    # Note: pytesseract requires Tesseract-OCR to be installed
    # Set the tesseract path if needed
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    try:
        positions = detector.run_detection()
        
        if positions['player_names'] or positions['chip_inputs']:
            print("\nPosition detection successful!")
            print("You can now use the detected positions in your automation script.")
        else:
            print("\nNo positions detected. Please ensure Action Tracker is visible on screen.")
            print("You may need to adjust detection parameters or use template matching.")
            
    except Exception as e:
        print(f"Error during detection: {e}")
        print("Make sure Action Tracker is running and visible.")

if __name__ == "__main__":
    main()