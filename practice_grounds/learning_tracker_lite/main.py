# Database viewer/editor for an exercise database viewer/editor to train sql skills
# By Fabian H. created 26.06.2026

import sqlite3
import database

# create connection
con = sqlite3.connect('learning_tracker_lite.db')

# Initialize Database (check if it exists and create if not)
database.init_db(con)

# Function to output all entries nicely
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

# Space for more cool stuff (under construction)

# Welcome screen and basic input information for the user
print('========================================================')
print('======== Welcome to learning tracker lite v1.0 =========')
print('========================================================')

# Loop to keep the programm running as long as the user does not quit by input
while True:
    # initial ask for user input
    action = input('[a]dd a new entry, [e]dit an existing entry, [d]elete an entry, [s]how entries sorted by date and time, [q] to quit: ').lower()

    # Loop to check user input for validity
    valid_action = {'a', 'e', 'd', 's', 'q'}
    while action not in valid_action:
        print('Sorry your your input is not a valid action, please try again.')
        action = input('[a]dd a new entry, [e]dit an existing entry, [d]elete an entry, [s]how entries sorted by date and time, [q] to quit: ').lower()


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

        # Add entry and give feedback if it was succesfull
        new_input = (subject, key_learnings, notes, time_spent, difficulty)
        executed = database.add_entry(con, new_input)
        if executed > 0:
            print(f'Entry added succesfully! {executed} row(s) affected')
        else:
            print('Something went wrong :(')
        

    # Get neccesary user input for showing all existing entries
    if action == 's':
        show_entries()

    # Get neccesary user input for entry deletion
    if action == 'd':
        # show the user all entries first
        show_entries()
        # ask which entry should be deleted
        entry_id = input('Please enter the ID of the entry you would like to delete: ')
        # validate input
        result = database.check_id(con, entry_id)
        while result is None:
            entry_id = input('This entry already does not exist, please try again: ')
            result = database.check_id(con, entry_id)

        # Delete entry and give feedback if it was done succesfully
        executed = database.delete_entry(con, entry_id)
        if executed > 0:
            print(f'Entry deleted succesfully! {executed} row(s) affected')
        else:
            print('Something went wrong :(')

    # Get neccesary user input for entry editing
    if action == 'e':
        # display all entries
        show_entries()
        # ask user which entry user wants to edit (id)
        entry_id = input('Please enter the ID of the entry you would like to edit: ')
        # validate input
        result = database.check_id(con, entry_id)
        while result is None:
            entry_id = input('This entry does not exist, please try again: ')
            result = database.check_id(con, entry_id)
        # ask user what user wants to edit?
        try:
            edit_parameter = int(input('''Please input the coresponding number of what you would like to edit (1,2,3,4 or 5): 
                                    1. Subject
                                    2. Key learnings
                                    3. Notes
                                    4. Time spent
                                    5. Difficulty
                                    Enter Number: 
                                    '''))
        except ValueError:
            print('Please enter a number!')

        valid_inputs = {1, 2, 3, 4, 5}
        while True:
            if edit_parameter not in valid_inputs:
                try:
                    edit_parameter = int(input('''Invalid Input, please choose a number from the list: 
                                        1. Subject
                                        2. Key learnings
                                        3. Notes
                                        4. Time spent
                                        5. Difficulty
                                        Enter Number: '''))
                    
                except ValueError:
                    print('Please enter a number!')
            else:
                break

        if edit_parameter == 1:
            parameter = 'subject'
        elif edit_parameter == 2:
            parameter = 'key_learnings'
        elif edit_parameter == 3:
            parameter = 'notes'
        elif edit_parameter == 4:
            parameter = 'time_spent'
        elif edit_parameter == 5:
            parameter = 'difficulty'

        new_value = input(f'What should the new value for {parameter} be? ')

        # pass the change to database.py and print confirmation
        executed = database.edit_entry(con, entry_id, edit_parameter, new_value)
        if executed > 0:
            print(f'Entry edited succesfully! {executed} row(s) affected')
        else:
            print(f'Something went wrong :( {executed} rows affected')

    # Quit the programm
    if action == 'q':
        break

# Close connection
con.close()

# test