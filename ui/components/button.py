import tkinter as tk
from static.config import config


class Button(tk.Label):

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.bind('<Enter>', self.mouse_enter)
        self.bind('<Leave>', self.mouse_leave)
        self.config(bg=config['button_bg_color'], fg=config['button_fg_color'])

    def configure(self, **kw):
        super().configure(**kw)

    def command(self, function):
        self.bind('<Button-1>', function)

    def mouse_enter(self, event):
        self.config(bg=config['button_bg_color_active'])

    def mouse_leave(self, event):
        self.config(bg=config['button_bg_color'])
