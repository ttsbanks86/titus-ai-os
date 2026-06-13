const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  getSettings: () => ipcRenderer.invoke('get-settings'),
  saveSettings: (s) => ipcRenderer.invoke('save-settings', s),
  getHotkey: () => ipcRenderer.invoke('get-hotkey'),
  setHotkey: (hk) => ipcRenderer.invoke('set-hotkey', hk),
  pasteText: (t) => ipcRenderer.invoke('paste-text', t),
  minimize: () => ipcRenderer.invoke('minimize'),
  quit: () => ipcRenderer.invoke('quit'),
  getMicList: () => ipcRenderer.invoke('get-mic-list'),
  setMicList: (l) => ipcRenderer.invoke('set-mic-list', l),
  transcribeFile: () => ipcRenderer.invoke('transcribe-file'),
  onNavigate: (cb) => ipcRenderer.on('navigate', (e, page) => cb(page))
});