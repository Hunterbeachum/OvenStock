import database

database.init_db()

conn = database.get_db_connection()
cur = conn.cursor()

cur.execute("INSERT INTO product (vendor, quantity) VALUES ('Panera Bread', 5);")
print(cur.execute("SELECT * FROM product;").fetchall())

conn.commit()
conn.close()
