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
    cur.execute("DELETE FROM entries WHERE id = ?", delete_id)
    rows_affected = cur.rowcount
    con.commit()
    return rows_affected

# display all entries to the user
def show_all(con):
    all_entries = []
    cur = con.cursor()
    for row in cur.execute("SELECT * FROM entries"):
        entry_id, subject, key_learnings, notes, time_spent, difficulty, timestamp = row
        all_entries.append(row)
    return all_entries

# check id validity
def check_id(con, entry_id):
    cur = con.cursor()
    cur.execute("SELECT id FROM entries WHERE id = ?", entry_id)
    result = cur.fetchone()
    return result
