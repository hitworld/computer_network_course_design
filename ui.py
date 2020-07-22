# -*- coding: utf-8 -*-

import tkinter as tk

class Mywindow:
    def __init__(self, name):
        self.window = tk.Tk()
        self.window.title(name)
        self.window.geometry('800x600')
        self.t = tk.Text(self.window, height = 20)
        self.t2 = tk.Text(self.window, height = 20)
        self.t.pack()
        self.t2.pack()

    def init_ui(self):
        self.window.mainloop()

    def show(self, message):
        self.t.insert('end', message)

    def show2(self, message):
        self.t2.insert('end', message)