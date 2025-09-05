# 📍 좌표 확인 도구 가이드

## 🔧 사용 가능한 좌표 도구들

### 1. **simple_coord_check.py** ⭐ 가장 간단
```bash
python simple_coord_check.py
```
- **옵션 1**: 5초간 마우스 좌표 실시간 표시
- **옵션 2**: 알려진 위치로 자동 이동
- 화면 해상도 확인 가능

### 2. **mouse_position_tracker.py** ⭐ 추천
```bash
python mouse_position_tracker.py
```
- 실시간 마우스 좌표 추적
- **SPACE**: 현재 좌표 저장
- **ESC**: 종료
- 저장된 좌표를 Python 코드로 출력

### 3. **click_coordinate_analyzer.py**
```bash
python click_coordinate_analyzer.py
```
- 클릭한 위치 자동 기록
- 스크린샷 자동 저장
- JSON 파일로 저장

### 4. **click_coordinate_collector.py**
```bash
python click_coordinate_collector.py
```
- 마우스 클릭 좌표 수집
- 레이블과 함께 저장

### 5. **coordinate_validator_en.py**
```bash
python coordinate_validator_en.py
```
- 알려진 좌표 검증
- 스크린샷에 좌표 표시
- 올바른 위치인지 확인

## 📊 현재 확인된 좌표들

### Player 위치
```python
coordinates = {
    'player1': (215, 354),
    'player2': (386, 364),
    'player3': (560, 485),
    'player4': (559, 486),
    'player5': (557, 364),
    'player6': (721, 362),
    'player7': (737, 369),
    'player8': (890, 369),
    'player9': (860, 364),
    'player10': (1037, 357),
}
```

### 컨트롤 버튼
```python
buttons = {
    'delete': (761, 108),
    'complete': (1733, 155),
    'close': (1745, 147),
    'edit': (815, 294),
}
```

## 💡 사용 예시

### 새로운 좌표 찾기
```bash
# 실시간으로 마우스 위치 보기
python mouse_position_tracker.py

# 원하는 위치에서 SPACE 누르기
# 좌표가 자동으로 저장됨
```

### 기존 좌표 확인
```bash
# 저장된 좌표로 마우스 이동
python simple_coord_check.py
# 2번 선택
```

### 좌표 검증
```bash
# 좌표가 올바른지 스크린샷으로 확인
python coordinate_validator_en.py
```

## 🖱️ 빠른 실행 명령

**현재 마우스 위치 즉시 보기:**
```bash
cd c:\claude02\ActionTracker_Automation && echo "1" | python simple_coord_check.py
```

**좌표 실시간 추적:**
```bash
cd c:\claude02\ActionTracker_Automation && python mouse_position_tracker.py
```

## 📝 참고사항

- 화면 해상도: **1920x1200**
- Action Tracker가 실행 중이어야 정확한 좌표 확인 가능
- 윈도우 위치가 바뀌면 좌표도 변경됨
- ESC 키로 언제든지 중단 가능

---

모든 좌표 도구가 정상 작동하며, 필요에 따라 선택해서 사용하시면 됩니다!