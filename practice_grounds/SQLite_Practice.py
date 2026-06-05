import sqlite3
connection = sqlite3.connect("test.db")

cursor = connection.cursor()

cursor.execute("CREATE TABLE movie(title, year, score)")

cursor.exectute("""INSERT INTO movie VALUES
                 ("Star Wars: Episode V The Empire Strikes Back", 1980, 9.8),
                 ("Star Wars: Episode IV A New Hope", 1977, 9.6)
                """)
connection.commit()