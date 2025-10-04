# Import built-in libraries
import sys
import os
import re

# From's import
from tkinter import *
from tkinter.ttk import *
from customtkinter import *
from pickledb import PickleDB
from fileAction import *

# Files Import
from proglang import *
from fileAction import isEdit, newFile, changeTitle

# Load configs from file config.json
config = PickleDB('config.json')

# Functions for synchronizing scrolling with two text fields
def on_yscrollcommand(*args):
    scroll.set(*args) 
    numbers.yview_moveto(args[0])

def scroll_command(*args):
    text.yview(*args)
    numbers.yview(*args)

# Create application
app = CTk()
app.config(relief='flat', border=0, borderwidth=0)

'''style = Style()
style.configure('Dark.TNotebook', background='#292929', bordercolor='#292929')
style.configure('Dark.TNotebook.Tab', background='#292929', foreground='white', borderwidth=0)
style.configure('Dark.TNotebook.Tab', padding=[5, 2])
style.map('Dark.TNotebook.Tab', background=[('selected', "#606060")], foreground=[('selected', 'white')])'''


'''fileChild = Frame(fileSwitch)
fileChild.configure(bg=config.get('bg'))
fileSwitch.add(fileChild, text="main.py")'''

#style.configure('TFrame', background=config.get('bg'))
# fileSwitch.pack(side='top', fill='x')

# Create work frame
bottom_frame = Frame(app) 
bottom_frame.pack(side='top', fill='both', expand=True)

# Create text field for line numbering
numbers = Text(app, width=4, bg='lightgray', state=DISABLED, relief=FLAT, font=config.get('font'), 
                background="#292929", foreground=config.get('num_color'),
                selectbackground="#292929", selectforeground="#FFFFFF", 
                highlightthickness=0,
                highlightbackground="#292929", highlightcolor="#292929", undo=False, insertbackground="#292929",
                insertborderwidth=0, inactiveselectbackground="#292929", borderwidth=10)
numbers.pack(in_=bottom_frame, side='left', fill='y')

# Create text field for writing code
text = Text(app, yscrollcommand=on_yscrollcommand, wrap=NONE, font=config.get('font'), bg=config.get('bg'), foreground=config.get('fg'),
            relief='flat', border=0, borderwidth=10, undo=True, insertbackground='#FFFFFF', insertwidth=1, highlightbackground="#303030",
            highlightcolor="#303030")
text.pack(in_=bottom_frame, side='left', fill='both', expand=True)

# Create scroll
scroll = CTkScrollbar(app, bg_color="#303030", command=scroll_command)
scroll.pack(in_=bottom_frame, side='left', fill='y')

# Create menubar
menubar = Menu(app, tearoff=False, bg='#292929', fg='white', activebackground="#7F0D83", activeforeground='white', border=0,activeborderwidth=0)

# Create commands for cascade 'File'
file = Menu(menubar, tearoff=False, bg='#292929', fg='white', activebackground="#7F0D83", activeforeground='white', border=0, activeborderwidth=0) 
file.add_command(label="New file", command=lambda: print(1), accelerator="      CTRL-N")
file.add_command(label="Open file", command=lambda: openFile(app, text), accelerator="     CTRL-O")
file.add_command(label="Close file", command=lambda: closeFile(app, text), accelerator="    CTRL-W")
file.add_separator()
file.add_command(label="Open Folder", command=lambda: print(1), accelerator="      CTRL-SHIFT-O")
file.add_separator()
file.add_command(label="Save file", command=lambda: saveFile(app, text), accelerator="    CTRL-S") 
file.add_command(label="Save file as", command=lambda: saveAsFile(app, text), accelerator="    CTRL-SHIFT-S") 
file.add_separator()
file.add_command(label="Exit", command=app.quit, accelerator="   ALT-F4") 

# Create commands for cascade 'Edit'
edit = Menu(menubar, tearoff=False, bg='#292929', fg='white', activebackground="#7F0D83", activeforeground='white', border=0, activeborderwidth=0) 
edit.add_command(label="Undo", command=text.edit_undo, accelerator="      CTRL-Z")
edit.add_command(label="Repo", command=text.edit_redo, accelerator="      CTRL-Y")

# Create cascades
menubar.add_cascade(label="File", menu=file) 
menubar.add_cascade(label="Edit", menu=edit)

# Update config
app.config(menu=menubar)

'''infoPanel = Frame(app, height=20)
frcodeLabel = Label(infoPanel, text="FavoRit Code", background=config.get('bg'), foreground=config.get('fg'))'''

# Numeration updater
def insert_numbers():
    count_of_lines = text.get(1.0, END).count('\n') + 1
    numbers.config(state=NORMAL)
    numbers.delete(1.0, END)
    numbers.insert(1.0, '\n'.join(map(str, range(1, count_of_lines))))
    numbers.config(state=DISABLED)

# Function, when text on edit
def on_edit(event):
    changes()
    insert_numbers()
    text.edit_modified(0) 

# Functions for syntax highlighting
def changes(event=None):
    global ptext

    current_text = text.get('1.0', 'end-1c')
    if current_text == ptext:
        return

    for tag in text.tag_names():
        text.tag_remove(tag, '1.0', 'end')

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, current_text):
            tag_name = f"tag{i}"
            text.tag_add(tag_name, start, end)
            text.tag_config(tag_name, foreground=color)
            i += 1

    ptext = current_text

    if newFile != True:
        if isEdit != True:
            changeTitle(app, "*")
        else:
            changeTitle(app, "")
    else:
        pass

def search_re(pat, text):
    matches = []
    lines = text.splitlines()

    pattern_compiled = re.compile(pat)
    for i, line in enumerate(lines):
        for match in pattern_compiled.finditer(line):
            start_index = f"{i + 1}.{match.start()}"
            end_index = f"{i + 1}.{match.end()}"
            matches.append((start_index, end_index))
    return matches

# Binds
text.bind('<<Modified>>', on_edit)
app.bind('<KeyRelease>', changes)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Starting
if __name__ == '__main__':
    app.title("FavoRit Code")
    insert_numbers()
    app.mainloop()