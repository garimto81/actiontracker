"""
Quick Test Script for Action Tracker Manager
빠른 테스트 스크립트
"""

from action_tracker_manager import ActionTrackerManager
import time

def test_with_custom_speeds():
    """Test with custom speed settings"""
    
    # Create manager with custom speeds (faster)
    custom_speeds = {
        "mouse_click_delay": 0.2,      # Faster mouse clicks
        "keyboard_type_interval": 0.01, # Faster typing
        "action_delay": 0.3,            # Shorter delays
        "screen_wait": 0.7,             # Shorter screen waits
        "pyautogui_pause": 0.2          # Faster overall
    }
    
    manager = ActionTrackerManager(custom_speeds)
    
    print("="*60)
    print("ACTION TRACKER MANAGER - QUICK TEST")
    print("="*60)
    
    manager.show_speed_settings()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Update Player 1 (existing name)",
            "action": lambda: manager.update_existing_name(1, "Test Player 1")
        },
        {
            "name": "Register Player 5 (empty seat)",
            "action": lambda: manager.register_new_name(5, "Test Player 5")
        },
        {
            "name": "Delete Player 3",
            "action": lambda: manager.delete_player(3)
        },
        {
            "name": "Batch update multiple players",
            "action": lambda: manager.batch_update([
                {"player": 2, "action": "update", "name": "Batch Update 2"},
                {"player": 6, "action": "register", "name": "Batch Register 6"},
                {"player": 7, "action": "register", "name": "Batch Register 7"}
            ])
        }
    ]
    
    print("\nAvailable tests:")
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"{i}. {scenario['name']}")
    
    choice = input("\nSelect test (1-4) or 'all' for all tests: ").strip()
    
    if choice == 'all':
        print("\nRunning all tests in 3 seconds...")
        time.sleep(3)
        for scenario in test_scenarios:
            print(f"\n>>> {scenario['name']}")
            scenario['action']()
            time.sleep(1)
    elif choice.isdigit() and 1 <= int(choice) <= len(test_scenarios):
        scenario = test_scenarios[int(choice) - 1]
        print(f"\nRunning: {scenario['name']}")
        print("Starting in 3 seconds...")
        time.sleep(3)
        scenario['action']()
    else:
        print("Invalid selection")
    
    # Save log
    manager.save_log()
    print("\nTest complete!")

def speed_comparison_test():
    """Compare different speed presets"""
    
    print("="*60)
    print("SPEED COMPARISON TEST")
    print("="*60)
    
    # Speed presets
    speed_presets = {
        "FAST": {
            "mouse_click_delay": 0.1,
            "keyboard_type_interval": 0.005,
            "action_delay": 0.2,
            "screen_wait": 0.5,
            "pyautogui_pause": 0.1
        },
        "NORMAL": {
            "mouse_click_delay": 0.3,
            "keyboard_type_interval": 0.02,
            "action_delay": 0.5,
            "screen_wait": 1.0,
            "pyautogui_pause": 0.3
        },
        "SLOW": {
            "mouse_click_delay": 0.5,
            "keyboard_type_interval": 0.05,
            "action_delay": 1.0,
            "screen_wait": 2.0,
            "pyautogui_pause": 0.5
        }
    }
    
    print("\nSpeed Presets:")
    for name, speeds in speed_presets.items():
        print(f"\n{name}:")
        print(f"  Mouse click delay: {speeds['mouse_click_delay']}s")
        print(f"  Typing interval: {speeds['keyboard_type_interval']}s")
        print(f"  Action delay: {speeds['action_delay']}s")
    
    preset_name = input("\nSelect preset (FAST/NORMAL/SLOW): ").upper()
    
    if preset_name in speed_presets:
        manager = ActionTrackerManager(speed_presets[preset_name])
        print(f"\nUsing {preset_name} preset")
        manager.show_speed_settings()
        
        # Test action
        player = int(input("Player number to test (1-10): "))
        name = input("Test name: ").strip()
        
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        # Time the operation
        import time
        start_time = time.time()
        manager.register_new_name(player, name)
        end_time = time.time()
        
        print(f"\nOperation completed in {end_time - start_time:.2f} seconds")
        manager.save_log()
    else:
        print("Invalid preset")

if __name__ == "__main__":
    print("ACTION TRACKER MANAGER - TEST SUITE")
    print("1. Quick test with custom speeds")
    print("2. Speed comparison test")
    
    choice = input("\nSelect test mode (1-2): ").strip()
    
    if choice == "1":
        test_with_custom_speeds()
    elif choice == "2":
        speed_comparison_test()
    else:
        print("Invalid choice")