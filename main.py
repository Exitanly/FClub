import tkinter as tk
from tk import messagebox
from functools import partial

class AuthWindow:
    def __init__(self, root, on_auth_success):
        self.root = root
        self.on_auth_success = on_auth_success

        self.aith_window = tk.Toplevel(root)
        self.auth_window.title("Авторизация")
        self.auth_window.geometry("300x200")
        self.auth_window.resizable(False, False)

        self.username = tk.StringVar()
        self.passworg = tk.StringVar()

        