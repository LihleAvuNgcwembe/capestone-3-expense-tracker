# Import Libraries
import os
import sys
import sqlite3
from category import Category, create_categories_table
from expense import Expense, create_expense_table
from income import Income, create_incomes_table
from datetime import datetime

# Change current directory to this current file
script_dr = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dr)

'''--------------------User Define functions section------------------------'''

'''------------Category functions---------------------'''


"""
The get_category_list():
It extracts data from categories table. Stores data in a
list as an instance of the Category class. Returns the list"""


def get_category_list():
    list = []
    try:

        # Get data from table called category
        with sqlite3.Connection('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''SELECT id, name, type, budget FROM categories''')

            # Insert data from cursor into a list as a Category object
            for row in cursor:
                list.append(Category(row[0], row[1], row[2], row[3]))

        return list
    except Exception as error:
        db.rollback()
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The update_budget_by_category():
Asks user to select a category. Then run the set_budget() to update the budget
values in the database"""


def update_budget_by_category(category_list):
    try:
        print("Choose Category:")
        for count, item in enumerate(category_list):
            print(f"{count + 1} - {item.name} - R{item.budget}")

        user_input = int(input("Enter number associated with category: "))

        selected_category = category_list[user_input - 1]

        selected_category.set_budget()

    except (Exception, ValueError, IndentationError) as error:
        print(f"Error: {error}")
        print("Press 'Enter' to return menu")


"""
The add_income_category():
Adds new income category to the expense tracker database.This function
prompts the user for the name of the new category, then inserts it into the
database."""


def add_income_category():
    try:
        # Get name of new category
        name = input("Enter name: ").lower()

        # insert current data into database
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO categories(name, type)
                           VALUES(?, ?)''', (name, 'income'))
            db.commit()
        print("New Gategory added successfully")

        input("Press 'ENTER' to return to menu")

    # catch sqlite3 errors
    except Exception as error:
        db.rollback()
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The delete_category():
Deletes category from the database"""


def delete_category(list_category):
    try:

        # Display available categories
        print("Please select the category you want to delete:")
        for count, item in enumerate(list_category):
            print(f"{count + 1} - {item.name}")

        # Prompt user to enter a number that matches index
        user_input = int(input(
            f"Enter a number between (1 - {len(list_category)}): "
            ))
        selected_category = list_category[user_input - 1]

        # Ask user for confirmation
        print(f"Do you want to delete {selected_category.name}")

        # Prompt user to enter number
        confirmation = int(input("1-Yes 2-No \nEnter Here: "))

        if confirmation == 1:

            # Delete selected category from  database
            with sqlite3.connect('Expense_tracker.db') as db:
                cursor = db.cursor()
                cursor.execute('''DELETE FROM categories
                               WHERE id = ? AND name = ?''',
                               (selected_category.id, selected_category.name))
            db.commit()
            print("Deletion sucessfull!")

        # Display message
        elif confirmation == 2:
            print("Deletion Canceled")

        # Dislpay Error message
        else:
            print("Error: invalid Index")

        input("Press 'ENTER' to return to menu")

    except (Exception, IndexError, ValueError) as error:
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The add_expense_category():
Adds a new expense category into the database. It prompts the user for the
name of category then inserts it into the database"""


def add_expense_category():
    try:
        # Get new of new category
        name = input("Enter name: ").lower()

        # insert current data into database
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO categories(name, type)
                           VALUES(?, ?)''', (name, 'expense'))
            db.commit()

        # Print message to User
        print("New category added!")
        input("Press 'ENTER' to return to menu")

    # catch sqlite3 errors
    except Exception as error:
        db.rollback()
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The check_budget():
Calculates the remaining budget amount based on the provided statements and
category."""


def check_budget(selected_category, list_of_statements):
    total = 0.0
    for item in list_of_statements:
        total += item.amount

    if total > selected_category.budget:
        print("You have exceeded the budget!")
    else:
        remaining_amount = selected_category.budget - total
        print(f"You have a remaining R{remaining_amount}")


"""
view_all_budget():
 Calculates the total expenses for each expense category."""


