"""
Chip Manager System with Google Sheets Integration
칩 입력 및 Google Sheets DB 연동 시스템
"""

import pyautogui
import time
import pandas as pd
import json
from datetime import datetime
import requests
from io import StringIO

# Player coordinates for names
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

# Chip input coordinates
CHIP_COORDS = {
    1: (1226, 622),
    2: (1382, 619),
    3: (1537, 615),
    4: (1688, 615),
    5: (1694, 615),
    6: (1694, 615),
    7: (1226, 622),
    8: (1382, 619),
    9: (1537, 615),
    10: (1688, 615)
}

# Other coordinates
SUB_NAME_FIELD = (785, 291)
COMPLETE_BUTTON = (1720, 139)
DELETE_BUTTON = (721, 112)

class ChipManager:
    def __init__(self):
        self.google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDY_i4330JANAjIz4sMncdJdRHsOkfUCjQusHTGQk2tykrhA4d09LeIp3XRbLd8hkN6SgSB47k_nux/pub?gid=998576925&single=true&output=csv"
        self.player_data = {}
        self.table_data = {}
        self.current_state = {
            "occupied_seats": [],
            "empty_seats": [],
            "player_names": {},
            "chip_stacks": {},
            "timestamp": None
        }
        
    def load_google_sheet_data(self):
        """Load player and chip data from Google Sheets"""
        try:
            print("Loading data from Google Sheets...")
            response = requests.get(self.google_sheet_url)
            response.raise_for_status()
            
            # Parse CSV data
            df = pd.read_csv(StringIO(response.text))
            
            # Group by table number
            self.table_data = {}
            for _, row in df.iterrows():
                table = str(row['Table'])
                if table not in self.table_data:
                    self.table_data[table] = {}
                
                seat = int(row['Seat'])
                self.table_data[table][seat] = {
                    'player': row['player'],
                    'chips': row['Chips'],
                    'notable': row['Notable'],
                    'camera_preset': row['Camera Preset'],
                    'updated_at': row['updatedAt']
                }
            
            print(f"Loaded data for {len(self.table_data)} tables")
            return True
            
        except Exception as e:
            print(f"Error loading Google Sheets data: {e}")
            return False
    
    def get_table_players(self, table_number):
        """Get players for specific table"""
        table_str = str(table_number)
        if table_str not in self.table_data:
            print(f"No data for table {table_number}")
            return {}
        
        return self.table_data[table_str]
    
    def input_chip_amount(self, seat_number, chip_amount):
        """Input chip amount for specific seat"""
        if seat_number not in CHIP_COORDS:
            print(f"Invalid seat number: {seat_number}")
            return False
        
        try:
            coords = CHIP_COORDS[seat_number]
            
            # Click chip input field
            print(f"  Clicking chip field for seat {seat_number}: {coords}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(0.3)
            
            # Clear existing value (triple click to select all)
            pyautogui.tripleClick()
            time.sleep(0.1)
            
            # Type chip amount
            print(f"  Typing chip amount: {chip_amount}")
            pyautogui.typewrite(str(chip_amount), interval=0.02)
            time.sleep(0.2)
            
            # Press Enter
            print(f"  Pressing Enter")
            pyautogui.press('enter')
            time.sleep(0.3)
            
            return True
            
        except Exception as e:
            print(f"Error inputting chips for seat {seat_number}: {e}")
            return False
    
    def update_player_name(self, seat_number, player_name, is_empty=False):
        """Update player name for specific seat"""
        if seat_number not in PLAYER_COORDS:
            print(f"Invalid seat number: {seat_number}")
            return False
        
        try:
            coords = PLAYER_COORDS[seat_number]
            
            if is_empty:
                # Register new name (simple 3-step process)
                print(f"  Registering new player at seat {seat_number}")
                pyautogui.click(coords[0], coords[1])
                time.sleep(0.3)
                
                pyautogui.typewrite(player_name, interval=0.02)
                time.sleep(0.2)
                
                pyautogui.press('enter')
                time.sleep(0.3)
            else:
                # Update existing name (full process)
                print(f"  Updating existing player at seat {seat_number}")
                pyautogui.click(coords[0], coords[1])
                time.sleep(1.0)
                
                pyautogui.click(SUB_NAME_FIELD[0], SUB_NAME_FIELD[1])
                time.sleep(0.3)
                
                pyautogui.tripleClick()
                time.sleep(0.1)
                pyautogui.typewrite(player_name, interval=0.02)
                time.sleep(0.2)
                
                pyautogui.press('enter')
                time.sleep(0.3)
                
                pyautogui.click(COMPLETE_BUTTON[0], COMPLETE_BUTTON[1])
                time.sleep(1.0)
            
            return True
            
        except Exception as e:
            print(f"Error updating player name for seat {seat_number}: {e}")
            return False
    
    def remove_player(self, seat_number):
        """Remove player from specific seat"""
        try:
            coords = PLAYER_COORDS[seat_number]
            
            print(f"  Removing player from seat {seat_number}")
            pyautogui.click(coords[0], coords[1])
            time.sleep(0.5)
            
            pyautogui.click(DELETE_BUTTON[0], DELETE_BUTTON[1])
            time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"Error removing player from seat {seat_number}: {e}")
            return False
    
    def process_table(self, table_number, current_occupied_seats=None):
        """Process entire table - update players and chips"""
        print(f"\n{'='*60}")
        print(f"Processing Table {table_number}")
        print(f"{'='*60}")
        
        # Get table data from Google Sheets
        table_players = self.get_table_players(table_number)
        if not table_players:
            print(f"No data found for table {table_number}")
            return False
        
        # If current state provided, use it
        if current_occupied_seats is None:
            current_occupied_seats = []
        
        # Process each seat
        results = {
            'updated_players': [],
            'updated_chips': [],
            'removed_players': [],
            'errors': []
        }
        
        # First, remove players not in the new table data
        for seat in current_occupied_seats:
            if seat not in table_players:
                print(f"\nRemoving player from seat {seat} (not in new data)")
                if self.remove_player(seat):
                    results['removed_players'].append(seat)
                else:
                    results['errors'].append(f"Failed to remove seat {seat}")
                time.sleep(0.5)
        
        # Then, update/add players and chips
        for seat, player_info in table_players.items():
            print(f"\nSeat {seat}: {player_info['player']}")
            print(f"  Chips: {player_info['chips']}")
            
            # Update player name
            is_empty = seat not in current_occupied_seats
            if self.update_player_name(seat, player_info['player'], is_empty):
                results['updated_players'].append(seat)
                print(f"  ✓ Player name updated")
            else:
                results['errors'].append(f"Failed to update player at seat {seat}")
                continue
            
            time.sleep(0.5)
            
            # Update chip amount
            if self.input_chip_amount(seat, player_info['chips']):
                results['updated_chips'].append(seat)
                print(f"  ✓ Chip amount updated")
            else:
                results['errors'].append(f"Failed to update chips at seat {seat}")
            
            time.sleep(0.5)
        
        # Save current state
        self.save_state(table_number, table_players)
        
        # Print results
        print(f"\n{'='*60}")
        print("RESULTS")
        print(f"{'='*60}")
        print(f"Updated players: {len(results['updated_players'])} seats")
        print(f"Updated chips: {len(results['updated_chips'])} seats")
        print(f"Removed players: {len(results['removed_players'])} seats")
        if results['errors']:
            print(f"Errors: {len(results['errors'])}")
            for error in results['errors']:
                print(f"  - {error}")
        print(f"{'='*60}")
        
        return results
    
    def save_state(self, table_number, table_players):
        """Save current state to file"""
        state = {
            'table_number': table_number,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'occupied_seats': list(table_players.keys()),
            'player_data': table_players
        }
        
        filename = f"table_{table_number}_state.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        print(f"\nState saved to {filename}")
    
    def load_state(self, table_number):
        """Load previous state from file"""
        filename = f"table_{table_number}_state.json"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            print(f"Loaded previous state from {state['timestamp']}")
            return state.get('occupied_seats', [])
            
        except FileNotFoundError:
            print(f"No previous state found for table {table_number}")
            return []
        except Exception as e:
            print(f"Error loading state: {e}")
            return []
    
    def batch_process_tables(self, table_numbers):
        """Process multiple tables"""
        for table_num in table_numbers:
            # Load previous state
            previous_occupied = self.load_state(table_num)
            
            # Process table
            self.process_table(table_num, previous_occupied)
            
            # Wait between tables
            time.sleep(2)
    
    def interactive_mode(self):
        """Interactive mode for manual control"""
        print("\n" + "="*60)
        print("CHIP MANAGER - INTERACTIVE MODE")
        print("="*60)
        
        # Load data
        if not self.load_google_sheet_data():
            print("Failed to load data. Check internet connection.")
            return
        
        # Show available tables
        print(f"\nAvailable tables: {list(self.table_data.keys())}")
        
        # Get table selection
        table_num = input("\nEnter table number: ").strip()
        
        if table_num not in self.table_data:
            print(f"Table {table_num} not found")
            return
        
        # Show table info
        table_players = self.get_table_players(table_num)
        print(f"\nTable {table_num} has {len(table_players)} players:")
        for seat, info in table_players.items():
            print(f"  Seat {seat}: {info['player']} - {info['chips']} chips")
        
        # Load previous state
        previous_occupied = self.load_state(table_num)
        if previous_occupied:
            print(f"\nPrevious state: Seats {previous_occupied} were occupied")
        
        # Confirm
        proceed = input("\nProceed with update? (y/n): ").strip().lower()
        
        if proceed == 'y':
            print("\nStarting in 3 seconds...")
            time.sleep(3)
            self.process_table(table_num, previous_occupied)


def test_chip_input():
    """Test chip input functionality"""
    manager = ChipManager()
    
    print("CHIP INPUT TEST")
    print("1. Test single chip input")
    print("2. Test table update from Google Sheets")
    print("3. Interactive mode")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        seat = int(input("Enter seat number (1-10): "))
        chips = input("Enter chip amount: ").strip()
        
        print("\nStarting in 3 seconds...")
        time.sleep(3)
        
        if manager.input_chip_amount(seat, chips):
            print("✓ Chip input successful")
        else:
            print("✗ Chip input failed")
    
    elif choice == "2":
        if manager.load_google_sheet_data():
            table_num = input("Enter table number: ").strip()
            
            print("\nStarting in 3 seconds...")
            time.sleep(3)
            
            previous = manager.load_state(table_num)
            manager.process_table(table_num, previous)
    
    elif choice == "3":
        manager.interactive_mode()


if __name__ == "__main__":
    test_chip_input()