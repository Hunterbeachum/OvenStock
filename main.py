import database

database.init_db()


print(database.exec_sql("INSERT INTO product (vendor, quantity) VALUES ('Panera Bread', 5);"))
print(database.exec_sql("SELECT * FROM product;"))
print(database.exec_sql("pragma table_info('product')"))
