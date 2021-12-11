import sqlite3


def connect_sqlite():
    return sqlite3.connect('/code/db/tweets_db.db')
