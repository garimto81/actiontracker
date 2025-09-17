"""
Test Integrated System with Sample Data
샘플 데이터로 통합 시스템 테스트
"""

import pandas as pd
import json
import pyautogui
import time
from datetime import datetime

# Coordinates
PLAYER_COORDS = {
    1: (233, 361), 2: (374, 359), 3: (544, 362), 4: (722, 359), 5: (886, 356),
    6: (1051, 354), 7: (1213, 355), 8: (1385, 383), 9: (1549, 367), 10: (1705, 356)
}

CHIP_COORDS = {
    1: (1226, 622), 2: (1382, 619), 3: (1537, 615), 4: (1688, 615), 5: (1694, 615),
    6: (1694, 615), 7: (1226, 622), 8: (1382, 619), 9: (1537, 615), 10: (1688, 615)
}

def test_sample_data_loading():
    """Test loading sample CSV data"""
    print("="*60)
    print("TEST 1: Loading Sample Data")
    print("="*60)
    
    # Test single table data
    try:
        df = pd.read_csv('sample_player_data.csv')
        print(f"[OK] Loaded sample_player_data.csv")
        print(f"     Rows: {len(df)}, Columns: {list(df.columns)}")
        
        # Check Seat column
        print(f"\n[INFO] Seat column check:")
        print(f"       Data type: {df['Seat'].dtype}")
        print(f"       Values: {df['Seat'].tolist()}")
        print(f"       NaN count: {df['Seat'].isna().sum()}")
        
        # Process data
        table_data = {}
        for _, row in df.iterrows():
            table = str(row['Table'])
            seat = int(row['Seat'])
            
            if table not in table_data:
                table_data[table] = {}
            
            table_data[table][seat] = {
                'player': row['player'],
                'chips': row['Chips'],
                'notable': row['Notable']
            }
        
        print(f"\n[OK] Processed {len(table_data)} table(s)")
        for table, seats in table_data.items():
            print(f"     Table {table}: {len(seats)} players")
            
    except Exception as e:
        print(f"[ERROR] Failed to load sample data: {e}")
        return None
    
    return table_data


def test_multi_table_loading():
    """Test loading multi-table data"""
    print("\n" + "="*60)
    print("TEST 2: Loading Multi-Table Data")
    print("="*60)
    
    try:
        df = pd.read_csv('sample_multi_table_data.csv')
        print(f"[OK] Loaded sample_multi_table_data.csv")
        print(f"     Total rows: {len(df)}")
        
        # Group by table
        table_groups = df.groupby('Table')
        print(f"\n[INFO] Tables found: {list(table_groups.groups.keys())}")
        
        for table_name, group in table_groups:
            seats = sorted(group['Seat'].tolist())
            print(f"       Table {table_name}: Seats {seats}")
            
        # Process all tables
        all_tables = {}
        for _, row in df.iterrows():
            table = str(row['Table'])
            seat = int(row['Seat'])
            
            if table not in all_tables:
                all_tables[table] = {}
            
            all_tables[table][seat] = {
                'player': row['player'],
                'chips': row['Chips'],
                'notable': row['Notable']
            }
        
        print(f"\n[OK] Processed {len(all_tables)} tables successfully")
        
    except Exception as e:
        print(f"[ERROR] Failed to load multi-table data: {e}")
        return None
    
    return all_tables


