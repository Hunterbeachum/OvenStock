import database

# this runs the schema.sql file and resets the table and database. Ideally we should only really run this once, but for testing purposes we are doing it every time
database.init_db()

database.query_db("INSERT INTO product (name, vendor, quantity) VALUES (?, ?, ?), (?, ?, ?);", ['Baguette','Panera Bread', 5, 'Kaiser Roll', 'West Side Bakery', 3])

# example of iterating each item from a query
for product in database.query_db("SELECT * FROM product;"):
    print(f"{product['vendor']}\'s {product['name']}: {product['quantity']}")

# you can iterate each row as well
for row in database.query_db("pragma table_info('product')"):
    for value in row:
        print(f'{value}\t', end='')
    print()
