# Action Tracker Automation 파일 목록

## 📁 프로젝트 구조

```
c:\claude02\ActionTracker_Automation\
│
├── 📄 문서 (Documentation)
│   ├── ACTION_TRACKER_AUTOMATION_GUIDE.md    # 전체 기획서
│   ├── TECHNICAL_IMPLEMENTATION.md           # 기술 구현 상세
│   └── FILE_INVENTORY.md                     # 파일 목록 (본 문서)
│
├── 🐍 핵심 자동화 스크립트 (Core Automation)
│   ├── action_tracker_automation_app.py      # GUI 메인 컨트롤 패널
│   ├── action_tracker_bulk_update.py         # 대량 업데이트 엔진
│   ├── action_tracker_final_automation_20250904_175627.py  # 최종 자동화 버전
│   ├── action_tracker_final_detector.py      # UI 요소 감지 시스템
│   ├── action_tracker_position_detector.py   # 위치 자동 감지
│   ├── action_tracker_targeted_detector.py   # 타겟 정밀 감지
│   └── corrected_automation_app.py           # 개선된 자동화 앱
│
├── 🔧 업데이트 유틸리티 (Update Utilities)
│   ├── auto_bulk_update.py                   # 자동 대량 업데이트
│   ├── complete_player1_updater.py           # 플레이어1 전용 업데이터
│   ├── player_name_updater.py                # 이름 전용 업데이터
│   ├── simple_player1_update.py              # 간단한 플레이어1 업데이트
│   ├── ultra_fast_mike_updater.py            # 고속 Mike 업데이터
│   ├── update_action_tracker_correct.py      # 정확한 업데이트
│   ├── update_action_tracker_fullscreen.py   # 전체화면 업데이트
│   ├── update_player1_name.py                # 플레이어1 이름 업데이트
│   └── update_players_now.py                 # 즉시 플레이어 업데이트
│
├── 🔍 분석 및 검증 도구 (Analysis & Validation)
│   ├── analyze_button_positions.py           # 버튼 위치 분석
│   ├── analyze_edit_screen_simple.py         # 편집 화면 분석
│   ├── analyze_name_edit_screen.py           # 이름 편집 화면 분석
│   ├── click_coordinate_analyzer.py          # 클릭 좌표 분석기
│   ├── click_coordinate_collector.py         # 클릭 좌표 수집기
│   ├── coordinate_validator.py               # 좌표 검증기
│   ├── coordinate_validator_en.py            # 좌표 검증기 (영문)
│   └── color_analyzer.py                     # 색상 분석기
│
├── 🎯 윈도우 관리 도구 (Window Management)
│   ├── check_action_tracker.py               # Action Tracker 확인
│   ├── continue_to_action_tracker.py         # Action Tracker 계속
│   ├── find_action_tracker_window.py         # 윈도우 찾기
│   ├── find_real_action_tracker.py           # 실제 윈도우 찾기
│   ├── launch_action_tracker.py              # Action Tracker 실행
│   ├── close_and_verify.py                   # 닫기 및 확인
│   └── close_folder_dialog.py                # 폴더 대화상자 닫기
│
├── 🌐 통합 도구 (Integration Tools)
│   ├── frame_poker_to_action_tracker.py      # Frame Poker 연동
│   ├── player_manager_with_delete.py         # 삭제 기능 플레이어 관리
│   └── player1_name_changer.py               # 플레이어1 이름 변경기
│
├── 🖼️ 스크린샷 및 이미지 (Screenshots & Images)
│   ├── action_tracker_*.png                  # Action Tracker UI 캡처
│   ├── click_*.png                          # 클릭 위치 스크린샷
│   ├── coordinate_*.png                      # 좌표 확인 이미지
│   ├── edit_screen_*.png                     # 편집 화면 캡처
│   ├── update_*.png                          # 업데이트 결과 캡처
│   ├── player*.png                           # 플레이어 관련 이미지
│   └── color_*.png                           # 색상 분석 이미지
│
├── 📊 데이터 파일 (Data Files)
│   ├── click_coordinates_*.json              # 클릭 좌표 데이터
│   ├── action_tracker_final_positions_*.json # 최종 위치 데이터
│   └── corrected_positions.py                # 수정된 위치 데이터
│
└── 🔬 테스트 도구 (Test Tools)
    ├── capture_main_screen.py                # 메인 화면 캡처
    ├── show_main_table.py                    # 메인 테이블 표시
    ├── simple_test.py                        # 간단한 테스트
    └── final_check.py                        # 최종 확인
```

## 📋 파일 카테고리별 설명

### 1. 핵심 자동화 엔진 (7개 파일)
- 메인 GUI 애플리케이션
- 대량 데이터 처리 엔진
- UI 요소 자동 감지 시스템
- 위치 기반 자동화 로직

### 2. 플레이어 업데이트 도구 (9개 파일)
- 개별 플레이어 업데이트
- 대량 플레이어 업데이트
- 선택적 필드 업데이트
- 고속 업데이트 최적화

### 3. 분석 및 검증 시스템 (8개 파일)
- 좌표 정확성 검증
- UI 요소 위치 분석
- 색상 기반 상태 감지
- 클릭 위치 수집 및 분석

### 4. 윈도우 제어 (7개 파일)
- Action Tracker 윈도우 관리
- 대화상자 제어
- 프로세스 실행 및 종료

### 5. 시스템 통합 (3개 파일)
- Frame Poker 연동
- 플레이어 데이터 동기화
- 외부 시스템 인터페이스

### 6. 리소스 파일 (80+ 파일)
- UI 스크린샷 (검증용)
- 클릭 위치 증거
- 색상 팔레트 분석
- JSON 데이터 파일

## 🚀 사용 순서

### 초기 설정
1. `find_action_tracker_window.py` - 윈도우 찾기
2. `coordinate_validator.py` - 좌표 검증
3. `analyze_button_positions.py` - UI 분석

### 일반 작업
1. `action_tracker_automation_app.py` - GUI 실행
2. 필요한 작업 선택
3. 자동 실행

### 대량 업데이트
1. CSV/JSON 데이터 준비
2. `action_tracker_bulk_update.py` 실행
3. 로그 확인

## 💡 주요 파일 관계도

```
action_tracker_automation_app.py (메인)
    ├── action_tracker_position_detector.py (위치 감지)
    ├── coordinate_validator.py (좌표 검증)
    ├── action_tracker_bulk_update.py (대량 처리)
    └── player_name_updater.py (개별 업데이트)
```

## 📝 버전 정보

- **최신 버전**: 20250904_175627
- **Python 버전**: 3.8+
- **주요 의존성**: pyautogui, opencv-cv2, PIL, tkinter

## 🔒 보안 참고사항

- 모든 스크립트는 로컬 실행용
- 민감한 데이터는 포함하지 않음
- 윈도우 권한 필요 (마우스/키보드 제어)

---

*File Inventory v1.0*
*Total Files: 100+ (Scripts: 35+, Images: 80+, Data: 5+)*
*Location: c:\claude02\ActionTracker_Automation\*