const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  saveFile: (data) => ipcRenderer.invoke("save-file", data),
  setAlwaysOnTop: (val) => ipcRenderer.invoke("set-always-on-top", val),
  isElectron: true
});
