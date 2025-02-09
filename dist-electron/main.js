import { app, BrowserWindow } from "electron";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { spawn } from "child_process";
import fs from "fs";
createRequire(import.meta.url);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
let python = null;
const logStream = fs.createWriteStream(path.join(__dirname, "backend.log"), { flags: "a" });
process.env.APP_ROOT = path.join(__dirname, "..");
const VITE_DEV_SERVER_URL = process.env["VITE_DEV_SERVER_URL"];
const MAIN_DIST = path.join(process.env.APP_ROOT, "dist-electron");
const RENDERER_DIST = path.join(process.env.APP_ROOT, "dist");
process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL ? path.join(process.env.APP_ROOT, "public") : RENDERER_DIST;
let win;
function createWindow() {
  win = new BrowserWindow({
    icon: path.join(process.env.VITE_PUBLIC, "electron-vite.svg"),
    webPreferences: {
      preload: path.join(__dirname, "preload.mjs")
    }
  });
  win.webContents.on("did-finish-load", () => {
    win == null ? void 0 : win.webContents.send("main-process-message", (/* @__PURE__ */ new Date()).toLocaleString());
  });
  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL);
  } else {
    win.loadFile(path.join(RENDERER_DIST, "index.html"));
  }
}
function createPythonProcess() {
  var _a, _b;
  python = spawn("python", ["./core/main.py", "--host", "localhost", "--port", "8232"], { stdio: ["ignore", "pipe", "pipe"] });
  (_a = python.stdout) == null ? void 0 : _a.on("data", (data) => {
    const message = data.toString();
    console.log(`Backend: ${message}`);
    logStream.write(`[STDOUT] ${message}
`);
  });
  (_b = python.stderr) == null ? void 0 : _b.on("data", (data) => {
    const message = data.toString();
    console.log(`Backend: ${message}`);
    logStream.write(`[STDERR] ${message}
`);
  });
  python.on("close", (code) => {
    console.log(`Python 进程退出，退出码: ${code}`);
    logStream.write(`[EXIT] Python 进程退出，退出码: ${code}
`);
  });
}
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    if (python) {
      python.kill();
    }
    app.quit();
    win = null;
  }
});
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
app.on("before-quit", () => {
  if (python) {
    python.kill();
  }
});
app.whenReady().then(createWindow).then(createPythonProcess);
export {
  MAIN_DIST,
  RENDERER_DIST,
  VITE_DEV_SERVER_URL
};
