"""
Action Tracker Player 1 Name Update Logic
플레이어 1번의 이름을 변경하는 완전한 자동화 스크립트
"""

import pyautogui
import time
import cv2
import numpy as np
from PIL import Image

class Player1NameUpdater:
    def __init__(self):
        """플레이어 1 이름 업데이터 초기화"""
        # 메인 화면 좌표 (이전 분석 결과 기반)
        self.player1_main_button = (209, 658)  # 메인 화면의 player1 빨간 버튼
        
        # 편집 화면 좌표 (분석된 편집 다이얼로그 기반)
        self.edit_name_field = (582, 196)      # NAME 필드의 골든 버튼
        self.edit_close_x = (1232, 73)         # X 버튼으로 닫기
        
        # 안전 설정
        self.click_delay = 0.5
        self.type_delay = 0.1
        self.dialog_wait = 1.0
        
    def capture_screenshot(self, filename="debug_screenshot.png"):
        """디버깅용 스크린샷 캡처"""
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"스크린샷 저장: {filename}")
        return screenshot
    
    def safe_click(self, x, y, description=""):
        """안전한 클릭 (좌표 유효성 검사 포함)"""
        try:
            print(f"클릭: ({x}, {y}) - {description}")
            pyautogui.click(x, y)
            time.sleep(self.click_delay)
            return True
        except Exception as e:
            print(f"클릭 실패: {e}")
            return False
    
    def safe_type(self, text, clear_first=True):
        """안전한 텍스트 입력"""
        try:
            if clear_first:
                # 기존 텍스트 전체 선택 후 삭제
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(self.type_delay)
            
            # 새 텍스트 입력
            pyautogui.typewrite(str(text))
            time.sleep(self.type_delay)
            return True
        except Exception as e:
            print(f"텍스트 입력 실패: {e}")
            return False
    
    def wait_for_dialog(self, wait_time=1.0):
        """다이얼로그가 열릴 때까지 대기"""
        print(f"다이얼로그 로딩 대기: {wait_time}초")
        time.sleep(wait_time)
    
    def check_main_screen(self):
        """메인 화면 상태 확인"""
        print("메인 화면 상태 확인 중...")
        screenshot = self.capture_screenshot("main_screen_check.png")
        
        # 간단한 색상 기반 확인 (빨간색 플레이어 버튼이 있는지)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 빨간색 범위 (실제로는 다크 레드)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        red_pixels = cv2.countNonZero(mask)
        is_main_screen = red_pixels > 1000  # 충분한 빨간색 픽셀이 있으면 메인 화면
        
        print(f"메인 화면 감지: {'예' if is_main_screen else '아니오'} (빨간 픽셀: {red_pixels})")
        return is_main_screen
    
    def check_edit_dialog(self):
        """편집 다이얼로그 상태 확인"""
        print("편집 다이얼로그 상태 확인 중...")
        screenshot = self.capture_screenshot("edit_dialog_check.png")
        
        # 간단한 확인: "NAME" 텍스트나 골든 버튼이 있는지
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # 골든색 범위
        lower_gold = np.array([15, 100, 100])
        upper_gold = np.array([35, 255, 255])
        mask = cv2.inRange(hsv, lower_gold, upper_gold)
        
        gold_pixels = cv2.countNonZero(mask)
        is_edit_dialog = gold_pixels > 5000  # 충분한 골든색 픽셀이 있으면 편집 다이얼로그
        
        print(f"편집 다이얼로그 감지: {'예' if is_edit_dialog else '아니오'} (골든 픽셀: {gold_pixels})")
        return is_edit_dialog
    
    def update_player1_name(self, new_name):
        """플레이어 1의 이름을 업데이트하는 메인 로직"""
        print("="*60)
        print(f"플레이어 1 이름 업데이트 시작: '{new_name}'")
        print("="*60)
        
        try:
            # 1단계: 메인 화면 확인
            if not self.check_main_screen():
                print("[경고] 메인 화면이 아닌 것 같습니다. 계속 진행합니다.")
            
            # 2단계: 플레이어 1 버튼 클릭 (메인 화면)
            print("\n[1단계] 메인 화면에서 Player1 버튼 클릭")
            if not self.safe_click(self.player1_main_button[0], self.player1_main_button[1], 
                                 "Player1 메인 버튼"):
                return False
            
            # 3단계: 편집 다이얼로그 로딩 대기
            print("\n[2단계] 편집 다이얼로그 로딩 대기")
            self.wait_for_dialog(self.dialog_wait)
            
            # 4단계: 편집 다이얼로그 확인
            if not self.check_edit_dialog():
                print("[오류] 편집 다이얼로그가 열리지 않았습니다.")
                return False
            
            # 5단계: NAME 필드 클릭
            print("\n[3단계] NAME 필드 클릭")
            if not self.safe_click(self.edit_name_field[0], self.edit_name_field[1], 
                                 "NAME 필드"):
                return False
            
            # 6단계: 새 이름 입력
            print(f"\n[4단계] 새 이름 입력: '{new_name}'")
            if not self.safe_type(new_name, clear_first=True):
                return False
            
            # 7단계: Enter로 확정
            print("\n[5단계] Enter로 이름 확정")
            pyautogui.press('enter')
            time.sleep(self.click_delay)
            
            # 8단계: 다이얼로그 닫기 (X 버튼 클릭)
            print("\n[6단계] 편집 다이얼로그 닫기")
            if not self.safe_click(self.edit_close_x[0], self.edit_close_x[1], 
                                 "다이얼로그 X 버튼"):
                return False
            
            # 9단계: 메인 화면 복귀 대기
            print("\n[7단계] 메인 화면 복귀 대기")
            time.sleep(self.dialog_wait)
            
            # 10단계: 최종 확인
            print("\n[8단계] 업데이트 완료 확인")
            final_screenshot = self.capture_screenshot("update_complete.png")
            
            print("="*60)
            print(f"✅ 플레이어 1 이름 업데이트 완료: '{new_name}'")
            print("최종 스크린샷: update_complete.png")
            print("="*60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 업데이트 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            
            # 오류 발생 시 스크린샷
            self.capture_screenshot("error_screenshot.png")
            return False
    
    def test_coordinates(self):
        """좌표 테스트 (실제 클릭하지 않고 위치만 확인)"""
        print("좌표 테스트 모드")
        print("="*40)
        
        # 현재 화면 캡처
        screenshot = pyautogui.screenshot()
        img_pil = Image.fromarray(np.array(screenshot))
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img_pil)
        
        # 테스트할 좌표들에 마커 표시
        coords = [
            (self.player1_main_button, "Player1 Main", "red"),
            (self.edit_name_field, "NAME Field", "blue"),
            (self.edit_close_x, "Close X", "green")
        ]
        
        for (x, y), label, color in coords:
            # 십자 마커 그리기
            draw.line([(x-20, y), (x+20, y)], fill=color, width=3)
            draw.line([(x, y-20), (x, y+20)], fill=color, width=3)
            draw.text((x+25, y-10), f"{label} ({x},{y})", fill=color)
            
            print(f"{label}: ({x}, {y})")
        
        # 테스트 이미지 저장
        img_pil.save("coordinate_test.png")
        print("좌표 테스트 이미지 저장: coordinate_test.png")

def main():
    """메인 실행 함수"""
    updater = Player1NameUpdater()
    
    print("Action Tracker Player 1 Name Updater")
    print("====================================")
    print()
    print("옵션:")
    print("1. 좌표 테스트 (실제 클릭 없이 위치만 확인)")
    print("2. 플레이어 1 이름 업데이트")
    print()
    
    try:
        choice = input("선택 (1 또는 2): ").strip()
        
        if choice == "1":
            updater.test_coordinates()
        
        elif choice == "2":
            new_name = input("새 플레이어 이름 입력: ").strip()
            if not new_name:
                print("이름을 입력해주세요.")
                return
            
            print(f"\n'{new_name}'으로 업데이트를 시작합니다...")
            print("Action Tracker가 활성화되어 있는지 확인하세요!")
            print("3초 후 시작...")
            
            for i in range(3, 0, -1):
                print(f"{i}...")
                time.sleep(1)
            
            success = updater.update_player1_name(new_name)
            
            if success:
                print("✅ 업데이트 성공!")
            else:
                print("❌ 업데이트 실패!")
        
        else:
            print("잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n사용자가 취소했습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()