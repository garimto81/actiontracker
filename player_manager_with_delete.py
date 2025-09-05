"""
Player Manager with Delete Function
플레이어 이름 변경 + 삭제 기능 포함
"""

import pyautogui
import time

# 모든 좌표 정보
COORDS = {
    'player1': (215, 354),        # Player1 버튼
    'edit': (815, 294),           # 편집 필드  
    'complete': (1733, 155),      # 완료 버튼
    'delete': (761, 108)          # 삭제 버튼 (새로 추가)
}

def ultra_fast_click(x, y, delay=0.15):
    """초고속 클릭"""
    pyautogui.click(x, y)
    time.sleep(delay)

def ultra_fast_type(text):
    """초고속 타이핑 + Enter"""
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.05)
    pyautogui.typewrite(text)
    time.sleep(0.05)
    pyautogui.press('enter')
    time.sleep(0.1)

def update_player1_name(name):
    """Player1 이름 변경"""
    print(f'ULTRA FAST UPDATE: Player1 -> {name}')
    print('=' * 40)
    start_time = time.time()

    print('[1] Player1 click')
    ultra_fast_click(COORDS['player1'][0], COORDS['player1'][1], 0.4)

    print('[2] Edit field click')
    ultra_fast_click(COORDS['edit'][0], COORDS['edit'][1], 0.2)

    print(f'[3] Type {name} + Enter')
    ultra_fast_type(name)

    print('[4] Complete button')
    ultra_fast_click(COORDS['complete'][0], COORDS['complete'][1], 0.2)

    elapsed = time.time() - start_time
    print('=' * 40)
    print(f'SUCCESS: {name} updated in {elapsed:.1f}s')
    print('=' * 40)

def delete_player1():
    """Player1 삭제"""
    print('ULTRA FAST DELETE: Player1')
    print('=' * 40)
    start_time = time.time()

    print('[1] Player1 click')
    ultra_fast_click(COORDS['player1'][0], COORDS['player1'][1], 0.4)

    print('[2] Delete button click')
    ultra_fast_click(COORDS['delete'][0], COORDS['delete'][1], 0.3)

    print('[3] Complete button')
    ultra_fast_click(COORDS['complete'][0], COORDS['complete'][1], 0.2)

    elapsed = time.time() - start_time
    print('=' * 40)
    print(f'SUCCESS: Player1 deleted in {elapsed:.1f}s')
    print('=' * 40)

def main():
    """메인 메뉴"""
    print('Player Manager - Fast Version')
    print('=' * 30)
    print('Coordinates:')
    for name, (x, y) in COORDS.items():
        print(f'  {name}: ({x}, {y})')
    
    print()
    print('OPTIONS:')
    print('1. Update name (custom)')
    print('2. Delete Player1')
    print('3. Quick update to Alice')
    print('4. Quick update to Bob')
    
    try:
        choice = input('Choose (1-4): ').strip()
        
        if choice == '1':
            name = input('Enter new name: ').strip()
            if name:
                print(f'Starting update to {name} in 1 second...')
                time.sleep(1)
                update_player1_name(name)
            else:
                print('No name entered.')
        
        elif choice == '2':
            print('Starting delete in 1 second...')
            time.sleep(1)
            delete_player1()
        
        elif choice == '3':
            print('Quick update to Alice in 1 second...')
            time.sleep(1)
            update_player1_name('Alice')
        
        elif choice == '4':
            print('Quick update to Bob in 1 second...')
            time.sleep(1)
            update_player1_name('Bob')
        
        else:
            print('Invalid choice.')
            
    except KeyboardInterrupt:
        print('\nCancelled.')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()