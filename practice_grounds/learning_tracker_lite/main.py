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

# Loop to keep the programm running as long as the user does not quit by input
while True:
    # initial ask for user input
    action = input('[a]dd a new entry, [e]dit an existing entry, [d]elete an entry, [s]how entries sorted by subject: ').lower()

    # Loop to check user input for validity
    valid_action = {'a', 'e', 'd', 's', 'q'}
    while action not in valid_action:
        print('Sorry your your input is not a valid action, please try again.')
        action = input('[a]dd a new entry, [e]dit an existing entry, [d]elete an entry, [s]how entries sorted by subject: ').lower()


    # Get neccesary input from user for new entry
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
        print(database.add_entry(con, new_input))

    # Get neccesary user input for entry editing
    if action == 'e':
        print('This functionality is WIP, thanks for your patience.')
        pass

    # Get neccesary user input for showing all existing entries
    if action == 's':
        def show_entries():
            all_entries = database.show_all(con)
            for entry in all_entries:
                print(f'''
                    | ID: {entry[0]} | 
                    | subject: {entry[1]} | 
                    | Your key learnings: {entry[2]} | 
                    | Your notes: {entry[3]} | 
                    | Time spent: {entry[4]} | 
                    | difficulty: {entry[5]} | 
                    | timestamp: {entry[6]} 
                    ''')
        show_entries()

    # Get neccesary user input for entry deletion
    if action == 'd':
        # show the user all entries first
        show_entries()
        # ask which entry should be deleted
        # validate input
        pass
        # Delete entry
        # delete_id = (entry_id, )
        # database.delete_entry(con, delete_id)

    # Quit the programm
    if action == 'q':
        break

# Close connection
con.close()