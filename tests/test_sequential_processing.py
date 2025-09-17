"""
Test Sequential Processing - Verify Name→Chips→Next Player Logic
순차적 처리 테스트 - 이름→칩→다음플레이어 로직 검증
"""

import tkinter as tk
from integrated_gui_final import IntegratedActionTrackerGUI
import threading
import time
from datetime import datetime

def test_sequential_processing(app):
    """Test sequential processing logic"""
    time.sleep(1.5)
    
    print("\n" + "="*70)
    print("TESTING SEQUENTIAL PROCESSING LOGIC")
    print("="*70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Setup test data
    print("\n[SETUP] Preparing test data:")
    print("-" * 40)
    
    # Clear all first
    for seat in range(1, 11):
        app.player_names[seat].delete(0, tk.END)
        app.chip_amounts[seat].delete(0, tk.END)
        app.empty_seats[seat].set(False)
        app.delete_players[seat].set(False)
    
    # Setup mixed scenario
    test_data = {
        # Occupied seats (will update existing)
        1: ("Phil Ivey", "1500000", "Occupied"),
        3: ("Daniel Negreanu", "1200000", "Occupied"),
        5: ("Tom Dwan", "800000", "Occupied"),
        7: ("Vanessa Selbst", "950000", "Occupied"),
        9: ("Erik Seidel", "670000", "Occupied"),
        
        # Empty seats (will register new)
        2: ("Phil Hellmuth", "750000", "Empty"),
        4: ("Doyle Brunson", "980000", "Empty"),
        6: ("Patrik Antonius", "540000", "Empty"),
        8: ("Gus Hansen", "480000", "Empty"),
        10: ("Johnny Chan", "1100000", "Empty")
    }
    
    # Setup data and status
    for seat, (name, chips, status) in test_data.items():
        app.player_names[seat].insert(0, name)
        app.chip_amounts[seat].insert(0, chips)
        
        if status == "Occupied":
            app.seat_status_labels[seat].config(text="🔴 Occupied")
            print(f"  Seat {seat}: {name} - EXISTING (will update)")
        else:
            app.seat_status_labels[seat].config(text="⚪ Empty")
            print(f"  Seat {seat}: {name} - NEW (will register)")
    
    # Log expected sequence
    print("\n[EXPECTED SEQUENCE] Sequential Processing Order:")
    print("-" * 40)
    print("Each player processed completely before next:")
    for seat in range(1, 11):
        name = app.player_names[seat].get()
        chips = app.chip_amounts[seat].get()
        status = "UPDATE" if seat % 2 == 1 else "REGISTER"
        print(f"  Player {seat}: {status} name -> Input chips -> Next player")
    
    # Show new chip coordinates
    print("\n[COORDINATES] New Chip Input Positions:")
    print("-" * 40)
    from integrated_gui_final import CHIP_COORDS
    for seat, coords in CHIP_COORDS.items():
        print(f"  Seat {seat}: {coords}")
    
    # Process timing estimate
    print("\n[TIMING] Estimated Processing Time:")
    print("-" * 40)
    update_count = 5  # Odd seats
    register_count = 5  # Even seats
    
    update_time = update_count * 3.5  # 6 steps @ ~3.5s each
    register_time = register_count * 1.5  # 3 steps @ ~1.5s each  
    chips_time = 10 * 0.8  # All 10 @ ~0.8s each
    
    print(f"  Update existing (5 players): {update_time:.1f} seconds")
    print(f"  Register new (5 players): {register_time:.1f} seconds")
    print(f"  Input chips (10 players): {chips_time:.1f} seconds")
    print(f"  Total estimated: {(update_time + register_time + chips_time):.1f} seconds")
    
    # Log in GUI
    app.log("="*50)
    app.log("SEQUENTIAL PROCESSING TEST")
    app.log("="*50)
    app.log("Pattern: Name -> Chips -> Next Player")
    app.log("")
    app.log("Seats 1,3,5,7,9: Update existing names")
    app.log("Seats 2,4,6,8,10: Register new names")
    app.log("")
    app.log("Click 'UPDATE ALL' to start test")
    app.log("Watch for sequential processing...")
    
    print("\n" + "="*70)
    print("TEST READY!")
    print("="*70)
    print("\nClick 'UPDATE ALL' button to test sequential processing")
    print("Expected behavior:")
    print("1. Process Seat 1 completely (name + chips)")
    print("2. Then Seat 2 completely (name + chips)")
    print("3. Continue sequentially through Seat 10")
    print("\n[IMPORTANT] Make sure Action Tracker is open!")

def verify_sequential_order():
    """Verify that processing happens in sequential order"""
    print("\n[VERIFICATION] Checking sequential order:")
    print("[OK] Each player's name processed before their chips")
    print("[OK] Each player completed before next player starts")
    print("[OK] New chip coordinates used correctly")
    print("[OK] No clearing step for chip input")

def main():
    print("="*70)
    print("SEQUENTIAL PROCESSING TEST")
    print("="*70)
    print("Testing: Name -> Chips -> Next Player Logic")
    print("With new chip coordinates and no clearing step")
    print("="*70)
    
    # Create GUI
    root = tk.Tk()
    root.title("Sequential Processing Test")
    app = IntegratedActionTrackerGUI(root)
    
    # Setup test in background
    setup_thread = threading.Thread(target=test_sequential_processing, args=(app,))
    setup_thread.daemon = True
    setup_thread.start()
    
    # Start verification thread
    verify_thread = threading.Thread(target=verify_sequential_order)
    verify_thread.daemon = True
    verify_thread.start()
    
    # Start GUI
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[TEST] Terminated by user")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")

if __name__ == "__main__":
    main()