import shutil
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
import os

from send2trash import send2trash

from core.byte_operations import encrypt_file_xor
from core.window_utils import center_window
from static.config import config
from static.enums import AppMode
from ui.components.button import Button
from ui.components.popup import ConfirmationWindow, MessageWindow


class App:
    """
    Main application
    """
    app = tk.Tk()
    app_mode = AppMode.Home
    app_running = False
    button_backward = None
    button_choose_file = None
    button_forward = None
    button_help = None
    button_home = None
    button_mode_create = None
    button_mode_open = None
    button_open_file = None
    button_save_file = None
    current_frame = None
    filename = ''
    frame_app = None
    frame_file = None
    frame_home = None
    frame_tips = None
    input_password = None
    label_app_title = None
    label_file_directory = None
    label_password = None
    new_filename = ''
    password = ''
    string_vars = tk.StringVar()
    text_tips = None

    def __init__(self):
        self.app.title("Turandot")
        center_window(self.app, 666, 407)
        self.app.resizable(False, False)
        self.app.configure(background='#333333')
        self.app.protocol('WM_DELETE_WINDOW', self.on_app_destroy)
        self.string_vars.trace('w', lambda name, index, mode, var=self.string_vars: self.on_password_update())
        self.load_frame_home(None)
        self.app.mainloop()

    def load_frame_home(self, event):

        if self.app_mode == AppMode.Open and self.app_running:
            nw = ConfirmationWindow(self.app,
                                    'Current opened file will be deleted.\nDo you want to continue?')
            nw.top.grab_set()
            nw.top.focus_set()
            self.app.wait_window(nw.top)
            nw.top.grab_release()
            if nw.return_value:
                try:
                    os.remove(self.new_filename)
                    self.app_running = False
                except FileNotFoundError:
                    pass
                except PermissionError:
                    MessageWindow(self.app, "The file is used by another application!")
                    return
            else:
                return

        self.filename = ""
        self.new_filename = ""
        self.password = ""
        try:
            self.input_password.delete(0, 'end')
        except:
            pass
        self.current_frame.destroy() if self.current_frame else None
        # Load Home Page
        self.frame_home = tk.Frame(self.app)
        self.frame_home.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.frame_home.configure(relief='flat', background=config['app_bg_color'])

        # App Title
        self.label_app_title = tk.Label(self.frame_home)
        self.label_app_title.place(relx=0.06, rely=0.074, height=226, width=586)
        self.label_app_title.configure(background=config['app_bg_color'],
                                       font='-family {Century Gothic} -size 64',
                                       foreground=config['app_fg_color'],
                                       text="Turandot")

        # Button Create
        self.button_mode_create = Button(self.frame_home)
        self.button_mode_create.config(font=('Century Gothic', 13, 'bold'))
        self.button_mode_create.place(relx=0.151, rely=0.713, height=66, relwidth=0.33)
        self.button_mode_create.config(relief='flat', text='Create')
        self.button_mode_create.command(self.on_select_app_mode)

        # Button Open
        self.button_mode_open = Button(self.frame_home)
        self.button_mode_open.config(font=('Century Gothic', 13, 'bold'))
        self.button_mode_open.place(relx=0.52, rely=0.713, height=66, relwidth=0.33)
        self.button_mode_open.config(relief='flat', text='Open')
        self.button_mode_open.command(self.on_select_app_mode)

        # Store Current Frame
        self.current_frame = self.frame_home

    def on_select_app_mode(self, event):
        if event.widget == self.button_mode_open:
            self.app_mode = AppMode.Open
        elif event.widget == self.button_mode_create:
            self.app_mode = AppMode.Create
        self.load_frame_app(None)

    # def load_frame_tips(self, event):
    #     # Destroy Current Frame
    #     self.current_frame.destroy() if self.current_frame else None
    #     # Load Frame Tips
    #     self.frame_tips = tk.Frame(self.app)
    #     self.frame_tips.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
    #     self.frame_tips.configure(relief='flat', background='#ffffff')
    #     self.text_tips = scrolledtext.ScrolledText(self.frame_tips)
    #     self.text_tips.place(relx=0.071, rely=0.098, relheight=0.698, relwidth=0.86)
    #     self.text_tips.configure(background='#f6f6f6', font=('Calibri', 12))
    #     self.text_tips.configure(foreground='black', relief='flat')
    #     if self.app_mode == AppMode.Create:
    #         self.text_tips.insert(tk.INSERT,
    #                               '                                        -----------------------\n                                             Decrypting\n                                        -----------------------\n1. Choose your encrypted file, and enter the password you used \n    to encrypt it.\n2. Click "open", the program will decrypt your file to a temporary \n    file and open it.\n3. You can then modify the temporary file.\n4. After modifying, close your file, and click "save". The program\n    will encrypt your modified temporary file and update your \n    original file.\n\n*  Closing the program, reselecting file or going back to main \n    menu will delete your temporary file.')
    #     elif self.app_mode == AppMode.Open:
    #         self.text_tips.insert(tk.INSERT,
    #                               '                                        -----------------------\n                                             Encrypting\n                                        -----------------------\n1. Choose the file you want it to be encrypted.\n2. Enter your preferred password.\n3. The program will encrypt the file using your password and \n    save it to a file with the name of your original file followed by \n    "_encrypted" suffix.\n\n*  Please always remember your password. The program cannot\n    tell whether the password is correct or not. If you forgot your \n    password, you can never decrypt your file!')
    #
    #     # Backward Button
    #     self.button_backward = Button(self.frame_tips)
    #     self.button_backward.place(relx=0.25, rely=0.86, height=33, relwidth=0.24)
    #     self.button_backward.config(text='Back')
    #     self.button_backward.command(self.load_frame_home)
    #
    #     # Forward Button
    #     self.button_forward = Button(self.frame_tips)
    #     self.button_forward.place(relx=0.51, rely=0.86, height=33, relwidth=0.24)
    #     self.button_forward.config(background='#f2f2f2', foreground='#000000', text='Continue')
    #     self.button_forward.command(self.load_frame_app)
    #
    #     # Store Current Frame
    #     self.current_frame = self.frame_tips

    def load_frame_app(self, event):
        # Destroy Current Frame
        self.current_frame.destroy() if self.current_frame else None
        # Load Frame App
        self.frame_app = tk.Frame(self.app)
        self.frame_app.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.frame_app.configure(relief='flat', background=config['app_bg_color'])

        # Return Button
        self.button_help = Button(self.frame_app)
        self.button_help.place(relx=0.03, rely=0.049, height=36, width=35)
        self.button_help.config(text='←', font='Calibri 14 bold')
        self.button_help.command(self.load_frame_home)

        # File Chooser Frame
        self.frame_file = tk.Frame(self.frame_app)
        self.frame_file.place(relx=0.101, rely=0.295, relheight=0.081, relwidth=0.8)
        self.frame_file.configure(relief='flat', background=config['app_bg_color'])

        # File Directory Label
        self.label_file_directory = tk.Label(self.frame_file)
        self.label_file_directory.place(relx=0.0, rely=0.0, height=33, width=400)
        self.label_file_directory.configure(background=config['button_bg_color_active'],
                                            foreground=config['button_fg_color'], font='Calibri 14 bold')

        # Choose File Button
        self.button_choose_file = Button(self.frame_file)
        self.button_choose_file.place(relx=0.75, rely=0.0, height=33, width=133)
        self.button_choose_file.config(text='Choose File', font='Calibri 14 bold')
        self.button_choose_file.command(self.select_file)

        # Password Label
        self.label_password = tk.Label(self.frame_app)
        self.label_password.place(relx=0.35, rely=0.467, height=33, width=200)
        self.label_password.configure(bg=config['app_bg_color'], fg=config['button_fg_color'],
                                      text='Please Enter Password', font='Calibri 14 bold')

        # Password Input
        self.input_password = tk.Entry(self.frame_app)
        self.input_password.place(relx=0.251, rely=0.663, height=29, relwidth=0.5)
        self.input_password.configure(textvariable=self.string_vars, background=config['button_bg_color_active'],
                                      font='Calibri 14 bold', fg=config['button_fg_color'], justify='center',
                                      relief='flat')
        self.input_password.delete(0, 'end')

        if self.app_mode == AppMode.Open:
            # Button Open File
            self.button_open_file = Button(self.frame_app)
            self.button_open_file.place(relx=0.25, rely=0.86, height=33, relwidth=0.24)
            self.button_open_file.config(text='Open', font='Calibri 14 bold')
            self.button_open_file.command(self.open_encrypted_file)

            # Button Save File
            self.button_save_file = Button(self.frame_app)
            self.button_save_file.place(relx=0.51, rely=0.86, height=33, relwidth=0.24)
            self.button_save_file.config(text='Save', font='Calibri 14 bold')
            self.button_save_file.command(self.save_encrypted_file)

        elif self.app_mode == AppMode.Create:

            # Button Save File
            self.button_save_file = Button(self.frame_app)
            self.button_save_file.place(relx=0.38, rely=0.86, height=33, relwidth=0.26)
            self.button_save_file.config(text='Save', font='Calibri 14 bold')
            self.button_save_file.command(self.create_encrypted_file)

        # Store Current Frame
        self.current_frame = self.frame_app

    def select_file(self, event):
        if self.app_running:
            popup = ConfirmationWindow(
                'This action will delete your tempting file,\n please remember to save it\n if needed.')
            popup.top.grab_set()
            popup.top.focus_set()
            self.app.wait_window(popup.top)
            popup.top.grab_release()
            if popup.return_value:
                os.remove(self.new_filename)
                self.app_running = False
            else:
                return
        else:
            self.filename = os.path.normpath(filedialog.askopenfilename(title='Select A File'))
            if self.filename:
                base_name, extension = os.path.splitext(os.path.basename(self.filename))
                self.label_file_directory.config(text=base_name)
            else:
                return

    def on_password_update(self):
        password = self.string_vars.get()
        if len(password) > len(self.password):
            self.password += password[(-1)]
        else:
            self.password = self.password[:-1]
        self.input_password.delete(0, 'end')
        self.input_password.insert(0, '*' * len(self.password))

    def open_encrypted_file(self, event):
        if self.filename is None or self.filename == '':
            MessageWindow(self.app, 'Please choose a file!')
        elif self.password == '':
            MessageWindow(self.app, 'Please enter password!')
        else:
            folder_path = os.path.dirname(self.filename)
            base_name, extension = os.path.splitext(os.path.basename(self.filename))
            self.new_filename = os.path.join(folder_path, base_name + ' - TURANDOT TEMP' + extension)
            print(self.new_filename)
            self.app_running = True
            encrypt_file_xor(self.filename, self.new_filename, self.password)
            os.startfile(self.new_filename)

    def save_encrypted_file(self, event):
        if not self.app_running:
            MessageWindow(self.app, 'Please open a file first!')
            return
        else:
            nw = ConfirmationWindow(self.app,
                                    'The original file will be send to \nRecycle Bin as a backup,\nDo you want to continue?')
            nw.top.grab_set()
            nw.top.focus_set()
            self.app.wait_window(nw.top)
            nw.top.grab_release()

            if nw.return_value:
                self.create_trash_backup()
                encrypt_file_xor(self.new_filename, self.filename, self.password)
                MessageWindow(self.app, 'File saved!')
            return

    def create_trash_backup(self):
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        folder_path = os.path.dirname(self.filename)
        base_name, extension = os.path.splitext(os.path.basename(self.filename))
        backup_name = f"{base_name}_{current_datetime}{extension}"
        backup_path = os.path.join(folder_path, backup_name)
        shutil.copy2(self.filename, backup_path)
        send2trash(backup_path)

    def delete_temp_file(self):
        if self.app_mode == AppMode.Open:
            try:
                os.remove(self.new_filename)
            except:
                pass

    def on_app_destroy(self):
        self.delete_temp_file()
        self.app.destroy()

    def create_encrypted_file(self, event):
        if self.filename is None or self.filename == '':
            MessageWindow(self.app, 'Please choose a file!')
            return
        if self.password == '':
            MessageWindow(self.app, 'Please enter password!')
            return
        folder_path = os.path.dirname(self.filename)
        base_name, extension = os.path.splitext(os.path.basename(self.filename))
        self.new_filename = os.path.join(folder_path, base_name + ' - Encrypted' + extension)
        encrypt_file_xor(self.filename, self.new_filename, self.password)
        MessageWindow(self.app, 'Encrypted file created!')
        os.startfile(folder_path)
