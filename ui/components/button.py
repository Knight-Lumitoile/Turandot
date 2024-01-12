import tkinter as tk


class Button(tk.Label):

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.bind('<Enter>', self.mouse_enter)
        self.bind('<Leave>', self.mouse_leave)
        self.colour = '#f6f6f6'
        self.hover_color = '#e9e9f6'

    def configure(self, **kw):
        super().configure(**kw)

    def command(self, function):
        self.bind('<Button-1>', function)

    def mouse_enter(self, event):
        self.configure(bg=self.hover_color)

    def mouse_leave(self, event):
        self.configure(bg=self.colour)


class PrimaryButton(Button):

    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        super().configure(bg='#f2f2f2', fg='#b894b8',font=('Calibri', 14, 'bold'))
        super().configure(fg='#b894b8')

    def mouse_enter(self, event):
        super().configure(bg='#b894b8', fg='#f2f2f2')

    def mouse_leave(self, event):
        super().configure(bg='#f2f2f2', fg='#b894b8')



