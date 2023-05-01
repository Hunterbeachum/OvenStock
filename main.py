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
                  ['HBEACHUM', '1111', 'ADMIN', 'password'])

app = Flask(__name__)
app.config.from_object('config')

# mail configuration (Caleb's Mailtrap)
# app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = 'f20c99535509c0'
# app.config['MAIL_PASSWORD'] = '024ef22a1b0c03'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

# mail configuration (Hunter's Mailtrap)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '8b744c11e3845e'
app.config['MAIL_PASSWORD'] = 'da329f17fc0648'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_SUPPRESS_SEND'] = False

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
            success_message = "User created!"
            flash(success_message)
    return render_template("add_user.html")


@app.route("/password_reset", methods=["GET", "POST"])
def password_reset():
    if request.method == "POST":
        id_submitted = request.form.get('user').upper()
        if (id_submitted in list_users()) and verify_password(id_submitted, request.form.get('old_pw')):
            database.query_db("database/users.db",
                              f"UPDATE users SET password = '{request.form.get('new_pw')}' WHERE username = '{id_submitted}'")
    return render_template("password_reset.html")


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
    return render_template("inventory.html")


@app.route("/inventory_sort<index>", methods=["GET", "POST"])
def sort_inventory(index):
    g.inventory = sorted(list_inventory(), key=lambda item: item[int(index)])
    return render_template("inventory.html")


# If you show the graph for each item, then click the sort button(s), the webpage goes blank.
# Otherwise, it works fine!

# @app.route("/analytics_sort<index>", methods=["GET", "POST"])
# def sort_analytics(index):
#    g.inventory = sorted(list_analytics(), key=lambda item: item[int(index)])
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
        prev = inventory[id_list.index(int(item_id))][3]
        database.query_db("database/inventory.db", f"UPDATE product SET quantity='{quantity}' WHERE id='{item_id}'")
        database.query_db("database/inventory.db",
                          f"INSERT INTO update_history (id, date_changed, prev, changed) VALUES (?, ?, ?, ?);",
                          [item_id, datetime.datetime.now(), prev, quantity])
        if int(quantity) == 0:
            item_name = ''
            for item in list_analytics():
                if item[0] == int(item_id):
                    item_name = item[1]
                    break
            msg = Message('Out of Inventory Alert', sender="8b744c11e3845e",
                          recipients=['846d7a87ef-c51084@inbox.mailtrap.io', 'hsbeachum@my.waketech.edu'])
            msg.html = f"<html><header style='font-size:30px;color:black;font-weight:bold;text-align:center;'>" + \
                       "<b>Bakery Inventory System</b></header>" + \
                       "<p/><p/><p/><p/><body style='text-decoration-line:underline;text-align:center;background-color:#DDD0C8;'>" + \
                       "You are <b style='color:red'>out of inventory</b> for an item: " + \
                       f"<u style='color:red;'>{item_name}<b style='font-weight:bold'>" \
                       "<p/><p><a href='localhost:5000/inventory'>Click Here to see changes</p>" + \
                       "</b></u></body></html>"
            mail.send(msg)
            print("Checkmark Reached! Email has been sent!")
    return redirect(url_for('inventory'))


@app.route("/inventory/example_transaction", methods=["GET"])
def example_transaction():
    if session.get("current_user", None) == 'ADMIN':
        for n in range(100):
            inventory = list_inventory()
            id_list = [n[0] for n in inventory]
            item_id = random.choice(id_list)
            quantity = random.randint(1, 1000)
            prev = inventory[id_list.index(int(item_id))][3]
            database.query_db("database/inventory.db", f"UPDATE product SET quantity='{quantity}' WHERE id='{item_id}'")
            database.query_db("database/inventory.db",
                              f"INSERT INTO update_history (id, date_changed, prev, changed) VALUES (?, ?, ?, ?);",
                              [item_id, datetime.datetime.now(), prev, quantity])
    return redirect(url_for('inventory'))


@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    if 'analytics' not in g:
        g.analytics = list_analytics()
    return render_template("analytics.html", img_data=None)


@app.route("/analytics/graph_<item_id>", methods=["GET"])
def create_analytics_graphic(item_id):
    if 'analytics' not in g:
        g.analytics = list_analytics()
    fig = Figure(figsize=(5, 4))
    ax = fig.subplots()
    item_history, x, y = [], ['Start'], []
    k = 0
    for list_item in list_analytics():
        if list_item[0] == int(item_id):
            if k == 0:
                y.append(list_item[3])
                k += 1
            item_history.append(list_item)
            x.append(list_item[2])
            y.append(list_item[4])
    ax.plot(x, y)
    ax.set_xticklabels([date[0:10] for date in x])
    item_name = ''
    for item in list_analytics():
        if item[0] == int(item_id):
            item_name = item[1]
            break
    ax.set_title(item_name)
    ax.set_xlabel('date')
    ax.set_ylabel('stock')
    fig.autofmt_xdate(rotation=45)
    fig.subplots_adjust(bottom=0.25)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    encoded = base64.b64encode(buf.getvalue()).decode('utf-8')
    g.analytics = item_history
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
