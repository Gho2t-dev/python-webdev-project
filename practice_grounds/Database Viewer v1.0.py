import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS products(name, price, rating)")

print("============================================")
print("============Database Viewer v1.0============")
print("============================================")


while True:
    act = input("What would you like to do? (i: insert new, o: output all, q to quit): ")

    data = []
    if act == "i":
        name = input("insert new product name: ")
        price = float(input("insert new product price: "))
        rating = float(input("insert new product rating: "))
        prod = (name, price, rating)
        data.append(prod)

        # print(data) # for debuging

        cur.executemany("INSERT INTO products VALUES(?,?,?)", data)

    elif act == "o":
        for row in cur.execute("SELECT name, price, rating FROM products"):
            print(row)

    con.commit()
    if act == "q":
        break

print("Goodbye!")
