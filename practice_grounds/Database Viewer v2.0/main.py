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


# Get neccesary input from user if user chooses to add a new entry
if action == 'a':
    subject = input('What subject were you working on today? ')
    key_learnings = input('What were some key learnings you gained today? ')
    notes = input('Here you can add some notes about what you did: ')  
    while True:  
        try:
            time_spent = float(input('How much time did you spend learning (in hours)? '))
            break
        except ValueError:
            print('Invalid input, please put in x.x format in hours. For example: 1.5')

    difficulty = 0
    while difficulty < 1 or difficulty > 10:
        try:
            difficulty = int(input('How difficult did you find what you worked on? (1-10) '))
            if difficulty < 1 or difficulty > 10:
                print('Please choose a valid number between 1-10')          
        except ValueError:
            print('Please choose a valid number between 1-10')


    # Add entry
    new_input = (subject, key_learnings, notes, time_spent, difficulty)
    database.add_entry(con, new_input)

# Close connection
con.close()