# Action Tracker 자동화 기술 구현 상세

## 🔬 핵심 기술 구현

### 1. 윈도우 탐지 및 제어

```python
import pygetwindow as gw
import pyautogui

def find_action_tracker_window():
    """Action Tracker 윈도우 찾기"""
    windows = gw.getWindowsWithTitle('Action Tracker')
    if windows:
        window = windows[0]
        # 윈도우 활성화 및 최상위로 가져오기
        window.activate()
        window.maximize()
        return window
    return None
```

### 2. 좌표 시스템 구현

```python
class CoordinateSystem:
    """Action Tracker UI 좌표 관리 시스템"""
    
    def __init__(self):
        self.base_resolution = (1920, 1080)
        self.current_resolution = pyautogui.size()
        self.scale_factor = self.calculate_scale()
        
        # 기본 좌표 (1920x1080 기준)
        self.base_coords = {
            'players': [
                (215, 354),   # Player 1
                (386, 364),   # Player 2
                (560, 485),   # Player 3
                (559, 486),   # Player 4
                (557, 364),   # Player 5
                (721, 362),   # Player 6
                (737, 369),   # Player 7
                (890, 369),   # Player 8
                (860, 364),   # Player 9
                (1037, 357),  # Player 10
            ],
            'buttons': {
                'delete': (761, 108),
                'complete': (1733, 155),
                'close': (1745, 147),
                'edit': (815, 294),
            }
        }
    
    def calculate_scale(self):
        """해상도별 좌표 스케일 계산"""
        x_scale = self.current_resolution[0] / self.base_resolution[0]
        y_scale = self.current_resolution[1] / self.base_resolution[1]
        return (x_scale, y_scale)
    
    def get_scaled_coord(self, coord):
        """스케일 적용된 좌표 반환"""
        x, y = coord
        scaled_x = int(x * self.scale_factor[0])
        scaled_y = int(y * self.scale_factor[1])
        return (scaled_x, scaled_y)
```

### 3. 이미지 인식 기반 탐지

```python
import cv2
import numpy as np
from PIL import ImageGrab

class UIElementDetector:
    """UI 요소 자동 탐지 시스템"""
    
    def __init__(self):
        self.templates = {}
        self.load_templates()
    
    def load_templates(self):
        """UI 템플릿 이미지 로드"""
        self.templates['delete_btn'] = cv2.imread('templates/delete_button.png')
        self.templates['player_slot'] = cv2.imread('templates/player_slot.png')
        self.templates['edit_dialog'] = cv2.imread('templates/edit_dialog.png')
    
    def find_element(self, element_name):
        """화면에서 UI 요소 찾기"""
        # 스크린샷 캡처
        screenshot = np.array(ImageGrab.grab())
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        
        # 템플릿 매칭
        template = self.templates[element_name]
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        
        # 최적 매칭 위치 찾기
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.8:  # 80% 이상 일치
            return max_loc
        return None
    
    def wait_for_element(self, element_name, timeout=10):
        """UI 요소가 나타날 때까지 대기"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            pos = self.find_element(element_name)
            if pos:
                return pos
            time.sleep(0.5)
        return None
```

### 4. 텍스트 입력 최적화

```python
import pyperclip

class TextInputHandler:
    """안정적인 텍스트 입력 처리"""
    
    def __init__(self):
        self.input_delay = 0.05
        self.korean_ime_enabled = False
    
    def safe_input(self, text):
        """안전한 텍스트 입력 (특수문자 지원)"""
        # 클립보드 사용 (특수문자 및 유니코드 지원)
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(self.input_delay)
    
    def clear_field(self):
        """입력 필드 초기화"""
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        time.sleep(self.input_delay)
    
    def type_number(self, number):
        """숫자 빠른 입력"""
        # 숫자는 직접 타이핑이 더 빠름
        pyautogui.typewrite(str(number), interval=0.01)
    
    def handle_korean(self, text):
        """한글 입력 처리"""
        if not self.korean_ime_enabled:
            pyautogui.hotkey('alt', 'shift')  # IME 전환
            self.korean_ime_enabled = True
        self.safe_input(text)
```

