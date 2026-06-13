const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getPort: () => ipcRenderer.invoke('get-port'),
  pasteText: (text) => ipcRenderer.invoke('paste-text', text),
  quitApp: () => ipcRenderer.invoke('quit-app'),
  onToggleRecording: (callback) => ipcRenderer.on('toggle-recording', callback)
});