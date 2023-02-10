import database
from database import *
from flask import *

# this runs the inventory_schema.sql file and resets the table and database. Ideally we should only really run this once, but for testing purposes we are doing it every time
database.init_db("database/inventory.db")
database.init_db("database/users.db")

database.query_db("database/inventory.db", "INSERT INTO product (name, vendor, quantity) VALUES (?, ?, ?), (?, ?, ?);", ['Baguette', 'Panera Bread', 5, 'Kaiser Roll', 'West Side Bakery', 3])
database.query_db("database/users.db", "INSERT INTO users (username, password) VALUES (?, ?), (?, ?);", ['HBEACHUM', '1111', 'TEST_USER_2', 'password'])


# example of iterating each item from a query
for product in database.query_db("database/inventory.db", "SELECT * FROM product;"):
    print(f"{product['vendor']}\'s {product['name']}: {product['quantity']}")

# you can iterate each row as well
for row in database.query_db("database/inventory.db", "pragma table_info('product')"):
    for value in row:
        print(f'{value}\t', end='')
    print()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("Group5HomePage.html")


@app.route("/login")
def login():
    return render_template("Group5LoginPage.html")


@app.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    if request.method == "POST":
        if request.form.get('id').upper() in list_users():
            print("User found in database")
    return render_template("ResetPageGroup5.html")


@app.route("/inventory")
def inventory():
    return render_template("Group5InventoryPage.html")


if __name__ == "__main__":
    app.run(debug=True)