### 5. 오류 복구 메커니즘

```python
class ErrorRecovery:
    """자동화 오류 복구 시스템"""
    
    def __init__(self):
        self.max_retries = 3
        self.retry_delay = 2
    
    def with_retry(self, func, *args, **kwargs):
        """함수 실행 with 자동 재시도"""
        for attempt in range(self.max_retries):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    self.recover_state()
                else:
                    raise
    
    def recover_state(self):
        """상태 복구 절차"""
        # ESC 키로 대화상자 닫기
        pyautogui.press('esc')
        time.sleep(0.5)
        
        # 메인 윈도우 재활성화
        window = find_action_tracker_window()
        if window:
            window.activate()
```

### 6. 대량 데이터 처리 엔진

```python
import pandas as pd
import json
from queue import Queue
from threading import Thread

class BulkDataProcessor:
    """대량 플레이어 데이터 처리"""
    
    def __init__(self):
        self.data_queue = Queue()
        self.coord_system = CoordinateSystem()
        self.text_handler = TextInputHandler()
        self.error_recovery = ErrorRecovery()
    
    def load_csv(self, filename):
        """CSV 파일 로드"""
        df = pd.read_csv(filename)
        for index, row in df.iterrows():
            self.data_queue.put({
                'player_num': row['player_num'],
                'name': row['name'],
                'chips': row['chips']
            })
    
    def load_json(self, filename):
        """JSON 파일 로드"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for player in data['players']:
                self.data_queue.put(player)
    
    def process_queue(self):
        """큐 처리 (멀티스레드 가능)"""
        while not self.data_queue.empty():
            player_data = self.data_queue.get()
            self.error_recovery.with_retry(
                self.update_single_player,
                player_data
            )
    
    def update_single_player(self, data):
        """단일 플레이어 업데이트"""
        player_num = data['player_num']
        name = data['name']
        chips = data['chips']
        
        # 플레이어 위치 클릭
        coord = self.coord_system.get_scaled_coord(
            self.coord_system.base_coords['players'][player_num - 1]
        )
        pyautogui.click(coord)
        time.sleep(0.5)
        
        # 편집 대화상자 열기
        pyautogui.doubleClick()
        time.sleep(0.5)
        
        # 이름 입력
        self.text_handler.clear_field()
        self.text_handler.safe_input(name)
        pyautogui.press('tab')
        
        # 칩 입력
        self.text_handler.clear_field()
        self.text_handler.type_number(chips)
        
        # 확인
        pyautogui.press('enter')
        time.sleep(0.5)
```

### 7. 실시간 모니터링 시스템

```python
import threading
from datetime import datetime

class AutomationMonitor:
    """자동화 프로세스 모니터링"""
    
    def __init__(self):
        self.status = 'idle'
        self.processed_count = 0
        self.error_count = 0
        self.start_time = None
        self.log_file = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    def start_monitoring(self):
        """모니터링 시작"""
        self.status = 'running'
        self.start_time = datetime.now()
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
    
    def _monitor_loop(self):
        """모니터링 루프"""
        while self.status == 'running':
            # CPU/메모리 사용량 체크
            self.check_system_resources()
            
            # 진행 상황 로깅
            self.log_progress()
            
            # 에러 임계값 체크
            if self.error_count > 10:
                self.trigger_alert("High error rate detected")
            
            time.sleep(5)  # 5초마다 체크
    
    def log_progress(self):
        """진행 상황 기록"""
        elapsed = (datetime.now() - self.start_time).seconds
        rate = self.processed_count / max(elapsed, 1) * 60  # per minute
        
        log_entry = f"[{datetime.now()}] Processed: {self.processed_count}, " \
                   f"Errors: {self.error_count}, Rate: {rate:.1f}/min\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
```

## 🔒 보안 및 안정성

### 1. 긴급 정지 메커니즘

