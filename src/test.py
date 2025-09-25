import tkinter as tk
from tkinter import ttk

class FileSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Switcher Example")

        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Список файлов (вкладок)
        self.files = ["file1.py", "file2.py", "file3.py"]

        # Создаем вкладки для каждого файла
        for file in self.files:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=file)

            # Добавим текстовое поле для редактирования кода
            text_area = tk.Text(frame)
            text_area.pack(fill='both', expand=True)

            # Заполним текстовое поле каким-то текстом (например, именем файла)
            text_area.insert('1.0', f"# This is {file}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSwitcherApp(root)
    root.geometry("600x400")
    root.mainloop()
