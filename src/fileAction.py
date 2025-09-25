from tkinter.filedialog import *
from tkinter import *

ftypes = [(u'All files', '*'), (u'Text file', '*.txt'), (u'Python', '*.py'), (u'C++', '*.cpp'), (u'C#', '*.cs'),
        (u'Java', '*.java')]

cur_path = ''
isEdit = False
newFile = True

def changeTitle(app, param):
    global cur_path
    app.title(f"FavoRit Code - {cur_path}{param}")

def closeFile(app, editArea):
    global cur_path
    cur_path = ''
    editArea.delete('1.0', 'end')
    app.title('FavoRit Code')

def openFile(app, editArea):
    global cur_path, newFile
    fn = Open(app, filetypes=ftypes).show()
    if fn == '':
        return
    editArea.delete('1.0', 'end')
    editArea.insert('1.0', open(fn, encoding="UTF-8").read())
    app.title(f"FavoRit Code - {fn}")
    cur_path = fn
    newFile = False

def saveFile(app, editArea):
    global cur_path, isEdit
    try:
        with open(cur_path, 'w', encoding='UTF-8') as f:
            text = editArea.get("1.0", END)
            f.write(text) 
            isEdit = False
            app.title(f"FavoRit Code - {cur_path}")
    except FileNotFoundError:
        saveAsFile(app, editArea)

def saveAsFile(app, editArea):
    global cur_path, isEdit
    fn = asksaveasfilename(filetypes=ftypes)
    if fn: 
        with open(fn, 'w', encoding='UTF-8') as f:
            text = editArea.get("1.0", END)
            f.write(text) 
        cur_path = fn
        isEdit = False
        app.title(f"FavoRit Code - {cur_path}")