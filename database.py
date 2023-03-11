import sqlite3
import hashlib


# TODO turn selections into constants for clarity when referenced in other files
# users_db_file = "database/users.db"
# inventory_db_file = "database/inventory.db"

def init_db(selection):
    conn = sqlite3.connect(selection)

    if selection == "database/inventory.db":
        with open('database/inventory_schema.sql') as file:
            conn.executescript(file.read())

    elif selection == "database/users.db":
        print("Reached users init")
        with open('database/users_schema.sql') as file:
            conn.executescript(file.read())

    conn.commit()
    conn.close()


def get_db(selection):
    conn = sqlite3.connect(selection)
    conn.row_factory = sqlite3.Row
    return conn

def update_product(product_name, quantity):
    print('\n\nupdate product\n\n')

    
    product = []

    for item in query_db("database/inventory.db", "SELECT * FROM product WHERE name = ?;", [product_name]):
        product = item 

    query_db("database/inventory.db", "INSERT INTO update_history(id, date_changed, prev, changed) VALUES (?, ?, ?, ?)", [product['id'], '03-07-2023', product['quantity'], quantity])
    #c.execute("UPDATE product SET quantity = ? WHERE id = ?", [quantity, product['id']])

    return


# Returns a list of usernames in users.db
def list_users():
    conn = sqlite3.connect("database/users.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users;")
    result = [n[0] for n in c.fetchall()]
    conn.close()
    return result


def list_inventory():
    conn = sqlite3.connect("database/inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM product;")
    result = [n for n in c.fetchall()]
    conn.close()
    return result

def list_analytics():
    conn = sqlite3.connect("database/inventory.db")
    c = conn.cursor()
    c.execute("SELECT a.id, b.name, a.date_changed, a.prev, a.changed FROM update_history a, product b WHERE a.id = b.id;")
    result = [n for n in c.fetchall()]
    conn.close()
    return result


# executes a sql statement and returns the output
# from https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/
def query_db(selection, query, args=()):
    conn = get_db(selection)
    cur = conn.cursor().execute(query, args)
    result = cur.fetchall()

    conn.commit()
    cur.close()

    return result


def verify_password(username, password):
    _conn = sqlite3.connect("database/users.db")
    _c = _conn.cursor()

    _c.execute("SELECT password FROM users WHERE username = '" + username + "';")
    result = _c.fetchone()[0] == password

    _conn.close()

    return result
