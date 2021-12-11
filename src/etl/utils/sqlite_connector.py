import sqlite3

from utils.config import db_path


def connect_sqlite():
    return sqlite3.connect(db_path)
