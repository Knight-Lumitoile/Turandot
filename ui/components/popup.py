import tkinter as tk

from ui.components.button import Button
from core.window_utils import center_window, center_child_window


class MessageWindow:
    def __init__(self, app, message_text):
        self.top = tk.Toplevel(app)
        center_child_window(app, self.top, 666, 407, 300, 50)
        self.top.overrideredirect(True)

        self.label = tk.Label(self.top, text=message_text, font=('Calibri', 14))
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.config(bg='#ffa3a3')

        self.top.after(1000, self.cleanup)

    def cleanup(self):
        self.top.destroy()


class ConfirmationWindow:

    def __init__(self, app, message_text):
        self.top = tk.Toplevel(app)
        center_window(self.top, 400, 200)
        self.top.configure(background='#ffffff')
        self.top.resizable(False, False)

        self.message = tk.Label(self.top)
        self.message.place(relx=0.075, rely=0.15, height=86, width=335)
        self.message.configure(background='#ffffff', foreground='#000000', text=message_text, font=('Calibri', 12))

        self.confirm = Button(self.top)
        self.confirm.place(relx=0.2, rely=0.75, height=26, width=80)
        self.confirm.config(background='#f6f6f6', foreground='#000000', text='Confirm')
        self.confirm.hover_color = '#ffa3a3'
        self.confirm.configure(command=self.on_confirm)  # Fix here

        self.cancel = Button(self.top)
        self.cancel.place(relx=0.6, rely=0.75, height=26, width=80)
        self.cancel.config(background='#f6f6f6', foreground='#000000', text='Cancel')
        self.cancel.hover_color = '#ffa3a3'
        self.cancel.configure(command=self.on_cancel)  # Fix here

        self.return_value = False

    def on_confirm(self):
        self.return_value = True
        self.top.destroy()

    def on_cancel(self):
        self.top.destroy()
