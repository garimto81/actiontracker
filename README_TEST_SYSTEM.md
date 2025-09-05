# Action Tracker Test Input System

## 🚀 Quick Start

### 실행 방법

1. **간단한 테스트 실행기 (권장)**
   ```cmd
   python test_runner_en.py
   ```

2. **배치 파일로 실행**
   ```cmd
   run_test.bat
   ```

3. **GUI 테스트 앱 (고급)**
   ```cmd
   python test_input_app.py
   ```

## 📋 테스트 모드

### 1️⃣ 정보 표시 모드
- 시스템 정보 확인
- 테스트 데이터 검토
- 화면 해상도 확인
- 현재 마우스 좌표 표시

### 2️⃣ 좌표 테스트 모드
- **실제 클릭 없음**
- 마우스만 이동하여 위치 확인
- 10명의 플레이어 위치 순차 확인
- Action Tracker 실행 없이도 테스트 가능

### 3️⃣ 시뮬레이션 모드
- **로직만 실행**
- 실제 마우스/키보드 조작 없음
- 처리 시간 예측
- 자동화 플로우 검증

### 4️⃣ 자동화 데모
- 전체 자동화 로직 설명
- 주요 기능 소개
- 구현 방식 안내

## 📁 테스트 데이터

### JSON 형식 (`test_players_data.json`)
```json
{
  "players": [
    {
      "num": 1,
      "name": "Daniel Negreanu",
      "chips": 1500000
    }
  ]
}
```

### CSV 형식 (`test_players.csv`)
```csv
player_num,name,chips
1,Daniel Negreanu,1500000
2,Phil Ivey,2000000
```

## 🎯 좌표 시스템

### 플레이어 위치 (1920x1080 기준)
```python
Player 1: (215, 354)
Player 2: (386, 364)
Player 3: (560, 485)
Player 4: (559, 486)
Player 5: (557, 364)
Player 6: (721, 362)
Player 7: (737, 369)
Player 8: (890, 369)
Player 9: (860, 364)
Player 10: (1037, 357)
```

### 컨트롤 버튼
```python
Delete: (761, 108)
Complete: (1733, 155)
Close: (1745, 147)
Edit: (815, 294)
```

## ⚙️ 설정 옵션

### 안전 설정
- **ESC 키**: 긴급 정지
- **Failsafe**: 화면 모서리로 마우스 이동 시 정지
- **Pause**: 각 동작 사이 0.5초 대기

### 속도 조절
- `pyautogui.PAUSE`: 기본 0.5초
- 테스트 앱에서 실시간 조절 가능 (0.1~2.0초)

## 📊 테스트 결과

### 예상 성능
- **플레이어당 처리 시간**: 2-3초
- **10명 처리**: 약 20-30초
- **정확도**: 99%+ (좌표 기반)

### 로그 정보
- 각 단계별 처리 상태
- 에러 발생 시 자세한 정보
- 처리 시간 통계

## 🔧 문제 해결

### 문제: 인코딩 에러
**해결**: `test_runner_en.py` 사용 (영문 버전)

### 문제: 좌표가 맞지 않음
**해결**: 
1. 화면 해상도 확인 (1920x1080 권장)
2. `coordinate_validator.py` 실행하여 재조정

### 문제: Action Tracker를 찾을 수 없음
**해결**:
1. Action Tracker가 실행 중인지 확인
2. 윈도우 제목이 "Action Tracker"인지 확인

## 📌 주의사항

1. **테스트 모드부터 시작**: 실제 실행 전 반드시 테스트
2. **Action Tracker 백업**: 중요한 데이터는 백업
3. **화면 해상도**: 1920x1080에 최적화됨
4. **권한**: 관리자 권한 필요할 수 있음

## 🎮 실제 사용 시나리오

### 시나리오 1: 토너먼트 시작
1. CSV 파일에 모든 플레이어 정보 준비
2. `test_runner_en.py` 실행
3. 옵션 3 (시뮬레이션)으로 테스트
4. Action Tracker 실행
5. 실제 자동 입력 실행

### 시나리오 2: 개별 업데이트
1. GUI 테스트 앱 실행
2. 특정 플레이어 선택
3. 개별 업데이트 실행

### 시나리오 3: 대량 처리
1. JSON 파일 준비 (100+ 플레이어)
2. 배치 모드로 실행
3. 자동 처리 및 로그 확인

## 📞 지원

문제 발생 시:
1. 로그 파일 확인
2. 테스트 모드로 재실행
3. 좌표 재조정

---

*Action Tracker Automation Test System v1.0*
*Location: c:\claude02\ActionTracker_Automation\*