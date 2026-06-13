const { app, BrowserWindow, ipcMain, Tray, Menu, globalShortcut } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow = null;
let tray = null;
let pythonProcess = null;

function startBackend() {
  // Try compiled backend first, then script fallback
  const possiblePaths = [
    path.join(process.resourcesPath, 'NR_Backend', 'NR_Backend.exe'),
    path.join(__dirname, '..', 'dist', 'NR_Backend', 'NR_Backend.exe'),
    path.join(__dirname, '..', 'backend.py')
  ];

  let backendPath = null;
  let isExe = false;
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      backendPath = p;
      isExe = p.endsWith('.exe');
      break;
    }
  }

  const env = Object.assign({}, process.env, { NR_PORT: '18926' });
  try {
    if (backendPath && isExe) {
      pythonProcess = spawn(backendPath, [], { env, stdio: 'pipe' });
    } else if (backendPath) {
      pythonProcess = spawn('C:\\Python313\\python.exe', [backendPath], { env, stdio: 'pipe' });
    } else {
      console.error('No backend found');
      return;
    }
    pythonProcess.on('error', (err) => console.error('Backend error:', err));
  } catch (err) {
    console.error('Failed to start backend:', err);
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 520, height: 680,
    frame: false, transparent: true, resizable: false, alwaysOnTop: true,
    icon: path.join(__dirname, '..', '..', 'APPS', 'NOLAReader.ico'),
    webPreferences: {
      nodeIntegration: false, contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  mainWindow.loadFile(path.join(__dirname, 'app.html'));
  mainWindow.on('close', (e) => {
    if (!app.isQuitting) { e.preventDefault(); mainWindow.hide(); }
  });
}

function createTray() {
  try {
    tray = new Tray(path.join(__dirname, '..', '..', 'APPS', 'NOLAReader.ico'));
    tray.setToolTip('NOLA Voice Reader');
    const m = Menu.buildFromTemplate([
      { label: 'Show', click: () => mainWindow && mainWindow.show() },
      { type: 'separator' },
      { label: 'Quit', click: () => {
        app.isQuitting = true;
        if (pythonProcess) pythonProcess.kill();
        app.quit();
      }}
    ]);
    tray.setContextMenu(m);
    tray.on('double-click', () => mainWindow && mainWindow.show());
  } catch (err) {}
}

function registerHotkeys() {
  try {
    globalShortcut.register('Alt+Shift+R', () => {
      if (mainWindow) {
        if (mainWindow.isVisible()) mainWindow.hide();
        else mainWindow.show();
      }
    });
  } catch (err) {}
}

ipcMain.handle('minimize-window', () => { if (mainWindow) mainWindow.hide(); });
ipcMain.handle('quit-app', () => {
  app.isQuitting = true;
  if (pythonProcess) pythonProcess.kill();
  app.quit();
});

app.whenReady().then(() => { startBackend(); createWindow(); createTray(); registerHotkeys(); });
app.on('will-quit', () => { globalShortcut.unregisterAll(); if (pythonProcess) pythonProcess.kill(); });