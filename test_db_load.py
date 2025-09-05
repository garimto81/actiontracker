"""
Test Google Sheets DB Loading
데이터베이스 로드 테스트 및 디버깅
"""

import pandas as pd
import requests
from io import StringIO
import numpy as np

def test_google_sheets_load():
    """Test loading data from Google Sheets with error handling"""
    
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDY_i4330JANAjIz4sMncdJdRHsOkfUCjQusHTGQk2tykrhA4d09LeIp3XRbLd8hkN6SgSB47k_nux/pub?gid=998576925&single=true&output=csv"
    
    print("="*60)
    print("GOOGLE SHEETS DB LOAD TEST")
    print("="*60)
    print(f"\nURL: {url[:100]}...")
    
    try:
        # Step 1: Download data
        print("\n1. Downloading data...")
        response = requests.get(url)
        response.raise_for_status()
        print(f"   [OK] Status Code: {response.status_code}")
        print(f"   [OK] Content Length: {len(response.text)} bytes")
        
        # Step 2: Parse CSV
        print("\n2. Parsing CSV...")
        df = pd.read_csv(StringIO(response.text))
        print(f"   [OK] Rows: {len(df)}")
        print(f"   [OK] Columns: {list(df.columns)}")
        
        # Step 3: Check data types
        print("\n3. Data Types:")
        for col in df.columns:
            print(f"   - {col}: {df[col].dtype}")
        
        # Step 4: Check for NaN values
        print("\n4. NaN Values Check:")
        nan_counts = df.isna().sum()
        for col, count in nan_counts.items():
            if count > 0:
                print(f"   [WARNING] {col}: {count} NaN values")
        
        # Step 5: Display first few rows
        print("\n5. First 5 rows:")
        print("-"*60)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(df.head())
        
        # Step 6: Check Seat column specifically (where error occurs)
        print("\n6. Seat Column Analysis:")
        print(f"   - Data type: {df['Seat'].dtype}")
        print(f"   - Unique values: {df['Seat'].unique()}")
        print(f"   - NaN count: {df['Seat'].isna().sum()}")
        
        # Step 7: Process data with error handling
        print("\n7. Processing Data with Error Handling...")
        table_data = {}
        error_rows = []
        
        for idx, row in df.iterrows():
            try:
                table = str(row['Table'])
                
                # Handle NaN in Seat column
                if pd.isna(row['Seat']):
                    print(f"   [WARNING] Row {idx}: Seat is NaN, skipping...")
                    error_rows.append(idx)
                    continue
                
                # Try to convert Seat to integer
                try:
                    seat = int(float(row['Seat']))  # First convert to float, then to int
                except (ValueError, TypeError):
                    print(f"   [WARNING] Row {idx}: Cannot convert Seat '{row['Seat']}' to integer, skipping...")
                    error_rows.append(idx)
                    continue
                
                if table not in table_data:
                    table_data[table] = {}
                
                # Handle other fields with defaults
                table_data[table][seat] = {
                    'player': row['player'] if pd.notna(row['player']) else 'Unknown',
                    'chips': row['Chips'] if pd.notna(row['Chips']) else 0,
                    'notable': row['Notable'] if pd.notna(row['Notable']) else False,
                    'camera_preset': row.get('Camera Preset', ''),
                    'updated_at': row.get('updatedAt', '')
                }
                
            except Exception as e:
                print(f"   [ERROR] Row {idx}: Error - {e}")
                error_rows.append(idx)
        
        print(f"\n   [OK] Successfully processed: {len(df) - len(error_rows)} rows")
        if error_rows:
            print(f"   [WARNING] Failed rows: {error_rows}")
        
        # Step 8: Display processed data
        print("\n8. Processed Table Data:")
        print("-"*60)
        for table, seats in table_data.items():
            print(f"\nTable {table}:")
            for seat, info in sorted(seats.items()):
                print(f"  Seat {seat}: {info['player']} - {info['chips']} chips")
        
        return table_data
        
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Network Error: {e}")
        return None
    
    except pd.errors.ParserError as e:
        print(f"\n[ERROR] CSV Parsing Error: {e}")
        return None
    
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_with_nan_handling():
    """Test with improved NaN handling"""
    
    print("\n" + "="*60)
    print("IMPROVED DATA LOADING WITH NaN HANDLING")
    print("="*60)
    
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDY_i4330JANAjIz4sMncdJdRHsOkfUCjQusHTGQk2tykrhA4d09LeIp3XRbLd8hkN6SgSB47k_nux/pub?gid=998576925&single=true&output=csv"
    
    try:
        # Load data
        response = requests.get(url)
        df = pd.read_csv(StringIO(response.text))
        
        # Clean data before processing
        print("\n1. Cleaning Data...")
        
        # Remove rows where Seat is NaN
        initial_count = len(df)
        df = df.dropna(subset=['Seat'])
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            print(f"   [OK] Removed {removed_count} rows with NaN Seat values")
        
        # Convert Seat to integer safely
        df['Seat'] = df['Seat'].apply(lambda x: int(float(x)) if pd.notna(x) else None)
        
        # Fill NaN values with defaults
        df['player'] = df['player'].fillna('Unknown')
        df['Chips'] = df['Chips'].fillna(0)
        df['Notable'] = df['Notable'].fillna(False)
        df['Table'] = df['Table'].fillna('0')
        
        print(f"   [OK] Data cleaned: {len(df)} valid rows")
        
        # Process cleaned data
        print("\n2. Processing Cleaned Data...")
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
        
        # Summary
        print(f"\n3. Summary:")
        print(f"   - Tables: {len(table_data)}")
        print(f"   - Total players: {sum(len(seats) for seats in table_data.values())}")
        
        for table in sorted(table_data.keys()):
            seats = table_data[table]
            print(f"   - Table {table}: {len(seats)} players (Seats: {sorted(seats.keys())})")
        
        return table_data
        
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("Testing Google Sheets DB Load...")
    print("\nTest 1: Detailed Analysis")
    data1 = test_google_sheets_load()
    
    print("\n\nTest 2: With NaN Handling")
    data2 = test_with_nan_handling()
    
    if data2:
        print("\n" + "="*60)
        print("[SUCCESS] DATA LOAD SUCCESSFUL!")
        print("="*60)
        print("\nYou can now use this data in the GUI.")
    else:
        print("\n" + "="*60)
        print("[FAILED] DATA LOAD FAILED")
        print("="*60)
        print("\nPlease check the error messages above.")