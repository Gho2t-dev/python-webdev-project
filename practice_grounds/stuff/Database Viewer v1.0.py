
# TODO 
# 

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
        print("======================================= Full Database contents ===========================================")
        for row in cur.execute("SELECT id, name, price, rating FROM products"):
            nr, name, price, rating = row
            print("|| Product ID: ", nr, "| Name: ", name, "| Price: ", price, "CHF. | Has a rating of: ", rating, " Points. ")
            print("__________________________________________________________________________________________________________")

    elif act == "d":
                
        try:
            remove = int(input("Type in the ID of the to be removed item: "))
        except ValueError:
            print("invalid ID, try again: ")
            continue

        cur.execute("DELETE FROM products WHERE id = ?", (remove,)) # Wert muss als tupple gegeben werden
        print(f"item with ID: {remove} sucessfully removed or it does not exist.")
        con.commit()

    elif act == "e":

        prod_id = int(input("Please enter the ID of the Product you would like to edit: "))
        cur.execute("SELECT id FROM products WHERE id = ?", (prod_id, ))
        result = cur.fetchone()

        while result is None:
            prod_id = int(input("Product not recognised, please enter the ID of the Product you would like to edit: "))
            cur.execute("SELECT id FROM products WHERE id = ?", (prod_id, ))
            result = cur.fetchone()

        while True:
            column = input("What would you like to edit? ((p)rice, (r)ating) ")
            if column == "p" or column == "r":
                break

        while True:    
            try:
                new_val = float(input("What would you like to put as the new value: "))
                break
            except ValueError:
                print("Invalid input.")

        if column == "p":
            cur.execute("UPDATE products SET price = ? WHERE id = ?", (new_val, prod_id))
            print("Success! Product has been updated succesfully.")
            con.commit()
        elif column == "r":
            cur.execute("UPDATE products SET rating = ? WHERE id = ?", (new_val, prod_id))
            print("Success! Product has been updated succesfully.")
            con.commit()
    elif act == "q":
            break
        
    con.commit()

print("Goodbye!")
con.close()