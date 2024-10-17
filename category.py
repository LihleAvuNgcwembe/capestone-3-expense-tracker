import sqlite3


class Category:

    def __init__(self, id, name, type, budget):
        self.id = id
        self.name = name
        self.type = type
        self.budget = budget

    def set_budget(self):
        try:
            user_input = float(input(f"Enter your budget {self.name}: "))

            self.budget = user_input

            with sqlite3.connect('Expense_tracker.db') as db:
                cursor = db.cursor()
                cursor.execute('''UPDATE categories
                               SET budget = ?
                               WHERE id = ?''',
                               (self.budget, self.id))

            print("New budget has been set!")
            input("Press 'Enter'")

        except (Exception, ValueError) as error:
            print(f"Error: {error}")
            print("Press 'Enter'")


# To generate the categories table if not exists
def create_categories_table():
    try:
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS categories(
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                type TEXT,
                budget DEFAULT 0.00)''')
            db.commit()

    except Exception as error:
        db.rollback()
        print(f"Error: {error}")
