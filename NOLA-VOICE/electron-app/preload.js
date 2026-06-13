const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('electronAPI', {
  pasteText: (text) => ipcRenderer.invoke('paste-text', text),
  quitApp: () => ipcRenderer.invoke('quit-app'),
  minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
  onToggleRecording: (callback) => ipcRenderer.on('toggle-recording', callback)
});