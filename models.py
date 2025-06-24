from peewee import *

DB = SqliteDatabase('sqlitedb.db')

class BaseModel(Model):
    class Meta:
        database = DB

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(null=True)
    role = CharField(default='user')

class Player(BaseModel):
    name = CharField()
    position = CharField()
    jersey_number = CharField()
    join_date = CharField()

class Training(BaseModel):
    coach_id = IntegerField()
    date = CharField()
    duration = CharField()
    focus_area = CharField()

class Match(BaseModel):
    opponent = CharField()
    date = CharField()
    location = CharField()
    score = CharField()  # Исправлено опечатку (было spore)

class PlayerStats(BaseModel):
    player = ForeignKeyField(Player, backref='stats')
    match = ForeignKeyField(Match, backref='player_stats')
    goals = IntegerField(default=0)
    assists = IntegerField(default=0)
    yellow_cards = IntegerField(default=0)
    red_cards = IntegerField(default=0)

if __name__ == "__main__":
    DB.connect()
    DB.create_tables([User, Player, Training, Match, PlayerStats], safe=True)
    
    # Создаем тестового администратора, если его нет
    if not User.select().where(User.username == 'admin').exists():
        User.create(
            username='admin',
            password='8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',  # sha256 hash of 'admin'
            role='admin',
            email='admin@example.com'
        )