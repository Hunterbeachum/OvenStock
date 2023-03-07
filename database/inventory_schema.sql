DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS update_history;

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

INSERT INTO product (name, vendor, quantity) VALUES 
    ('Kaiser Rolls', 'Pabera Bread', 40),
    ('Baguette', 'Pabera Bread', 50),
    ('Sourdough Roll', 'Chicago Bakery', 30),
    ('Rosemary Foccacia', 'Chicao Bakery', 26),
    ('Focaccia Dough', 'West Side Bakery', 20),
    ('Irish Soda Bread', 'West Side Bakery', 14),
    ('Pumpernickel', 'Tacoma Baking', 23),
    ('Marble Bread', 'Tacoma Baking', 28),
    ('Blueberry Muffin', 'Ricks Breakfeast Bread', 70),
    ('Banana Muffin', 'Ricks Breakfeast Bread', 63),
    ('Strawberry Muffin', 'Ricks Breakfeast Bread', 68),
    ('Apple Muffin', 'Ricks Breakfeast Bread', 62);

