# Action Tracker 통합 시스템 가이드

## 🎯 시스템 개요

플레이어 이름, 칩 스택, 자동 감지를 모두 통합한 완전한 관리 시스템

### 주요 기능
1. **Google Sheets DB 연동** - 실시간 플레이어/칩 데이터 로드
2. **자동 감지** - 현재 플레이어 상태 자동 파악
3. **칩 입력** - 각 시트별 칩 스택 입력
4. **상태 저장/로드** - 작업 상태 저장 및 재사용

## 📊 Google Sheets 데이터 구조

```csv
Camera Preset | player | Table | Notable | Chips | updatedAt | Seat
```

- **Table**: 테이블 번호
- **Seat**: 시트 번호 (1-10)
- **player**: 플레이어 이름
- **Chips**: 칩 스택 수량
- **Notable**: 주요 플레이어 여부

## 💰 칩 입력 프로세스

### 칩 좌표
```python
Seat 1: (1226, 622)
Seat 2: (1382, 619)
Seat 3: (1537, 615)
Seat 4: (1688, 615)
Seat 5-6: (1694, 615)
Seat 7: (1226, 622)
Seat 8: (1382, 619)
Seat 9: (1537, 615)
Seat 10: (1688, 615)
```

### 입력 프로세스
1. 칩 입력 필드 클릭
2. 기존 값 지우기 (Triple Click)
3. 새 칩 수량 입력
4. Enter 키 입력

## 🔄 전체 워크플로우

### 1단계: 데이터 로드
```
1. GUI 실행
2. "Load from DB" 클릭
3. 테이블 선택
4. "Apply Table Data" 클릭
```

### 2단계: 현재 상태 확인
```
1. "Auto Detect" 클릭
2. 빈자리/등록된 자리 자동 감지
3. 필요시 수동 조정
```

### 3단계: 업데이트 실행
```
옵션 A: 이름만 업데이트
- "UPDATE NAMES ONLY" 클릭

옵션 B: 칩만 업데이트
- "UPDATE CHIPS ONLY" 클릭

옵션 C: 모두 업데이트
- "UPDATE ALL" 클릭
```

### 4단계: 상태 저장
```
1. "Save State" 클릭
2. JSON 파일로 저장
3. 다음 작업시 "Load State"로 재사용
```

## 🎮 GUI 구성

### 상단 - 테이블 선택
- Table 콤보박스
- Load from DB 버튼
- Apply Table Data 버튼

### 중앙 - 플레이어/칩 관리
각 시트별로:
- **Seat**: 시트 번호
- **Status**: 🔴 Occupied / ⚪ Empty / ⚫ Unknown
- **Empty**: 빈자리 체크박스
- **Player Name**: 플레이어 이름 입력
- **Chips**: 칩 수량 입력
- **Delete**: 삭제 체크박스

### 우측 - 컨트롤
- **Speed Settings**: Ultra Fast / Fast / Normal / Slow
- **Actions**: 
  - 📝 UPDATE NAMES ONLY
  - 💰 UPDATE CHIPS ONLY
  - 🔄 UPDATE ALL
  - 🗑️ DELETE SELECTED

## 🚀 사용 시나리오

### 시나리오 1: 새 테이블 세팅
```
1. Load from DB → 테이블 선택
2. Apply Table Data
3. UPDATE ALL 실행
4. Save State
```

### 시나리오 2: 칩 카운트 업데이트
```
1. Load State (이전 상태)
2. 칩 수량만 수정
3. UPDATE CHIPS ONLY
```

### 시나리오 3: 플레이어 교체
```
1. Auto Detect (현재 상태 파악)
2. 변경된 시트의 이름 수정
3. UPDATE NAMES ONLY
```

## 🔧 속도 설정

| 모드 | 클릭 | 타이핑 | 화면대기 | 용도 |
|------|------|--------|----------|------|
| Ultra Fast | 0.08s | 0.008s | 0.4s | 테스트 |
| Fast | 0.15s | 0.012s | 0.6s | 빠른 작업 |
| Normal | 0.30s | 0.020s | 1.0s | 일반 작업 |
| Slow | 0.50s | 0.050s | 2.0s | 안전한 작업 |

## 📁 파일 구조

```
ActionTracker_Automation/
├── integrated_gui_final.py      # 통합 GUI (최종)
├── chip_manager_system.py       # 칩 관리 시스템
├── auto_detect_players.py       # 자동 감지
├── table_X_state.json          # 테이블별 상태 저장
└── gui_auto_config.json        # 자동 설정 파일
```

## ⚠️ 주의사항

1. **플레이어 등록 여부 확인**
   - 빈자리는 3단계 프로세스
   - 기존 플레이어는 5단계 프로세스

2. **칩 입력 제약**
   - 플레이어가 등록된 시트만 칩 입력 가능
   - 빈자리는 칩 입력 불가

3. **테이블 데이터 적용**
   - 기존 데이터는 모두 삭제됨
   - 테이블에 없는 시트는 자동으로 빈자리 처리

## 💡 팁

- **빠른 업데이트**: Ultra Fast 모드 사용 (불안정할 수 있음)
- **안전한 작업**: Slow 모드 + Save State 활용
- **반복 작업**: Load State로 이전 상태 빠르게 복원
- **일괄 처리**: UPDATE ALL로 한 번에 처리

## 🐛 문제 해결

### 감지 실패
- Action Tracker가 전체 화면에 보이는지 확인
- 화면 해상도 변경 확인

### 칩 입력 실패
- 플레이어가 먼저 등록되었는지 확인
- 칩 좌표가 정확한지 확인

### Google Sheets 로드 실패
- 인터넷 연결 확인
- URL이 올바른지 확인

## 📞 실행 명령

```bash
# 통합 GUI 실행
python integrated_gui_final.py

# 칩 관리 테스트
python chip_manager_system.py

# 자동 감지 테스트
python auto_detect_players.py
```

완전 자동화된 Action Tracker 관리 시스템을 즐기세요! 🎮