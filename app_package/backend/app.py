"""
FastAPI Backend for Action Tracker Automation
Cross-platform automation server with REST API
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
import pandas as pd
import requests
from io import StringIO
import platform
import subprocess
import os
import sys
from datetime import datetime
import threading
import queue
import logging

# Platform-specific imports
if platform.system() == "Windows":
    import pyautogui
    import win32gui
    import win32con
    AUTOMATION_AVAILABLE = True
else:
    AUTOMATION_AVAILABLE = False
    print("Note: Direct automation only available on Windows. Remote control mode enabled.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Action Tracker Automation API",
    description="Cross-platform automation system for poker tournament management",
    version="2.0.0"
)

# CORS configuration for Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state management
class AutomationState:
    def __init__(self):
        self.is_running = False
        self.current_operation = None
        self.progress = 0
        self.table_data = {}
        self.current_table = None
        self.connected_clients = set()
        self.operation_queue = queue.Queue()
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Load saved settings or return defaults"""
        settings_file = "settings.json"
        default_settings = {
            "speed": "normal",
            "mouse_click_delay": 0.3,
            "keyboard_type_interval": 0.02,
            "action_delay": 0.5,
            "screen_wait": 1.0,
            "google_sheets_url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSDY_i4330JANAjIz4sMncdJdRHsOkfUCjQusHTGQk2tykrhA4d09LeIp3XRbLd8hkN6SgSB47k_nux/pub?gid=998576925&single=true&output=csv",
            "coordinates": {
                "player_coords": {
                    "1": [233, 361], "2": [374, 359], "3": [544, 362], 
                    "4": [722, 359], "5": [886, 356], "6": [1051, 354],
                    "7": [1213, 355], "8": [1385, 383], "9": [1549, 367], 
                    "10": [1705, 356]
                },
                "chip_coords": {
                    "1": [220, 620], "2": [400, 620], "3": [555, 620],
                    "4": [700, 620], "5": [870, 620], "6": [1060, 620],
                    "7": [1220, 620], "8": [1370, 620], "9": [1555, 620],
                    "10": [1720, 620]
                },
                "sub_name_field": [785, 291],
                "complete_button": [1720, 139],
                "delete_button": [721, 112]
            }
        }
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
        
        return default_settings
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open("settings.json", 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False

state = AutomationState()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Pydantic models for API
class PlayerData(BaseModel):
    seat: int
    name: str
    chips: Optional[int] = None
    is_empty: bool = False
    delete: bool = False

class TableData(BaseModel):
    table_name: str
    players: List[PlayerData]

class AutomationRequest(BaseModel):
    operation: str  # "update_all", "update_names", "update_chips", "auto_detect"
    table: Optional[str] = None
    players: Optional[List[PlayerData]] = None
    speed: Optional[str] = "normal"

class SettingsUpdate(BaseModel):
    speed: Optional[str] = None
    mouse_click_delay: Optional[float] = None
    keyboard_type_interval: Optional[float] = None
    action_delay: Optional[float] = None
    screen_wait: Optional[float] = None
    google_sheets_url: Optional[str] = None
    coordinates: Optional[Dict[str, Any]] = None

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Action Tracker Automation API",
        "version": "2.0.0",
        "platform": platform.system(),
        "automation_available": AUTOMATION_AVAILABLE,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "automation_available": AUTOMATION_AVAILABLE,
        "platform": platform.system(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/settings")
async def get_settings():
    """Get current settings"""
    return state.settings

@app.post("/settings")
async def update_settings(settings: SettingsUpdate):
    """Update settings"""
    try:
        if settings.speed:
            state.settings["speed"] = settings.speed
            # Update speed-related delays
            speed_presets = {
                "ultra_fast": {"mouse_click_delay": 0.15, "keyboard_type_interval": 0.01, 
                              "action_delay": 0.2, "screen_wait": 0.6},
                "fast": {"mouse_click_delay": 0.1, "keyboard_type_interval": 0.01,
                        "action_delay": 0.2, "screen_wait": 0.5},
                "normal": {"mouse_click_delay": 0.3, "keyboard_type_interval": 0.02,
                          "action_delay": 0.5, "screen_wait": 1.0},
                "slow": {"mouse_click_delay": 0.5, "keyboard_type_interval": 0.05,
                        "action_delay": 1.0, "screen_wait": 2.0}
            }
            
            if settings.speed in speed_presets:
                state.settings.update(speed_presets[settings.speed])
        
        # Update individual settings if provided
        update_fields = ["mouse_click_delay", "keyboard_type_interval", 
                        "action_delay", "screen_wait", "google_sheets_url"]
        
        for field in update_fields:
            value = getattr(settings, field, None)
            if value is not None:
                state.settings[field] = value
        
        if settings.coordinates:
            state.settings["coordinates"].update(settings.coordinates)
        
        # Save settings
        state.save_settings()
        
        # Broadcast settings update
        await manager.broadcast({
            "type": "settings_updated",
            "settings": state.settings
        })
        
        return {"message": "Settings updated successfully", "settings": state.settings}
    
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/google-sheets/load")
async def load_google_sheets():
    """Load data from Google Sheets"""
    try:
        url = state.settings["google_sheets_url"]
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse CSV data
        df = pd.read_csv(StringIO(response.text))
        
        # Group by table
        tables = {}
        for table_name in df['Table'].unique():
            table_df = df[df['Table'] == table_name]
            players = []
            
            for _, row in table_df.iterrows():
                players.append({
                    "seat": int(row['Seat']),
                    "name": str(row['Player Name']) if pd.notna(row['Player Name']) else "",
                    "chips": int(row['Chips']) if pd.notna(row['Chips']) else 0,
                    "is_empty": pd.isna(row['Player Name']) or str(row['Player Name']).strip() == ""
                })
            
            tables[table_name] = players
        
        state.table_data = tables
        
        # Broadcast data update
        await manager.broadcast({
            "type": "data_loaded",
            "tables": list(tables.keys()),
            "count": len(tables)
        })
        
        return {
            "message": "Data loaded successfully",
            "tables": list(tables.keys()),
            "total_tables": len(tables)
        }
    
    except Exception as e:
        logger.error(f"Error loading Google Sheets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tables")
async def get_tables():
    """Get list of available tables"""
    return {
        "tables": list(state.table_data.keys()),
        "current_table": state.current_table,
        "total": len(state.table_data)
    }

@app.get("/tables/{table_name}")
async def get_table_data(table_name: str):
    """Get data for specific table"""
    if table_name not in state.table_data:
        raise HTTPException(status_code=404, detail="Table not found")
    
    return {
        "table": table_name,
        "players": state.table_data[table_name]
    }

@app.post("/automation/start")
async def start_automation(request: AutomationRequest, background_tasks: BackgroundTasks):
    """Start automation process"""
    if not AUTOMATION_AVAILABLE:
        return {
            "message": "Direct automation not available on this platform",
            "platform": platform.system(),
            "suggestion": "Use remote control mode or run on Windows"
        }
    
    if state.is_running:
        raise HTTPException(status_code=409, detail="Automation already running")
    
    try:
        state.is_running = True
        state.current_operation = request.operation
        state.progress = 0
        
        # Add automation task to background
        background_tasks.add_task(
            run_automation,
            request.operation,
            request.table,
            request.players,
            request.speed
        )
        
        return {
            "message": f"Started {request.operation}",
            "operation": request.operation,
            "status": "running"
        }
    
    except Exception as e:
        state.is_running = False
        logger.error(f"Error starting automation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/stop")
async def stop_automation():
    """Stop automation process"""
    if not state.is_running:
        return {"message": "No automation running"}
    
    state.is_running = False
    state.current_operation = None
    
    # Broadcast stop event
    await manager.broadcast({
        "type": "automation_stopped",
        "timestamp": datetime.now().isoformat()
    })
    
    return {"message": "Automation stopped", "status": "stopped"}

@app.get("/automation/status")
async def get_automation_status():
    """Get current automation status"""
    return {
        "is_running": state.is_running,
        "current_operation": state.current_operation,
        "progress": state.progress,
        "platform": platform.system(),
        "automation_available": AUTOMATION_AVAILABLE
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to automation server",
            "platform": platform.system(),
            "automation_available": AUTOMATION_AVAILABLE
        })
        
        while True:
            # Keep connection alive and handle messages
            data = await websocket.receive_text()
            
            # Echo received message (can be extended for commands)
            await websocket.send_json({
                "type": "echo",
                "data": data,
                "timestamp": datetime.now().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected from WebSocket")

# Automation functions (Windows-specific)
async def run_automation(operation: str, table: str, players: List[PlayerData], speed: str):
    """Run automation process (Windows only)"""
    if not AUTOMATION_AVAILABLE:
        logger.warning("Automation not available on this platform")
        return
    
    try:
        # Apply speed settings
        apply_speed_settings(speed)
        
        # Get player data
        if players is None and table:
            players = state.table_data.get(table, [])
        
        # Execute operation
        if operation == "update_all":
            await update_all_players(players)
        elif operation == "update_names":
            await update_names_only(players)
        elif operation == "update_chips":
            await update_chips_only(players)
        elif operation == "auto_detect":
            await auto_detect_seats()
        
        # Send completion message
        await manager.broadcast({
            "type": "automation_complete",
            "operation": operation,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Automation error: {e}")
        await manager.broadcast({
            "type": "automation_error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        })
    
    finally:
        state.is_running = False
        state.current_operation = None
        state.progress = 0

def apply_speed_settings(speed: str):
    """Apply speed settings for automation"""
    if not AUTOMATION_AVAILABLE:
        return
    
    speed_presets = {
        "ultra_fast": 0.15,
        "fast": 0.1,
        "normal": 0.3,
        "slow": 0.5
    }
    
    pyautogui.PAUSE = speed_presets.get(speed, 0.3)

async def update_all_players(players: List):
    """Update all player names and chips"""
    # Implementation would go here
    # This is a placeholder for the actual automation logic
    pass

async def update_names_only(players: List):
    """Update only player names"""
    # Implementation would go here
    pass

async def update_chips_only(players: List):
    """Update only chip counts"""
    # Implementation would go here
    pass

async def auto_detect_seats():
    """Auto-detect occupied seats"""
    # Implementation would go here
    pass

# Main entry point
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8888))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting Action Tracker Automation API on {host}:{port}")
    logger.info(f"Platform: {platform.system()}")
    logger.info(f"Automation Available: {AUTOMATION_AVAILABLE}")
    
    uvicorn.run(app, host=host, port=port, log_level="info")