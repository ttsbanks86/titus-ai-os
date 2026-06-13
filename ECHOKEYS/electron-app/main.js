const { app, BrowserWindow, ipcMain, Tray, Menu, globalShortcut, clipboard } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow = null;
let tray = null;
let pythonProcess = null;

function startBackend() {
  const isExe = process.execPath.endsWith('.exe') && !process.execPath.includes('electron.exe');
  let backendPath;
  let backendArgs = [];
  
  // Try to find the compiled backend first
  const possiblePaths = [
    path.join(process.resourcesPath, 'WMI_Backend', 'WMI_Backend.exe'), // Packaged
    path.join(__dirname, '..', 'dist', 'WMI_Backend', 'WMI_Backend.exe'), // Dev Build
    path.join(__dirname, '..', '..', 'ECHOKEYS', 'dist', 'WMI_Backend', 'WMI_Backend.exe') // Shared
  ];

  for (const p of possiblePaths) {
    if (require('fs').existsSync(p)) {
      backendPath = p;
      break;
    }
  }

  const env = Object.assign({}, process.env, { EK_PORT: '18924' });

  if (backendPath) {
    console.log('Starting compiled backend:', backendPath);
    pythonProcess = spawn(backendPath, [], { env, stdio: 'pipe' });
  } else {
    console.log('Starting script backend');
    const scriptPath = path.join(__dirname, '..', 'backend.py');
    pythonProcess = spawn('C:\\Python313\\python.exe', [scriptPath], { env, stdio: 'pipe' });
  }
  
  pythonProcess.on('error', (err) => { console.error('Backend error:', err); });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 460,
    height: 600,
    frame: false,
    transparent: true,
    resizable: false,
    alwaysOnTop: true,
    icon: path.join(__dirname, '..', '..', 'APPS', 'WhisperMyIdea.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'app.html'));
  
  mainWindow.on('close', (e) => {
    if (!app.isQuitting) {
      e.preventDefault();
      mainWindow.hide();
    }
  });
}

function createTray() {
  try {
    const iconPath = path.join(__dirname, '..', '..', 'APPS', 'WhisperMyIdea.ico');
    tray = new Tray(iconPath);
    tray.setToolTip('Whisper My Idea — Alt+Space');
    const contextMenu = Menu.buildFromTemplate([
      { label: 'Show', click: () => mainWindow && mainWindow.show() },
      { type: 'separator' },
      { label: 'Quit', click: () => {
        app.isQuitting = true;
        if (pythonProcess) pythonProcess.kill();
        app.quit();
      }}
    ]);
    tray.setContextMenu(contextMenu);
    tray.on('double-click', () => mainWindow && mainWindow.show());
  } catch (err) {
    console.error('Tray error:', err);
  }
}

function registerHotkeys() {
  try {
    globalShortcut.register('Alt+Space', () => {
      if (mainWindow) {
        if (mainWindow.isVisible()) mainWindow.hide();
        else mainWindow.show();
      }
    });
  } catch (err) {
    console.error('Hotkey error:', err);
  }
}

ipcMain.handle('paste-text', (e, text) => {
  if (text) {
    clipboard.writeText(text);
    if (mainWindow) mainWindow.hide();
  }
});

ipcMain.handle('quit-app', () => {
  app.isQuitting = true;
  if (pythonProcess) pythonProcess.kill();
  app.quit();
});

app.whenReady().then(() => {
  startBackend();
  createWindow();
  createTray();
  registerHotkeys();
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
  if (pythonProcess) pythonProcess.kill();
});