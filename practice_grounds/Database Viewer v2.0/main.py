# Database viewer/editor for an exercise database viewer/editor to train sql skills
# By Fabian H. created 26.06.2026

import sqlite3
import database

# create connection
con = sqlite3.connect('learning_tracker_lite.db')

# Initialize Database (check if it exists and create if not)
database.init_db(con)

# Space for more cool stuff (under construction)

# Welcome screen and basic input information for the user
print('========================================================')
print('======== Welcome to learning tracker lite v1.0==========')
print('========================================================')
action = input('[a]dd a new entry, [e]dit an existing entry, [d]elete an entry, [s]how entries sorted by subject: ')

# TEST:
new_input = ('programming', 'sql database commands', 'i love programming', '1.8', '7')
database.add_entry(con, new_input)

# Close connection
con.close()