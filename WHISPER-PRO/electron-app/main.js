const { app, BrowserWindow, ipcMain, Tray, Menu, globalShortcut, clipboard, dialog, nativeImage } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow, hudWindow, tray, backendProcess;
let currentHotkey = 'Ctrl+Shift+Space';
let currentMode = 'Voice';
let currentMic = 'Default';
let isRecording = false;
let hudAudioChunks = [];
const DATA_DIR = path.join(app.getPath('userData'), '..', '..', '..', 'WHISPER-PRO', 'data');
const SETTINGS_FILE = path.join(DATA_DIR, 'settings.json');
const ICON_PATH = path.join(__dirname, '..', '..', 'APPS', 'WhisperMyIdea.ico');

// ─── Settings ────────────────────────────────────────────────────────────
function getSettings() {
  try {
    if (fs.existsSync(SETTINGS_FILE)) return JSON.parse(fs.readFileSync(SETTINGS_FILE, 'utf8'));
  } catch(e) {}
  return { hotkey: 'Ctrl+Shift+Space', mode: 'Voice', mic: 'Default', autoPaste: true, saveHistory: true, launchAtStartup: false };
}

function saveSettings(s) {
  try {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    fs.writeFileSync(SETTINGS_FILE, JSON.stringify(s, null, 2));
  } catch(e) {}
}

// ─── Startup Registry ────────────────────────────────────────────────────
const STARTUP_KEY = 'WhisperMyIdeaPro';
function setStartupLaunch(enable) {
  try {
    const { execSync } = require('child_process');
    const exePath = process.execPath;
    if (enable) {
      execSync(`reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "${STARTUP_KEY}" /t REG_SZ /d "${exePath}" /f`);
    } else {
      execSync(`reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "${STARTUP_KEY}" /f 2>nul`);
    }
  } catch(e) {}
}

// ─── Backend ─────────────────────────────────────────────────────────────
function startBackend() {
  const paths = [
    path.join(process.resourcesPath, 'backend', 'WMIP_Backend.exe'),
    path.join(__dirname, '..', 'backend', 'dist', 'WMIP_Backend', 'WMIP_Backend.exe'),
    path.join(__dirname, '..', 'backend', 'server.py')
  ];
  let bp = null;
  for (const p of paths) { if (fs.existsSync(p)) { bp = p; break; } }
  const env = Object.assign({}, process.env, { WMIP_PORT: '18927' });
  try {
    if (bp && bp.endsWith('.exe')) backendProcess = spawn(bp, [], { env, stdio: 'pipe' });
    else if (bp) backendProcess = spawn('C:\\Python313\\python.exe', [bp], { env, stdio: 'pipe' });
  } catch(e) {}
}

// ─── Main Window ─────────────────────────────────────────────────────────
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 780, height: 580, show: false,
    icon: ICON_PATH,
    webPreferences: { nodeIntegration: false, contextIsolation: true, preload: path.join(__dirname, 'preload.js') }
  });
  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));
  mainWindow.on('close', (e) => { if (!app.isQuitting) { e.preventDefault(); mainWindow.hide(); } });
}

// ─── Floating HUD ────────────────────────────────────────────────────────
function createHUD() {
  if (hudWindow) { hudWindow.show(); hudWindow.focus(); return; }
  hudWindow = new BrowserWindow({
    width: 320, height: 100, frame: false, transparent: true,
    alwaysOnTop: true, resizable: false, skipTaskbar: true,
    hasShadow: false,
    webPreferences: { nodeIntegration: false, contextIsolation: true, preload: path.join(__dirname, 'preload.js') }
  });
  hudWindow.loadFile(path.join(__dirname, 'hud.html'));
  hudWindow.setPosition(
    Math.round(require('electron').screen.getPrimaryDisplay().workAreaSize.width / 2 - 160),
    Math.round(require('electron').screen.getPrimaryDisplay().workAreaSize.height / 2 - 50)
  );
  hudWindow.on('closed', () => { hudWindow = null; });
}

function closeHUD() {
  if (hudWindow) { hudWindow.close(); hudWindow = null; }
}

// ─── Paste into Active App ──────────────────────────────────────────────
function pasteToActiveApp(text) {
  if (!text) return;
  clipboard.writeText(text);
  try {
    const { execSync } = require('child_process');
    execSync('powershell -noprofile -command "& {Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(\'^v\')}"', { timeout: 2000 });
  } catch(e) {
    // Fallback: just put it on clipboard
  }
}

// ─── Tray ────────────────────────────────────────────────────────────────
const MODES = ['Voice', 'Message', 'Email', 'Meeting', 'Bullets'];
let micList = ['Default'];

