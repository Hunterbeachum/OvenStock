import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')

    with open('schema.sql') as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
    

# executes a sql statement and returns the output
# from https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/
def query_db(query, args=()):
    conn = get_db()
    cur = conn.cursor().execute(query, args)
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return result
