# Database for an exercise database viewer/editor to train sql skills
# By Fabian H. created 26.06.2026

def init_db(con):
    # Create a cursor to the Database
    cur = con.cursor()
    # Create DB on first startup
    cur.execute("CREATE TABLE IF NOT EXISTS entries(" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "subject TEXT," \
    "key_learnings TEXT," \
    "notes TEXT," \
    "time_spent REAL," \
    "difficulty INTEGER," \
    "datetime TEXT DEFAULT (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'))" \
    ")")

# adds a new entry to the database
def add_entry(con, new_input):
    cur = con.cursor()
    cur.execute("INSERT INTO entries (subject, key_learnings, notes, time_spent, difficulty) VALUES (?,?,?,?,?)", new_input)
    rows_affected = cur.rowcount
    con.commit()
    return rows_affected

# Delete an entry from the database
def delete_entry(con, delete_id):
    cur = con.cursor()
    cur.execute("DELETE FROM entries WHERE id = ?", (delete_id, ))
    rows_affected = cur.rowcount
    con.commit()
    return rows_affected

# Edits a parameter of an entry
def edit_entry(con, edit_id, parameter_id, new_value):
    cur = con.cursor()

    if parameter_id == 1:
        cur.execute("UPDATE entries SET subject = ? WHERE id = ?", (new_value, edit_id))
    elif parameter_id == 2:
        cur.execute("UPDATE entries SET key_learnings = ? WHERE id = ?", (new_value, edit_id))
    elif parameter_id == 3:
        cur.execute("UPDATE entries SET notes = ? WHERE id = ?", (new_value, edit_id))
    elif parameter_id == 4:
        cur.execute("UPDATE entries SET time_spent = ? WHERE id = ?", (new_value, edit_id))
    elif parameter_id == 5:
        cur.execute("UPDATE entries SET difficulty = ? WHERE id = ?", (new_value, edit_id))

    rows_affected = cur.rowcount
    con.commit()
    return rows_affected

# Edit full entry
def edit_full_entry(con, edit_id, new_input):
    cur = con.cursor()
    cur.execute(
        "UPDATE entries SET subject = ?, key_learnings = ?, notes = ?, time_spent = ?, difficulty = ? WHERE id = ?",
        (new_input[0],
         new_input[1],
         new_input[2],
         new_input[3],
         new_input[4],
         edit_id)
         )
    con.commit()
    rows_affected = cur.rowcount
    return rows_affected

# display all entries to the user
def show_all(con):
    all_entries = []
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM entries ORDER BY id ASC"):
        all_entries.append(row)
    return all_entries

# check id validity
def check_id(con, entry_id):
    cur = con.cursor()
    cur.execute("SELECT id FROM entries WHERE id = ?", (entry_id, ))
    result = cur.fetchone()
    return result

# show entry chosen by ID
def show_entry(con, entry_id):
    cur = con.cursor()
    entry = cur.execute("SELECT * FROM entries WHERE id = ?", (entry_id, ))
    return entry