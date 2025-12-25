const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
    openFile: () => ipcRenderer.invoke('dialog:openFile')
});
