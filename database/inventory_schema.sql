DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS update_history;
DROP TABLE IF EXISTS vendor;

CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR2,
    vendor VARCHAR2,
    quantity INTEGER
);


CREATE TABLE update_history (
    id INTEGER REFERENCES product(id),
    date_changed DATE,
    prev INTEGER,
    changed INTEGER
);

CREATE TABLE vendor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR2,
    phone CHAR(32),
    address VARCHAR2,
    email VARCHAR2
);

INSERT INTO vendor (name, phone, address, email) VALUES
    ('Pabera Bread','555 123-4567', '321 Street Rd. Holly Springs, NC', 'pabera@bread.com'),
    ('Chicago Bakery','555 234-5678', '100 Chicago Rd. Witcheta, KS', 'chicago.bakery@mail.com'),
    ('West Side Bakery','555 345-6789', '52 West St. Tacoma, WA', 'west@side.com'),
    ('Tacoma Baking','555 819-1234', '8900 South Blvd. Chicago IL', 'contact@tacoma.com'),
    ('Ricks Breakfeast Bread','555 999-9990', 'Rocky Rd. Woonsocket RI', 'rick@breakfeast.com');


INSERT INTO product (name, vendor, quantity) VALUES 
    ('Kaiser Rolls', 'Pabera Bread', 40),
    ('Baguette', 'Pabera Bread', 50),
    ('Sourdough Roll', 'Chicago Bakery', 30),
    ('Rosemary Foccacia', 'Chicago Bakery', 0),
    ('Focaccia Dough', 'West Side Bakery', 0),
    ('Irish Soda Bread', 'West Side Bakery', 14),
    ('Pumpernickel', 'Tacoma Baking', 23),
    ('Marble Bread', 'Tacoma Baking', 28),
    ('Blueberry Muffin', 'Ricks Breakfeast Bread', 70),
    ('Banana Muffin', 'Ricks Breakfeast Bread', 63),
    ('Strawberry Muffin', 'Ricks Breakfeast Bread', 68),
    ('Apple Muffin', 'Ricks Breakfeast Bread', 62);

