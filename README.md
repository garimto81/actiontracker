# Action Tracker Automation System

포커 게임 플레이어 정보 자동 관리 시스템

## 🚀 주요 기능

- **Google Sheets 연동**: 실시간 데이터 동기화
- **자동화 입력**: PyAutoGUI를 활용한 마우스/키보드 자동화
- **대용량 테이블 관리**: 100+ 테이블 페이지네이션
- **스마트 검색**: 실시간 테이블 필터링
- **즐겨찾기 & 최근 사용**: 빠른 테이블 접근

## 📦 설치

### 필요 패키지
```bash
pip install tkinter
pip install pyautogui
pip install pandas
pip install numpy
pip install requests
pip install Pillow
```

## 🎮 사용법

### 실행
```bash
# Python으로 직접 실행
python integrated_gui_final.py

# 또는 배치 파일 실행 (Windows)
RUN_MAIN.bat
```

### Google Sheets 설정
```python
# integrated_gui_final.py 파일에서 URL 수정
GOOGLE_SHEET_CSV_URL = "YOUR_GOOGLE_SHEET_CSV_URL"
```

## ⚡ 속도 설정

### Fast Mode (추천)
- Mouse Click: 0.1초
- Keyboard Type: 0.01초
- Action Delay: 0.2초
- Screen Wait: 0.2초

## 🎯 핵심 파일

- `integrated_gui_final.py` - 메인 프로그램
- `RUN_MAIN.bat` - 실행 배치 파일
- `test_*.py` - 테스트 파일들

## 📊 테이블 관리

### 100개 이상 테이블 처리
1. **페이지네이션**: 10개씩 표시
2. **검색**: 실시간 필터링
3. **그룹**: 범위별 자동 분류
4. **즐겨찾기**: 자주 사용 테이블 저장

### 테스트 모드
"Test 100 Tables" 버튼으로 100개 테이블 시뮬레이션

## 🔧 문제 해결

### 삭제 프로세스
- 2단계 간소화: 플레이어 클릭 → Delete 버튼
- Delete 체크박스만으로 삭제 실행

### Empty 체크박스
- GFX 상태 표시용
- 테이블 전환 시 상태 유지

## 📝 라이선스

Private Use

## 👨‍💻 개발

Developed with Claude AI Assistant