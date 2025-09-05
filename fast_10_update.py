"""
Fast 10 Players Update
10명 플레이어 빠른 업데이트
"""

import pyautogui
import time
from datetime import datetime

# 빠른 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1  # 더 빠르게

# 플레이어 좌표와 이름
PLAYERS = [
    (1, (215, 354), "Johnny Chan"),
    (2, (374, 359), "Chris Ferguson"),
    (3, (544, 362), "Stu Ungar"),
    (4, (722, 359), "Vanessa Selbst"),
    (5, (886, 356), "Jason Koon"),
    (6, (1051, 354), "Fedor Holz"),
    (7, (1213, 355), "Justin Bonomo"),
    (8, (1385, 383), "Stephen Chidwick"),
    (9, (1549, 367), "Dan Smith"),
    (10, (1705, 356), "Bryn Kenney")
]

print("="*60)
print("FAST 10 PLAYERS UPDATE")
print("="*60)
print("\nUpdating 10 players in 3 seconds...")

time.sleep(3)

start = time.time()
success = 0

for num, (x, y), name in PLAYERS:
    try:
        print(f"Player {num}: {name}", end=" ")
        
        # 빠른 클릭
        pyautogui.click(x, y)
        time.sleep(0.3)
        
        # 더블클릭
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # 텍스트 입력
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(name, interval=0.01)
        pyautogui.press('enter')
        time.sleep(0.3)
        
        print("[OK]")
        success += 1
        
    except:
        print("[FAIL]")
        continue

elapsed = time.time() - start

print("\n" + "="*60)
print(f"Complete! {success}/10 updated in {elapsed:.1f}s")
print("="*60)

# 스크린샷
screenshot = pyautogui.screenshot()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"fast_update_{timestamp}.png"
screenshot.save(filename)
print(f"Screenshot: {filename}")