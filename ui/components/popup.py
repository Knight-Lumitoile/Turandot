import tkinter as tk

from static.config import config
from ui.components.button import Button
from core.window_utils import center_window, center_child_window


class MessageWindow:
    def __init__(self, app, message_text):
        self.top = tk.Toplevel(app)
        center_child_window(app, self.top, 666, 407, 500, 60)
        self.top.overrideredirect(True)

        self.label = tk.Label(self.top, text=message_text, font='Calibri 14 bold')
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.config(bg='#ffa3a3')

        self.top.after(2000, self.cleanup)

    def cleanup(self):
        self.top.destroy()


class ConfirmationWindow:

    def __init__(self, app, message_text):
        self.top = tk.Toplevel(app)
        center_window(self.top, 400, 200)
        self.top.configure(bg=config['app_bg_color'])
        self.top.resizable(False, False)

        self.message = tk.Label(self.top)
        self.message.place(relx=0.075, rely=0.15, height=86, width=335)
        self.message.configure(bg=config['app_bg_color'], fg=config['app_fg_color'], text=message_text,
                               font='Calibri 14 bold')

        self.confirm = Button(self.top)
        self.confirm.place(relx=0.2, rely=0.75, height=36, width=80)
        self.confirm.config(text='Yes', font='Calibri 14 bold')
        self.confirm.command(self.on_confirm)  # Fix here

        self.cancel = Button(self.top)
        self.cancel.place(relx=0.6, rely=0.75, height=36, width=80)
        self.cancel.config(text='No', font='Calibri 14 bold')
        self.cancel.hover_color = '#ffa3a3'
        self.cancel.command(self.on_cancel)  # Fix here

        self.return_value = False

    def on_confirm(self, event):
        self.return_value = True
        self.top.destroy()

    def on_cancel(self, event):
        self.top.destroy()
