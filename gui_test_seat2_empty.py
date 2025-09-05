"""
GUI Test - Seat 2 Empty Scenario
2번 자리 비어있는 시나리오 GUI 테스트
"""

import tkinter as tk
from integrated_gui_final import IntegratedActionTrackerGUI
import threading
import time

def setup_test_scenario(app):
    """Setup test scenario with seat 2 empty"""
    time.sleep(1.5)  # Wait for GUI
    
    print("\n" + "="*60)
    print("SETTING UP TEST SCENARIO - SEAT 2 EMPTY")
    print("="*60)
    
    # Clear all first
    for seat in range(1, 11):
        app.player_names[seat].delete(0, tk.END)
        app.chip_amounts[seat].delete(0, tk.END)
        app.empty_seats[seat].set(False)
        app.delete_players[seat].set(False)
    
    # Setup occupied seats (1, 3-10)
    occupied_data = {
        1: ("Phil Ivey", "1500000"),
        3: ("Daniel Negreanu", "1200000"),
        4: ("Doyle Brunson", "980000"),
        5: ("Tom Dwan", "620000"),
        6: ("Patrik Antonius", "540000"),
        7: ("Gus Hansen", "480000"),
        8: ("Vanessa Selbst", "890000"),
        9: ("Erik Seidel", "670000"),
        10: ("Johnny Chan", "1100000")
    }
    
    print("\n[OCCUPIED SEATS] Setting up existing players:")
    for seat, (name, chips) in occupied_data.items():
        app.player_names[seat].insert(0, name)
        app.chip_amounts[seat].insert(0, chips)
        app.seat_status_labels[seat].config(text="🔴 Occupied")
        app.empty_seats[seat].set(False)
        print(f"  Seat {seat}: {name} ({int(chips):,} chips)")
    
    # Setup empty seat 2
    print("\n[EMPTY SEAT] Setting up new player for registration:")
    app.player_names[2].insert(0, "Phil Hellmuth")
    app.chip_amounts[2].insert(0, "750000")
    app.seat_status_labels[2].config(text="⚪ Empty")
    app.empty_seats[2].set(False)  # Has data but needs registration
    print(f"  Seat 2: Phil Hellmuth (750,000 chips) - TO BE REGISTERED")
    
    # Log in GUI
    app.log("="*50)
    app.log("TEST SCENARIO LOADED")
    app.log("="*50)
    app.log("Seats 1,3-10: Existing players (UPDATE)")
    app.log("Seat 2: New player (REGISTER)")
    app.log("")
    app.log("Click 'UPDATE ALL' to:")
    app.log("1. Update 9 existing names")
    app.log("2. Register 1 new name (Seat 2)")
    app.log("3. Input chips for all 10 players")
    app.log("")
    app.log("Watch the Activity Log for progress...")
    
    print("\n" + "="*60)
    print("TEST SCENARIO READY!")
    print("="*60)
    print("\nINSTRUCTIONS:")
    print("1. Click 'UPDATE ALL' button to process all players")
    print("2. Watch the Activity Log for detailed progress")
    print("3. The process will:")
    print("   - Update 9 existing player names (6-step process each)")
    print("   - Register 1 new player in Seat 2 (3-step process)")
    print("   - Input chips for all 10 players")
    print("\nEstimated time: ~43 seconds")
    print("\n[IMPORTANT] Make sure Action Tracker is open and visible!")

def main():
    print("="*70)
    print("ACTION TRACKER GUI TEST - SEAT 2 EMPTY SCENARIO")
    print("="*70)
    print("This test will simulate a real table with Seat 2 empty")
    print("="*70)
    
    # Create GUI
    root = tk.Tk()
    root.title("Action Tracker - Test Scenario (Seat 2 Empty)")
    app = IntegratedActionTrackerGUI(root)
    
    # Setup test scenario in background
    setup_thread = threading.Thread(target=setup_test_scenario, args=(app,))
    setup_thread.daemon = True
    setup_thread.start()
    
    # Start GUI
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[TEST] Terminated by user")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")

if __name__ == "__main__":
    main()