import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')

    with open('schema.sql') as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('database.db')
    

# executes a sql statement and returns the output
def exec_sql(statement):
    conn = get_db_connection()

    cur = conn.cursor()
    result = cur.execute(statement).fetchall()

    conn.commit()
    conn.close()

    return result
