const { BrowserWindow, app, ipcMain, dialog } = require('electron');
const fs = require('fs').promises;

let win;
const createWindow = () => {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    titleBarStyle: 'hidden',
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false
    }
  })

  win.loadFile("src/editor/renderer/index.html");
  // win.webContents.openDevTools();
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

ipcMain.handle('openFile', async () => {
    const result = await dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [
            { name: 'Python', extensions: ['py'] },
            { name: 'All Files', extensions: ['*'] }
        ]
    });

    if (result.canceled) {
        return null; // Если диалог был отменен, возвращаем null
    }
    const filePath = result.filePaths[0];
    try {
        const content = await fs.readFile(filePath, 'utf-8'); // Читаем файл
        return { path: filePath, content }; // Возвращаем путь и содержимое файла
    } catch (error) {
        console.error('Error reading file:', error);
        return null; // В случае ошибки возвращаем null
    }
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})