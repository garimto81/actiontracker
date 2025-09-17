# Action Tracker Automation System

## ⚠️ 현재 상태: 칩 입력 문제 해결 중

### 🔴 칩 입력 문제 상황
현재 **칩 입력 기능이 정상 작동하지 않는 문제**가 있습니다.

#### 문제 증상:
1. **이름 입력은 정상 작동** - 플레이어 이름 업데이트는 문제없이 동작
2. **칩 입력만 실패** - 숫자 입력 후 반영되지 않음

#### 현재 구현된 로직:
```python
def input_chips(self, seat, chips):
    # 1. 플레이어 이름 좌표 클릭 (PLAYER_COORDS 사용)
    coords = PLAYER_COORDS[seat]
    pyautogui.click(coords[0], coords[1])
    
    # 2. 기존 값 지우기
    pyautogui.tripleClick()
    
    # 3. 칩 금액 입력
    for digit in str(chips):
        pyautogui.press(digit)
        time.sleep(0.1)
    
    # 4. Enter 키로 확정
    pyautogui.press('enter')
```

#### 시도한 해결 방법들:
1. ✅ 좌표 변경 (CHIP_COORDS → PLAYER_COORDS)
2. ✅ Enter 키 추가
3. ✅ Triple Click으로 기존 값 지우기
4. ✅ 입력 딜레이 추가 (0.1초)
5. ❌ **여전히 작동하지 않음**

#### 추가 조사 필요 사항:
- Action Tracker의 정확한 칩 입력 프로세스
- 칩 입력 필드가 별도로 존재하는지 확인
- 입력 후 추가 확인 단계가 필요한지

---

## 📁 프로젝트 구조

```
ActionTracker_Automation/
├── main/                              # 메인 애플리케이션
│   ├── integrated_gui_final_FINAL.py  # ⭐ 최종 GUI (Thread-safe 버전)
│   ├── action_tracker_manager.py      # 자동화 관리 모듈
│   └── chip_manager_system.py         # 칩 관리 시스템
│
├── tests/                             # 테스트 파일
│   └── test_chip_with_enter.py        # 칩 입력 테스트
│
├── tools/                             # 유틸리티
│   ├── coordinates/                   # 좌표 도구
│   └── debug/                         # 디버그 도구
│
└── old_versions/                      # 이전 버전
```

---

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 필요 패키지 설치
pip install pyautogui pandas numpy requests pillow
```

### 2. 메인 애플리케이션 실행
```bash
python main/integrated_gui_final_FINAL.py
```

---

## 🔧 주요 기능

### 1. Google Sheets 연동
- **URL**: 구글 시트 공개 CSV 링크 사용
- **자동 로드**: 테이블 데이터 실시간 동기화
- **다중 테이블**: 여러 테이블 동시 관리

### 2. 플레이어 관리

#### 이름 업데이트 프로세스 (✅ 정상 작동)
1. 플레이어 좌표 클릭
2. 서브 다이얼로그 이름 필드 클릭
3. Triple Click으로 전체 선택
4. 새 이름 입력
5. 완료 버튼 클릭

#### 칩 입력 프로세스 (❌ 문제 발생)
1. 플레이어 이름 좌표 클릭
2. Triple Click으로 선택
3. 칩 금액 입력
4. Enter 키 입력
**→ 현재 이 프로세스가 작동하지 않음**

#### 삭제 프로세스 (✅ 정상 작동)
1. 플레이어 좌표 클릭
2. 삭제 버튼 클릭

### 3. 자동 감지
- 플레이어 상태 자동 확인
- 빈 자리/점유 자리 구분
- 색상 분석 기반

### 4. 속도 설정
- **Ultra Fast**: 최소 딜레이 (0.1초)
- **Fast**: 빠른 처리 (0.3초)
- **Normal**: 안정적 처리 (0.5초)
- **Slow**: 디버깅용 (1.0초)

---

## 📍 좌표 시스템

### 플레이어 좌표 (이름 클릭 위치)
```python
PLAYER_COORDS = {
    1: (233, 361),   2: (374, 359),   3: (544, 362),
    4: (722, 359),   5: (886, 356),   6: (1051, 354),
    7: (1213, 355),  8: (1385, 383),  9: (1549, 367),
    10: (1705, 356)
}
```

### 기타 중요 좌표
```python
SUB_NAME_FIELD = (785, 291)   # 이름 입력 필드
COMPLETE_BUTTON = (1720, 139) # 완료 버튼
DELETE_BUTTON = (721, 112)    # 삭제 버튼
```

---

## 🧪 테스트 방법

### 칩 입력 테스트
```bash
# 칩 입력 디버깅
python tools/debug/debug_chip_input.py