def view_all_budgets(category_list, total_amount_list):

    # Filter category with type expense
    expense_category_list = [item for item in category_list
                             if item.type == "expense"]

    # Create a dictionary to store all categories total
    category_total = {}

    # Calculate the total amounts for each category
    for item in total_amount_list:
        category = item.category
        amount = item.amount
        category_total.setdefault(category, 0)
        category_total[category] += amount

    # Display categories
    print("Current budget on each category")
    print("------------------------------------------------------------------")
    for count, item in enumerate(expense_category_list):

        print(f"{count + 1} - {item.name}")
        print("-----------------------------------------------")
        print(f"Budget - {item.budget}")

        # Check if key exist in dictionary
        if item.name in category_total.keys():
            print(f"Total - R{category_total[item.name]}\n")
        else:
            print("Total - R0.0\n")

    print("------------------------------------------------------------------")


'''------------Expense functions---------------------'''

"""add_expense():
Prompts the user to add a new expense to the expense tracker.This function
will prompt the user for a description of the expense. Filter the provided
category list to include only categories of type 'expense'. Prompt the
user to select a category from the filtered list. Prompt the user for the
expense amount.Get the current date and time. Insert the new expense record
into the 'expenses' table in the 'Expense_tracker.db' database."""


def add_expense(category_list):
    try:
        expense_category_list = []
        description = input("Provide description of the expense: ")

        # append all categories with the type expense into a new list
        for item in category_list:
            if item.type == 'expense':
                expense_category_list.append(item)

        # Ask the user to selexct an expense category
        print("Please select the following categories: ")
        for count, item in enumerate(expense_category_list):
            print(f"{count + 1} - {item.name}")

        # Prompt user for number related to avialable categors
        category_input = int(input("Enter the number next to the category: "))

        category = expense_category_list[category_input - 1]

        # Ask user for Cost
        amount = float(input("Enter amount: "))

        # Get Current date
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect('Expense_tracker.db') as db:
            cusror = db.cursor()
            cusror.execute('''INSERT INTO expenses
                           (description, category_id, amount, created_on)
                           VALUES (?, ?, ?, ?)''',
                           (description, category.id, amount, current_date))
        db.commit()

        print("New Expense added!")
        input("Press 'ENTER' to return to menu")

    except (Exception, ValueError, IndentationError) as error:
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""the get_expense_list():
Retrieves the list of expenses from the 'Expense_Tracker.db' database. This
function will.Initialize an empty list to store the expenses. Connect to the
'Expense_Tracker.db' database. Execute an SQL query to fetch the expense data,
including description, category name, amount, and created date. Store each
expense as an Expense object in the list. Return the list of expenses."""


def get_expense_list():
    try:
        # Declare an initialise an emoty list
        expense_list = []

        # Get expense data from the database
        with sqlite3.connect("Expense_Tracker.db") as db:
            cursor = db.cursor()
            cursor.execute('''SELECT
                        expenses.description, categories.name, expenses.amount,
                        expenses.created_on
                        FROM expenses
                        INNER JOIN categories
                        ON expenses.category_id = categories.id''')

            # Store all expenses in a list as an Expense object
            for row in cursor:
                expense_list.append(Expense(row[0], row[1], row[2], row[3]))

        return expense_list

    except Exception as error:
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The sort_expense():
Sorts and displays expenses for a selected category and checks if the budget
is exceeded.This function will filter the category list to include only
categories of type 'expense'. Prompt the user to select an expense category.
Retrieve and display expenses for the selected category.Calculate the total
expenses for the selected category. Check if the total expenses exceed the
budget for the selected category."""


