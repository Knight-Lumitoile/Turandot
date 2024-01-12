from ctypes import windll

from ui.app import App


def main():
    windll.shcore.SetProcessDpiAwareness(1)
    App()


if __name__ == '__main__':
    main()
