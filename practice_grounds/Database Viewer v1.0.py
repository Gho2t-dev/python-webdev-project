
# TODO 
# Make code more robust

import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT, name, price, rating)")

print("=================================================================================================================")
print("============================================Database Viewer v1.0=================================================")
print("=================================================================================================================")


while True:   # Input loop
    act = input("What would you like to do? (i: insert new, e: to edit, o: output all, d: delete entry, q to quit): ").lower()
    if act not in ["i", "e", "o", "d", "q"]:
        print("not a valid action, try again.")
        continue
        
        
    elif act == "i":
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

        cur.execute("INSERT INTO products (name, price, rating) VALUES(?,?,?)", prod) # Bei auto inkrementing ID muss festgelegt werden WO die werte eingefügt werden.
        print(f"Added '{name}' successfully.")
            
    elif act == "o":
        for row in cur.execute("SELECT id, name, price, rating FROM products"):
            nr, name, price, rating = row
            print("__________________________________________________________________________________________________________")
            print("|| Product ID: ", nr, "| Name: ", name, "| Price: ", price, "CHF. |Has a rating of: ", rating, " Points. ")
            print("__________________________________________________________________________________________________________")

    elif act == "d":
                
        try:
            remove = int(input("Type in the ID of the to be removed item: "))
        except ValueError:
            print("invalid ID, try again: ")
            continue

        cur.execute("DELETE FROM products WHERE id = ?", (remove,)) # Wert muss als tupple gegeben werden
        print(f"item with ID: {remove} sucessfully removed or it does not exist.")

    elif act == "e":

        try:
            prod_id = int(input("Input the ID of the product you would like to edit: "))
        except ValueError:
            print("Invalid ID, please try again.")
            continue
        while True:
            column = input("What would you like to edit? ((p)rice, (r)ating) ")
            if column == "p" or "r":
                break
            
        try:
            new_val = float(input("What would you like to put as the new value: "))
        except ValueError:
            continue

        if column == "p":
            cur.execute("UPDATE products SET price = ? WHERE id = ?", (new_val, prod_id))
        elif column == "r":
            cur.execute("UPDATE products SET rating = ? WHERE id = ?", (new_val, prod_id))

    elif act == "q":
            break
        
    con.commit()

print("Goodbye!")
con.close()