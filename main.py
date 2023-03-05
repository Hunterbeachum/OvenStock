import database
from database import *
from flask import *

# this runs the inventory_schema.sql file and resets the table and database. Ideally we should only really run this
# once, but for testing purposes we are doing it every time
database.init_db("database/inventory.db")
database.init_db("database/users.db")

database.query_db("database/inventory.db", "INSERT INTO product (name, vendor, quantity) VALUES (?, ?, ?), (?, ?, ?);",
                  ['Baguette', 'Panera Bread', 5, 'Kaiser Roll', 'West Side Bakery', 3])
database.query_db("database/users.db", "INSERT INTO users (username, password) VALUES (?, ?), (?, ?);",
                  ['HBEACHUM', '1111', 'TEST_USER_2', 'password'])

# example of iterating each item from a query
for product in database.query_db("database/inventory.db", "SELECT * FROM product;"):
    print(f"{product['vendor']}\'s {product['name']}: {product['quantity']}")

# you can iterate each row as well
for row in database.query_db("database/inventory.db", "pragma table_info('product')"):
    for value in row:
        print(f'{value}\t', end='')
    print()

app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_submitted = request.form.get('id').upper()
        if (id_submitted in list_users()) and verify_password(id_submitted, request.form.get('pw')):
            session['current_user'] = id_submitted
            return redirect("/")
        elif id_submitted is "":
            return "Error, please submit a password"


@app.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    if request.method == "POST":
        id_submitted = request.form.get('id').upper()
        if (id_submitted in list_users()) and verify_password(id_submitted, request.form.get('old_pw')):
            database.query_db("database/users.db",
                              f"UPDATE users SET password = '{request.form.get('new_pw')}' WHERE username = '{id_submitted}'")
    return render_template("ResetPageGroup5.html")


@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    if 'inventory' not in g:
        g.inventory = list_inventory()
    return render_template("Group5InventoryPage.html")


@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    return render_template("analytics.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("current_user", None)
    return redirect("/")


@app.errorhandler(401)
def error_401(error):
    return render_template("error.html"), 401


@app.errorhandler(403)
def error_403(error):
    return render_template("error.html"), 403


@app.errorhandler(404)
def error_404(error):
    return render_template("error.html"), 404


@app.errorhandler(405)
def error_405(error):
    return render_template("error.html"), 405


@app.errorhandler(413)
def error_413(error):
    return render_template("error.html"), 413


if __name__ == "__main__":
    app.run(debug=True)
