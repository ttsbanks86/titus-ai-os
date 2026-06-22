const { app, BrowserWindow, ipcMain, dialog, shell } = require("electron");
const path = require("path");
const { exec } = require("child_process");
const fs = require("fs");

const TTS_DIR = path.resolve(__dirname, "..");
let mainWindow;
let serverProcess;

// ── Start the Express API server as a child process ──────────
function startServer() {
  serverProcess = require("child_process").fork(
    path.join(__dirname, "server.js"),
    [],
    { silent: true }
  );
  serverProcess.stdout.on("data", d => console.log("[server]", d.toString().trim()));
  serverProcess.stderr.on("data", d => console.error("[server err]", d.toString().trim()));
}

// ── Create the desktop window ────────────────────────────────
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 780,
    height: 860,
    minWidth: 640,
    minHeight: 700,
    title: "TTS Studio",
    backgroundColor: "#0a0a10",
    titleBarStyle: "hidden",
    titleBarOverlay: {
      color: "#13131c",
      symbolColor: "#7070a0",
      height: 36
    },
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js")
    },
    icon: path.join(__dirname, "icon.png"),
    show: false,
    alwaysOnTop: false
  });

  // Wait for server to be ready, then load
  waitForServer(() => {
    mainWindow.loadURL("http://localhost:3737");
    mainWindow.once("ready-to-show", () => {
      mainWindow.show();
    });
  });

  mainWindow.on("closed", () => { mainWindow = null; });
}

function waitForServer(cb, attempts = 0) {
  const http = require("http");
  const req = http.get("http://localhost:3737", () => cb());
  req.on("error", () => {
    if (attempts < 20) setTimeout(() => waitForServer(cb, attempts + 1), 300);
  });
  req.end();
}

// ── IPC: show save dialog for downloads ─────────────────────
ipcMain.handle("save-file", async (event, { buffer, filename }) => {
  const { filePath } = await dialog.showSaveDialog(mainWindow, {
    defaultPath: path.join(require("os").homedir(), "Downloads", filename),
    filters: [
      { name: "Audio", extensions: ["mp3", "wav"] }
    ]
  });
  if (!filePath) return { cancelled: true };
  fs.writeFileSync(filePath, Buffer.from(buffer));
  shell.showItemInFolder(filePath);
  return { saved: true, filePath };
});

// ── IPC: always-on-top toggle ────────────────────────────────
ipcMain.handle("set-always-on-top", (event, value) => {
  mainWindow.setAlwaysOnTop(value);
  return value;
});

// ── App lifecycle ────────────────────────────────────────────
app.whenReady().then(() => {
  startServer();
  createWindow();
});

app.on("window-all-closed", () => {
  if (serverProcess) serverProcess.kill();
  app.quit();
});

app.on("activate", () => {
  if (!mainWindow) createWindow();
});
