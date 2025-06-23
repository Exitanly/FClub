from peewee import *

DB = SqliteDatabase('sqlitedb.db')


class Table(Model):

    class Meta:
        database = DB

class User(Table):
    id = IntegerField(unique=True)
    username = CharField
    password = CharField
    role = CharField

class Player(Table):
    id = IntegerField
    name = CharField
    position = CharField
    jersey_number = CharField
    join_date = CharField

class Training(Table):
    id = IntegerField
    coach_id = IntegerField
    date = CharField
    duration = CharField
    focus_area = CharField

class Match(Table):
    id = IntegerField
    opponent = CharField
    date = CharField
    location = CharField
    spore = CharField

class Player_stats(Table):
    id = IntegerField
    player_id = IntegerField
    match_id = CharField
    goals = CharField
    assists = CharField
    yellow_cards = CharField
    red_cards = CharField


if __name__ == "__main__":
    DB.connect()
    DB.create_tables(
        models=[
            User,
            Player,
            Training,
            Match,
            Player_stats
        ],
        safe=True
    )