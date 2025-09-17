/**
 * Action Tracker Automation - Main Application Logic
 */

// Configuration
const config = {
    backendUrl: 'http://localhost:8888',
    wsUrl: 'ws://localhost:8888/ws',
    reconnectInterval: 5000,
    toastDuration: 3000
};

// Global state
let ws = null;
let isConnected = false;
let currentTable = null;
let tableData = {};
let automationRunning = false;

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    connectWebSocket();
    setupEventListeners();
    loadInitialData();
    detectPlatform();
});

// Initialize application components
function initializeApp() {
    // Generate player cards (10 seats)
    generatePlayerCards();
    
    // Set default speed
    setSpeed('fast');
    
    // Start connection check
    setInterval(checkConnection, 5000);
}

// Generate player card UI
function generatePlayerCards() {
    const playerGrid = document.getElementById('playerGrid');
    playerGrid.innerHTML = '';
    
    for (let i = 1; i <= 10; i++) {
        const card = document.createElement('div');
        card.className = 'player-card empty';
        card.id = `player-${i}`;
        card.innerHTML = `
            <div class="seat-number">Seat ${i}</div>
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="empty-${i}">
                <label class="form-check-label" for="empty-${i}">
                    Empty Seat
                </label>
            </div>
            <input type="text" class="player-input" id="name-${i}" placeholder="Player Name">
            <input type="number" class="chip-input" id="chips-${i}" placeholder="Chips">
            <div class="form-check mt-2">
                <input class="form-check-input" type="checkbox" id="delete-${i}">
                <label class="form-check-label" for="delete-${i}">
                    Delete Player
                </label>
            </div>
        `;
        playerGrid.appendChild(card);
    }
}

// WebSocket connection
function connectWebSocket() {
    try {
        ws = new WebSocket(config.wsUrl);
        
        ws.onopen = () => {
            console.log('WebSocket connected');
            setConnectionStatus(true);
            showToast('Connected to automation server', 'success');
        };
        
        ws.onmessage = (event) => {
            handleWebSocketMessage(JSON.parse(event.data));
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            showToast('Connection error', 'error');
        };
        
        ws.onclose = () => {
            console.log('WebSocket disconnected');
            setConnectionStatus(false);
            
            // Attempt reconnection
            setTimeout(connectWebSocket, config.reconnectInterval);
        };
    } catch (error) {
        console.error('Failed to connect WebSocket:', error);
        setTimeout(connectWebSocket, config.reconnectInterval);
    }
}

// Handle WebSocket messages
function handleWebSocketMessage(message) {
    console.log('WebSocket message:', message);
    
    switch (message.type) {
        case 'connected':
            addLog('Connected to automation server', 'success');
            break;
            
        case 'data_loaded':
            addLog(`Loaded ${message.count} tables from Google Sheets`, 'info');
            loadTables();
            break;
            
        case 'automation_complete':
            automationRunning = false;
            updateButtonStates();
            hideProgress();
            showToast(`${message.operation} completed successfully`, 'success');
            addLog(`Automation completed: ${message.operation}`, 'success');
            break;
            
        case 'automation_error':
            automationRunning = false;
            updateButtonStates();
            hideProgress();
            showToast(`Error: ${message.error}`, 'error');
            addLog(`Automation error: ${message.error}`, 'error');
            break;
            
        case 'progress_update':
            updateProgress(message.progress, message.message);
            break;
            
        case 'settings_updated':
            addLog('Settings updated', 'info');
            break;
    }
}

// Setup event listeners
function setupEventListeners() {
    // Speed control buttons
    document.querySelectorAll('.speed-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            setSpeed(btn.dataset.speed);
        });
    });
    
    // Google Sheets buttons
    document.getElementById('loadSheetsBtn').addEventListener('click', loadGoogleSheets);
    document.getElementById('refreshBtn').addEventListener('click', loadTables);
    
    // Table search
    document.getElementById('tableSearch').addEventListener('input', filterTables);
    
    // Action buttons
    document.getElementById('autoDetectBtn').addEventListener('click', () => startAutomation('auto_detect'));
    document.getElementById('updateNamesBtn').addEventListener('click', () => startAutomation('update_names'));
    document.getElementById('updateChipsBtn').addEventListener('click', () => startAutomation('update_chips'));
    document.getElementById('updateAllBtn').addEventListener('click', () => startAutomation('update_all'));
    document.getElementById('stopBtn').addEventListener('click', stopAutomation);
    
    // Empty seat checkboxes
    for (let i = 1; i <= 10; i++) {
        const emptyCheckbox = document.getElementById(`empty-${i}`);
        emptyCheckbox.addEventListener('change', () => {
            const card = document.getElementById(`player-${i}`);
            if (emptyCheckbox.checked) {
                card.classList.add('empty');
                card.classList.remove('occupied');
                document.getElementById(`name-${i}`).disabled = true;
                document.getElementById(`chips-${i}`).disabled = true;
            } else {
                card.classList.remove('empty');
                card.classList.add('occupied');
                document.getElementById(`name-${i}`).disabled = false;
                document.getElementById(`chips-${i}`).disabled = false;
            }
        });
    }
}

// Load initial data
async function loadInitialData() {
    try {
        // Load settings
        const settingsResponse = await fetch(`${config.backendUrl}/settings`);
        if (settingsResponse.ok) {
            const settings = await settingsResponse.json();
            console.log('Loaded settings:', settings);
        }
        
        // Load tables
        loadTables();
        
    } catch (error) {
        console.error('Failed to load initial data:', error);
    }
}

// Load Google Sheets data
async function loadGoogleSheets() {
    showLoading();
    addLog('Loading data from Google Sheets...', 'info');
    
    try {
        const response = await fetch(`${config.backendUrl}/google-sheets/load`);
        
        if (response.ok) {
            const data = await response.json();
            showToast(`Loaded ${data.total_tables} tables`, 'success');
            addLog(`Successfully loaded ${data.total_tables} tables`, 'success');
            loadTables();
        } else {
            throw new Error('Failed to load Google Sheets');
        }
    } catch (error) {
        console.error('Error loading Google Sheets:', error);
        showToast('Failed to load Google Sheets', 'error');
        addLog('Error loading Google Sheets', 'error');
    } finally {
        hideLoading();
    }
}

// Load tables list
async function loadTables() {
    try {
        const response = await fetch(`${config.backendUrl}/tables`);
        
        if (response.ok) {
            const data = await response.json();
            tableData = data;
            renderTables(data.tables);
        }
    } catch (error) {
        console.error('Error loading tables:', error);
    }
}

// Render table buttons
function renderTables(tables) {
    const tableGrid = document.getElementById('tableGrid');
    tableGrid.innerHTML = '';
    
    tables.forEach(table => {
        const btn = document.createElement('button');
        btn.className = 'table-btn';
        btn.textContent = table;
        btn.onclick = () => selectTable(table);
        
        if (table === currentTable) {
            btn.classList.add('selected');
        }
        
        tableGrid.appendChild(btn);
    });
}

// Filter tables
function filterTables() {
    const searchTerm = document.getElementById('tableSearch').value.toLowerCase();
    const buttons = document.querySelectorAll('.table-btn');
    
    buttons.forEach(btn => {
        if (btn.textContent.toLowerCase().includes(searchTerm)) {
            btn.style.display = 'block';
        } else {
            btn.style.display = 'none';
        }
    });
}

// Select table
async function selectTable(tableName) {
    currentTable = tableName;
    
    // Update UI
    document.querySelectorAll('.table-btn').forEach(btn => {
        btn.classList.remove('selected');
        if (btn.textContent === tableName) {
            btn.classList.add('selected');
        }
    });
    
    // Load table data
    try {
        const response = await fetch(`${config.backendUrl}/tables/${tableName}`);
        
        if (response.ok) {
            const data = await response.json();
            applyTableData(data.players);
            addLog(`Selected table: ${tableName}`, 'info');
        }
    } catch (error) {
        console.error('Error loading table data:', error);
        showToast('Failed to load table data', 'error');
    }
}

// Apply table data to UI
function applyTableData(players) {
    // Clear all fields first
    for (let i = 1; i <= 10; i++) {
        document.getElementById(`name-${i}`).value = '';
        document.getElementById(`chips-${i}`).value = '';
        document.getElementById(`empty-${i}`).checked = false;
        document.getElementById(`delete-${i}`).checked = false;
        
        const card = document.getElementById(`player-${i}`);
        card.classList.remove('empty', 'occupied');
    }
    
    // Apply player data
    players.forEach(player => {
        const seat = player.seat;
        if (seat >= 1 && seat <= 10) {
            const nameInput = document.getElementById(`name-${seat}`);
            const chipsInput = document.getElementById(`chips-${seat}`);
            const emptyCheckbox = document.getElementById(`empty-${seat}`);
            const card = document.getElementById(`player-${seat}`);
            
            if (player.is_empty || !player.name) {
                emptyCheckbox.checked = true;
                nameInput.disabled = true;
                chipsInput.disabled = true;
                card.classList.add('empty');
            } else {
                nameInput.value = player.name || '';
                chipsInput.value = player.chips || '';
                card.classList.add('occupied');
            }
        }
    });
}

// Get current player data
function getPlayerData() {
    const players = [];
    
    for (let i = 1; i <= 10; i++) {
        const isEmpty = document.getElementById(`empty-${i}`).checked;
        const isDelete = document.getElementById(`delete-${i}`).checked;
        const name = document.getElementById(`name-${i}`).value;
        const chips = document.getElementById(`chips-${i}`).value;
        
        players.push({
            seat: i,
            name: isEmpty ? '' : name,
            chips: chips ? parseInt(chips) : null,
            is_empty: isEmpty,
            delete: isDelete
        });
    }
    
    return players;
}

// Start automation
async function startAutomation(operation) {
    if (automationRunning) {
        showToast('Automation already running', 'warning');
        return;
    }
    
    if (!currentTable && operation !== 'auto_detect') {
        showToast('Please select a table first', 'warning');
        return;
    }
    
    automationRunning = true;
    updateButtonStates();
    showProgress();
    
    const players = getPlayerData();
    const speed = document.querySelector('.speed-btn.active').dataset.speed;
    
    const requestData = {
        operation: operation,
        table: currentTable,
        players: players,
        speed: speed
    };
    
    addLog(`Starting ${operation}...`, 'info');
    
    try {
        const response = await fetch(`${config.backendUrl}/automation/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (response.ok) {
            const data = await response.json();
            showToast(data.message, 'success');
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to start automation');
        }
    } catch (error) {
        console.error('Error starting automation:', error);
        showToast(error.message, 'error');
        addLog(`Error: ${error.message}`, 'error');
        automationRunning = false;
        updateButtonStates();
        hideProgress();
    }
}

// Stop automation
async function stopAutomation() {
    try {
        const response = await fetch(`${config.backendUrl}/automation/stop`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const data = await response.json();
            showToast(data.message, 'info');
            addLog('Automation stopped', 'warning');
            automationRunning = false;
            updateButtonStates();
            hideProgress();
        }
    } catch (error) {
        console.error('Error stopping automation:', error);
        showToast('Failed to stop automation', 'error');
    }
}

// Set speed
function setSpeed(speed) {
    document.querySelectorAll('.speed-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.speed === speed) {
            btn.classList.add('active');
        }
    });
    
    // Update backend settings
    updateSettings({ speed: speed });
}

// Update settings
async function updateSettings(settings) {
    try {
        const response = await fetch(`${config.backendUrl}/settings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settings)
        });
        
        if (response.ok) {
            console.log('Settings updated');
        }
    } catch (error) {
        console.error('Error updating settings:', error);
    }
}

// UI Helper Functions

function setConnectionStatus(connected) {
    isConnected = connected;
    const statusElement = document.getElementById('connectionStatus');
    
    if (connected) {
        statusElement.className = 'status-badge status-connected';
        statusElement.innerHTML = '<i class="bi bi-wifi"></i> Connected';
    } else {
        statusElement.className = 'status-badge status-disconnected';
        statusElement.innerHTML = '<i class="bi bi-wifi-off"></i> Disconnected';
    }
}

function showProgress() {
    document.querySelector('.progress-container').style.display = 'block';
}

function hideProgress() {
    document.querySelector('.progress-container').style.display = 'none';
    updateProgress(0, '');
}

function updateProgress(percent, message) {
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    
    progressBar.style.width = `${percent}%`;
    progressText.textContent = message || `${percent}%`;
}

function updateButtonStates() {
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(btn => {
        if (btn.id === 'stopBtn') {
            btn.disabled = !automationRunning;
        } else {
            btn.disabled = automationRunning;
        }
    });
}

function showLoading() {
    document.getElementById('loadingSpinner').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.remove('active');
}

function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    
    const icon = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        warning: 'bi-exclamation-triangle-fill',
        info: 'bi-info-circle-fill'
    }[type];
    
    toast.innerHTML = `
        <i class="bi ${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, config.toastDuration);
}

function addLog(message, type = 'info') {
    const logContainer = document.getElementById('logContainer');
    const timestamp = new Date().toLocaleTimeString();
    
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;
    logEntry.innerHTML = `
        <span class="log-time">[${timestamp}]</span>
        ${message}
    `;
    
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
    
    // Keep only last 100 logs
    while (logContainer.children.length > 100) {
        logContainer.removeChild(logContainer.firstChild);
    }
}

async function checkConnection() {
    try {
        const response = await fetch(`${config.backendUrl}/health`);
        setConnectionStatus(response.ok);
    } catch (error) {
        setConnectionStatus(false);
    }
}

function detectPlatform() {
    const platformBadge = document.getElementById('platformBadge');
    const platform = window.navigator.platform;
    
    if (platform.includes('Win')) {
        platformBadge.textContent = 'Windows';
    } else if (platform.includes('Mac')) {
        platformBadge.textContent = 'macOS';
    } else if (platform.includes('Linux')) {
        platformBadge.textContent = 'Linux';
    } else {
        platformBadge.textContent = 'Web';
    }
}