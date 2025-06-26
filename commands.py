from models import DB, User, ROLE_PLAYER, ROLE_COACH, ROLE_ADMIN
from peewee import DoesNotExist
from hashlib import sha256

def hash_password(password):
    """Хеширование пароля с использованием SHA-256"""
    return sha256(password.encode('utf-8')).hexdigest()

def register_user(username, email, password, role):
    """Регистрация нового пользователя с указанием роли"""
    try:
        with DB.atomic():
            # Проверка существования пользователя
            if User.select().where(User.username == username).exists():
                return False, "Пользователь с таким именем уже существует"
            
            # Проверка допустимости роли
            if role not in [ROLE_PLAYER, ROLE_COACH]:
                return False, "Неверно указана роль"
            
            # Создание нового пользователя
            User.create(
                username=username,
                password=hash_password(password),
                email=email,
                role=role
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

# Инициализация базы данных при импорте
if not DB.is_closed():
    DB.close()

DB.connect()
if not User.table_exists():
    from models import initialize_database
    initialize_database()