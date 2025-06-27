import tkinter as tk
from tkinter import ttk, messagebox
from models import User, Player, DB
from functools import partial

class AdminInterface:
    def __init__(self, root, user_id):
        self.root = root
        self.user = User.get(User.id == user_id)
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.create_control_buttons()
        self.create_coaches_section()

    def create_control_buttons(self):
        """Создает кнопки управления"""
        control_frame = tk.Frame(self.frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            control_frame, 
            text="Список тренеров", 
            command=self.show_coaches_list,
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Список игроков",
            command=self.show_players_list,
            bg="#2196F3",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

    def show_coaches_list(self):
        """Показывает список тренеров"""
        self.clear_interface()
        self.create_coaches_section()

    def show_players_list(self):
        """Показывает список игроков"""
        self.clear_interface()
        self.create_players_section()

    def clear_interface(self):
        """Очищает текущий интерфейс"""
        for widget in self.frame.winfo_children()[1:]:  # Сохраняем только control_buttons
            widget.destroy()

    def create_coaches_section(self):
        """Создает раздел со списком тренеров"""
        coaches_frame = tk.LabelFrame(self.frame, text="Список тренеров", padx=10, pady=10)
        coaches_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица тренеров
        columns = ("id", "username", "actions")
        self.coaches_tree = ttk.Treeview(
            coaches_frame, 
            columns=columns, 
            show="headings"
        )
        
        # Настройка колонок
        self.coaches_tree.heading("id", text="ID")
        self.coaches_tree.heading("username", text="Имя")
        self.coaches_tree.heading("actions", text="Действия")
        
        self.coaches_tree.column("id", width=50, anchor='center')
        self.coaches_tree.column("username", width=200)
        self.coaches_tree.column("actions", width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(coaches_frame, orient="vertical", command=self.coaches_tree.yview)
        self.coaches_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.coaches_tree.pack(fill=tk.BOTH, expand=True)
        
        self.update_coaches_list()

    def create_players_section(self):
        """Создает раздел со списком игроков"""
        players_frame = tk.LabelFrame(self.frame, text="Список игроков", padx=10, pady=10)
        players_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица игроков
        columns = ("id", "name", "jersey", "actions")
        self.players_tree = ttk.Treeview(
            players_frame, 
            columns=columns, 
            show="headings"
        )
        
        # Настройка колонок
        self.players_tree.heading("id", text="ID")
        self.players_tree.heading("name", text="Имя")
        self.players_tree.heading("jersey", text="Номер")
        self.players_tree.heading("actions", text="Действия")
        
        self.players_tree.column("id", width=50, anchor='center')
        self.players_tree.column("name", width=200)
        self.players_tree.column("jersey", width=80, anchor='center')
        self.players_tree.column("actions", width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(players_frame, orient="vertical", command=self.players_tree.yview)
        self.players_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.players_tree.pack(fill=tk.BOTH, expand=True)
        
        self.update_players_list()

    def update_coaches_list(self):
        """Обновляет список тренеров"""
        for item in self.coaches_tree.get_children():
            self.coaches_tree.delete(item)
            
        coaches = User.select().where(User.role == 'coach').order_by(User.username)
        
        for coach in coaches:
            btn_frame = tk.Frame()
            tk.Button(
                btn_frame,
                text="Удалить",
                command=partial(self.delete_coach, coach.id),
                bg="#f44336",
                fg="white"
            ).pack(padx=5)
            
            self.coaches_tree.insert("", tk.END, values=(
                coach.id,
                coach.username,
                ""
            ))
            self.coaches_tree.window_create("", window=btn_frame)

    def update_players_list(self):
        """Обновляет список игроков"""
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)
            
        players = Player.select().join(User).order_by(Player.name)
        
        for player in players:
            btn_frame = tk.Frame()
            tk.Button(
                btn_frame,
                text="Удалить",
                command=partial(self.delete_player, player.id),
                bg="#f44336",
                fg="white"
            ).pack(padx=5)
            
            self.players_tree.insert("", tk.END, values=(
                player.id,
                player.name,
                player.jersey_number,
                ""
            ))
            self.players_tree.window_create("", window=btn_frame)

    def delete_coach(self, coach_id):
        """Удаляет тренера"""
        try:
            with DB.atomic():
                # Удаляем из users
                User.delete().where(User.id == coach_id).execute()
                messagebox.showinfo("Успех", "Тренер успешно удален")
                self.update_coaches_list()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить тренера: {str(e)}")

    def delete_player(self, player_id):
        """Удаляет игрока"""
        try:
            with DB.atomic():
                # Получаем user_id игрока
                player = Player.get(Player.id == player_id)
                user_id = player.user.id
                
                # Удаляем из players
                Player.delete().where(Player.id == player_id).execute()
                # Удаляем из users
                User.delete().where(User.id == user_id).execute()
                
                messagebox.showinfo("Успех", "Игрок успешно удален")
                self.update_players_list()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить игрока: {str(e)}")