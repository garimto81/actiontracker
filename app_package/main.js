const { app, BrowserWindow, ipcMain, Menu, Tray, dialog, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let backendProcess;
let tray;
let isQuitting = false;

// Configuration
const config = {
  backendPort: 8888,
  backendHost: 'localhost',
  width: 1400,
  height: 900,
  minWidth: 1200,
  minHeight: 700
};

// Create main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: config.width,
    height: config.height,
    minWidth: config.minWidth,
    minHeight: config.minHeight,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    title: 'Action Tracker Automation',
    show: false,
    frame: true,
    backgroundColor: '#2c3e50'
  });

  // Load the web interface
  mainWindow.loadFile('index.html');

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // Check backend connection
    checkBackendConnection();
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    if (!isQuitting) {
      mainWindow = null;
    }
  });

  // Prevent window close, minimize to tray instead
  mainWindow.on('close', (event) => {
    if (!isQuitting) {
      event.preventDefault();
      mainWindow.hide();
      
      if (process.platform === 'darwin') {
        app.dock.hide();
      }
    }
  });

  // Create application menu
  createMenu();
}

// Create application menu
function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Load Google Sheets',
          accelerator: 'CmdOrCtrl+L',
          click: () => {
            mainWindow.webContents.send('menu-action', 'load-sheets');
          }
        },
        {
          label: 'Import CSV',
          accelerator: 'CmdOrCtrl+I',
          click: () => {
            mainWindow.webContents.send('menu-action', 'import-csv');
          }
        },
        { type: 'separator' },
        {
          label: 'Settings',
          accelerator: 'CmdOrCtrl+,',
          click: () => {
            mainWindow.webContents.send('menu-action', 'settings');
          }
        },
        { type: 'separator' },
        {
          label: 'Quit',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => {
            isQuitting = true;
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { label: 'Undo', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
        { label: 'Redo', accelerator: 'Shift+CmdOrCtrl+Z', role: 'redo' },
        { type: 'separator' },
        { label: 'Cut', accelerator: 'CmdOrCtrl+X', role: 'cut' },
        { label: 'Copy', accelerator: 'CmdOrCtrl+C', role: 'copy' },
        { label: 'Paste', accelerator: 'CmdOrCtrl+V', role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { label: 'Reload', accelerator: 'CmdOrCtrl+R', role: 'reload' },
        { label: 'Force Reload', accelerator: 'CmdOrCtrl+Shift+R', role: 'forceReload' },
        { label: 'Toggle Developer Tools', accelerator: 'F12', role: 'toggleDevTools' },
        { type: 'separator' },
        { label: 'Actual Size', accelerator: 'CmdOrCtrl+0', role: 'resetZoom' },
        { label: 'Zoom In', accelerator: 'CmdOrCtrl+Plus', role: 'zoomIn' },
        { label: 'Zoom Out', accelerator: 'CmdOrCtrl+-', role: 'zoomOut' },
        { type: 'separator' },
        { label: 'Toggle Fullscreen', accelerator: 'F11', role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Automation',
      submenu: [
        {
          label: 'Start Automation',
          accelerator: 'F5',
          click: () => {
            mainWindow.webContents.send('menu-action', 'start-automation');
          }
        },
        {
          label: 'Stop Automation',
          accelerator: 'F6',
          click: () => {
            mainWindow.webContents.send('menu-action', 'stop-automation');
          }
        },
        { type: 'separator' },
        {
          label: 'Auto Detect Seats',
          accelerator: 'CmdOrCtrl+D',
          click: () => {
            mainWindow.webContents.send('menu-action', 'auto-detect');
          }
        },
        {
          label: 'Update Names Only',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow.webContents.send('menu-action', 'update-names');
          }
        },
        {
          label: 'Update Chips Only',
          accelerator: 'CmdOrCtrl+H',
          click: () => {
            mainWindow.webContents.send('menu-action', 'update-chips');
          }
        },
        {
          label: 'Update All',
          accelerator: 'CmdOrCtrl+U',
          click: () => {
            mainWindow.webContents.send('menu-action', 'update-all');
          }
        }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Documentation',
          click: () => {
            shell.openExternal('https://github.com/yourusername/action-tracker-automation/wiki');
          }
        },
        {
          label: 'Report Issue',
          click: () => {
            shell.openExternal('https://github.com/yourusername/action-tracker-automation/issues');
          }
        },
        { type: 'separator' },
        {
          label: 'About',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'About Action Tracker Automation',
              message: 'Action Tracker Automation v2.0.0',
              detail: 'Cross-platform automation system for poker tournament management.\n\n© 2025 ActionTracker Team',
              buttons: ['OK']
            });
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Create system tray
function createTray() {
  tray = new Tray(path.join(__dirname, 'assets', 'tray-icon.png'));
  
  const contextMenu = Menu.buildFromTemplate([
    {
      label: 'Show App',
      click: () => {
        mainWindow.show();
        if (process.platform === 'darwin') {
          app.dock.show();
        }
      }
    },
    {
      label: 'Start Automation',
      click: () => {
        mainWindow.webContents.send('menu-action', 'start-automation');
      }
    },
    {
      label: 'Stop Automation',
      click: () => {
        mainWindow.webContents.send('menu-action', 'stop-automation');
      }
    },
    { type: 'separator' },
    {
      label: 'Quit',
      click: () => {
        isQuitting = true;
        app.quit();
      }
    }
  ]);

  tray.setToolTip('Action Tracker Automation');
  tray.setContextMenu(contextMenu);

  // Show window on tray double-click
  tray.on('double-click', () => {
    mainWindow.show();
    if (process.platform === 'darwin') {
      app.dock.show();
    }
  });
}

// Start Python backend
function startBackend() {
  const backendPath = app.isPackaged
    ? path.join(process.resourcesPath, 'backend', 'app.py')
    : path.join(__dirname, 'backend', 'app.py');

  const pythonPath = app.isPackaged
    ? path.join(process.resourcesPath, 'backend', 'venv', 'Scripts', 'python.exe')
    : 'python';

  console.log('Starting backend:', pythonPath, backendPath);

  backendProcess = spawn(pythonPath, [backendPath], {
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
    backendProcess = null;
  });
}

// Check backend connection
async function checkBackendConnection() {
  const maxRetries = 10;
  let retries = 0;

  const checkConnection = async () => {
    try {
      const response = await fetch(`http://${config.backendHost}:${config.backendPort}/health`);
      if (response.ok) {
        console.log('Backend connected successfully');
        mainWindow.webContents.send('backend-status', 'connected');
        return true;
      }
    } catch (error) {
      console.log(`Backend connection attempt ${retries + 1} failed`);
    }

    retries++;
    if (retries < maxRetries) {
      setTimeout(checkConnection, 2000);
    } else {
      console.error('Failed to connect to backend');
      mainWindow.webContents.send('backend-status', 'disconnected');
      
      dialog.showErrorBox(
        'Backend Connection Failed',
        'Unable to connect to the automation backend. Please restart the application.'
      );
    }
  };

  // Start checking after a delay
  setTimeout(checkConnection, 3000);
}

// Stop backend process
function stopBackend() {
  if (backendProcess) {
    console.log('Stopping backend...');
    backendProcess.kill('SIGTERM');
    backendProcess = null;
  }
}

// IPC handlers
ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

ipcMain.handle('get-platform', () => {
  return process.platform;
});

ipcMain.handle('minimize-window', () => {
  mainWindow.minimize();
});

ipcMain.handle('maximize-window', () => {
  if (mainWindow.isMaximized()) {
    mainWindow.restore();
  } else {
    mainWindow.maximize();
  }
});

ipcMain.handle('close-window', () => {
  mainWindow.close();
});

// App event handlers
app.whenReady().then(() => {
  createWindow();
  createTray();
  startBackend();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    } else {
      mainWindow.show();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  isQuitting = true;
  stopBackend();
});

app.on('will-quit', (event) => {
  if (backendProcess) {
    event.preventDefault();
    stopBackend();
    setTimeout(() => {
      app.quit();
    }, 1000);
  }
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  dialog.showErrorBox('Unexpected Error', error.message);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});