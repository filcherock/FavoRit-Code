from tkinter.filedialog import *

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
    pass