"""
Simple Player1 Name Update Logic
사용자가 클릭한 정확한 좌표를 사용한 간단한 이름 변경 로직
"""

import pyautogui
import time

class SimplePlayer1Updater:
    def __init__(self):
        """초기화 - 사용자가 클릭한 정확한 좌표 사용"""
        # 사용자가 클릭하여 수집한 좌표들
        self.COORDINATES = {
            'player1_button': (215, 354),     # Player1 버튼 (사용자 클릭)
            'player_edit_field': (815, 294)   # Player 편집 필드 (사용자 클릭)
        }
        
        # 안전 설정
        self.click_delay = 0.8    # 클릭 후 대기 시간
        self.type_delay = 0.2     # 타이핑 후 대기 시간
        
    def safe_click(self, coordinate_name, description=""):
        """안전한 클릭 실행"""
        if coordinate_name not in self.COORDINATES:
            print(f"❌ 좌표를 찾을 수 없습니다: {coordinate_name}")
            return False
            
        x, y = self.COORDINATES[coordinate_name]
        
        try:
            print(f"🖱️  클릭: ({x}, {y}) - {description}")
            pyautogui.click(x, y)
            time.sleep(self.click_delay)
            return True
        except Exception as e:
            print(f"❌ 클릭 실패: {e}")
            return False
    
    def safe_type(self, text, clear_first=True):
        """안전한 텍스트 입력"""
        try:
            if clear_first:
                print(f"📝 기존 텍스트 지우기")
                pyautogui.hotkey('ctrl', 'a')  # 전체 선택
                time.sleep(self.type_delay)
                
            print(f"✏️  입력: '{text}'")
            pyautogui.typewrite(str(text))
            time.sleep(self.type_delay)
            return True
        except Exception as e:
            print(f"❌ 입력 실패: {e}")
            return False
    
    def update_player1_name(self, new_name):
        """Player1 이름 업데이트 - 간단한 2단계 로직"""
        print("=" * 60)
        print(f"🎯 Player1 이름 변경 시작: '{new_name}'")
        print("=" * 60)
        
        try:
            # 1단계: Player1 버튼 클릭
            print("\n[1단계] Player1 버튼 클릭")
            if not self.safe_click('player1_button', 'Player1 버튼'):
                return False
            
            # 2단계: 편집 필드 클릭 및 이름 입력
            print("\n[2단계] 편집 필드에 새 이름 입력")
            if not self.safe_click('player_edit_field', '편집 필드'):
                return False
            
            # 3단계: 새 이름 입력
            print(f"\n[3단계] 새 이름 입력")
            if not self.safe_type(new_name, clear_first=True):
                return False
            
            # 4단계: Enter로 확정
            print(f"\n[4단계] Enter로 확정")
            pyautogui.press('enter')
            time.sleep(self.click_delay)
            
            print("\n" + "=" * 60)
            print(f"✅ 완료! Player1 이름이 '{new_name}'로 변경되었습니다.")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            return False
    
    def test_coordinates(self):
        """좌표 테스트 (실제 클릭 없이 위치만 확인)"""
        print("🧪 좌표 테스트 모드")
        print("-" * 40)
        
        for name, (x, y) in self.COORDINATES.items():
            print(f"{name}: ({x}, {y})")
        
        # 현재 화면에 마커 표시
        try:
            import pyautogui
            from PIL import Image, ImageDraw
            
            screenshot = pyautogui.screenshot()
            draw = ImageDraw.Draw(screenshot)
            
            colors = ['red', 'blue', 'green', 'yellow']
            for i, (name, (x, y)) in enumerate(self.COORDINATES.items()):
                color = colors[i % len(colors)]
                
                # 십자 마커
                draw.line([(x-25, y), (x+25, y)], fill=color, width=4)
                draw.line([(x, y-25), (x, y+25)], fill=color, width=4)
                
                # 라벨
                draw.text((x+30, y-15), f"{name}\n({x},{y})", fill=color)
            
            screenshot.save("coordinate_test_simple.png")
            print("📷 좌표 테스트 이미지 저장: coordinate_test_simple.png")
            
        except Exception as e:
            print(f"⚠️  이미지 저장 실패: {e}")

def main():
    """메인 실행"""
    updater = SimplePlayer1Updater()
    
    print("🎮 Simple Player1 Name Updater")
    print("=" * 40)
    print("수집된 좌표:")
    for name, (x, y) in updater.COORDINATES.items():
        print(f"  {name}: ({x}, {y})")
    print()
    print("옵션:")
    print("1. 좌표 테스트 (마커 표시)")
    print("2. Player1 이름 변경")
    print()
    
    try:
        choice = input("선택 (1 또는 2): ").strip()
        
        if choice == "1":
            updater.test_coordinates()
            
        elif choice == "2":
            new_name = input("새 플레이어 이름 입력: ").strip()
            if not new_name:
                print("❌ 이름을 입력해주세요.")
                return
                
            print(f"\n🚀 '{new_name}'로 업데이트를 시작합니다...")
            print("⚠️  Action Tracker가 활성화되어 있는지 확인하세요!")
            
            # 카운트다운
            for i in range(3, 0, -1):
                print(f"⏰ {i}초 후 시작...")
                time.sleep(1)
            
            print("\n🎬 시작!")
            success = updater.update_player1_name(new_name)
            
            if success:
                print("\n🎉 업데이트 성공!")
                
                # 결과 확인 제안
                print("\n💡 결과 확인:")
                print("   Action Tracker에서 Player1 버튼을 확인해보세요.")
                
            else:
                print("\n💥 업데이트 실패!")
                print("   좌표가 정확한지 확인해보세요.")
        
        else:
            print("❌ 잘못된 선택입니다.")
            
    except KeyboardInterrupt:
        print("\n🛑 사용자가 취소했습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    main()