"""
Run Now - 10 Players Update
즉시 실행 버전
"""

import pyautogui
import time
from datetime import datetime

# 안전 설정
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

# 10명 좌표와 새 이름
PLAYERS = [
    ((215, 354), "Alice Johnson"),
    ((374, 359), "Bob Williams"),
    ((544, 362), "Charlie Brown"),
    ((722, 359), "David Miller"),
    ((886, 356), "Emma Davis"),
    ((1051, 354), "Frank Wilson"),
    ((1213, 355), "Grace Moore"),
    ((1385, 383), "Henry Taylor"),
    ((1549, 367), "Ivy Anderson"),
    ((1705, 356), "Jack Thomas")
]

print("="*60)
print("STARTING 10 PLAYERS UPDATE NOW")
print("="*60)
print("\nUpdating to:")
for i, (_, name) in enumerate(PLAYERS, 1):
    print(f"  Player {i}: {name}")

print("\nStarting in 3 seconds...")
print("Press ESC to stop!\n")

time.sleep(3)

start_time = time.time()
success = 0

for i, ((x, y), name) in enumerate(PLAYERS, 1):
    print(f"[{i}/10] Updating to {name}...", end=" ")
    
    try:
        # 클릭
        pyautogui.click(x, y)
        time.sleep(0.3)
        
        # 더블클릭
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # 텍스트 지우고 입력
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')
        time.sleep(0.1)
        pyautogui.typewrite(name, interval=0.02)
        time.sleep(0.2)
        
        # Enter
        pyautogui.press('enter')
        time.sleep(0.3)
        
        print("✓")
        success += 1
        
    except Exception as e:
        print(f"✗ ({e})")

elapsed = time.time() - start_time

print("\n" + "="*60)
print(f"COMPLETE: {success}/10 players updated")
print(f"Time: {elapsed:.1f} seconds")
print("="*60)

# 스크린샷
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot = pyautogui.screenshot()
filename = f"update_result_{timestamp}.png"
screenshot.save(filename)
print(f"\nScreenshot saved: {filename}")

print("\nUpdated names:")
for i, (_, name) in enumerate(PLAYERS, 1):
    print(f"  Player {i}: {name}")