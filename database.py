import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')

    with open('res/schema.sql') as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn
