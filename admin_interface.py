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
        """Показывает список тренеров с кнопками удаления"""
        self.clear_interface()
        
        coaches_frame = tk.LabelFrame(self.frame, text="Список тренеров", padx=10, pady=10)
        coaches_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview
        tree = ttk.Treeview(coaches_frame, columns=("id", "username"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("username", text="Имя")
        
        tree.column("id", width=50, anchor='center')
        tree.column("username", width=200)

        # Отдельный фрейм для кнопок
        buttons_frame = tk.Frame(coaches_frame)
        buttons_frame.pack(fill=tk.X, pady=5)

        # Заполняем данными
        coaches = User.select().where(User.role == 'coach').order_by(User.username)
        for coach in coaches:
            tree.insert("", tk.END, values=(coach.id, coach.username))
            
            # Добавляем кнопку удаления в отдельный фрейм
            tk.Button(
                buttons_frame,
                text=f"Удалить {coach.username}",
                command=partial(self.delete_user, coach.id),
                bg="#f44336",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)

        tree.pack(fill=tk.BOTH, expand=True)

    def show_players_list(self):
        """Показывает список игроков с кнопками удаления"""
        self.clear_interface()
        
        players_frame = tk.LabelFrame(self.frame, text="Список игроков", padx=10, pady=10)
        players_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview
        tree = ttk.Treeview(players_frame, columns=("id", "name", "jersey"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("name", text="Имя")
        tree.heading("jersey", text="Номер")
        
        tree.column("id", width=50, anchor='center')
        tree.column("name", width=200)
        tree.column("jersey", width=80, anchor='center')

        # Отдельный фрейм для кнопок
        buttons_frame = tk.Frame(players_frame)
        buttons_frame.pack(fill=tk.X, pady=5)

        # Заполняем данными
        players = Player.select().join(User).order_by(Player.name)
        for player in players:
            tree.insert("", tk.END, values=(player.id, player.name, player.jersey_number))
            
            # Добавляем кнопку удаления в отдельный фрейм
            tk.Button(
                buttons_frame,
                text=f"Удалить {player.name}",
                command=partial(self.delete_player, player.id),
                bg="#f44336",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)

        tree.pack(fill=tk.BOTH, expand=True)

    def delete_user(self, user_id):
        """Удаляет пользователя (тренера)"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого тренера?"):
            try:
                with DB.atomic():
                    User.delete().where(User.id == user_id).execute()
                    messagebox.showinfo("Успех", "Тренер успешно удален")
                    self.show_coaches_list()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить тренера: {str(e)}")

    def delete_player(self, player_id):
        """Удаляет игрока и связанного пользователя"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого игрока?"):
            try:
                with DB.atomic():
                    player = Player.get(Player.id == player_id)
                    user_id = player.user.id
                    Player.delete().where(Player.id == player_id).execute()
                    User.delete().where(User.id == user_id).execute()
                    messagebox.showinfo("Успех", "Игрок успешно удален")
                    self.show_players_list()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить игрока: {str(e)}")

    def clear_interface(self):
        """Очищает текущий интерфейс"""
        for widget in self.frame.winfo_children()[1:]:  # Сохраняем только control_buttons
            widget.destroy()