"""
Test with Sample Data in GUI
샘플 데이터로 GUI 테스트
"""

import tkinter as tk
from integrated_gui_final import IntegratedActionTrackerGUI
import threading
import time

def auto_fill_test_data(app):
    """Auto fill test data after GUI loads"""
    time.sleep(1)  # Wait for GUI to load
    
    print("[TEST] Starting auto-fill test data...")
    
    # Fill player names for seats 1-3
    app.player_names[1].insert(0, "Phil Ivey")
    app.player_names[2].insert(0, "Daniel Negreanu")
    app.player_names[3].insert(0, "Tom Dwan")
    
    # Fill chips
    app.chip_amounts[1].insert(0, "1500000")
    app.chip_amounts[2].insert(0, "1200000")  
    app.chip_amounts[3].insert(0, "800000")
    
    # Mark seats 1-2 as occupied (existing names)
    app.seat_status_labels[1].config(text="🔴 Occupied")
    app.seat_status_labels[2].config(text="🔴 Occupied")
    
    # Mark seat 3 as empty (new name to register)
    app.seat_status_labels[3].config(text="⚪ Empty")
    
    # Uncheck empty checkboxes for seats with data
    app.empty_seats[1].set(False)
    app.empty_seats[2].set(False)
    app.empty_seats[3].set(False)
    
    print("[TEST] Test data filled:")
    print("  Seat 1: Phil Ivey (1,500,000) - Occupied")
    print("  Seat 2: Daniel Negreanu (1,200,000) - Occupied")
    print("  Seat 3: Tom Dwan (800,000) - Empty (will register)")
    print()
    print("[TEST] Ready for testing!")
    print("  1. Click 'UPDATE NAMES ONLY' to test name updates")
    print("  2. Click 'UPDATE CHIPS ONLY' to test chip updates")
    print("  3. Click 'UPDATE ALL' to test complete update")
    print()
    print("[TEST] Check Activity Log for debug messages")

def main():
    print("="*60)
    print("GUI TEST WITH SAMPLE DATA")
    print("="*60)
    
    # Create GUI
    root = tk.Tk()
    app = IntegratedActionTrackerGUI(root)
    
    # Auto-fill test data in background
    fill_thread = threading.Thread(target=auto_fill_test_data, args=(app,))
    fill_thread.daemon = True
    fill_thread.start()
    
    # Log initial message
    app.log("=== TEST MODE ===")
    app.log("Sample data will be auto-filled")
    app.log("Seats 1-2: Existing players (update)")
    app.log("Seat 3: New player (register)")
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()