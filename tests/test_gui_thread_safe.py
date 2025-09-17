"""
Thread-safe GUI 테스트
수정된 integrated_gui_final_FINAL.py 실행
"""

import sys
import os

# Add the directory to path
sys.path.insert(0, r'C:\claude02\ActionTracker_Automation')

def run_app():
    """Run the fixed GUI application"""
    try:
        print("Starting Action Tracker GUI - Thread Safe Version")
        print("=" * 60)
        
        # Import after path is set
        import tkinter as tk
        from integrated_gui_final_FINAL import IntegratedActionTrackerGUI
        
        # Create root window
        root = tk.Tk()
        
        # Create app
        app = IntegratedActionTrackerGUI(root)
        
        print("GUI launched successfully!")
        print("\nFeatures fixed:")
        print("1. Thread-safe logging with queue")
        print("2. Thread-safe status label updates")
        print("3. Chip input: Click player name -> Type chips -> Press Enter")
        print("\nCoordinates being used:")
        print("- Player names: (233,361), (374,359), etc.")
        print("- Chip input: Uses PLAYER_COORDS, not CHIP_COORDS")
        print("\nReady to use!")
        print("=" * 60)
        
        # Run the app
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_app()