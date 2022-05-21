import sqlite3
import config as c
import logging
from flask import g


def get_db():
    if hasattr(g, '__db'):
        return g.__db

    config = c.get_config()

    g.__db = sqlite3.connect(config.database.path)
    try:
        g.__db.execute("""CREATE TABLE alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            status TEXT, 
            labels TEXT, 
            annotations TEXT, 
            startsAt datetime, 
            endsAt datetime,
            generatorUrl TEXT
        )""")
    except Exception as e:
        pass
    try:
        g.__db.execute("""CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            alertId INTEGER, 
            text TEXT, 
            createdAt datetime DEFAULT (datetime('now','localtime'))
        )""")
    except:
        pass
    return g.__db

