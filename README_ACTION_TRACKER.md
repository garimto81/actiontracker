# Action Tracker Manager

## Features

### 1. Update Existing Name
- For players who already have names
- Process: Click player → Click name field → Clear → Type new name → Enter → Complete

### 2. Register New Name  
- For empty player positions
- Process: Click player → Type name → Enter (Simple 3-step process)

### 3. Delete Player
- Remove player name from position
- Process: Click player → Click Delete button

### 4. Batch Update
- Process multiple players at once
- Supports mixed operations (update, register, delete)

### 5. Speed Control
- Customizable speed settings for each action type:
  - `mouse_click_delay`: Delay after mouse clicks (default: 0.3s)
  - `keyboard_type_interval`: Interval between keystrokes (default: 0.02s)
  - `action_delay`: Delay between actions (default: 0.5s)
  - `screen_wait`: Wait for screen transitions (default: 1.0s)
  - `pyautogui_pause`: Global PyAutoGUI pause (default: 0.3s)

## Speed Presets

### Fast Mode
- Mouse click: 0.1s
- Typing: 0.01s/char
- Actions: 0.2s
- Screen wait: 0.5s

### Normal Mode (Default)
- Mouse click: 0.3s
- Typing: 0.02s/char
- Actions: 0.5s
- Screen wait: 1.0s

### Slow Mode
- Mouse click: 0.5s
- Typing: 0.05s/char
- Actions: 1.0s
- Screen wait: 2.0s

## Usage

### Interactive Mode
```python
python action_tracker_manager.py
```
- Interactive menu with all features
- Select options 1-7 for different functions

### Quick Test
```python
python quick_test.py
```
- Test individual functions
- Speed comparison tests

### Programmatic Usage
```python
from action_tracker_manager import ActionTrackerManager

# Create manager with custom speeds
manager = ActionTrackerManager({
    "mouse_click_delay": 0.2,
    "keyboard_type_interval": 0.01
})

# Update existing name
manager.update_existing_name(1, "New Name")

# Register new name
manager.register_new_name(5, "Player Five")

# Delete player
manager.delete_player(3)

# Batch update
manager.batch_update([
    {"player": 1, "action": "update", "name": "John"},
    {"player": 2, "action": "register", "name": "Jane"},
    {"player": 3, "action": "delete"}
])
```

## Player Coordinates
- Player 1: (233, 361)
- Player 2: (374, 359)
- Player 3: (544, 362)
- Player 4: (722, 359)
- Player 5: (886, 356)
- Player 6: (1051, 354)
- Player 7: (1213, 355)
- Player 8: (1385, 383)
- Player 9: (1549, 367)
- Player 10: (1705, 356)

## Logging
- All actions are logged with timestamps
- Screenshots before/after batch operations
- Save logs with option 7 in interactive menu