def sort_expense(category_list, expense_list):
    sum_of_expense = 0.00
    if not category_list:
        print("category lists empty!")
        input("Press 'ENTER' to return to menu")
    else:
        try:
            expense_category = [item for item in category_list
                                if item.type == "expense"]

            # Ask user to select a category
            print("Select expense category:")
            for count, item in enumerate(expense_category):
                print(f"{count + 1} - {item.name}")

            # Prompts user to enter a number associated with the category
            user_input = int(input("Enter the number next to the category: "))

            # Store selected category in variable
            selected_category = expense_category[user_input - 1]

            # Store expenses with same category in a list:
            sorted_expense_list = [item for item in expense_list
                                   if item.category == selected_category.name]

            if not sorted_expense_list:
                print(f"Sorry '{selected_category.name}' is empty")
            else:
                # Display sorted list
                print("------------------------------------------------------")
                print(f"all expenses for {selected_category.name}")
                for item in sorted_expense_list:
                    print(f"{count+1} - {item.description} - R{item.amount}")
                    print(f"Date - {item.created_on}\n")
                    sum_of_expense += item.amount
                print("------------------------------------------------------")
                sum_of_expense = round(sum_of_expense)
                print(f"Current budget: R{selected_category.budget}")
                print(f"Total: R{sum_of_expense}")

                # Check if the budget was exceeded
                check_budget(selected_category, sorted_expense_list)

            input("Press enter to return to menu")

        except (ValueError, IndentationError) as error:
            print(f"Error: {error}")
            input("Press 'ENTER' to return to menu")


'''------------Income functions---------------------'''


"""
The get_income_list() function:
Extract records from incomes table
Store records into a list
Returns that list"""


