from models import DB, User
from peewee import DoesNotExist
import hashlib

def hash_password(password):
    """Хеширование пароля с использованием SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username, email, password):
    """Регистрация нового пользователя"""
    try:
        # Проверяем, существует ли пользователь с таким именем
        if User.select().where(User.username == username).exists():
            return False, "Пользователь с таким именем уже существует"
        
        # Создаем нового пользователя
        User.create(
            username=username,
            password=hash_password(password),
            email=email,
            role='user'
        )
        return True, "Регистрация прошла успешно!"
    except Exception as e:
        return False, f"Ошибка при регистрации: {str(e)}"

def authenticate_user(username, password):
    """Аутентификация пользователя"""
    try:
        user = User.get(User.username == username)
        if user.password == hash_password(password):
            return True, "Успешная авторизация", user.role
        return False, "Неверный пароль", None
    except DoesNotExist:
        return False, "Пользователь не найден", None
    except Exception as e:
        return False, f"Ошибка при авторизации: {str(e)}", None

def initialize_database():
    """Инициализация базы данных"""
    try:
        DB.connect()
        DB.create_tables([User], safe=True)
        
        # Создаем тестового администратора, если его нет
        if not User.select().where(User.username == 'admin').exists():
            User.create(
                username='admin',
                password=hash_password('admin123'),
                role='admin',
                email='admin@example.com'
            )
    except Exception as e:
        print(f"Ошибка при инициализации БД: {str(e)}")
    finally:
        if not DB.is_closed():
            DB.close()

# Инициализируем БД при импорте модуля
initialize_database()