# 칩 입력 테스트 (Enter 키 포함)
python tests/test_chip_with_enter.py
```

### 좌표 캡처
```bash
# 10개 좌표 캡처 도구
python tools/coordinates/capture_10_coordinates.py

# 실시간 마우스 좌표 추적
python tools/coordinates/simple_coordinate_tracker.py
```

---

## 🐛 알려진 문제와 해결

### 1. RuntimeError: main thread is not in main loop
**문제**: 스레드에서 GUI 직접 업데이트 시 발생
**해결**: Queue 기반 로깅 시스템 구현
```python
# Queue 사용
self.log_queue = queue.Queue()
self.log_queue.put(message)

# 메인 스레드에서 처리
self.root.after(100, self.process_log_queue)
```

### 2. 칩 입력 오버플로우
**문제**: 숫자가 너무 빨리 입력되어 오버플로우
**해결**: 각 숫자 입력 사이 0.1초 딜레이
```python
for digit in chip_str:
    pyautogui.press(digit)
    time.sleep(0.1)  # 딜레이 추가
```

### 3. 칩 입력 미작동 (현재 문제)
**문제**: 칩 입력 프로세스가 작동하지 않음
**조사 중**: 실제 Action Tracker의 칩 입력 방식 확인 필요

---

## 📝 기술 구현 세부사항

### Thread-Safe GUI
- Queue 기반 로깅 시스템
- `root.after()` 사용한 GUI 업데이트
- 스레드 간 안전한 통신

### PyAutoGUI 설정
```python
pyautogui.FAILSAFE = True  # 좌상단 이동시 중단
pyautogui.PAUSE = 0.1      # 기본 명령 간 딜레이
```

### 속도 최적화
- 동적 속도 조절
- 상황별 딜레이 설정
- 병렬 처리 가능 작업 구분

---

## 📊 프로세스 로직

### 1. 빈 자리 + 새 이름 → 신규 등록
```
1. 플레이어 좌표 클릭
2. 이름 필드에 새 이름 입력
3. 완료 버튼 클릭
```

### 2. 기존 플레이어 + 새 이름 → 이름 업데이트
```
1. 플레이어 좌표 클릭
2. 서브 다이얼로그의 이름 필드 클릭
3. Triple Click으로 전체 선택
4. 새 이름 입력
5. 완료 버튼 클릭
```

### 3. 칩 입력 (문제 발생 중)
```
1. 플레이어 이름 좌표 클릭
2. 기존 값 지우기
3. 칩 금액 입력
4. Enter 키 입력
```

---

## 🛠️ 빌드 방법

### EXE 파일 생성
```bash
cd builds
build_exe.bat
```

### 포터블 버전
```bash
cd builds
build_portable.bat
```

---

## 📈 버전 히스토리

### v1.0 FINAL (2025-09-11)
- ✅ Thread-safe GUI 구현
- ✅ Queue 기반 로깅 시스템
- ✅ 프로젝트 구조 정리
- ❌ 칩 입력 문제 미해결

### 이전 버전
- `integrated_gui_final.py` - 초기 버전
- `integrated_gui_final_fixed.py` - 버그 수정
- `integrated_gui_final_fixed_v2.py` - 추가 개선

---

## ⚙️ 설정 파일

### Google Sheets URL
```python
self.sheet_url = "https://docs.google.com/spreadsheets/d/e/..."
```

### 속도 설정
```python
self.speed_vars = {
    "mouse_click_delay": 0.1,
    "keyboard_type_interval": 0.05,
    "action_delay": 0.1,
    "screen_wait": 0.2
}
```

---

## 🔍 디버깅 도구

### 1. 칩 입력 디버깅
```bash
python tools/debug/debug_chip_input.py
```
- 다양한 입력 방법 테스트
- 포커스 문제 확인
- 단계별 실행

### 2. 좌표 확인
```bash
python tools/coordinates/simple_coordinate_tracker.py
```
- 실시간 마우스 좌표
- RGB 색상 값
- 화면 위치 확인

---

## 📞 문제 해결 지원

### 칩 입력 문제 해결을 위한 체크리스트:
1. ☐ Action Tracker가 활성 창인지 확인
2. ☐ 올바른 좌표를 사용하는지 확인
3. ☐ 칩 입력 필드가 별도로 존재하는지 확인
4. ☐ Enter 키 외에 다른 확인 방법이 있는지 확인
5. ☐ 칩 입력 시 특별한 포맷이 필요한지 확인

---

## 📄 라이센스
Internal Use Only

---

## 🔄 업데이트 필요 사항

1. **칩 입력 문제 해결** - 최우선
2. 칩 입력 프로세스 재검증
3. Action Tracker UI 변경사항 확인
4. 대체 입력 방법 연구

---

*Last Updated: 2025-09-11*
*Status: 칩 입력 기능 수정 진행 중*