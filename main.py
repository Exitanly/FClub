import tkinter as tk
from tkinter import messagebox
from functools import partial
from commands import register_user, authenticate_user

class AuthWindow:
    def __init__(self, root, on_auth_success):
        self.root = root
        self.on_auth_success = on_auth_success
        
        # окно авторизации
        self.auth_window = tk.Toplevel(root)
        self.auth_window.title("Авторизация")
        self.auth_window.geometry("300x200")
        self.auth_window.resizable(False, False)
        
        # Переменные для хранения ввода
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        
        # Фрейм для элементов
        frame = tk.Frame(self.auth_window, padx=10, pady=10)
        frame.pack(expand=True)
        
        # Элементы формы
        tk.Label(frame, text="Логин:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.username).grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.password, show="*").grid(row=1, column=1, pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=2, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Регистрация", command=self.register).pack(side=tk.LEFT, padx=5)
        
        # Центрируем окно
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
            self.on_auth_success(username, role)
            self.auth_window.destroy()
        else:
            messagebox.showerror("Ошибка", message)
    
    def register(self):
        # Создаем окно регистрации
        reg_window = tk.Toplevel(self.auth_window)
        reg_window.title("Регистрация")
        reg_window.geometry("300x250")
        reg_window.resizable(False, False)
        
        # Дополнительные поля для регистрации
        email = tk.StringVar()
        confirm_pass = tk.StringVar()
        
        frame = tk.Frame(reg_window, padx=10, pady=10)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Логин:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.username).grid(row=0, column=1, pady=5)
        
        tk.Label(frame, text="Email: (Необязательно)").grid(row=1, column=0, sticky="w")
        tk.Entry(frame, textvariable=email).grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.password, show="*").grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="Подтвердите пароль:").grid(row=3, column=0, sticky="w")
        tk.Entry(frame, textvariable=confirm_pass, show="*").grid(row=3, column=1, pady=5)
        
        tk.Button(frame, text="Зарегистрироваться", 
                 command=partial(self.do_register, email, confirm_pass, reg_window)
                ).grid(row=4, columnspan=2, pady=10)
        
        self.center_window(reg_window)
    
    def do_register(self, email, confirm_pass, window):
        # Проверка данных регистрации
        if not all([self.username.get(), email.get(), self.password.get(), confirm_pass.get()]):
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
            return
            
        if self.password.get() != confirm_pass.get():
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
            
        # Регистрация пользователя в БД
        success, message = register_user(self.username.get(), email.get(), self.password.get())
        
        if success:
            messagebox.showinfo("Успех", message)
            window.destroy()
        else:
            messagebox.showerror("Ошибка", message)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное окно")
        self.root.geometry("800x600")
        self.current_user = None
        self.user_role = None
        
        # Меню
        self.create_menu()
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Не авторизован")
        tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
        
        # Основное содержимое
        self.create_content()
        
        # Показываем окно авторизации при старте
        self.show_auth_window()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню Помощь
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_content(self):
        content_frame = tk.Frame(self.root, padx=10, pady=10)
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(content_frame, text="Добро пожаловать в приложение!", 
                font=("Arial", 14)).pack(pady=20)
        
        # Пример кнопок с разными функциями
        tk.Button(content_frame, text="Открыть профиль", 
                 command=self.open_profile).pack(pady=5, fill=tk.X)
        
        tk.Button(content_frame, text="Настройки", 
                 command=self.open_settings).pack(pady=5, fill=tk.X)
        
        tk.Button(content_frame, text="Выйти", 
                 command=self.logout).pack(pady=5, fill=tk.X)
    
    def show_auth_window(self):
        # Блокируем главное окно пока открыто окно авторизации
        self.root.withdraw()
        AuthWindow(self.root, self.on_auth_success)
    
    def on_auth_success(self, username, role):
        # Разблокируем главное окно после успешной авторизации
        self.current_user = username
        self.user_role = role
        self.root.deiconify()
        self.status_var.set(f"Авторизован: {username} ({role})")
        messagebox.showinfo("Добро пожаловать", f"Здравствуйте, {username}!")
    
    def logout(self):
        self.current_user = None
        self.user_role = None
        self.status_var.set("Не авторизован")
        self.show_auth_window()
    
    def open_profile(self):
        if self.current_user:
            messagebox.showinfo("Профиль", f"Профиль пользователя: {self.current_user}\nРоль: {self.user_role}")
        else:
            messagebox.showerror("Ошибка", "Вы не авторизованы")
    
    def open_settings(self):
        messagebox.showinfo("Настройки", "Здесь будут настройки приложения")
    
    def show_about(self):
        messagebox.showinfo("О программе", "Это приложение футбольного клуба.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()