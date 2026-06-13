const { app, BrowserWindow, ipcMain, Tray, Menu, globalShortcut, clipboard } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow = null;
let tray = null;
let pythonProcess = null;

function startBackend() {
  const isExe = process.execPath.endsWith('.exe') && !process.execPath.includes('electron.exe');
  let backendPath;
  
  const possiblePaths = [
    path.join(process.resourcesPath, 'WMI_Backend', 'WMI_Backend.exe'),
    path.join(__dirname, '..', '..', 'ECHOKEYS', 'dist', 'WMI_Backend', 'WMI_Backend.exe'),
    path.join(__dirname, '..', 'dist', 'WMI_Backend', 'WMI_Backend.exe')
  ];

  for (const p of possiblePaths) {
    if (require('fs').existsSync(p)) {
      backendPath = p;
      break;
    }
  }

  const env = Object.assign({}, process.env, { EK_PORT: '18925' });

  if (backendPath) {
    console.log('Starting compiled backend:', backendPath);
    pythonProcess = spawn(backendPath, [], { env, stdio: 'pipe' });
  } else {
    console.log('Starting script backend');
    const scriptPath = path.join(__dirname, '..', '..', 'ECHOKEYS', 'backend.py');
    pythonProcess = spawn('C:\\Python313\\python.exe', [scriptPath], { env, stdio: 'pipe' });
  }
  
  pythonProcess.on('error', (err) => { console.error('Backend error:', err); });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 460, height: 600,
    frame: false, transparent: true, resizable: false, alwaysOnTop: true,
    icon: path.join(__dirname, '..', '..', 'APPS', 'VoiceMyIdea.ico'),
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
    const iconPath = path.join(__dirname, '..', '..', 'APPS', 'VoiceMyIdea.ico');
    tray = new Tray(iconPath);
    tray.setToolTip('Voice My Idea — Alt+Space');
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
  } catch (err) {}
}

function registerHotkeys() {
  try {
    globalShortcut.register('Alt+Space', () => {
      if (mainWindow) {
        if (mainWindow.isVisible()) mainWindow.hide();
        else mainWindow.show();
      }
    });
  } catch (err) {}
}

ipcMain.handle('paste-text', (e, text) => {
  if (text) { clipboard.writeText(text); if (mainWindow) mainWindow.hide(); }
});
ipcMain.handle('quit-app', () => {
  app.isQuitting = true; if (pythonProcess) pythonProcess.kill(); app.quit();
});
ipcMain.handle('minimize-window', () => { if (mainWindow) mainWindow.hide(); });

app.whenReady().then(() => { startBackend(); createWindow(); createTray(); registerHotkeys(); });
app.on('will-quit', () => { globalShortcut.unregisterAll(); if (pythonProcess) pythonProcess.kill(); });