from flask_login import UserMixin
from peewee import SqliteDatabase, IntegerField, CharField, TextField, \
    BigIntegerField, Model, AutoField, DateTimeField, ForeignKeyField

from server import manager

# SQLite database using WAL journal mode and 64MB cache.
sqlite_db = SqliteDatabase('app.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})

class Users(Model, UserMixin):
    id = AutoField()
    login = TextField(unique=True)
    password = TextField()
    magiclink = TextField()
    url_counter = IntegerField()
    is_enable = TextField()

    class Meta:
        database = sqlite_db
        

@manager.user_loader
def load_user(user_id):
    try:
        return Users.get(user_id)
    except Exception as identifier:
        print(identifier)

with sqlite_db:
    sqlite_db.create_tables([Users])