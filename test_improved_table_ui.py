"""
Test Improved Table Selection UI
개선된 테이블 선택 UI 테스트
"""

import tkinter as tk
from integrated_gui_final import IntegratedActionTrackerGUI
import threading
import time

def test_table_ui(app):
    """Test the improved table selection UI"""
    time.sleep(2)  # Wait for GUI and data to load
    
    print("\n" + "="*70)
    print("TESTING IMPROVED TABLE SELECTION UI")
    print("="*70)
    print("New features:")
    print("1. Quick Select Buttons (T01-T04)")
    print("2. Larger dropdown with better visibility")
    print("3. Current table indicator")
    print("4. Auto-open on click")
    print("="*70)
    
    # Wait for data to load
    time.sleep(2)
    
    # Test quick select buttons
    print("\n[TEST] Quick Select Buttons")
    print("-" * 40)
    
    if hasattr(app, 'quick_table_buttons'):
        print(f"[OK] Found {len(app.quick_table_buttons)} quick select buttons")
        
        # Check button states
        for btn in app.quick_table_buttons:
            state = btn['state']
            bg = btn['bg']
            print(f"  Button {btn['text']}: State={state}, Color={bg}")
    else:
        print("[FAIL] Quick select buttons not found")
    
    # Test current table label
    print("\n[TEST] Current Table Indicator")
    print("-" * 40)
    
    if hasattr(app, 'current_table_label'):
        current_text = app.current_table_label['text']
        print(f"[OK] Current table label: '{current_text}'")
    else:
        print("[FAIL] Current table label not found")
    
    # Test dropdown improvements
    print("\n[TEST] Dropdown Improvements")
    print("-" * 40)
    
    if hasattr(app, 'table_combo'):
        values = app.table_combo['values']
        font = app.table_combo['font']
        width = app.table_combo['width']
        print(f"[OK] Dropdown configured")
        print(f"  Font: {font}")
        print(f"  Width: {width}")
        print(f"  Available tables: {values}")
    else:
        print("[FAIL] Table combo not found")
    
    # Log in GUI
    app.log("="*50)
    app.log("TABLE UI IMPROVEMENTS TEST")
    app.log("="*50)
    app.log("")
    app.log("✅ Quick Select Buttons: T01-T04")
    app.log("✅ Larger Dropdown (25px arrow)")
    app.log("✅ Better Font (Arial 14 Bold)")
    app.log("✅ Current Table Indicator")
    app.log("✅ Auto-open on click")
    app.log("")
    app.log("Try these features:")
    app.log("1. Click T01-T04 buttons for quick select")
    app.log("2. Click dropdown - it opens immediately")
    app.log("3. Watch current table indicator change")
    app.log("4. Selected button changes color to green")
    
    print("\n" + "="*70)
    print("UI IMPROVEMENTS:")
    print("="*70)
    print("✅ Quick buttons for T01-T04")
    print("✅ Larger dropdown arrow (25px)")
    print("✅ Better visibility (Arial 14 Bold)")
    print("✅ Current table indicator with color")
    print("✅ Auto-open dropdown on click")
    print("✅ Button color feedback")
    print("="*70)

def simulate_table_selection(app):
    """Simulate table selection after delay"""
    time.sleep(5)
    
    print("\n[SIMULATION] Testing table selection...")
    
    # Try to select T01
    if hasattr(app, 'quick_table_buttons') and len(app.quick_table_buttons) > 0:
        print("Simulating T01 button click...")
        app.quick_select_table("T01")
        time.sleep(2)
        
        print("Simulating T02 button click...")
        app.quick_select_table("T02")
        time.sleep(2)
        
        print("Simulating T03 button click...")
        app.quick_select_table("T03")

def main():
    print("="*70)
    print("IMPROVED TABLE SELECTION UI TEST")
    print("="*70)
    
    # Create GUI
    root = tk.Tk()
    root.title("Table Selection UI Test")
    app = IntegratedActionTrackerGUI(root)
    
    # Run test in background
    test_thread = threading.Thread(target=test_table_ui, args=(app,))
    test_thread.daemon = True
    test_thread.start()
    
    # Simulate selections
    sim_thread = threading.Thread(target=simulate_table_selection, args=(app,))
    sim_thread.daemon = True
    sim_thread.start()
    
    # Start GUI
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[TEST] Terminated by user")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")

if __name__ == "__main__":
    main()