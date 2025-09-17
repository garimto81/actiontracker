"""
Simple analysis tool for player name edit screen
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageDraw
import time

def analyze_edit_screen():
    """Analyze the current edit screen"""
    print("Taking screenshot in 3 seconds...")
    time.sleep(3)
    
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save("edit_screen_capture.png")
    print("Screenshot saved: edit_screen_capture.png")
    
    # Convert to OpenCV format
    img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Find white/light areas (likely input fields)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter for input field-like shapes
    input_fields = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        # Look for rectangular input fields
        if 80 < w < 400 and 20 < h < 80 and area > 1000:
            input_fields.append({
                'center_x': x + w//2,
                'center_y': y + h//2,
                'bounds': (x, y, w, h)
            })
    
    # Create visualization
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Draw detected input fields
    for i, field in enumerate(input_fields):
        x, y, w, h = field['bounds']
        draw.rectangle([x, y, x+w, y+h], outline="red", width=3)
        draw.text((x, y-20), f"Input {i+1}", fill="red")
        
        # Draw center cross
        cx, cy = field['center_x'], field['center_y']
        draw.line([(cx-20, cy), (cx+20, cy)], fill="red", width=3)
        draw.line([(cx, cy-20), (cx, cy+20)], fill="red", width=3)
    
    # Save visualization
    img_pil.save("edit_screen_analysis.png")
    print(f"Analysis saved: edit_screen_analysis.png")
    
    # Print results
    print(f"\nDetected {len(input_fields)} input fields:")
    for i, field in enumerate(input_fields):
        print(f"  Field {i+1}: Center({field['center_x']}, {field['center_y']})")
    
    return input_fields

if __name__ == "__main__":
    print("Edit Screen Analyzer")
    print("===================")
    print("Make sure the edit dialog is open, then wait 3 seconds...")
    
    fields = analyze_edit_screen()
    print(f"\nAnalysis complete! Found {len(fields)} input areas.")