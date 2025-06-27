import tkinter as tk
from tkinter import ttk, messagebox
from models import Player, Match, PlayerStats, DB, Training, User
from datetime import datetime
from functools import partial

class PlayerInterface:
    def __init__(self, root, user_id):
        self.root = root
        self.user = User.get(User.id == user_id)
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        try:
            self.player = Player.get(Player.user == self.user)
            self.player_exists = True
        except Player.DoesNotExist:
            self.player = None
            self.player_exists = False
        
        self.create_player_info_section()
        self.create_stats_section()
        self.create_trainings_button()
        
    def create_trainings_button(self):
        """Создает кнопку для просмотра тренировок"""
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            btn_frame,
            text="Мои тренировки",
            command=self.show_trainings,
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5
        ).pack(pady=5, fill=tk.X)

    def show_trainings(self):
        """Показывает окно со списком всех тренировок"""
        trainings_window = tk.Toplevel(self.root)
        trainings_window.title("Список тренировок")
        trainings_window.geometry("900x600")
        
        # Основной фрейм
        main_frame = tk.Frame(trainings_window, padx=10, pady=10)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Таблица тренировок
        columns = ("id", "date", "duration", "focus_area", "coach")
        self.trainings_tree = ttk.Treeview(
            main_frame, 
            columns=columns, 
            show="headings"
        )
        
        # Настройка колонок
        self.trainings_tree.heading("id", text="ID")
        self.trainings_tree.heading("date", text="Дата")
        self.trainings_tree.heading("duration", text="Длительность (мин)")
        self.trainings_tree.heading("focus_area", text="Область внимания")
        self.trainings_tree.heading("coach", text="Тренер")
        
        self.trainings_tree.column("id", width=50, anchor='center')
        self.trainings_tree.column("date", width=100)
        self.trainings_tree.column("duration", width=120, anchor='center')
        self.trainings_tree.column("focus_area", width=300)
        self.trainings_tree.column("coach", width=150)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(
            main_frame, 
            orient="vertical", 
            command=self.trainings_tree.yview
        )
        self.trainings_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение элементов
        self.trainings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка закрытия
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            btn_frame,
            text="Закрыть",
            command=trainings_window.destroy,
            bg="#f44336",
            fg="white"
        ).pack(pady=5)
        
        # Загрузка данных
        self.update_trainings_list()

    def update_trainings_list(self):
        """Загружает список тренировок из БД"""
        for item in self.trainings_tree.get_children():
            self.trainings_tree.delete(item)
            
        trainings = (Training
                    .select(Training, User)
                    .join(User)
                    .order_by(Training.date.desc()))
        
        for training in trainings:
            self.trainings_tree.insert("", tk.END, values=(
                training.id,
                training.date.strftime('%Y-%m-%d'),
                training.duration,
                training.focus_area,
                training.coach.username
            ))

    def create_player_info_section(self):
        info_frame = tk.LabelFrame(self.frame, text="Информация об игроке", padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=5)
        
        # Поля для ввода
        self.name_var = tk.StringVar(value=self.player.name if self.player else "")
        self.position_var = tk.StringVar(value=self.player.position if self.player else "")
        self.jersey_var = tk.IntVar(value=self.player.jersey_number if self.player else 0)
        self.join_date_var = tk.StringVar(
            value=self.player.join_date.strftime('%Y-%m-%d') if self.player else datetime.now().strftime('%Y-%m-%d')
        )
        
        # Сетка для полей ввода
        tk.Label(info_frame, text="ФИО:").grid(row=0, column=0, sticky="w", pady=2)
        tk.Entry(info_frame, textvariable=self.name_var).grid(row=0, column=1, sticky="ew", pady=2, padx=5)
        
        tk.Label(info_frame, text="Позиция:").grid(row=1, column=0, sticky="w", pady=2)
        tk.Entry(info_frame, textvariable=self.position_var).grid(row=1, column=1, sticky="ew", pady=2, padx=5)
        
        tk.Label(info_frame, text="Игровой номер:").grid(row=2, column=0, sticky="w", pady=2)
        tk.Entry(info_frame, textvariable=self.jersey_var).grid(row=2, column=1, sticky="ew", pady=2, padx=5)
        
        tk.Label(info_frame, text="Дата присоединения:").grid(row=3, column=0, sticky="w", pady=2)
        tk.Entry(info_frame, textvariable=self.join_date_var, state='readonly').grid(row=3, column=1, sticky="ew", pady=2, padx=5)
        
        btn_text = "Обновить данные" if self.player_exists else "Сохранить данные"
        tk.Button(
            info_frame, 
            text=btn_text, 
            command=self.save_player_info,
            bg="#4CAF50",
            fg="white"
        ).grid(row=4, columnspan=2, pady=10, sticky="ew")

    def create_stats_section(self):
        stats_frame = tk.LabelFrame(self.frame, text="Статистика матчей", padx=10, pady=10)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Выбор матча
        match_frame = tk.Frame(stats_frame)
        match_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(match_frame, text="Матч:").pack(side=tk.LEFT)
        self.match_var = tk.StringVar()
        self.match_combobox = ttk.Combobox(match_frame, textvariable=self.match_var, state="readonly")
        self.match_combobox.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.update_matches_list()
        
        # Поля статистики
        stats_entry_frame = tk.Frame(stats_frame)
        stats_entry_frame.pack(fill=tk.X, pady=5)
        
        self.goals_var = tk.IntVar(value=0)
        self.assists_var = tk.IntVar(value=0)
        self.yellow_var = tk.IntVar(value=0)
        self.red_var = tk.IntVar(value=0)
        
        # Сетка для статистики
        tk.Label(stats_entry_frame, text="Голы:").grid(row=0, column=0, sticky="e", padx=2)
        tk.Entry(stats_entry_frame, textvariable=self.goals_var, width=3).grid(row=0, column=1, padx=2)
        
        tk.Label(stats_entry_frame, text="Передачи:").grid(row=0, column=2, sticky="e", padx=2)
        tk.Entry(stats_entry_frame, textvariable=self.assists_var, width=3).grid(row=0, column=3, padx=2)
        
        tk.Label(stats_entry_frame, text="Желтые:").grid(row=0, column=4, sticky="e", padx=2)
        tk.Entry(stats_entry_frame, textvariable=self.yellow_var, width=3).grid(row=0, column=5, padx=2)
        
        tk.Label(stats_entry_frame, text="Красные:").grid(row=0, column=6, sticky="e", padx=2)
        tk.Entry(stats_entry_frame, textvariable=self.red_var, width=3).grid(row=0, column=7, padx=2)
        
        tk.Button(
            stats_entry_frame, 
            text="Сохранить статистику", 
            command=self.save_player_stats,
            bg="#2196F3",
            fg="white"
        ).grid(row=1, columnspan=8, pady=10, sticky="ew")
        
        # Таблица статистики
        self.stats_tree = ttk.Treeview(stats_frame, columns=("match", "goals", "assists", "yellow", "red"), show="headings")
        
        # Настройка колонок
        self.stats_tree.heading("match", text="Матч")
        self.stats_tree.heading("goals", text="Голы")
        self.stats_tree.heading("assists", text="Передачи")
        self.stats_tree.heading("yellow", text="Желтые")
        self.stats_tree.heading("red", text="Красные")
        
        self.stats_tree.column("match", width=200)
        self.stats_tree.column("goals", width=50, anchor='center')
        self.stats_tree.column("assists", width=70, anchor='center')
        self.stats_tree.column("yellow", width=70, anchor='center')
        self.stats_tree.column("red", width=70, anchor='center')
        
        self.stats_tree.pack(fill=tk.BOTH, expand=True)
        self.update_stats_table()

    def update_matches_list(self):
        """Обновляет список матчей в выпадающем меню"""
        matches = Match.select().order_by(Match.date.desc())
        match_list = [f"{m.date.strftime('%Y-%m-%d')} - {m.opponent} ({m.location})" for m in matches]
        self.match_combobox['values'] = match_list
        if match_list:
            self.match_var.set(match_list[0])

    def update_stats_table(self):
        """Обновляет таблицу статистики"""
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
            
        if not self.player_exists:
            return
            
        stats = (PlayerStats
                .select(PlayerStats, Match)
                .join(Match)
                .where(PlayerStats.player == self.player)
                .order_by(Match.date.desc()))
        
        for stat in stats:
            match_info = f"{stat.match.date.strftime('%Y-%m-%d')} - {stat.match.opponent}"
            self.stats_tree.insert("", tk.END, values=(
                match_info,
                stat.goals,
                stat.assists,
                stat.yellow_cards,
                stat.red_cards
            ))

    def save_player_info(self):
        """Сохраняет информацию об игроке в БД"""
        try:
            data = {
                'user': self.user,
                'name': self.name_var.get().strip(),
                'position': self.position_var.get().strip(),
                'jersey_number': self.jersey_var.get(),
                'join_date': datetime.strptime(self.join_date_var.get(), '%Y-%m-%d').date()
            }
            
            # Валидация данных
            if not data['name']:
                raise ValueError("Не указано ФИО игрока")
            if not data['position']:
                raise ValueError("Не указана позиция игрока")
            if data['jersey_number'] < 0:
                raise ValueError("Номер игрока не может быть отрицательным")
            
            with DB.atomic() as transaction:
                if self.player_exists:
                    # Обновляем существующую запись
                    Player.update(**data).where(Player.id == self.player.id).execute()
                else:
                    # Создаем новую запись
                    self.player = Player.create(**data)
                    self.player_exists = True
                
                messagebox.showinfo("Успех", "Данные игрока успешно сохранены")
                self.update_stats_table()
                
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", str(ve))
        except Exception as e:
            messagebox.showerror("Ошибка базы данных", f"Не удалось сохранить данные: {str(e)}")
            import traceback
            traceback.print_exc()

    def save_player_stats(self):
        """Сохраняет статистику игрока для выбранного матча"""
        try:
            if not self.player_exists:
                messagebox.showerror("Ошибка", "Сначала сохраните информацию об игроке")
                return
                
            match_text = self.match_var.get()
            if not match_text:
                raise ValueError("Не выбран матч")
                
            # Парсим выбранный матч
            match_date_str, rest = match_text.split(" - ", 1)
            opponent = rest.split(" (")[0]
            match_date = datetime.strptime(match_date_str, '%Y-%m-%d').date()
            
            # Находим матч в БД
            match = Match.get(
                (Match.date == match_date) & 
                (Match.opponent == opponent))
            
            # Подготавливаем данные статистики
            stats_data = {
                'player': self.player,
                'match': match,
                'goals': self.goals_var.get(),
                'assists': self.assists_var.get(),
                'yellow_cards': self.yellow_var.get(),
                'red_cards': self.red_var.get()
            }
            
            # Валидация
            if any(value < 0 for value in [stats_data['goals'], stats_data['assists'], 
                  stats_data['yellow_cards'], stats_data['red_cards']]):
                raise ValueError("Значения статистики не могут быть отрицательными")
            
            with DB.atomic():
                PlayerStats.create(**stats_data)
                self.update_stats_table()
                self.clear_stats_fields()
                messagebox.showinfo("Успех", "Статистика успешно сохранена")
                
        except ValueError as ve:
            messagebox.showerror("Ошибка ввода", str(ve))
        except Match.DoesNotExist:
            messagebox.showerror("Ошибка", "Выбранный матч не найден в базе данных")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить статистику: {str(e)}")

    def clear_stats_fields(self):
        """Очищает поля ввода статистики"""
        self.goals_var.set(0)
        self.assists_var.set(0)
        self.yellow_var.set(0)
        self.red_var.set(0)