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
    "time_spend REAL," \
    "difficulty INTEGER," \
    "datetime TEXT DEFAULT (strftime('%Y-%m-%d %H:%M', 'now', 'localtime'))" \
    ")")