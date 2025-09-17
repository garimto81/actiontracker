"""
Test GUI Functionality
GUI 기능 테스트 및 디버깅
"""

import tkinter as tk
from integrated_gui_final import IntegratedActionTrackerGUI
import time

def test_gui():
    """Test the GUI without actual automation"""
    print("=" * 60)
    print("GUI FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Create root window
    root = tk.Tk()
    app = IntegratedActionTrackerGUI(root)
    
    # Simulate data entry
    print("\n1. Setting test data...")
    
    # Set some test names
    app.name_entries[1].insert(0, "Test Player 1")
    app.name_entries[2].insert(0, "Test Player 2")
    app.name_entries[3].insert(0, "Test Player 3")
    
    # Set some chips
    app.chip_entries[1].insert(0, "100000")
    app.chip_entries[2].insert(0, "200000")
    app.chip_entries[3].insert(0, "300000")
    
    # Mark seat 1-2 as occupied, 3 as empty
    app.empty_seats[1].set(False)
    app.empty_seats[2].set(False)
    app.empty_seats[3].set(True)
    
    print("2. Data set successfully")
    print("   - Seat 1: Test Player 1 (100000 chips)")
    print("   - Seat 2: Test Player 2 (200000 chips)")
    print("   - Seat 3: Empty")
    
    # Check speed vars
    print("\n3. Speed variables check:")
    for key, var in app.speed_vars.items():
        try:
            value = var.get()
            print(f"   - {key}: {value}")
        except Exception as e:
            print(f"   - {key}: ERROR - {e}")
    
    # Test coordination
    print("\n4. Coordinates check:")
    from integrated_gui_final import PLAYER_COORDS, CHIP_COORDS, SUB_NAME_FIELD, COMPLETE_BUTTON
    
    print(f"   - PLAYER_COORDS[1]: {PLAYER_COORDS.get(1, 'NOT FOUND')}")
    print(f"   - CHIP_COORDS[1]: {CHIP_COORDS.get(1, 'NOT FOUND')}")
    print(f"   - SUB_NAME_FIELD: {SUB_NAME_FIELD}")
    print(f"   - COMPLETE_BUTTON: {COMPLETE_BUTTON}")
    
    print("\n5. GUI is ready for testing")
    print("   - Click 'UPDATE NAMES ONLY' to test name updates")
    print("   - Check the Activity Log for debug messages")
    print("   - Press Ctrl+C to exit")
    
    # Start the GUI
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nTest terminated by user")
    except Exception as e:
        print(f"\nError during test: {e}")

if __name__ == "__main__":
    test_gui()