def get_income_list():

    try:
        # Create a list to srore income data
        income_list = []

        # Get income data from database
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''SELECT
                           incomes.description,
                           categories.name,
                           incomes.amount,
                           incomes.created_on
                           FROM incomes
                           INNER JOIN categories
                           ON incomes.category_id = categories.id''')

            # Store income data into list
            for row in cursor:
                income_list.append(Income(row[0], row[1], row[2], row[3]))

        # Return list
        return income_list

    except (Exception) as error:
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The add_income() function:
Ask the user to enter a description, select a category from a list of
caregories provided by the argument, and enter an amount. The function also
generates a variable to store current date and time.then insert that data into
the incomes table as a new record"""


def add_income(category_list):

    try:
        # Prompts user to enter a short description
        description = input(
            "Enter a brief description of the income statement: "
            )

        # Filter category list and stores only type 'income'
        income_category_list = [item for item in category_list
                                if item.type == "income"]

        # Display categories of type stored in filterd list
        print("Select one of the income categories")
        for count, item in enumerate(income_category_list):
            print(f"{count + 1} - {item.name}")

        # Prompts user to eneter a number related to the category
        category = int(input(
            "Enter the number associated with the category: "
            ))

        # Store selected category details into a variable
        selected_category = income_category_list[category - 1]

        # Prompts user to enter an amount
        amount = float(input("Enter the amount earned: R"))

        # Generate current date and time then stores it in a variable
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Store all Data into the incomes table of the database
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO incomes
                           (description, category_id, amount, created_on)
                           VALUES(?, ?, ?, ?)''',
                           (description, selected_category.id,
                            amount, current_date))
            db.commit()

        # Display a message whenever a record is added successfully
        print("New record Added!")
        input("Press 'ENTER' to return to menu")

    except (Exception, ValueError, IndentationError) as error:
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The sort_income() function:
filters categories with type 'income' into a new list. Prompts user to select
category. Displays all records with the same category along with sum of all
amounts """


def sort_income(category_list, income_list):

    if not category_list:
        print("The category list is empty")
        input("Press 'ENTER' to return to menu")
    else:
        total_income = 0.0
        try:

            # filter category with type income into a list
            income_category_list = [item for item in category_list
                                    if item.type == 'income']

            # Ask the user to select category
            print("Select income category:")
            for count, item in enumerate(income_category_list):
                print(f"{count + 1} - {item.name}")

            # Prompt user to enter a number associated with category
            user_input = int(input(
                "Enter number associated with the category: "))

            # Store the selected category data into  a variable
            selected_category = income_category_list[user_input - 1]

            # filter all records in incomes with selected category
            sorted_income_list = [item for item in income_list
                                  if item.category == selected_category.name]

            # Validate if sorted list is empty
            if not sorted_income_list:
                print(f"There are no records in {selected_category.name}")

            else:
                # Display sorted list
                print("------------------------------------------------------")
                print(f"all income for {selected_category.name}")
                for item in sorted_income_list:
                    print(f"{count+1} - {item.description} - R{item.amount}")
                    print(f"Date - {item.created_on}\n")
                    total_income += item.amount
                print("------------------------------------------------------")
                total_income = round(total_income, 2)
                print(f"Current budget: R{selected_category.budget}")
                print(f"Total: R{total_income}")

            input("Press enter to return to menu")

        except (ValueError, IndentationError) as error:
            print(f"Error: {error}")
            input("Press 'ENTER' to return to menu")


"""
The create_goals_table():
Creates a table for storing financial goals in the SQLite database. Connects to
the SQLite database named 'Expense_tracker.db'. Create a table named 'goals'
if it does not already exist.The function will print a success message if the
table is created successfully or an error message if an exception occurs."""


def create_goals_table():
    try:

        # Create table if not exist
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY,
                description  TEXT,
                target_amount REAL,
                end_date TEXT)''')
            db.commit()
            print("Goals table created successfully.")

    except Exception as error:
        print(f"Error: {error}")


"""
The add_goal():
Prompts the user to enter details for a new financial goal and adds it to the
goals table in the SQLite database. This function will prompt the user for a
description of the goal. Prompt the user for the target amount to be saved for
the goal. Prompt the user for the end date by which the goal should be
achieved, in the format 'YYYY-MM-DD'. Parse and format the date input to a
SQLite-compatible string. Insert the goal details into the 'goals' table in
the 'Expense_tracker.db' database. Print a success message and prompt the user
to press 'ENTER' to return to the menu."""


def add_goal():
    try:
        # Prompt user for description
        description = input("Enter your goal: ")

        # Prompt user for amount
        amount = float(input("Enter target amount: "))

        # Prompt user for due date
        date = input("Enter end date int format(yyyy-mm-dd): ")

        # Parse user date input
        formated_date = datetime.strptime(date, "%Y-%m-%d")

        # Convert to SQLite compatible string
        sqlite_date_str = formated_date.strftime('%Y-%m-%d %H:%M:%S')

        # Insert given data into database
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''INSERT INTO goals
                           (description, target_amount, end_date)
                           VALUES (?, ?, ?)''',
                           (description, amount,  sqlite_date_str))
            db.commit()

        # Display message for successfull insertion
        print("New goal added!")
        input("Press 'ENTER' to return to menu")

    except (Exception, ValueError) as error:
        print(f"Error: {error}")
        input("Press 'ENTER' to return to menu")


"""
The get goasl():
Retrieves all financial goals from the 'goals' table in the SQLite database.
This function will, connect to the SQLite database named 'Expense_tracker.db'.
Execute a query to select the 'description', 'target_amount', and 'end_date'
for all records in the 'goals' table. Fetch all the results from the query and
store them in a list. Return the list of goals, where each goal is represented
as a tuple containing its description, target amount, and end date.
"""


def get_goals():
    try:

        # Select data from goals table
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''SELECT description, target_amount, end_date
                           FROM  goals''')

            # Store data into goals
            goals = cursor.fetchall()

        # return goals
        return goals

    except Exception as error:
        print(f"Error: {error}")
        input("Press 'ENTER'")


"""
The check_goals():
Checks the status of a financial goals based on current savings, incomes,
expenses, and displays an appropriate message. It Calculates the total income
from the provided income list. It Calculate the total expenses from the
provided expense list. It Determines the current savings by subtracting total
expenses from total income. It retrieves the goal description, target amount,
and end date from the provided goal. It Compares current savings with the
target amount and the current date with the goal's end date. It displays a
congratulatory message if the goal has been met within the end date. It
display a failure message if the goal has not been met and the end date has
passed. and finally displays the remaining amount needed to reach the goal if
it has not been met yet and the end date has not passed."""


def check_goals(goal, income_list, expense_list):
    total_expense = 0.0
    total_income = 0.0
    current_date = datetime.now()

    for item in income_list:
        total_income += item.amount

    for item in expense_list:
        total_expense += item.amount

    savings = total_income - total_expense

    description = goal[0]
    target_amount = float(goal[1])
    end_date = goal[2]

    end_date_formated = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    remainder = target_amount - savings

    print(f"Current savings: R{savings}")
    if savings >= target_amount and current_date <= end_date_formated:
        print(f"Congratulation! You have completed '{description}'")

    elif current_date > end_date_formated:
        print("End date has long since past")

    else:
        print(f"You are R{remainder} away from reaching your goal")


# Main menu for the application
def main(category_list, expense_list, income_list):
    total_expense = 0.00
    total_income = 0.00
    while True:
        try:
            menu_input = int(input('''Welcome Enter the following option:
1. Add expense
2. View expenses
3. View expenses by category
4. Add income
5. View incomes
6. View income by category
7. Create New Category
8. Set budget for a category
9. View budget by category
10. Set financial goals
11. View progress towards financial goals
12. Quit
Enter a number between (1 - 12): '''))

            if menu_input == 1:
                add_expense(category_list)
                expense_list = get_expense_list()

            elif menu_input == 2:

                # Check if expense list is empty
                if not expense_list:
                    print("Not expenses found in list!")
                    input("Press 'Enter' to return to menu")
                else:

                    # Display all expenses in list
                    print("--------------------------------------------------")
                    print("All expenses")
                    for count, item in enumerate(expense_list):
                        print(
                            f"{count+1} - {item.description} - R{item.amount}")
                        print(f"Date - {item.created_on}\n")
                        total_expense += item.amount
                    print("--------------------------------------------------")
                    total_expense = round(total_expense, 2)
                    print(f"Total: R{total_expense}")
                    input("Press 'Enter' to return to Menu")

            elif menu_input == 3:
                sort_expense(category_list, expense_list)

            elif menu_input == 4:
                add_income(category_list)
                income_list = get_income_list()

            elif menu_input == 5:

                # Check if income list is empty
                if not income_list:
                    print("No income detected!")
                    input("Press 'Enter' to return to menu")
                else:

                    # Display all income in list
                    print("--------------------------------------------------")
                    print("All income")
                    for count, item in enumerate(income_list):
                        print(
                            f"{count+1} - {item.description} - R{item.amount}")
                        print(f"Date - {item.created_on}\n")
                        total_income += item.amount
                    print("--------------------------------------------------")
                    total_income = round(total_income, 2)
                    print(f"Total: R{total_income}")
                    input("Press 'Enter' to return to Menu")

            elif menu_input == 6:
                sort_income(category_list, income_list)

            elif menu_input == 7:

                # Ask user to choose between which type
                print("Which type of category do you wish to create:")
                print("1 - Income \t2 - Expenses")

                # Prompt user to enter number of 1 or 2
                option = int(input("Enter a number between 1 or 2: "))

                # Create income category
                if option == 1:
                    add_income_category()

                # Create expense category
                elif option == 2:
                    add_expense_category()

                # Prints Error if user didn't enter 1 or 2
                else:
                    print("Error: Please choose a number between 1 or 2")

                # Update existing list
                category_list = get_category_list()

            elif menu_input == 8:
                update_budget_by_category(category_list)
                category_list = get_category_list

            elif menu_input == 9:
                view_all_budgets(category_list, expense_list)

            elif menu_input == 10:
                add_goal()

            elif menu_input == 11:
                goals = get_goals()

                print("Goals:")
                print("------------------------------------------------------")
                for goal in goals:
                    print(f"Goal: {goal[0]}")
                    print(f"Taget: R{goal[1]}")
                    print(f"End Date: {goal[2]}")
                    check_goals(goal, income_list, expense_list)
                    print("")
                print("------------------------------------------------------")
                input("Press 'Enter' to return to menu")

            elif menu_input == 12:
                print("Goodbye!!")
                break
            else:
                print("Error: You have entered a non-existing index!")
        except ValueError as error:
            print(f"Error: {error}")
            input("Press 'Enter' to return to menu")


'''-------------------------Main function starts----------------------------'''

# Check if database exist
db = 'Expense_Tracker.db'
if os.path.isfile(db):

    create_categories_table()
    create_incomes_table()
    create_expense_table()
    create_goals_table()

    # List to store categories
    category_list = get_category_list()
    expense_list = get_expense_list()
    income_list = get_income_list()

    main(category_list, expense_list, income_list)

# if database doesn't exist
else:
    print("Error: File 'Expense_Tracker.db' is not found!")
