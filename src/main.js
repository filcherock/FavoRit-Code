const { BrowserWindow, app, ipcMain } = require('electron')

let win;
const createWindow = () => {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    frame: false,
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
    }
  })

  win.loadFile("src/editor/renderer/index.html")
  win.webContents.openDevTools()

}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
        }
    })
})

let maximizeToggle = false;
ipcMain.on("manualMinimize", () => {
    win.minimize();
});

ipcMain.on("manualMaximize", () => {
    if (maximizeToggle) {
        win.unmaximize();
    } else {
        win.maximize();
    }
    maximizeToggle = !maximizeToggle;
});

ipcMain.on("manualClose", () => {
    app.quit();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})