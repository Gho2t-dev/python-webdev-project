import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS products(name, price, rating)")

print("============================================")
print("============Database Viewer v1.0============")
print("============================================")


while True:
    act = input("What would you like to do? (i: insert new, o: output all, q to quit): ").lower()

    if act == "i":
        name = input("insert new product name: ")

        while True:
            try:
                price = float(input("insert new product price: "))
            except ValueError:
                print("Invalid number. Please try again")
                continue
            break

        while True:
            try:
                rating = float(input("insert new product rating: "))
            except ValueError:
                print("Invalid number. Please try again")
                continue
            break
        prod = (name, price, rating)

        # print(data) # for debuging

        cur.execute("INSERT INTO products VALUES(?,?,?)", prod)
        con.commit()
        print(f"Added '{name}' successfully.")
        
    elif act == "o":
        for row in cur.execute("SELECT name, price, rating FROM products"):
            print(row)

    elif act == "q":
        break

print("Goodbye!")
con.close()