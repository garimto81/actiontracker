"""
Execute 10 Players Update
10명 플레이어 즉시 실행
"""

import pyautogui
import time
from datetime import datetime

# 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# 플레이어 데이터
PLAYERS = [
    ((215, 354), "Player_One"),
    ((374, 359), "Player_Two"),
    ((544, 362), "Player_Three"),
    ((722, 359), "Player_Four"),
    ((886, 356), "Player_Five"),
    ((1051, 354), "Player_Six"),
    ((1213, 355), "Player_Seven"),
    ((1385, 383), "Player_Eight"),
    ((1549, 367), "Player_Nine"),
    ((1705, 356), "Player_Ten")
]

print("="*60)
print("EXECUTING 10 PLAYERS UPDATE")
print("="*60)

# 3초 카운트다운
for i in range(3, 0, -1):
    print(f"Starting in {i}...")
    time.sleep(1)

print("\nUpdating players...")
print("-"*40)

start_time = time.time()
success = 0

for i, ((x, y), name) in enumerate(PLAYERS, 1):
    print(f"Player {i}: {name} ", end="")
    
    try:
        # 플레이어 클릭
        pyautogui.click(x, y)
        time.sleep(0.3)
        
        # 더블클릭
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # 텍스트 삭제
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        
        # 새 이름 입력
        pyautogui.typewrite(name, interval=0.02)
        time.sleep(0.2)
        
        # Enter
        pyautogui.press('enter')
        time.sleep(0.3)
        
        print("[OK]")
        success += 1
        
    except Exception as e:
        print(f"[FAIL: {e}]")

# 결과
elapsed = time.time() - start_time

print("\n" + "="*60)
print("UPDATE COMPLETE")
print("="*60)
print(f"Success: {success}/10 players")
print(f"Time: {elapsed:.1f} seconds")

# 스크린샷
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot = pyautogui.screenshot()
filename = f"result_{timestamp}.png"
screenshot.save(filename)
print(f"Screenshot: {filename}")
print("="*60)