function rebuildTray() {
  const s = getSettings();
  const template = [
    {
      label: isRecording ? '⏺ Stop Recording' : '🎤 Toggle Recording',
      click: () => toggleRecordingFromTray()
    },
    {
      label: '📂 Transcribe File...',
      click: () => transcribeFile()
    },
    { type: 'separator' },
    {
      label: '⚙️ Settings',
      click: () => { mainWindow && mainWindow.show(); mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html')); }
    },
    {
      label: '📋 History',
      click: () => { mainWindow && mainWindow.show(); mainWindow.webContents.send('navigate', 'history'); }
    },
    { type: 'separator' },
    {
      label: 'Change Mode',
      submenu: MODES.map(m => ({
        label: m === s.mode ? `✓ ${m}` : m,
        click: () => { currentMode = m; saveSettings({ ...getSettings(), mode: m }); rebuildTray(); }
      }))
    },
    {
      label: 'Change Microphone',
      submenu: micList.map(m => ({
        label: m === s.mic ? `✓ ${m}` : m,
        click: () => { currentMic = m; saveSettings({ ...getSettings(), mic: m }); rebuildTray(); }
      }))
    },
    { type: 'separator' },
    { label: '🔄 Check for Updates...', enabled: false },
    { type: 'separator' },
    { label: 'Quit', click: () => { app.isQuitting = true; if (backendProcess) backendProcess.kill(); app.quit(); } }
  ];
  try {
    if (!tray) {
      tray = new Tray(ICON_PATH);
      tray.setToolTip(`Whisper My Idea Pro (${s.hotkey})`);
      tray.on('double-click', () => toggleRecordingFromTray());
    }
    tray.setContextMenu(Menu.buildFromTemplate(template));
  } catch(e) {}
}

// ─── Recording Flow ──────────────────────────────────────────────────────
function toggleRecordingFromTray() {
  if (isRecording) { stopHUDRecording(); return; }
  startHUDRecording();
}

function startHUDRecording() {
  isRecording = true;
  createHUD();
  rebuildTray();
  setTimeout(() => {
    if (hudWindow) hudWindow.webContents.send('start-recording', currentMode, currentMic);
  }, 300);
}

function stopHUDRecording() {
  if (hudWindow) hudWindow.webContents.send('stop-recording');
}

function onHUDTranscriptionComplete(text) {
  isRecording = false;
  closeHUD();
  rebuildTray();
  if (text && text.length > 0 && !text.startsWith('Error') && !text.startsWith('No speech')) {
    const s = getSettings();
    if (s.autoPaste !== false) pasteToActiveApp(text);
    else clipboard.writeText(text);
  }
}

// ─── File Transcription ──────────────────────────────────────────────────
async function transcribeFile() {
  const result = await dialog.showOpenDialog({ properties: ['openFile'], filters: [
    { name: 'Audio Files', extensions: ['wav', 'mp3', 'm4a', 'ogg', 'webm', 'flac'] }
  ]});
  if (result.canceled || !result.filePaths[0]) return;
  const filePath = result.filePaths[0];
  try {
    const r = await fetch('http://127.0.0.1:18927/transcribe', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ audio_path: filePath, mode: currentMode })
    });
    const d = await r.json();
    if (d.text && d.text.length > 0 && !d.text.startsWith('Error')) pasteToActiveApp(d.text);
  } catch(e) {}
}

// ─── Hotkeys ─────────────────────────────────────────────────────────────
function registerHotkeys(hk) {
  try {
    globalShortcut.unregisterAll();
    currentHotkey = hk || currentHotkey;
    globalShortcut.register(currentHotkey, () => toggleRecordingFromTray());
    if (tray) tray.setToolTip(`Whisper My Idea Pro (${currentHotkey})`);
  } catch(e) {}
}

// ─── IPC ─────────────────────────────────────────────────────────────────
ipcMain.handle('get-settings', () => getSettings());
ipcMain.handle('save-settings', (e, s) => { saveSettings(s); if (s.launchAtStartup !== undefined) setStartupLaunch(s.launchAtStartup); rebuildTray(); return true; });
ipcMain.handle('get-hotkey', () => currentHotkey);
ipcMain.handle('set-hotkey', (e, hk) => { saveSettings({ ...getSettings(), hotkey: hk }); registerHotkeys(hk); return true; });
ipcMain.handle('minimize', () => mainWindow && mainWindow.hide());
ipcMain.handle('quit', () => { app.isQuitting = true; if (backendProcess) backendProcess.kill(); app.quit(); });
ipcMain.handle('paste-text', (e, t) => { if (t) pasteToActiveApp(t); });
ipcMain.handle('transcription-complete', (e, text) => onHUDTranscriptionComplete(text));
ipcMain.handle('get-mic-list', () => micList);
ipcMain.handle('set-mic-list', (e, list) => { micList = list; rebuildTray(); });
ipcMain.handle('transcribe-file', async () => await transcribeFile());

// ─── Init ────────────────────────────────────────────────────────────────
app.whenReady().then(() => {
  const s = getSettings();
  currentHotkey = s.hotkey || 'Ctrl+Shift+Space';
  currentMode = s.mode || 'Voice';
  currentMic = s.mic || 'Default';
  if (s.launchAtStartup) setStartupLaunch(true);
  startBackend();
  createMainWindow();
  rebuildTray();
  registerHotkeys(currentHotkey);
});

app.on('will-quit', () => { globalShortcut.unregisterAll(); if (backendProcess) backendProcess.kill(); });
app.on('window-all-closed', () => {});
