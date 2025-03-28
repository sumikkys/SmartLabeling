import { app, BrowserWindow, ipcMain, dialog } from 'electron'
// import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
// import { exec, ChildProcess} from 'child_process'
import { spawn, ChildProcess } from 'child_process'
import fs from 'fs'

// const require = createRequire(import.meta.url)
const __dirname = path.dirname(fileURLToPath(import.meta.url))

let python: ChildProcess | null = null;
const logStream = fs.createWriteStream(path.join(__dirname, 'backend.log'), { flags: 'a' })


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
      allowRunningInsecureContent: true, // 允许不安全的内容加载
      webSecurity: false,                // 禁用web安全策略
      nodeIntegration: true,
      contextIsolation: true,
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
  const pythonScriptPath = app.isPackaged 
    ? path.join(process.resourcesPath!, 'core/main.py')
    : path.join(__dirname, '../core/main.py')

  const args = [pythonScriptPath, '--host', 'localhost', '--port', '8232']

  python = spawn('python', args, {
    stdio: ['ignore', 'pipe', 'pipe'],
    shell: true
  })

  python.stdout?.on('data', (data) => {
    const message = data.toString()
    console.log(`Backend: ${message}`)
    logStream.write(`[STDOUT] ${message}\n`)
  })

  python.stderr?.on('data', (data) => {
    const message = data.toString()
    console.log(`Backend: ${message}`)
    logStream.write(`[STDERR] ${message}\n`)
  })

  python.on('close', (code) => {
    console.log(`Python 进程退出，退出码: ${code}`);
    logStream.write(`[EXIT] Python 进程退出，退出码: ${code}\n`);
  })
}

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  // 在非macOS平台上，关闭所有窗口时退出应用程序
  if (process.platform !== 'darwin') {
    if (python) {
      python.kill()  // 关闭 Python 进程
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
    python.kill()  // 关闭 Python 进程
  }
})


// app.whenReady().then(createWindow).then(createPythonProcess)

app.whenReady().then(() => {
  createWindow()
  createPythonProcess()

  // 监听渲染进程的文件选择请求
  ipcMain.handle('loadFiles', async () => {
    // 弹出文件选择对话框，让用户选择上传文件
    const result = await dialog.showOpenDialog({
      title: '选择上传的图片',
      properties: ['openFile', 'multiSelections'],  // 选择文件并允许多选
      filters: [{ name: '图片', extensions: ['jpg', 'jepg', 'png', 'bmp'] },]
    })

    if (result.filePaths) {
      return result.filePaths  // 返回文件的绝对路径
    }
    return null
  })

  // 监听渲染进程的文件夹选择请求
  ipcMain.handle('selectDirectory', async (_, title: string) => {
    try {
      // 弹出文件夹选择对话框，让用户选择文件夹的保存路径
      const result = await dialog.showOpenDialog({
        title: title || '',
        properties: ['openDirectory', 'createDirectory'] // 选择文件夹
      })

      if (!result.canceled) {
        const folderPath = result.filePaths[0]
        // 检查文件夹是否存在，如果不存在就创建
        if (!fs.existsSync(folderPath)) {
          fs.mkdirSync(folderPath, { recursive: true })
        }
        return folderPath // 返回文件夹路径
      }
    } catch (error) {
      console.error('创建文件夹失败:', error)
      throw error
    }
  })

  // 监听渲染进程的读取json文件请求
  ipcMain.handle('read-json-file', (_, filePath: string) => {
    return new Promise((resolve, reject) => {
      fs.readFile(filePath, 'utf-8', (error, data) => {
        if (error) {
          console.error('读取失败:', error)
          reject(new Error(`文件读取失败: ${error.message}`))
          return
        }
        try {
          const parsed = JSON.parse(data)
          resolve(parsed)
        } catch (parseError) {
          reject(new Error(`JSON解析失败: ${(parseError as Error).message}`))
        }
      })
    })
  })
})