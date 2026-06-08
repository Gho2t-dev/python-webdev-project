import sqlite3

# 1. Connect to the database (If the file doesn't exist, Python will create it!)
connection = sqlite3.connect("my_app.db")

# 2. Create a cursor object (Think of this as your blinking cursor in a text editor)
cursor = connection.cursor()

# 3. Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL,
    stock INTEGER
)
""")

# 4. Insert data safely (Using ? placeholders to prevent SQL injection)
new_products = [
    ("Wireless Mouse", 29.99, 150),
    ("Mechanical Keyboard", 89.99, 45),
    ("USB-C Cable", 12.50, 300)
]

cursor.executemany("""
INSERT INTO products (name, price, stock) 
VALUES (?, ?, ?)
""", new_products)

# 5. COMMIT changes (Crucial! If you don't commit, your inserts won't save)
connection.commit()

# 6. Query and fetch the data
cursor.execute("SELECT name, price FROM products WHERE price > 20")
rows = cursor.fetchall()

print("--- Products over $20 ---")
for row in rows:
    # row is a tuple, e.g., ("Wireless Mouse", 29.99)
    print(f"Product: {row[0]} | Price: ${row[1]}")

# 7. Close the connection when done
connection.close()
