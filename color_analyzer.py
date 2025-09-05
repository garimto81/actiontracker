"""
Analyze colors in Action Tracker screenshot to determine proper detection ranges
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image
import time

def analyze_colors():
    """Analyze colors in the current screenshot"""
    print("Taking screenshot for color analysis...")
    time.sleep(2)
    
    screenshot = pyautogui.screenshot()
    img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Save the screenshot
    screenshot.save("color_analysis_screenshot.png")
    
    # Convert to HSV
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    
    # Analyze specific regions where we expect player buttons
    # Based on the previous screenshot, player buttons are around y=180
    player_row_y = 180
    chip_row_y = 310
    
    print("Analyzing player button colors...")
    
    # Sample colors from player button area
    player_colors_bgr = []
    player_colors_hsv = []
    
    # Sample from multiple player button positions
    for x in range(100, 900, 80):  # Approximate x positions of player buttons
        y = player_row_y
        if y < img_cv.shape[0] and x < img_cv.shape[1]:
            bgr_color = img_cv[y, x]
            hsv_color = hsv[y, x]
            player_colors_bgr.append(bgr_color)
            player_colors_hsv.append(hsv_color)
    
    print("Player button colors (BGR):")
    for i, color in enumerate(player_colors_bgr):
        print(f"  Sample {i+1}: {color}")
    
    print("Player button colors (HSV):")
    for i, color in enumerate(player_colors_hsv):
        print(f"  Sample {i+1}: {color}")
    
    # Analyze chip button colors
    print("\nAnalyzing chip button colors...")
    
    chip_colors_bgr = []
    chip_colors_hsv = []
    
    for x in range(100, 900, 80):
        y = chip_row_y
        if y < img_cv.shape[0] and x < img_cv.shape[1]:
            bgr_color = img_cv[y, x]
            hsv_color = hsv[y, x]
            chip_colors_bgr.append(bgr_color)
            chip_colors_hsv.append(hsv_color)
    
    print("Chip button colors (BGR):")
    for i, color in enumerate(chip_colors_bgr):
        print(f"  Sample {i+1}: {color}")
    
    print("Chip button colors (HSV):")
    for i, color in enumerate(chip_colors_hsv):
        print(f"  Sample {i+1}: {color}")
    
    # Calculate average colors and suggest ranges
    if player_colors_hsv:
        player_h_values = [c[0] for c in player_colors_hsv if c[1] > 50]  # Filter out low saturation
        if player_h_values:
            avg_player_h = np.mean(player_h_values)
            print(f"\nPlayer button average Hue: {avg_player_h}")
            print(f"Suggested player range: H={max(0, avg_player_h-20)} to {min(180, avg_player_h+20)}")
    
    if chip_colors_hsv:
        chip_h_values = [c[0] for c in chip_colors_hsv if c[1] > 50]
        if chip_h_values:
            avg_chip_h = np.mean(chip_h_values)
            print(f"\nChip button average Hue: {avg_chip_h}")
            print(f"Suggested chip range: H={max(0, avg_chip_h-15)} to {min(180, avg_chip_h+15)}")
    
    # Create a visualization of sampled colors
    create_color_visualization(player_colors_bgr, chip_colors_bgr)
    
    return player_colors_hsv, chip_colors_hsv

def create_color_visualization(player_colors, chip_colors):
    """Create a visualization of sampled colors"""
    # Create color palette image
    palette_height = 100
    palette_width = max(len(player_colors), len(chip_colors)) * 50 + 50
    
    palette = np.ones((palette_height * 2, palette_width, 3), dtype=np.uint8) * 255
    
    # Draw player colors in top half
    for i, color in enumerate(player_colors):
        x_start = i * 50 + 10
        x_end = x_start + 40
        palette[10:palette_height-10, x_start:x_end] = color
    
    # Draw chip colors in bottom half
    for i, color in enumerate(chip_colors):
        x_start = i * 50 + 10
        x_end = x_start + 40
        palette[palette_height+10:palette_height*2-10, x_start:x_end] = color
    
    # Convert BGR to RGB for PIL
    palette_rgb = cv2.cvtColor(palette, cv2.COLOR_BGR2RGB)
    palette_img = Image.fromarray(palette_rgb)
    
    # Save the color palette
    palette_img.save("color_palette.png")
    print("\nColor palette saved as color_palette.png")

if __name__ == "__main__":
    player_colors, chip_colors = analyze_colors()
    print("\nColor analysis complete!")
    print("Check color_analysis_screenshot.png and color_palette.png")