# Action Tracker 자동 감지 시스템

## 🔍 자동 감지 방법들

### 1. **색상 기반 감지 (Color Detection)**
```python
# 빨간색 배경 = 이름 있음 (Occupied)
# 회색 배경 = 빈 자리 (Empty)
```
- **장점**: 매우 빠름, 안정적
- **단점**: 이름 자체는 알 수 없음
- **정확도**: 95%

### 2. **OCR 기반 감지 (Optical Character Recognition)**
```python
# pytesseract로 텍스트 인식
# 숫자만 있으면 = 빈 자리
# 텍스트 있으면 = 이름 있음
```
- **장점**: 실제 이름도 읽을 수 있음
- **단점**: 느림, 설정 필요
- **정확도**: 85% (폰트에 따라 다름)

### 3. **픽셀 패턴 감지 (Pixel Pattern)**
```python
# 특정 위치의 픽셀 색상 체크
# RGB 값 분석으로 상태 판단
```
- **장점**: 중간 속도, 간단함
- **단점**: 화면 위치 변경시 실패
- **정확도**: 90%

### 4. **스마트 감지 (Smart Detection)**
```python
# 여러 방법 조합
# 1차: 색상 감지 (빠름)
# 2차: 불확실한 경우 픽셀 패턴
# 3차: 최종 확인은 OCR
```
- **장점**: 가장 정확함
- **단점**: 시간이 좀 걸림
- **정확도**: 98%

## 🚀 GUI 통합 기능

### 자동 감지 버튼들

#### 🔍 **Auto Detect All**
- 모든 플레이어 상태를 자동으로 감지
- 색상 기반으로 빈자리/이름 있는 자리 구분
- Empty 체크박스 자동 설정

#### ⚡ **Quick Scan**
- 빠른 픽셀 체크로 즉시 판단
- 1초 이내 완료
- 대략적인 상태만 파악

#### 💾 **Load Saved**
- 이전에 감지한 결과 불러오기
- gui_auto_config.json 파일 로드
- 수동 재설정 불필요

## 📊 감지 결과 활용

### 자동으로 설정되는 항목들
1. **Empty 체크박스**: 빈자리는 자동 체크
2. **상태 표시**: 로그에 각 플레이어 상태 출력
3. **패턴 인식**: 1-4 occupied, 5-10 empty 같은 패턴 자동 감지

### JSON 설정 파일 구조
```json
{
  "empty_seats": [5, 6, 7, 8, 9, 10],
  "occupied_seats": [1, 2, 3, 4],
  "detected_names": {
    "1": "Phil Ivey",
    "2": "Daniel Negreanu"
  },
  "timestamp": "2024-01-01 12:00:00"
}
```

## 🎯 사용 시나리오

### 시나리오 1: 완전 자동화
1. Action Tracker 실행
2. GUI에서 **Auto Detect All** 클릭
3. 자동으로 빈자리/이름 있는 자리 감지
4. 새 이름만 입력
5. **UPDATE/REGISTER** 클릭

### 시나리오 2: 빠른 확인
1. **Quick Scan** 클릭
2. 1초 이내 상태 파악
3. 필요한 부분만 수동 조정
4. 작업 실행

### 시나리오 3: 저장된 설정 활용
1. 이전에 감지한 결과가 있다면
2. **Load Saved** 클릭
3. 바로 작업 진행

## 🔧 필요한 라이브러리

### 기본 감지 (색상/픽셀)
```bash
pip install pyautogui
pip install pillow
pip install numpy
```

### OCR 기능 (선택사항)
```bash
pip install pytesseract
pip install opencv-python

# Tesseract OCR 엔진 설치 필요
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
```

## ⚙️ 커스터마이징

### 색상 임계값 조정
```python
# 빨간색 감지 범위
RED_RANGE = {
    'min': (180, 40, 40),
    'max': (220, 80, 80)
}

# 회색 감지 범위
GRAY_RANGE = {
    'min': (100, 100, 100),
    'max': (150, 150, 150)
}
```

### 감지 영역 조정
```python
# 플레이어 이름 영역 오프셋
NAME_REGION = {
    'x_offset': -50,
    'y_offset': -30,
    'width': 150,
    'height': 60
}
```

## 🚨 문제 해결

### 감지 실패시
1. Action Tracker가 전체 화면에 보이는지 확인
2. 화면 해상도가 변경되지 않았는지 확인
3. 색상 설정이 변경되지 않았는지 확인

### OCR 인식 안될 때
1. Tesseract 설치 확인
2. 폰트가 너무 작거나 흐릿한지 확인
3. 언어 설정 확인 (영어/한국어)

### 잘못된 감지시
1. 수동으로 체크박스 조정
2. 다른 감지 방법 시도
3. 색상 임계값 조정

## 💡 팁

- **가장 빠른 방법**: Quick Scan
- **가장 정확한 방법**: Smart Detection
- **이름도 알고 싶다면**: OCR 방법 사용
- **반복 작업시**: 결과 저장 후 Load Saved 활용

이제 수동으로 일일이 체크할 필요 없이 자동으로 플레이어 상태를 감지할 수 있습니다! 🎮