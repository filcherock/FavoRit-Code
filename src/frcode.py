import sys
import os

from tkinter import *
from tkinter.ttk import *
from customtkinter import *
from pickledb import PickleDB

config = PickleDB('config.json')

def on_yscrollcommand(*args):
    scroll.set(*args) 
    numbers.yview_moveto(args[0])

def scroll_command(*args):
    text.yview(*args)
    numbers.yview(*args)

app = Tk()
app.config(relief='flat', border=0, borderwidth=0)

numbers = Text(app, width=4, bg='lightgray', state=DISABLED, relief=FLAT, font=config.get('font'), 
                background="#303030", foreground=config.get('fg'),
                selectbackground="#303030", selectforeground="#FFFFFF", 
                highlightthickness=0,
                highlightbackground="#303030", highlightcolor="#303030", undo=False, insertbackground="#303030",
                insertborderwidth=0, inactiveselectbackground="#303030")
numbers.grid(row=0, column=0, sticky='NS')

scroll = Scrollbar(app)
scroll.grid(row=0, column=2, sticky='NS')

text = Text(app, yscrollcommand=on_yscrollcommand, wrap=NONE, font=config.get('font'), bg="#303030", foreground=config.get('fg'),
            relief='flat', border=0, borderwidth=0, undo=True, insertbackground='#FFFFFF', insertwidth=1)
text.grid(row=0, column=1, sticky='NSWE')

scroll.config(command=scroll_command)

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

def set_focus():
    text.focus_set()
    app.after(100, set_focus)

text.bind('<<Modified>>', on_edit)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

if __name__ == '__main__':
    set_focus()
    app.mainloop()