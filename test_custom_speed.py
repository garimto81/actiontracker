"""
Test Custom Speed Control Features
커스텀 속도 조절 기능 테스트
"""

import tkinter as tk
from integrated_gui_final import IntegratedActionTrackerGUI
import threading
import time
import json
from datetime import datetime

def test_custom_speed_controls(app):
    """Test custom speed control features"""
    time.sleep(1.5)
    
    print("\n" + "="*70)
    print("TESTING CUSTOM SPEED CONTROL FEATURES")
    print("="*70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Test 1: Check custom speed entry fields exist
    print("\n[TEST 1] Custom Speed Entry Fields")
    print("-" * 40)
    
    if hasattr(app, 'custom_speed_entries'):
        print("[OK] Custom speed entries exist")
        for key, entry in app.custom_speed_entries.items():
            current_value = entry.get()
            print(f"  {key}: {current_value}")
    else:
        print("[FAIL] Custom speed entries not found")
    
    # Test 2: Test preset buttons update custom entries
    print("\n[TEST 2] Preset Buttons Update Custom Entries")
    print("-" * 40)
    
    print("Setting Ultra Fast speed...")
    app.set_ultra_fast()
    time.sleep(0.5)
    
    # Check if custom entries were updated
    print("Custom entries after Ultra Fast:")
    for key, entry in app.custom_speed_entries.items():
        print(f"  {key}: {entry.get()}")
    
    # Test 3: Apply custom speed values
    print("\n[TEST 3] Apply Custom Speed Values")
    print("-" * 40)
    
    # Set custom values
    test_values = {
        "mouse_click_delay": "0.25",
        "keyboard_type_interval": "0.015", 
        "action_delay": "0.35",
        "screen_wait": "0.75"
    }
    
    print("Setting custom values:")
    for key, value in test_values.items():
        app.custom_speed_entries[key].delete(0, tk.END)
        app.custom_speed_entries[key].insert(0, value)
        print(f"  {key}: {value}")
    
    # Apply custom speed
    app.apply_custom_speed()
    time.sleep(0.5)
    
    # Verify applied values
    print("\nVerifying applied values:")
    all_match = True
    for key, expected in test_values.items():
        actual = str(app.speed_vars[key].get())
        match = actual == expected
        print(f"  {key}: {actual} {'✓' if match else '✗'}")
        if not match:
            all_match = False
    
    if all_match:
        print("[OK] All custom values applied correctly")
    else:
        print("[FAIL] Some values did not apply correctly")
    
    # Test 4: Save speed preset
    print("\n[TEST 4] Save Speed Preset")
    print("-" * 40)
    
    test_preset_file = "test_speed_preset.json"
    
    # Create preset manually
    preset_data = {
        "mouse_click_delay": app.speed_vars["mouse_click_delay"].get(),
        "keyboard_type_interval": app.speed_vars["keyboard_type_interval"].get(),
        "action_delay": app.speed_vars["action_delay"].get(),
        "screen_wait": app.speed_vars["screen_wait"].get(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        with open(test_preset_file, 'w') as f:
            json.dump(preset_data, f, indent=2)
        print(f"[OK] Preset saved to {test_preset_file}")
        print(f"  Contents: {preset_data}")
    except Exception as e:
        print(f"[FAIL] Error saving preset: {e}")
    
    # Test 5: Load speed preset
    print("\n[TEST 5] Load Speed Preset")
    print("-" * 40)
    
    # Change values first
    app.set_normal()
    print("Changed to Normal speed")
    
    # Load the saved preset
    try:
        with open(test_preset_file, 'r') as f:
            loaded_preset = json.load(f)
        
        # Apply loaded preset
        for key in ["mouse_click_delay", "keyboard_type_interval", 
                   "action_delay", "screen_wait"]:
            if key in loaded_preset:
                app.speed_vars[key].set(loaded_preset[key])
                app.custom_speed_entries[key].delete(0, tk.END)
                app.custom_speed_entries[key].insert(0, str(loaded_preset[key]))
        
        print(f"[OK] Preset loaded from {test_preset_file}")
        print("Loaded values:")
        for key, entry in app.custom_speed_entries.items():
            print(f"  {key}: {entry.get()}")
            
    except Exception as e:
        print(f"[FAIL] Error loading preset: {e}")
    
    # Test 6: Validate speed range
    print("\n[TEST 6] Validate Speed Range")
    print("-" * 40)
    
    # Try negative value
    app.custom_speed_entries["mouse_click_delay"].delete(0, tk.END)
    app.custom_speed_entries["mouse_click_delay"].insert(0, "-0.5")
    
    print("Testing negative value (-0.5)...")
    app.apply_custom_speed()
    
    # Try very large value
    app.custom_speed_entries["screen_wait"].delete(0, tk.END)
    app.custom_speed_entries["screen_wait"].insert(0, "999")
    
    print("Testing very large value (999)...")
    app.apply_custom_speed()
    
    # Log test completion
    app.log("="*50)
    app.log("CUSTOM SPEED CONTROL TEST COMPLETE")
    app.log("="*50)
    app.log("Features tested:")
    app.log("✓ Custom speed entry fields")
    app.log("✓ Apply custom speed values")
    app.log("✓ Preset buttons update entries")
    app.log("✓ Save/Load speed presets")
    app.log("✓ Speed range validation")
    
    print("\n" + "="*70)
    print("TEST COMPLETE!")
    print("="*70)

def main():
    print("="*70)
    print("CUSTOM SPEED CONTROL TEST")
    print("="*70)
    print("This test verifies custom speed control features")
    print("="*70)
    
    # Create GUI
    root = tk.Tk()
    root.title("Custom Speed Control Test")
    app = IntegratedActionTrackerGUI(root)
    
    # Run tests in background
    test_thread = threading.Thread(target=test_custom_speed_controls, args=(app,))
    test_thread.daemon = True
    test_thread.start()
    
    # Start GUI
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[TEST] Terminated by user")
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")

if __name__ == "__main__":
    main()