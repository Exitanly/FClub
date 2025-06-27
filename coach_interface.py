import tkinter as tk
from tkinter import ttk, messagebox
from models import Training, User, DB, Match
from datetime import datetime
from functools import partial

class CoachInterface:
    def __init__(self, root, user_id):
        self.root = root
        self.coach = User.get(User.id == user_id)
        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.create_control_buttons()
        self.create_trainings_section()

    def create_control_buttons(self):
        """Создает кнопки управления тренировками и матчами"""
        control_frame = tk.Frame(self.frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            control_frame, 
            text="Управление тренировками", 
            command=self.show_trainings_management,
            bg="#4CAF50",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            control_frame,
            text="Управление матчами",
            command=self.show_matches_management,
            bg="#FF9800",
            fg="white",
            padx=10
        ).pack(side=tk.LEFT, padx=5)

    def show_trainings_management(self):
        """Показывает интерфейс управления тренировками"""
        # Очищаем текущий интерфейс
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.create_control_buttons()
        self.create_trainings_section()

    def show_matches_management(self):
        """Показывает интерфейс управления матчами"""
        # Очищаем текущий интерфейс
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.create_control_buttons()
        self.create_matches_section()

    def create_trainings_section(self):
        """Создает раздел управления тренировками"""
        trainings_frame = tk.LabelFrame(self.frame, text="Управление тренировками", padx=10, pady=10)
        trainings_frame.pack(fill=tk.BOTH, expand=True)

        # Кнопка добавления тренировки
        tk.Button(
            trainings_frame, 
            text="Добавить тренировку", 
            command=self.show_add_training_window,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5, anchor=tk.NE)

        # Таблица тренировок
        columns = ("id", "date", "duration", "focus_area", "coach")
        self.trainings_tree = ttk.Treeview(
            trainings_frame, 
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
        self.trainings_tree.column("focus_area", width=250)
        self.trainings_tree.column("coach", width=150)
        
        scrollbar = ttk.Scrollbar(trainings_frame, orient="vertical", command=self.trainings_tree.yview)
        self.trainings_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.trainings_tree.pack(fill=tk.BOTH, expand=True)
        
        self.update_trainings_list()

    def create_matches_section(self):
        """Создает раздел управления матчами"""
        matches_frame = tk.LabelFrame(self.frame, text="Управление матчами", padx=10, pady=10)
        matches_frame.pack(fill=tk.BOTH, expand=True)

        # Кнопка добавления матча
        tk.Button(
            matches_frame, 
            text="Добавить матч", 
            command=self.show_add_match_window,
            bg="#FF9800",
            fg="white"
        ).pack(pady=5, anchor=tk.NE)

        # Таблица матчей
        columns = ("id", "opponent", "date", "location", "score")
        self.matches_tree = ttk.Treeview(
            matches_frame, 
            columns=columns, 
            show="headings"
        )
        
        # Настройка колонок
        self.matches_tree.heading("id", text="ID")
        self.matches_tree.heading("opponent", text="Противник")
        self.matches_tree.heading("date", text="Дата")
        self.matches_tree.heading("location", text="Стадион")
        self.matches_tree.heading("score", text="Счет")
        
        self.matches_tree.column("id", width=50, anchor='center')
        self.matches_tree.column("opponent", width=150)
        self.matches_tree.column("date", width=100)
        self.matches_tree.column("location", width=150)
        self.matches_tree.column("score", width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(matches_frame, orient="vertical", command=self.matches_tree.yview)
        self.matches_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.matches_tree.pack(fill=tk.BOTH, expand=True)
        
        self.update_matches_list()

    def show_add_training_window(self):
        """Показывает окно добавления новой тренировки"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить тренировку")
        add_window.geometry("400x300")
        add_window.resizable(False, False)

        # Поля для ввода
        frame = tk.Frame(add_window, padx=10, pady=10)
        frame.pack(expand=True)

        # Дата тренировки
        tk.Label(frame, text="Дата тренировки:").grid(row=0, column=0, sticky="w", pady=5)
        self.training_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        tk.Entry(frame, textvariable=self.training_date_var).grid(row=0, column=1, sticky="ew", pady=5)

        # Длительность
        tk.Label(frame, text="Длительность (мин):").grid(row=1, column=0, sticky="w", pady=5)
        self.duration_var = tk.IntVar(value=90)
        tk.Entry(frame, textvariable=self.duration_var).grid(row=1, column=1, sticky="ew", pady=5)

        # Область внимания
        tk.Label(frame, text="Область внимания:").grid(row=2, column=0, sticky="w", pady=5)
        self.focus_area_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.focus_area_var).grid(row=2, column=1, sticky="ew", pady=5)

        # Кнопки
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        tk.Button(
            btn_frame, 
            text="Сохранить", 
            command=partial(self.save_training, add_window),
            bg="#2196F3",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, 
            text="Отмена", 
            command=add_window.destroy,
            bg="#f44336",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

    def show_add_match_window(self):
        """Показывает окно добавления нового матча"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить матч")
        add_window.geometry("400x300")
        add_window.resizable(False, False)

        # Поля для ввода
        frame = tk.Frame(add_window, padx=10, pady=10)
        frame.pack(expand=True)

        # Противник
        tk.Label(frame, text="Противник:").grid(row=0, column=0, sticky="w", pady=5)
        self.opponent_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.opponent_var).grid(row=0, column=1, sticky="ew", pady=5)

        # Дата матча
        tk.Label(frame, text="Дата матча:").grid(row=1, column=0, sticky="w", pady=5)
        self.match_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        tk.Entry(frame, textvariable=self.match_date_var).grid(row=1, column=1, sticky="ew", pady=5)

        # Стадион
        tk.Label(frame, text="Стадион:").grid(row=2, column=0, sticky="w", pady=5)
        self.location_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.location_var).grid(row=2, column=1, sticky="ew", pady=5)

        # Счет
        tk.Label(frame, text="Счет (необязательно):").grid(row=3, column=0, sticky="w", pady=5)
        self.score_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.score_var).grid(row=3, column=1, sticky="ew", pady=5)

        # Кнопки
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=4, columnspan=2, pady=10)

        tk.Button(
            btn_frame, 
            text="Сохранить", 
            command=partial(self.save_match, add_window),
            bg="#2196F3",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, 
            text="Отмена", 
            command=add_window.destroy,
            bg="#f44336",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

    def save_training(self, window):
        """Сохраняет новую тренировку в БД"""
        try:
            training_data = {
                'coach': self.coach,
                'date': datetime.strptime(self.training_date_var.get(), '%Y-%m-%d').date(),
                'duration': self.duration_var.get(),
                'focus_area': self.focus_area_var.get().strip()
            }

            # Валидация данных
            if not training_data['focus_area']:
                raise ValueError("Укажите область внимания")
            if training_data['duration'] <= 0:
                raise ValueError("Длительность должна быть положительным числом")

            with DB.atomic():
                Training.create(**training_data)
                messagebox.showinfo("Успех", "Тренировка успешно добавлена")
                window.destroy()
                self.update_trainings_list()

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить тренировку: {str(e)}")

    def save_match(self, window):
        """Сохраняет новый матч в БД"""
        try:
            match_data = {
                'opponent': self.opponent_var.get().strip(),
                'date': datetime.strptime(self.match_date_var.get(), '%Y-%m-%d').date(),
                'location': self.location_var.get().strip(),
                'score': self.score_var.get().strip() or None
            }

            # Валидация данных
            if not match_data['opponent']:
                raise ValueError("Укажите противника")
            if not match_data['location']:
                raise ValueError("Укажите стадион")

            with DB.atomic():
                Match.create(**match_data)
                messagebox.showinfo("Успех", "Матч успешно добавлен")
                window.destroy()
                self.update_matches_list()

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить матч: {str(e)}")

    def update_trainings_list(self):
        """Обновляет список тренировок в таблице"""
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

    def update_matches_list(self):
        """Обновляет список матчей в таблице"""
        for item in self.matches_tree.get_children():
            self.matches_tree.delete(item)
            
        matches = Match.select().order_by(Match.date.desc())
        
        for match in matches:
            self.matches_tree.insert("", tk.END, values=(
                match.id,
                match.opponent,
                match.date.strftime('%Y-%m-%d'),
                match.location,
                match.score if match.score else "-"
            ))