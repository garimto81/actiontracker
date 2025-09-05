# Action Tracker Automation - 프로세스 로직 가이드

## 📋 목차
1. [이름 입력 프로세스](#이름-입력-프로세스)
2. [칩 입력 프로세스](#칩-입력-프로세스)
3. [좌표 시스템](#좌표-시스템)
4. [순차 처리 로직](#순차-처리-로직)
5. [속도 설정](#속도-설정)

---

## 🎯 이름 입력 프로세스

### 1. 기존 이름 업데이트 (Occupied Seat)
**함수명**: `update_existing_name(seat, new_name)`  
**단계**: 5단계 프로세스 (Clear 단계 제거됨)

| 단계 | 동작 | 좌표 | 딜레이 |
|------|------|------|--------|
| 1 | 플레이어 클릭 | `PLAYER_COORDS[seat]` | `action_delay` |
| 2 | 이름 필드 클릭 | `(785, 291)` | `action_delay` |
| 3 | 새 이름 타이핑 | - | `keyboard_type_interval` × 글자수 |
| 4 | Enter 키 | - | `action_delay` |
| 5 | Complete 버튼 클릭 | `(1720, 139)` | `screen_wait` |

**예상 소요 시간**: ~3초 (Normal Speed)

### 2. 새 이름 등록 (Empty Seat)
**함수명**: `register_new_name(seat, name)`  
**단계**: 3단계 프로세스

| 단계 | 동작 | 좌표 | 딜레이 |
|------|------|------|--------|
| 1 | 플레이어 클릭 | `PLAYER_COORDS[seat]` | `action_delay` |
| 2 | 이름 타이핑 | - | `keyboard_type_interval` × 글자수 |
| 3 | Enter 키 | - | `screen_wait` |

**예상 소요 시간**: ~1.5초 (Normal Speed)

---

## 💰 칩 입력 프로세스

**함수명**: `input_chips(seat, chips)`  
**단계**: 3단계 프로세스 (Clear 단계 제거됨)

| 단계 | 동작 | 좌표 | 딜레이 |
|------|------|------|--------|
| 1 | 칩 필드 클릭 | `CHIP_COORDS[seat]` | `mouse_click_delay` |
| 2 | 칩 금액 타이핑 | - | `keyboard_type_interval` × 글자수 |
| 3 | Enter 키 | - | `action_delay` |

**예상 소요 시간**: ~0.8초 (Normal Speed)

⚠️ **중요**: 칩 입력 시 기존 값 지우기(Clear) 단계가 없음

---

## 📍 좌표 시스템

### 플레이어 좌표 (PLAYER_COORDS)
```python
{
    1: (233, 361),   2: (374, 359),   3: (544, 362),   
    4: (722, 359),   5: (886, 356),   6: (1051, 354),  
    7: (1213, 355),  8: (1385, 383),  9: (1549, 367),  
    10: (1705, 356)
}
```

### 칩 입력 좌표 (CHIP_COORDS) - 새로운 좌표
```python
{
    1: (220, 620),   2: (400, 620),   3: (555, 620),   
    4: (700, 620),   5: (870, 620),   6: (1060, 620),  
    7: (1220, 620),  8: (1370, 620),  9: (1555, 620),  
    10: (1720, 620)
}
```

### 고정 좌표
- **SUB_NAME_FIELD**: `(785, 291)` - 서브 화면 이름 입력 필드
- **COMPLETE_BUTTON**: `(1720, 139)` - 완료 버튼

---

## 🔄 순차 처리 로직

### UPDATE ALL 프로세스
**함수명**: `update_all()`  
**처리 방식**: 각 플레이어를 완전히 처리한 후 다음 플레이어로 이동

```
for seat in [1, 2, 3, ... 10]:
    1. 좌석 상태 확인
       - Empty 체크박스 확인
       - 이름 존재 여부 확인
    
    2. 이름 처리
       - Occupied 상태 → update_existing_name() [5단계]
       - Empty 상태 → register_new_name() [3단계]
    
    3. 칩 처리 (같은 플레이어)
       - input_chips() [3단계]
    
    4. 다음 플레이어로 이동
```

### 처리 순서 예시
```
Seat 1: 이름 업데이트 → 칩 입력 → 완료
Seat 2: 이름 등록 → 칩 입력 → 완료
Seat 3: 이름 업데이트 → 칩 입력 → 완료
...
```

---

## ⚡ 속도 설정

### 속도 프리셋

| 설정 | Mouse Click | Keyboard Type | Action Delay | Screen Wait |
|------|------------|---------------|--------------|-------------|
| **Ultra Fast** | 0.08s | 0.008s | 0.15s | 0.4s |
| **Fast** | 0.15s | 0.012s | 0.25s | 0.6s |
| **Normal** (기본) | 0.3s | 0.02s | 0.5s | 1.0s |
| **Slow** | 0.5s | 0.05s | 1.0s | 2.0s |

### 전체 처리 시간 예상 (10명 기준)

| 시나리오 | Normal | Fast | Ultra Fast |
|----------|--------|------|------------|
| 5 Occupied + 5 Empty | ~28초 | ~11초 | ~4.5초 |
| 10 Occupied | ~35초 | ~14초 | ~5.5초 |
| 10 Empty | ~23초 | ~9초 | ~3.5초 |

---

## 🔍 디버깅 정보

### 로그 출력 형식
```
[DEBUG] Seat 1 - Name: 'Phil Ivey', Empty: False
[DEBUG] Seat 1 status: '🔴 Occupied'
Seat 1: Updating existing name to 'Phil Ivey'
  Step 1: Clicking player at (233, 361)
  Step 2: Clicking name field at (785, 291)
  Step 3: Typing new name: 'Phil Ivey'
  Step 4: Pressing Enter
  Step 5: Clicking Complete at (1720, 139)
  ✅ Successfully updated seat 1
Seat 1: Inputting chips: 1500000
  Inputting chips for seat 1 at (220, 620)
  ✓ Chips input complete for seat 1
Seat 1: ✅ Complete
```

### 에러 처리
- 각 함수는 try-except로 감싸져 있음
- 에러 발생 시 상세 traceback 로그 출력
- GUI 상태 표시: Ready(green) / Processing(orange) / Error(red)

---

## ⚠️ 주의사항

1. **Action Tracker가 열려 있고 화면에 표시되어야 함**
2. **해상도가 좌표 시스템과 일치해야 함**
3. **Google Sheets 연결 시 네트워크 필요**
4. **Windows 전용 (pyautogui 사용)**
5. **칩 입력 시 Clear 단계 없음 - 자동 선택됨**

---

## 📊 상태 관리

### 좌석 상태
- **🔴 Occupied**: 기존 플레이어 있음 (5단계 업데이트 - Clear 제거)
- **⚪ Empty**: 비어있음 (3단계 등록)
- **⚫ Unknown**: 초기 상태

### 데이터 소스
1. **Google Sheets**: 자동 로드 (시작 시 500ms 후)
2. **수동 입력**: GUI에서 직접 입력
3. **JSON 파일**: Save/Load State 기능

---

## 🚀 Quick Start

1. Action Tracker 실행
2. `integrated_gui_final.py` 실행
3. 자동으로 Google Sheets 데이터 로드
4. 테이블 선택 시 자동 적용
5. UPDATE ALL 클릭으로 전체 처리

---

*Last Updated: 2024*  
*Version: Final with Sequential Processing*