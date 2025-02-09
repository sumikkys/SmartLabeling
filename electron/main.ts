import { app, BrowserWindow } from 'electron'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
// import { exec, ChildProcess} from 'child_process'
import { spawn, ChildProcess } from 'child_process'
import fs from 'fs'

const require = createRequire(import.meta.url)
const __dirname = path.dirname(fileURLToPath(import.meta.url))

let python: ChildProcess | null = null;
const logStream = fs.createWriteStream(path.join(__dirname, 'backend.log'), { flags: 'a' });


// The built directory structure
//
// ├─┬─┬ dist
// │ │ └── index.html
// │ │
// │ ├─┬ dist-electron
// │ │ ├── main.js
// │ │ └── preload.mjs
// │
process.env.APP_ROOT = path.join(__dirname, '..')

// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
export const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']
export const MAIN_DIST = path.join(process.env.APP_ROOT, 'dist-electron')
export const RENDERER_DIST = path.join(process.env.APP_ROOT, 'dist')

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL ? path.join(process.env.APP_ROOT, 'public') : RENDERER_DIST

let win: BrowserWindow | null

function createWindow() {
  win = new BrowserWindow({
    icon: path.join(process.env.VITE_PUBLIC, 'electron-vite.svg'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
    },
  })

  // Test active push message to Renderer-process.
  win.webContents.on('did-finish-load', () => {
    win?.webContents.send('main-process-message', (new Date).toLocaleString())
  })

  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL)
  } else {
    // win.loadFile('dist/index.html')
    win.loadFile(path.join(RENDERER_DIST, 'index.html'))
  }
  // python = exec('python ./core/main.py', (error, stdout, stderr) => {
  //   if (error) {
  //     console.error(`Error starting Python: ${error}`);
  //     return;
  //   }else{
  //     console.log('Python started successfully');
  //   }
  //   console.log(`stdout: ${stdout}`);
  //   console.error(`stderr: ${stderr}`);
  // });
}

function createPythonProcess() {
  // 启动 Python 后端
  python = spawn('python', ['./core/main.py', '--host', 'localhost', '--port', '8232'], { stdio: ['ignore', 'pipe', 'pipe'] });

  python.stdout?.on('data', (data) => {
    const message = data.toString();
    console.log(`Backend: ${message}`);
    logStream.write(`[STDOUT] ${message}\n`);
  });

  python.stderr?.on('data', (data) => {
    const message = data.toString();
    console.log(`Backend: ${message}`);
    logStream.write(`[STDERR] ${message}\n`);
  });

  python.on('close', (code) => {
    console.log(`Python 进程退出，退出码: ${code}`);
    logStream.write(`[EXIT] Python 进程退出，退出码: ${code}\n`);
  });
}

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  // 在非macOS平台上，关闭所有窗口时退出应用程序
  if (process.platform !== 'darwin') {
    if (python) {
      python.kill();  // 关闭 Python 进程
    }
    app.quit()
    win = null
  }
})

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

app.on('before-quit', () => {
  if (python) {
    python.kill();  // 关闭 Python 进程
  }
})


app.whenReady().then(createWindow).then(createPythonProcess)
