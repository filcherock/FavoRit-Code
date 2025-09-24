import sys
import os
import re

from tkinter import *
from tkinter.ttk import *
from customtkinter import *
from pickledb import PickleDB
from fileAction import *

from proglang import *
from fileAction import isEdit, newFile, cur_path, changeTitle

config = PickleDB('config.json')

def on_yscrollcommand(*args):
    scroll.set(*args) 
    numbers.yview_moveto(args[0])

def scroll_command(*args):
    text.yview(*args)
    numbers.yview(*args)

app = CTk()
app.config(relief='flat', border=0, borderwidth=0)

numbers = Text(app, width=4, bg='lightgray', state=DISABLED, relief=FLAT, font=config.get('font'), 
                background="#292929", foreground=config.get('num_color'),
                selectbackground="#292929", selectforeground="#FFFFFF", 
                highlightthickness=0,
                highlightbackground="#292929", highlightcolor="#292929", undo=False, insertbackground="#292929",
                insertborderwidth=0, inactiveselectbackground="#292929", borderwidth=10)
numbers.grid(row=0, column=0, sticky='NS')

scroll = CTkScrollbar(app, bg_color="#303030", command=scroll_command)
scroll.grid(row=0, column=2, sticky='NS')

text = Text(app, yscrollcommand=on_yscrollcommand, wrap=NONE, font=config.get('font'), bg=config.get('bg'), foreground=config.get('fg'),
            relief='flat', border=0, borderwidth=10, undo=True, insertbackground='#FFFFFF', insertwidth=1, highlightbackground="#303030",
            highlightcolor="#303030")
text.grid(row=0, column=1, sticky='NSWE')

#scroll.config(command=scroll_command)

menubar = Menu(app, tearoff=False, bg='#292929', fg='white', activebackground="#7F0D83", activeforeground='white', border=0,activeborderwidth=0)

file = Menu(menubar, tearoff=False, bg='#292929', fg='white', activebackground="#7F0D83", activeforeground='white', border=0, activeborderwidth=0) 
file.add_command(label="New file", command=lambda: print(1), accelerator="      CTRL-N")
file.add_command(label="Open file", command=lambda: openFile(app, text), accelerator="     CTRL-O")
file.add_command(label="Close file", command=lambda: print(1), accelerator="    CTRL-W")
file.add_separator()
file.add_command(label="Open Folder", command=lambda: print(1), accelerator="      CTRL-SHIFT-O")
file.add_separator()
file.add_command(label="Save file", command=lambda: saveFile(app, text), accelerator="    CTRL-S") 
file.add_command(label="Save file as", command=lambda: saveAsFile(app, text), accelerator="    CTRL-SHIFT-S") 
file.add_separator()
file.add_command(label="Exit", command=app.quit, accelerator="   ALT-F4") 

edit = Menu(menubar, tearoff=False, bg='#292929', fg='white', activebackground="#7F0D83", activeforeground='white', border=0, activeborderwidth=0) 
edit.add_command(label="Undo", command=text.edit_undo, accelerator="      CTRL-Z")
edit.add_command(label="Repo", command=text.edit_redo, accelerator="      CTRL-Y")

menubar.add_cascade(label="File", menu=file) 
menubar.add_cascade(label="Edit", menu=edit)

app.config(menu=menubar, relief='flat', border=0, borderwidth=0)

infoPanel = Frame(app, height=20)
frcodeLabel = Label(infoPanel, text="FavoRit Code", background=config.get('bg'), foreground=config.get('fg'))

def insert_numbers():
    count_of_lines = text.get(1.0, END).count('\n') + 1
    numbers.config(state=NORMAL)
    numbers.delete(1.0, END)
    numbers.insert(1.0, '\n'.join(map(str, range(1, count_of_lines))))
    numbers.config(state=DISABLED)

insert_numbers()

def on_edit(event):
    insert_numbers()
    text.edit_modified(0)

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

    if newFile != False:
        if isEdit != True:
            changeTitle(app, f"FavoRit Code - {cur_path}", "*")
        else:
            changeTitle(app, f"FavoRit Code - {cur_path}", "")
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

text.bind('<<Modified>>', on_edit)
app.bind('<KeyRelease>', changes)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

if __name__ == '__main__':
    app.title("FavoRit Code")
    app.mainloop()