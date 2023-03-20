import datetime
import random
import database
from database import *
from flask import *

# this runs the inventory_schema.sql file and resets the table and database. Ideally we should only really run this once, but for testing purposes we are doing it every time
database.init_db("database/inventory.db")
database.init_db("database/users.db")

database.query_db("database/users.db", "INSERT INTO users (username, password) VALUES (?, ?), (?, ?);",
                  ['HBEACHUM', '1111', 'TEST_USER_2', 'password'])

update_product('Kaiser Rolls', 20)
database.query_db("database/users.db", "INSERT INTO users (username, password) VALUES (?, ?), (?, ?);",
                  ['HBEACHUM', '1111', 'ADMIN', 'password'])

# example of iterating each item from a query
for product in database.query_db("database/inventory.db", "SELECT * FROM product;"):
    print(f"{product['vendor']}\'s {product['name']}: {product['quantity']}")

for log in database.query_db("database/inventory.db", "SELECT * FROM update_history;"):
    print(f"{log['id']} {log['date_changed']}, {log['prev']} {log['changed']}")

# you can iterate each row as well
for row in database.query_db("database/inventory.db", "pragma table_info('product')"):
    for value in row:
        print(f'{value}\t', end='')
    print()

app = Flask(__name__)
app.config.from_object('config')

# searching for all out-of-stock inventory
empty_items = []
for product in database.query_db("database/inventory.db", "SELECT * FROM product WHERE quantity = 0;"):
    empty_items.append(product)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_submitted = request.form.get('id').upper()
        # creating nested if statements to allow invalid password catching
        if id_submitted in list_users():
            if verify_password(id_submitted, request.form.get('pw')):
                session['current_user'] = id_submitted
            # else below should display "invalid password for username received" to the <p> element with ID ('login-message')
            else:
                login_error = "Invalid password for given username."
                flash(login_error, 'error')
        # elif below should display "invalid username" to the <p> element with the ID ('login-message')
        elif id_submitted not in list_users():
            login_error = "Username not found, try creating an account?"
            flash(login_error, 'error')

    return redirect("/")


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        new_user = request.form.get('new-user')
        if new_user in list_users():
            user_error = "Username is already in database."
            flash(user_error, 'error')
        else:
            new_pass = request.form.get('new-pass')
            new_email = request.form.get('new-email')
            # Add username, password, and email to database
            database.query_db("database/users.db", f"INSERT INTO users (username, password) VALUES(?, ?)",
                              [new_user, new_pass])
    return render_template("AddUserGroup5.html")


@app.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    if request.method == "POST":
        id_submitted = request.form.get('user').upper()
        if (id_submitted in list_users()) and verify_password(id_submitted, request.form.get('old_pw')):
            database.query_db("database/users.db",
                              f"UPDATE users SET password = '{request.form.get('new_pw')}' WHERE username = '{id_submitted}'")
    return render_template("ResetPageGroup5.html")


@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    if 'inventory' not in g:
        g.inventory = list_inventory()
    if request.method == "POST":
        inventory_addition = [request.form.get('name'), request.form.get('vendor'), request.form.get('quantity')]
        if None not in inventory_addition:
            database.query_db("database/inventory.db",
                              "INSERT INTO product (name, vendor, quantity) VALUES (?, ?, ?);", inventory_addition)
            return redirect(url_for('inventory'))
    return render_template("Group5InventoryPage.html")


@app.route("/inventory/delete_<item_id>", methods=["GET"])
def delete_item(item_id):
    if session.get("current_user", None) == 'ADMIN':
        database.query_db("database/inventory.db", f"DELETE FROM product WHERE id='{item_id}'")
    return redirect(url_for('inventory'))


@app.route("/inventory/transaction_<item_id>_<quantity>", methods=["GET"])
def transaction(item_id, quantity):
    if session.get("current_user", None) == 'ADMIN':
        inventory = list_inventory()
        id_list = [n[0] for n in list_inventory()]
        if item_id == 'example':
            item_id = random.choice(id_list)
            quantity = random.randint(0, 4)
        prev = inventory[id_list.index(item_id)][3]
        database.query_db("database/inventory.db", f"UPDATE product SET quantity='{quantity}' WHERE id='{item_id}'")
        database.query_db("database/inventory.db",
                          f"INSERT INTO update_history (id, date_changed, prev, changed) VALUES (?, ?, ?, ?);",
                          [item_id, datetime.datetime.now(), prev, quantity])
    return redirect(url_for('inventory'))


@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    if 'analytics' not in g:
        g.analytics = list_analytics()
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