def test_json_state():
    """Test JSON state saving/loading"""
    print("\n" + "="*60)
    print("TEST 3: JSON State Management")
    print("="*60)
    
    try:
        # Load processed data
        with open('sample_table_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"[OK] Loaded sample_table_data.json")
        
        # Create state file for each table
        for table_name, seats in data.items():
            state = {
                'table': table_name,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'occupied_seats': list(seats.keys()),
                'empty_seats': [s for s in range(1, 11) if str(s) not in seats],
                'player_data': seats
            }
            
            filename = f'test_state_table_{table_name}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Created state file: {filename}")
            print(f"     Occupied: {state['occupied_seats']}")
            print(f"     Empty: {state['empty_seats']}")
            
    except Exception as e:
        print(f"[ERROR] JSON state test failed: {e}")
        return False
    
    return True


def test_action_sequence():
    """Test the complete action sequence (without actual clicking)"""
    print("\n" + "="*60)
    print("TEST 4: Action Sequence Simulation")
    print("="*60)
    
    # Load sample data
    try:
        with open('sample_table_data.json', 'r', encoding='utf-8') as f:
            table_data = json.load(f)
        
        # Simulate processing Table T01
        table = 'T01'
        players = table_data[table]
        
        print(f"[SIMULATION] Processing Table {table}")
        print("-" * 40)
        
        # Track which seats need which operations
        operations = {
            'update_name': [],
            'register_name': [],
            'input_chips': [],
            'delete': []
        }
        
        # Assume seats 1-4 have existing names, 5-10 are empty
        existing_seats = [1, 2, 3, 4]
        
        for seat_str, player_info in players.items():
            seat = int(seat_str)
            
            if seat in existing_seats:
                operations['update_name'].append(seat)
                print(f"[PLAN] Seat {seat}: UPDATE existing -> {player_info['player']}")
            else:
                operations['register_name'].append(seat)
                print(f"[PLAN] Seat {seat}: REGISTER new -> {player_info['player']}")
            
            operations['input_chips'].append(seat)
            print(f"       Then input chips: {player_info['chips']:,}")
        
        # Summary
        print(f"\n[SUMMARY] Operation Plan:")
        print(f"  - Update existing names: Seats {operations['update_name']}")
        print(f"  - Register new names: Seats {operations['register_name']}")
        print(f"  - Input chips: All {len(operations['input_chips'])} seats")
        
        # Calculate estimated time
        time_estimate = (
            len(operations['update_name']) * 3.5 +  # Update takes ~3.5s
            len(operations['register_name']) * 1.5 +  # Register takes ~1.5s
            len(operations['input_chips']) * 1.0  # Chips take ~1s
        )
        print(f"\n[TIME] Estimated execution time: {time_estimate:.1f} seconds")
        
    except Exception as e:
        print(f"[ERROR] Action sequence test failed: {e}")
        return False
    
    return True


def test_coordinate_validation():
    """Validate all coordinates are within screen bounds"""
    print("\n" + "="*60)
    print("TEST 5: Coordinate Validation")
    print("="*60)
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    print(f"[INFO] Screen size: {screen_width} x {screen_height}")
    
    # Check player coordinates
    print("\n[CHECK] Player coordinates:")
    invalid = []
    for seat, (x, y) in PLAYER_COORDS.items():
        if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
            invalid.append(f"Seat {seat}: ({x}, {y})")
            print(f"  [FAIL] Seat {seat}: ({x}, {y}) - OUT OF BOUNDS")
        else:
            print(f"  [OK] Seat {seat}: ({x}, {y})")
    
    # Check chip coordinates
    print("\n[CHECK] Chip coordinates:")
    for seat, (x, y) in CHIP_COORDS.items():
        if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
            invalid.append(f"Chip {seat}: ({x}, {y})")
            print(f"  [FAIL] Chip {seat}: ({x}, {y}) - OUT OF BOUNDS")
        else:
            print(f"  [OK] Chip {seat}: ({x}, {y})")
    
    if invalid:
        print(f"\n[WARNING] {len(invalid)} coordinates are out of bounds!")
        print("These coordinates may need adjustment for your screen.")
    else:
        print("\n[OK] All coordinates are within screen bounds")
    
    return len(invalid) == 0


def main():
    """Run all tests"""
    print("="*70)
    print("INTEGRATED SYSTEM TEST SUITE")
    print("="*70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    results = []
    
    # Test 1: Sample data loading
    result1 = test_sample_data_loading()
    results.append(("Sample Data Loading", result1 is not None))
    
    # Test 2: Multi-table loading
    result2 = test_multi_table_loading()
    results.append(("Multi-Table Loading", result2 is not None))
    
    # Test 3: JSON state
    result3 = test_json_state()
    results.append(("JSON State Management", result3))
    
    # Test 4: Action sequence
    result4 = test_action_sequence()
    results.append(("Action Sequence", result4))
    
    # Test 5: Coordinate validation
    result5 = test_coordinate_validation()
    results.append(("Coordinate Validation", result5))
    
    # Final summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("-" * 70)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Fix Google Sheets by adding Seat numbers (1-10)")
        print("2. Or use sample CSV files for testing")
        print("3. Run integrated_gui_final.py to use the system")
    else:
        print("\n[WARNING] Some tests failed. Please check the errors above.")
    
    # Create quick start file
    quick_start = {
        'test_results': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'passed': passed,
            'total': total,
            'details': dict(results)
        },
        'sample_files': [
            'sample_player_data.csv',
            'sample_multi_table_data.csv', 
            'sample_table_data.json'
        ],
        'state_files': [
            'test_state_table_T01.json'
        ]
    }
    
    with open('test_results.json', 'w') as f:
        json.dump(quick_start, f, indent=2)
    
    print(f"\nTest results saved to: test_results.json")


if __name__ == "__main__":
    main()