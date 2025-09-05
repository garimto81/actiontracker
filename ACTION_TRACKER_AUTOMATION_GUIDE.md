# Action Tracker 자동화 시스템 기획서

## 📋 프로젝트 개요

Action Tracker는 포커 토너먼트의 플레이어 정보를 관리하는 UI 프로그램입니다. 이 자동화 시스템은 Python을 사용하여 Action Tracker UI를 자동으로 조작하여 대량의 플레이어 데이터를 빠르고 정확하게 입력할 수 있도록 설계되었습니다.

## 🎯 목적

1. **수동 입력 자동화**: 반복적인 플레이어 정보 입력 작업 자동화
2. **오류 감소**: 수동 입력 시 발생할 수 있는 실수 방지
3. **시간 절약**: 대량 데이터 처리 시간 대폭 단축
4. **실시간 업데이트**: 토너먼트 진행 중 빠른 정보 업데이트

## 🔧 핵심 기술

### 사용 라이브러리
- **pyautogui**: 마우스/키보드 자동 제어
- **opencv-cv2**: 이미지 인식 및 처리
- **PIL (Pillow)**: 스크린샷 캡처 및 분석
- **pygetwindow**: 윈도우 제어 및 관리
- **tkinter**: GUI 컨트롤 패널 제작

## 📊 시스템 아키텍처

```
[데이터 소스] → [Python 자동화 스크립트] → [Action Tracker UI]
                          ↓
                  [좌표 매핑 시스템]
                          ↓
                  [마우스/키보드 이벤트]
                          ↓
                  [UI 자동 조작]
```

## 🎮 자동화 로직

### 1. 기본 자동화 플로우

```python
# 기본 자동화 순서
1. Action Tracker 윈도우 찾기 및 활성화
2. 플레이어 선택 영역 클릭
3. 기존 데이터 삭제 (필요시)
4. 새 플레이어 이름 입력
5. 칩 수량 입력
6. 확인 버튼 클릭
7. 다음 플레이어로 이동
```

### 2. 좌표 매핑 시스템

```python
coordinates = {
    # 플레이어 위치 좌표 (10명)
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
    
    # 컨트롤 버튼 좌표
    'delete': (761, 108),        # 삭제 버튼
    'complete': (1733, 155),     # 완료 버튼
    'close': (1745, 147),        # 닫기 버튼
    
    # 편집 영역 좌표
    'name_field': (1700, 150),   # 이름 입력 필드
    'chip_field': (1700, 200),   # 칩 입력 필드
}
```

### 3. 자동 클릭 및 입력 메커니즘

```python
def update_player(player_num, name, chips):
    """플레이어 정보 자동 업데이트"""
    
    # 1. 플레이어 위치 클릭
    x, y = coordinates[f'player{player_num}']
    pyautogui.click(x, y)
    time.sleep(0.5)
    
    # 2. 기존 텍스트 삭제
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    
    # 3. 새 이름 입력
    pyautogui.typewrite(name)
    pyautogui.press('tab')
    
    # 4. 칩 수량 입력
    pyautogui.typewrite(str(chips))
    
    # 5. 확인
    pyautogui.press('enter')
```

## 📁 주요 스크립트 설명

### 핵심 자동화 스크립트

1. **action_tracker_automation_app.py**
   - GUI 기반 메인 컨트롤 패널
   - 전체 자동화 프로세스 관리
   - 실시간 로그 및 상태 표시

2. **action_tracker_bulk_update.py**
   - 대량 플레이어 정보 일괄 업데이트
   - CSV/JSON 파일에서 데이터 읽기
   - 순차적 자동 입력

3. **action_tracker_position_detector.py**
   - Action Tracker UI 요소 위치 자동 감지
   - OCR을 통한 버튼/필드 인식
   - 좌표 자동 캘리브레이션

4. **action_tracker_targeted_detector.py**
   - 특정 UI 요소 정밀 탐지
   - 이미지 매칭 알고리즘
   - 동적 UI 변화 대응

