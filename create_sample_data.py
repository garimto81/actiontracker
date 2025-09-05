"""
Create Sample Data for Testing
테스트용 샘플 데이터 생성
"""

import pandas as pd
import json

def create_sample_csv():
    """Create sample CSV file with proper Seat numbers"""
    
    # Sample data with Seat numbers assigned
    data = {
        'Camera Preset': ['camA', 'camB', None, None, 'camE', 'camF', 'camG', 'camH', None, None],
        'player': ['Phil Ivey', 'Daniel Negreanu', 'Doyle Brunson', 'Phil Hellmuth', 
                   'Tom Dwan', 'Patrik Antonius', 'Gus Hansen', 'Vanessa Selbst', 
                   'Erik Seidel', 'Johnny Chan'],
        'Table': ['T01', 'T01', 'T01', 'T01', 'T01', 'T01', 'T01', 'T01', 'T01', 'T01'],
        'Notable': [True, True, True, False, False, False, False, True, False, True],
        'Chips': [1500000, 1200000, 980000, 750000, 620000, 540000, 480000, 890000, 670000, 1100000],
        'updatedAt': ['2025-09-03', '2025-09-03', '2025-09-02', '2025-09-02', '2025-09-01',
                      '2025-09-01', '2025-09-01', '2025-09-03', '2025-09-02', '2025-09-03'],
        'Seat': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # IMPORTANT: Seat numbers!
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    csv_filename = 'sample_player_data.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Sample CSV created: {csv_filename}")
    print("\nData preview:")
    print(df)
    
    # Also create data for multiple tables
    multi_table_data = []
    
    # Table 1 (Full table)
    for seat in range(1, 11):
        multi_table_data.append({
            'Camera Preset': f'cam{seat}' if seat <= 5 else None,
            'player': f'Player T1-{seat}',
            'Table': 'T01',
            'Notable': seat <= 3,
            'Chips': 100000 * seat,
            'updatedAt': '2025-09-03',
            'Seat': seat
        })
    
    # Table 2 (Partial table - only seats 1,3,5,7,9)
    for seat in [1, 3, 5, 7, 9]:
        multi_table_data.append({
            'Camera Preset': None,
            'player': f'Player T2-{seat}',
            'Table': 'T02',
            'Notable': False,
            'Chips': 50000 * seat,
            'updatedAt': '2025-09-03',
            'Seat': seat
        })
    
    # Table 3 (Partial table - only seats 2,4,6,8)
    for seat in [2, 4, 6, 8]:
        multi_table_data.append({
            'Camera Preset': None,
            'player': f'Player T3-{seat}',
            'Table': 'T03',
            'Notable': seat == 2,
            'Chips': 75000 * seat,
            'updatedAt': '2025-09-02',
            'Seat': seat
        })
    
    # Create multi-table DataFrame
    df_multi = pd.DataFrame(multi_table_data)
    
    # Save to CSV
    multi_csv_filename = 'sample_multi_table_data.csv'
    df_multi.to_csv(multi_csv_filename, index=False)
    print(f"\nMulti-table CSV created: {multi_csv_filename}")
    print("\nMulti-table data summary:")
    print(df_multi.groupby('Table')['Seat'].apply(list))
    
    return df, df_multi


def test_with_sample_data():
    """Test data processing with sample data"""
    
    print("\n" + "="*60)
    print("TESTING WITH SAMPLE DATA")
    print("="*60)
    
    # Read sample data
    df = pd.read_csv('sample_player_data.csv')
    
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
    
    # Display results
    print("\nProcessed Table Data:")
    for table, seats in table_data.items():
        print(f"\nTable {table}:")
        for seat, info in sorted(seats.items()):
            notable = "[NOTABLE]" if info['notable'] else ""
            print(f"  Seat {seat}: {info['player']:20} - {info['chips']:,} chips {notable}")
    
    # Save as JSON
    with open('sample_table_data.json', 'w', encoding='utf-8') as f:
        json.dump(table_data, f, indent=2, ensure_ascii=False)
    
    print("\n[OK] Sample data processed successfully!")
    print("Saved to: sample_table_data.json")
    
    return table_data


def fix_google_sheets_data():
    """
    Provide solution for Google Sheets data issue
    """
    print("\n" + "="*60)
    print("SOLUTION FOR GOOGLE SHEETS DATA")
    print("="*60)
    print()
    print("PROBLEM IDENTIFIED:")
    print("-" * 40)
    print("The 'Seat' column in your Google Sheets is empty (all NaN values).")
    print("This is why the error 'cannot convert float NaN to integer' occurs.")
    print()
    print("SOLUTION:")
    print("-" * 40)
    print("You need to add Seat numbers (1-10) to your Google Sheets data.")
    print()
    print("GOOGLE SHEETS STRUCTURE SHOULD BE:")
    print("-" * 40)
    print("Camera Preset | player         | Table | Notable | Chips   | updatedAt  | Seat")
    print("camA          | Phil Ivey      | T01   | True    | 1500000 | 2025-09-03 | 1   ")
    print("camB          | Daniel Negreanu| T01   | False   | 1200000 | 2025-09-03 | 2   ")
    print("              | Doyle Brunson  | T01   | False   | 980000  | 2025-09-02 | 3   ")
    print("...           | ...            | ...   | ...     | ...     | ...        | ... ")
    print()
    print("IMPORTANT:")
    print("-" * 40)
    print("1. Each player MUST have a Seat number (1-10)")
    print("2. Seat numbers should match the actual seat positions in Action Tracker")
    print("3. For empty seats, simply don't include that row in the spreadsheet")
    print()
    print("EXAMPLE:")
    print("-" * 40)
    print("If Table T01 has players only in seats 1, 3, 5, 7:")
    print("- Include 4 rows with Seat values: 1, 3, 5, 7")
    print("- Seats 2, 4, 6, 8, 9, 10 will be automatically marked as empty")


if __name__ == "__main__":
    # Create sample data
    print("Creating sample data files...")
    df1, df2 = create_sample_csv()
    
    # Test with sample data
    test_with_sample_data()
    
    # Show solution
    fix_google_sheets_data()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Fix your Google Sheets by adding Seat numbers (1-10)")
    print("2. Or use the sample CSV files created here for testing")
    print("3. Update the GUI to handle missing Seat data gracefully")
    print()
    print("Sample files created:")
    print("- sample_player_data.csv (single table)")
    print("- sample_multi_table_data.csv (multiple tables)")
    print("- sample_table_data.json (processed data)")