```python
import keyboard

class EmergencyStop:
    """긴급 정지 시스템"""
    
    def __init__(self):
        self.stopped = False
        keyboard.add_hotkey('esc', self.emergency_stop)
    
    def emergency_stop(self):
        """긴급 정지 실행"""
        self.stopped = True
        print("EMERGENCY STOP ACTIVATED")
        # 모든 자동화 중지
        pyautogui.FAILSAFE = True
        pyautogui.moveTo(0, 0)  # 좌상단으로 마우스 이동
```

### 2. 데이터 검증

```python
class DataValidator:
    """입력 데이터 검증"""
    
    @staticmethod
    def validate_player_name(name):
        """플레이어 이름 검증"""
        if not name or len(name) > 50:
            return False
        # 특수문자 체크
        forbidden_chars = ['<', '>', '/', '\\', '|']
        return not any(char in name for char in forbidden_chars)
    
    @staticmethod
    def validate_chip_count(chips):
        """칩 수량 검증"""
        try:
            chips = int(chips)
            return 0 <= chips <= 999999999
        except:
            return False
```

## 📊 성능 최적화

### 1. 병렬 처리

```python
from concurrent.futures import ThreadPoolExecutor

class ParallelProcessor:
    """병렬 처리 최적화"""
    
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def process_batch(self, player_list):
        """배치 병렬 처리"""
        futures = []
        for player in player_list:
            future = self.executor.submit(self.process_player, player)
            futures.append(future)
        
        # 결과 수집
        results = []
        for future in futures:
            results.append(future.result())
        return results
```

### 2. 캐싱 시스템

```python
class CoordinateCache:
    """좌표 캐싱 시스템"""
    
    def __init__(self):
        self.cache = {}
        self.cache_file = 'coordinate_cache.json'
        self.load_cache()
    
    def load_cache(self):
        """캐시 로드"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                self.cache = json.load(f)
    
    def save_cache(self):
        """캐시 저장"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def get_coord(self, element_name):
        """캐시된 좌표 반환"""
        return self.cache.get(element_name)
```

## 🚀 고급 기능

### 1. AI 기반 UI 인식

```python
class AIUIRecognition:
    """AI 기반 UI 요소 인식"""
    
    def __init__(self):
        # TensorFlow/PyTorch 모델 로드
        self.model = self.load_model()
    
    def detect_elements(self, screenshot):
        """딥러닝으로 UI 요소 탐지"""
        # 이미지 전처리
        processed = self.preprocess(screenshot)
        
        # 모델 예측
        predictions = self.model.predict(processed)
        
        # 바운딩 박스 추출
        elements = self.extract_bounding_boxes(predictions)
        return elements
```

### 2. 자연어 명령 처리

```python
class NaturalLanguageCommands:
    """자연어 명령 처리"""
    
    def parse_command(self, command):
        """자연어 명령 파싱"""
        # 예: "플레이어 3번을 Mike로 변경하고 칩을 100만으로 설정"
        if "플레이어" in command:
            # 플레이어 번호 추출
            player_num = self.extract_number(command)
            
            # 이름 추출
            if "로 변경" in command:
                name = self.extract_name(command)
            
            # 칩 수량 추출
            if "칩" in command:
                chips = self.extract_chips(command)
            
            return {
                'action': 'update_player',
                'player_num': player_num,
                'name': name,
                'chips': chips
            }
```

## 📝 결론

이 기술 구현은 Action Tracker 자동화의 핵심 메커니즘을 상세히 설명합니다. 윈도우 제어, 좌표 시스템, 이미지 인식, 텍스트 입력, 오류 복구, 대량 처리, 모니터링 등 모든 핵심 기능이 포함되어 있습니다.

시스템은 확장 가능하고 유지보수가 용이하도록 설계되었으며, 향후 AI 기반 기능 추가나 API 연동 등으로 더욱 발전할 수 있습니다.

---
*Technical Documentation v1.0*
*Created for Action Tracker Automation System*