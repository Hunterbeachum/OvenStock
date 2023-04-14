import base64
import datetime
import random
from io import BytesIO

from flask import *
from flask_mail import Mail, Message
from matplotlib.figure import Figure

import database
from database import *

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

# mail configuration (Hunter's Mailtrap)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '8b744c11e3845e'
app.config['MAIL_PASSWORD'] = 'da329f17fc0648'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_SUPPRESS_SEND'] = False
mail = Mail(app)

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
        new_user = request.form.get('new-user').upper()
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


@app.route("/inventory_sort<index>", methods=["GET", "POST"])
def sort_inventory(index):
    g.reverse = int(index)
    print(int(index), g.reverse)
    g.inventory = sorted(list_inventory(), key=lambda item: item[int(index)])
    print(g.inventory)
    return render_template("Group5InventoryPage.html")


# If you show the graph for each item, then click the sort button(s), the webpage goes blank.
# Otherwise, it works fine!

# @app.route("/analytics_sort<index>", methods=["GET", "POST"])
# def sort_analytics(index):
#    g.reverse = int(index)
#    print(int(index), g.reverse)
#    g.inventory = sorted(list_analytics(), key=lambda item: item[int(index)])
#    print(g.inventory)
#    return render_template("analytics.html")


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
        if int(quantity) == 0:
            msg = Message('Out of Inventory Alert', sender="8b744c11e3845e",
                          recipients=['846d7a87ef-c51084@inbox.mailtrap.io', 'hsbeachum@my.waketech.edu'])
            msg.html = f"<html><header style='color:black;font-weight:bold;'><b>Bakery Inventory System</b></header><p></p>" + \
                       "<body style='background-color:#DDD0C8;color:red;'>" + \
                       "You are out of inventory for an item with <u style='color:red'>ID = <b>" + str(
                item_id) + "</b></u></body></html>"
            print("Checkmark Reached!")
            mail.send(msg)
    return redirect(url_for('inventory'))


@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    if 'analytics' not in g:
        g.analytics = list_analytics()
    return render_template("analytics.html")


@app.route("/analytics/graph_<item_id>", methods=["GET"])
def create_analytics_graphic(item_id):
    if 'analytics' not in g:
        g.analytics = list_analytics()
    fig = Figure(figsize=(5, 4))
    ax = fig.subplots()
    ax.plot([1, 2])
    item_name = ''
    for item in list_analytics():
        if item[0] == int(item_id):
            item_name = item[1]
            break
    ax.set_title(item_name)
    ax.set_xlabel('date')
    ax.set_ylabel('stock')
    buf = BytesIO()
    fig.savefig(buf, format="png")
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
    return render_template("analytics.html", img_data=encoded)


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
