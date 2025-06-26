from peewee import *
from datetime import datetime

DB = SqliteDatabase('sqlitedb.db')

# Константы для ролей
ROLE_PLAYER = 'player'
ROLE_COACH = 'coach'
ROLE_ADMIN = 'admin'

class BaseModel(Model):
    class Meta:
        database = DB

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(null=True)
    role = CharField(default=ROLE_PLAYER)

    class Meta:
        table_name = 'users'

class Player(BaseModel):
    id = AutoField()  # Автоматически увеличивающийся ID
    user = ForeignKeyField(User, unique=True)  # Связь 1:1 с пользователем
    name = CharField()
    position = CharField()
    jersey_number = IntegerField()
    join_date = DateField(default=datetime.now)  # Дата с автоматическим заполнением

    class Meta:
        table_name = 'players'

class Training(BaseModel):
    id = AutoField()
    coach = ForeignKeyField(User)
    date = DateField()
    duration = IntegerField()  # В минутах
    focus_area = CharField()
    notes = TextField(null=True)

    class Meta:
        table_name = 'trainings'

class Match(BaseModel):
    id = AutoField()
    opponent = CharField()
    date = DateField()
    location = CharField()
    score = CharField(null=True)
    notes = TextField(null=True)

    class Meta:
        table_name = 'matches'

class PlayerStats(BaseModel):
    id = AutoField()
    player = ForeignKeyField(Player, backref='stats')
    match = ForeignKeyField(Match, backref='player_stats')
    goals = IntegerField(default=0)
    assists = IntegerField(default=0)
    yellow_cards = IntegerField(default=0)
    red_cards = IntegerField(default=0)

    class Meta:
        table_name = 'player_stats'

def initialize_database():
    with DB:
        DB.create_tables([User, Player, Training, Match, PlayerStats])
        
        # Создаем тестового администратора
        if not User.select().where(User.username == 'admin').exists():
            from hashlib import sha256
            admin_pass = sha256('admin123'.encode()).hexdigest()
            admin = User.create(
                username='admin',
                password=admin_pass,
                role=ROLE_ADMIN,
                email='admin@club.com'
            )
            
            # Создаем связанную запись игрока для админа (пример)
            Player.create(
                user=admin,
                name="Администратор Системы",
                position="Не указана",
                jersey_number=0,
                join_date=datetime.now()
            )

if __name__ == "__main__":
    initialize_database()