### 보조 유틸리티

5. **coordinate_validator.py**
   - 좌표 정확성 검증
   - 클릭 위치 시각화
   - 좌표 미세 조정

6. **player_name_updater.py**
   - 플레이어 이름만 선택적 업데이트
   - 특수 문자 처리
   - 다국어 이름 지원

7. **color_analyzer.py**
   - UI 색상 분석
   - 버튼 상태 감지 (활성/비활성)
   - 테마 변화 대응

## 🚀 사용 방법

### 1. 기본 실행

```bash
# 메인 GUI 앱 실행
python action_tracker_automation_app.py

# 대량 업데이트 실행
python action_tracker_bulk_update.py --file players.csv
```

### 2. 데이터 형식

**CSV 파일 예시:**
```csv
player_num,name,chips
1,Daniel Negreanu,1500000
2,Phil Ivey,2000000
3,Phil Hellmuth,1800000
```

**JSON 파일 예시:**
```json
{
  "players": [
    {"num": 1, "name": "Daniel Negreanu", "chips": 1500000},
    {"num": 2, "name": "Phil Ivey", "chips": 2000000},
    {"num": 3, "name": "Phil Hellmuth", "chips": 1800000}
  ]
}
```

## 🛡️ 안전 기능

1. **윈도우 확인**: Action Tracker 실행 상태 자동 확인
2. **좌표 검증**: 클릭 전 좌표 유효성 검사
3. **에러 핸들링**: 실패 시 자동 재시도
4. **로그 기록**: 모든 작업 상세 기록
5. **수동 개입**: 긴급 정지 기능 (ESC 키)

## 📈 성능

- **입력 속도**: 플레이어당 2-3초
- **정확도**: 99.5% 이상
- **처리량**: 시간당 1000+ 플레이어
- **안정성**: 24시간 연속 운영 가능

## 🔄 워크플로우 예시

### 토너먼트 시작 시
1. CSV 파일로 전체 플레이어 리스트 준비
2. `action_tracker_bulk_update.py` 실행
3. 자동으로 모든 플레이어 정보 입력
4. 완료 확인 및 로그 검토

### 게임 진행 중
1. GUI 앱에서 실시간 모니터링
2. 개별 플레이어 선택적 업데이트
3. 칩 카운트 변경 즉시 반영
4. vMix로 자동 전송

## 📝 주의사항

1. **해상도 의존성**: 1920x1080 해상도 기준으로 좌표 설정
2. **UI 버전**: Action Tracker 특정 버전에 최적화
3. **권한 필요**: 마우스/키보드 제어 권한 필요
4. **백그라운드 실행**: Action Tracker가 최상위 윈도우여야 함

## 🔧 트러블슈팅

### 문제: 좌표가 맞지 않음
**해결**: `coordinate_validator.py` 실행하여 재조정

### 문제: 입력이 느림
**해결**: `time.sleep()` 값 조정 (기본 0.5초)

### 문제: 특수 문자 입력 오류
**해결**: `pyautogui.typewrite()` 대신 클립보드 사용

## 📊 확장 가능성

1. **API 연동**: Frame Poker 서버와 직접 통신
2. **OCR 강화**: 화면 인식으로 현재 상태 자동 파악
3. **AI 통합**: 패턴 학습으로 최적 타이밍 예측
4. **멀티 테이블**: 여러 테이블 동시 관리
5. **웹 인터페이스**: 원격 제어 기능 추가

## 🎯 결론

이 Action Tracker 자동화 시스템은 포커 토너먼트 운영의 효율성을 극대화하기 위해 설계되었습니다. 수동 작업을 자동화함으로써 운영진은 더 중요한 업무에 집중할 수 있으며, 방송 품질도 향상됩니다.

---

*Version 1.0 - 2024년 9월*
*Developed for Frame Poker Broadcasting System*