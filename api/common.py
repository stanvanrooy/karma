import sqlite3
import config as c
import logging
from flask import g


def get_db():
    if hasattr(g, '__db'):
        return g.__db

    config = c.get_config()
    g.__db = sqlite3.connect(config.database.path)
    _ensure_tables()
    return g.__db


def _ensure_tables():
    _ensure_alert_table()
    _ensure_note_table()


def _ensure_alert_table():
    db = get_db()
    db.execute("""CREATE TABLE if not exists alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        status TEXT, 
        labels TEXT, 
        annotations TEXT, 
        startsAt datetime, 
        endsAt datetime,
        generatorUrl TEXT
    )""")


def _ensure_note_table():
    db = get_db()
    db.execute("""CREATE TABLE if not exists notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        alertId INTEGER, 
        text TEXT, 
        createdAt datetime DEFAULT (datetime('now','localtime'))
    )""")

