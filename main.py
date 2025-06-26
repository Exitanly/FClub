import tkinter as tk
from tkinter import messagebox
from functools import partial
from models import ROLE_PLAYER, ROLE_COACH, User
from commands import register_user, authenticate_user
from player_interface import PlayerInterface

class AuthWindow:
    def __init__(self, root, on_auth_success):
        self.root = root
        self.on_auth_success = on_auth_success
        
        # Окно авторизации
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
            # Получаем ID пользователя
            user = User.get(User.username == username)
            self.on_auth_success(username, role, user.id)
            self.auth_window.destroy()
        else:
            messagebox.showerror("Ошибка", message)
    
    def register(self):
        # Создаем окно регистрации
        reg_window = tk.Toplevel(self.auth_window)
        reg_window.title("Регистрация")
        reg_window.geometry("350x300")
        reg_window.resizable(False, False)
        
        # Переменные для формы
        email = tk.StringVar()
        confirm_pass = tk.StringVar()
        role_var = tk.StringVar(value=ROLE_PLAYER)
        
        frame = tk.Frame(reg_window, padx=10, pady=10)
        frame.pack(expand=True)
        
        # Поля формы
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
        
        # Выбор роли
        tk.Label(frame, text="Роль:").grid(row=row, column=0, sticky="w")
        role_frame = tk.Frame(frame)
        role_frame.grid(row=row, column=1, sticky="w")
        tk.Radiobutton(role_frame, text="Игрок", variable=role_var, 
                      value=ROLE_PLAYER).pack(side=tk.LEFT)
        tk.Radiobutton(role_frame, text="Тренер", variable=role_var, 
                      value=ROLE_COACH).pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Кнопка регистрации
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
        self.root.geometry("1000x700")
        self.current_user = None
        self.user_role = None
        self.user_id = None
        
        # Меню
        self.create_menu()
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Не авторизован")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, 
                            relief=tk.SUNKEN, anchor=tk.W, padx=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Основной контент
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
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
    
    def show_auth_window(self):
        self.root.withdraw()
        AuthWindow(self.root, self.on_auth_success)
    
    def on_auth_success(self, username, role, user_id):
        self.current_user = username
        self.user_role = role
        self.user_id = user_id
        self.root.deiconify()
        
        # Обновляем статус бар
        role_name = "Игрок" if role == ROLE_PLAYER else "Тренер"
        self.status_var.set(f"Авторизован: {username} ({role_name})")
        
        # Очищаем основной фрейм
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Показываем соответствующий интерфейс
        if role == ROLE_PLAYER:
            self.show_player_interface()
        else:
            self.show_coach_interface()
    
    def show_player_interface(self):
        """Показывает интерфейс для игрока"""
        PlayerInterface(self.main_frame, self.user_id)
        
        # Добавляем общие кнопки
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Выйти", command=self.logout).pack(side=tk.RIGHT)
    
    def show_coach_interface(self):
        """Показывает интерфейс для тренера"""
        tk.Label(self.main_frame, text=f"Добро пожаловать, тренер {self.current_user}!", 
                font=("Arial", 14)).pack(pady=20)
        
        # Здесь будет интерфейс тренера
        tk.Label(self.main_frame, text="Интерфейс тренера в разработке").pack()
        
        # Кнопки
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Выйти", command=self.logout).pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="Управление тренировками", 
                 command=self.show_trainings).pack(side=tk.LEFT)
    
    def show_trainings(self):
        """Показывает управление тренировками (заглушка)"""
        messagebox.showinfo("Тренировки", "Функционал управления тренировками в разработке")
    
    def logout(self):
        self.current_user = None
        self.user_role = None
        self.user_id = None
        self.status_var.set("Не авторизован")
        
        # Очищаем основной фрейм
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Показываем окно авторизации
        self.show_auth_window()
    
    def show_about(self):
        messagebox.showinfo("О программе", 
                          "Приложение футбольного клуба\nВерсия 1.0\n\n2023")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()