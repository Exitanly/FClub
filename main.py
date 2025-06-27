import tkinter as tk
from tkinter import messagebox
from functools import partial
from models import ROLE_PLAYER, ROLE_COACH, ROLE_ADMIN, User
from commands import register_user, authenticate_user
from player_interface import PlayerInterface
from coach_interface import CoachInterface
from admin_interface import AdminInterface

class AuthWindow:
    def __init__(self, root, on_auth_success):
        self.root = root
        self.on_auth_success = on_auth_success
        
        self.auth_window = tk.Toplevel(root)
        self.auth_window.title("Авторизация")
        self.auth_window.geometry("300x200")
        self.auth_window.resizable(False, False)
        
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        frame = tk.Frame(self.auth_window, padx=10, pady=10)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Логин:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.username).grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.password, show="*").grid(row=1, column=1, pady=5)
        
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Регистрация", command=self.register).pack(side=tk.LEFT, padx=5)
        
        self.center_window(self.auth_window)
        
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')
    
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
            
        success, message, role = authenticate_user(username, password)
        
        if success:
            user = User.get(User.username == username)
            self.on_auth_success(username, role, user.id)
            self.auth_window.destroy()
        else:
            messagebox.showerror("Ошибка", message)
    
    def register(self):
        reg_window = tk.Toplevel(self.auth_window)
        reg_window.title("Регистрация")
        reg_window.geometry("350x300")
        reg_window.resizable(False, False)
        
        email = tk.StringVar()
        confirm_pass = tk.StringVar()
        role_var = tk.StringVar(value=ROLE_PLAYER)
        
        frame = tk.Frame(reg_window, padx=10, pady=10)
        frame.pack(expand=True)
        
        row = 0
        tk.Label(frame, text="Логин:").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.username).grid(row=row, column=1, pady=5)
        row += 1
        
        tk.Label(frame, text="Email:").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=email).grid(row=row, column=1, pady=5)
        row += 1
        
        tk.Label(frame, text="Пароль:").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.password, show="*").grid(row=row, column=1, pady=5)
        row += 1
        
        tk.Label(frame, text="Подтвердите пароль:").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=confirm_pass, show="*").grid(row=row, column=1, pady=5)
        row += 1
        
        tk.Label(frame, text="Роль:").grid(row=row, column=0, sticky="w")
        role_frame = tk.Frame(frame)
        role_frame.grid(row=row, column=1, sticky="w")
        tk.Radiobutton(role_frame, text="Игрок", variable=role_var, 
                      value=ROLE_PLAYER).pack(side=tk.LEFT)
        tk.Radiobutton(role_frame, text="Тренер", variable=role_var, 
                      value=ROLE_COACH).pack(side=tk.LEFT, padx=10)
        row += 1
        
        tk.Button(frame, text="Зарегистрироваться", 
                 command=partial(self.do_register, email, confirm_pass, role_var, reg_window)
                ).grid(row=row, columnspan=2, pady=10)
        
        self.center_window(reg_window)
    
    def do_register(self, email, confirm_pass, role_var, window):
        if not all([self.username.get(), email.get(), self.password.get(), confirm_pass.get()]):
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
            return
            
        if self.password.get() != confirm_pass.get():
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
            
        success, message = register_user(
            self.username.get(),
            email.get(),
            self.password.get(),
            role_var.get()
        )
        
        if success:
            messagebox.showinfo("Успех", message)
            window.destroy()
        else:
            messagebox.showerror("Ошибка", message)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Футбольный клуб - Главное меню")
        self.root.geometry("1200x800")
        self.current_user = None
        self.user_role = None
        self.user_id = None
        
        self.create_menu()
        
        self.status_var = tk.StringVar()
        self.status_var.set("Не авторизован")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, 
                            relief=tk.SUNKEN, anchor=tk.W, padx=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.show_auth_window()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_auth_window(self):
        self.root.withdraw()
        AuthWindow(self.root, self.on_auth_success)
    
    def on_auth_success(self, username, role, user_id):
        self.current_user = username
        self.user_role = role
        self.user_id = user_id
        self.root.deiconify()
        
        role_names = {
            ROLE_ADMIN: "Администратор",
            ROLE_COACH: "Тренер", 
            ROLE_PLAYER: "Игрок"
        }
        self.status_var.set(f"Авторизован: {username} ({role_names.get(role, 'Неизвестная роль')})")
        
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        if role == ROLE_ADMIN:
            AdminInterface(self.main_frame, user_id)
        elif role == ROLE_COACH:
            CoachInterface(self.main_frame, user_id)
        else:
            PlayerInterface(self.main_frame, user_id)
    
    def show_about(self):
        messagebox.showinfo("О программе", 
                          "Приложение футбольного клуба\nВерсия 3.0\n\n2023")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()