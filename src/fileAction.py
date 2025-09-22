from tkinter.filedialog import *
from tkinter import *

ftypes = [(u'All files', '*'), (u'Text file', '*.txt'), (u'Python', '*.py'), (u'C++', '*.cpp'), (u'C#', '*.cs'),
        (u'Java', '*.java')]

def openFile(app, editArea):
    fn = Open(app, filetypes=ftypes).show()
    if fn == '':
        return
    editArea.delete('1.0', 'end')
    editArea.insert('1.0', open(fn, encoding="UTF-8").read())

def saveFile(app, editArea):
    pass

def saveAsFile(app, editArea):
    fn = asksaveasfilename(filetypes=ftypes)
    if fn: 
        with open(fn, 'w', encoding='UTF-8') as f:
            text = editArea.get("1.0", END)
            f.write(text) 