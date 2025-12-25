import { editor } from "../code.js";

const { ipcRenderer } = require("electron");
const ipc = ipcRenderer;

document.querySelector("#minimize").addEventListener("click", () => {
    ipc.send("manualMinimize");
})

document.querySelector("#maximize").addEventListener("click", () => {
    ipc.send("manualMaximize");
})

document.querySelector("#close").addEventListener("click", () => {
    ipc.send("manualClose");
})

let DecoMenuBoolean = true;
document.querySelector('#titleBarModeChange').addEventListener('click', function (e) {
    var decoMenu = document.querySelector('#decoMode')
    var fsMenu = document.querySelector('#fsMode')
    var changerBtn = document.querySelector('#titleBarModeChange')
    if (DecoMenuBoolean) {
        decoMenu.style.display = 'none'
        fsMenu.style.display = 'flex'
        changerBtn.innerHTML = '<i class="fa-solid fa-backward"></i>'
    } else {
        fsMenu.style.display = 'none'
        decoMenu.style.display = 'flex'
        changerBtn.innerHTML = '<i class="fa-regular fa-folder"></i>'
    }
    DecoMenuBoolean = !DecoMenuBoolean
})

document.addEventListener('DOMContentLoaded', () => {
    const menuBtns = document.querySelectorAll('.menuBtn');

    menuBtns.forEach(btn => {
        btn.addEventListener('click', (event) => {
            const dropdown = event.target.nextElementSibling;

            // Закрыть другие открытые меню
            document.querySelectorAll('.dropdown-content').forEach(content => {
                if (content !== dropdown) {
                    content.style.display = 'none';
                }
            });

            // Переключить текущее выпадающее меню
            dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
        });
    });

    // Закрытие выпадающих меню при клике вне их
    window.addEventListener('click', (event) => {
        if (!event.target.classList.contains('menuBtn')) {
            document.querySelectorAll('.dropdown-content').forEach(content => {
                content.style.display = 'none';
            });
        }
    });

    // Обработчики событий для кнопок внутри выпадающих меню
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    
    dropdownItems.forEach(item => {
    item.addEventListener('click', async () => {
        if (item.textContent === 'Open File') {
            const result = await ipc.invoke("openFile"); // Используем ipc.invoke
            editor.setValue(result.content);
        }
    });
});
});
