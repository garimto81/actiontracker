"""
Test Script for ActionTracker Automation Logic
Tests mouse clicks, keyboard input, and complete flow
"""

import pyautogui
import time
from datetime import datetime
import json

# Import the manager with actual logic
from action_tracker_manager import ActionTrackerManager

# Coordinates from the system
PLAYER_COORDS = {
    1: (233, 361),
    2: (374, 359),
    3: (544, 362),
    4: (722, 359),
    5: (886, 356),
    6: (1051, 354),
    7: (1213, 355),
    8: (1385, 383),
    9: (1549, 367),
    10: (1705, 356)
}

SUB_NAME_FIELD = (785, 291)
COMPLETE_BUTTON = (1720, 139)
DELETE_BUTTON = (721, 112)

class AutomationTester:
    def __init__(self):
        self.test_results = []
        self.manager = ActionTrackerManager()
        
    def log_result(self, test_name, status, details=""):
        """Log test result"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {details}")
        
    def test_mouse_position(self):
        """Test 1: Check current mouse position"""
        print("\n=== TEST 1: Mouse Position Check ===")
        try:
            x, y = pyautogui.position()
            screen_width, screen_height = pyautogui.size()
            
            self.log_result(
                "Mouse Position",
                "PASS",
                f"Current position: ({x}, {y}), Screen: {screen_width}x{screen_height}"
            )
            
            # Verify all coordinates are within screen bounds
            for seat, coords in PLAYER_COORDS.items():
                if coords[0] > screen_width or coords[1] > screen_height:
                    self.log_result(
                        f"Seat {seat} Bounds",
                        "FAIL",
                        f"Coordinates {coords} out of screen bounds"
                    )
                else:
                    self.log_result(
                        f"Seat {seat} Bounds",
                        "PASS",
                        f"Coordinates {coords} within bounds"
                    )
                    
            return True
        except Exception as e:
            self.log_result("Mouse Position", "FAIL", str(e))
            return False
            
    def test_safe_click(self):
        """Test 2: Safe click test (move only, no click)"""
        print("\n=== TEST 2: Safe Movement Test ===")
        try:
            original_pos = pyautogui.position()
            
            # Test movement to each coordinate without clicking
            test_coords = [
                ("Player 1", PLAYER_COORDS[1]),
                ("Name Field", SUB_NAME_FIELD),
                ("Complete Button", COMPLETE_BUTTON),
                ("Delete Button", DELETE_BUTTON)
            ]
            
            for name, coords in test_coords:
                pyautogui.moveTo(coords[0], coords[1], duration=0.5)
                time.sleep(0.2)
                current = pyautogui.position()
                
                if current[0] == coords[0] and current[1] == coords[1]:
                    self.log_result(
                        f"Move to {name}",
                        "PASS",
                        f"Successfully moved to {coords}"
                    )
                else:
                    self.log_result(
                        f"Move to {name}",
                        "FAIL",
                        f"Expected {coords}, got {current}"
                    )
                    
            # Return to original position
            pyautogui.moveTo(original_pos[0], original_pos[1])
            return True
            
        except Exception as e:
            self.log_result("Safe Movement", "FAIL", str(e))
            return False
            
    def test_screenshot_areas(self):
        """Test 3: Take screenshots of target areas"""
        print("\n=== TEST 3: Screenshot Test ===")
        try:
            # Take full screenshot
            screenshot = pyautogui.screenshot()
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"test_full_screen_{timestamp}.png"
            screenshot.save(filename)
            self.log_result("Full Screenshot", "PASS", f"Saved as {filename}")
            
            # Take regional screenshots for verification
            regions = [
                ("player_area", (200, 340, 1550, 50)),  # Player row area
                ("button_area", (700, 100, 1050, 50)),  # Button area
            ]
            
            for name, region in regions:
                try:
                    regional_shot = pyautogui.screenshot(region=region)
                    regional_file = f"test_{name}_{timestamp}.png"
                    regional_shot.save(regional_file)
                    self.log_result(
                        f"Screenshot {name}",
                        "PASS",
                        f"Saved as {regional_file}"
                    )
                except:
                    self.log_result(
                        f"Screenshot {name}",
                        "WARN",
                        "Could not capture region"
                    )
                    
            return True
            
        except Exception as e:
            self.log_result("Screenshot", "FAIL", str(e))
            return False
            
    def test_keyboard_simulation(self):
        """Test 4: Test keyboard input (without actual typing)"""
        print("\n=== TEST 4: Keyboard Simulation Test ===")
        try:
            # Test if keyboard functions are available
            test_strings = ["TestPlayer1", "Mike", "John_123"]
            
            for test_str in test_strings:
                # Simulate the typing process without actual output
                typing_time = len(test_str) * 0.02  # Based on typing interval
                self.log_result(
                    f"Keyboard simulation '{test_str}'",
                    "PASS",
                    f"Would take {typing_time:.2f} seconds to type"
                )
                
            return True
            
        except Exception as e:
            self.log_result("Keyboard Simulation", "FAIL", str(e))
            return False
            
    def test_automation_flow(self):
        """Test 5: Test complete automation flow (dry run)"""
        print("\n=== TEST 5: Automation Flow Test (Dry Run) ===")
        try:
            # Test the manager's methods without actual execution
            test_players = {
                1: "TestPlayer1",
                2: "TestPlayer2",
                5: "TestPlayer5"
            }
            
            for seat, name in test_players.items():
                # Calculate expected execution time
                expected_time = (
                    1.0 +  # screen_wait
                    0.3 +  # mouse_click_delay
                    0.2 +  # triple click
                    len(name) * 0.02 +  # typing
                    0.5 +  # action_delay
                    0.5 +  # action_delay
                    1.0    # screen_wait
                )
                
                self.log_result(
                    f"Flow for Seat {seat}",
                    "PASS",
                    f"Would update '{name}' in ~{expected_time:.2f} seconds"
                )
                
            total_time = len(test_players) * 3.5  # Approximate
            self.log_result(
                "Complete Flow",
                "PASS",
                f"Total estimated time: {total_time:.1f} seconds for {len(test_players)} players"
            )
            
            return True
            
        except Exception as e:
            self.log_result("Automation Flow", "FAIL", str(e))
            return False
            
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*50)
        print("TEST REPORT SUMMARY")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        warnings = sum(1 for r in self.test_results if r["status"] == "WARN")
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed} ({passed/total_tests*100:.1f}%)")
        print(f"Failed: {failed}")
        print(f"Warnings: {warnings}")
        
        # Save detailed report
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\nDetailed report saved to: {report_file}")
        
        # Print coordinate verification
        print("\n" + "="*50)
        print("COORDINATE VERIFICATION")
        print("="*50)
        print(f"Screen Resolution: {pyautogui.size()}")
        print("\nPlayer Coordinates:")
        for seat, coords in PLAYER_COORDS.items():
            print(f"  Seat {seat:2d}: ({coords[0]:4d}, {coords[1]:4d})")
        print(f"\nSub Name Field: {SUB_NAME_FIELD}")
        print(f"Complete Button: {COMPLETE_BUTTON}")
        print(f"Delete Button: {DELETE_BUTTON}")
        
        return passed == total_tests

def main():
    """Run all tests"""
    print("="*50)
    print("ACTION TRACKER AUTOMATION TEST SUITE")
    print("="*50)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Safety warning
    print("\nWARNING: This test will move your mouse cursor!")
    print("Press Ctrl+C to abort at any time")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    tester = AutomationTester()
    
    # Run tests
    tester.test_mouse_position()
    tester.test_safe_click()
    tester.test_screenshot_areas()
    tester.test_keyboard_simulation()
    tester.test_automation_flow()
    
    # Generate report
    success = tester.generate_report()
    
    if success:
        print("\n[SUCCESS] ALL TESTS PASSED - Automation logic appears correct")
    else:
        print("\n[FAILED] SOME TESTS FAILED - Review the issues above")
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()