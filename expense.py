import sqlite3


class Expense:
    def __init__(self, description, category, amount, created_on):
        self.description = description
        self.category = category
        self.amount = amount
        self.created_on = created_on


# Check and generate an expense tables
def create_expense_table():
    try:
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY,
                description TEXT NOT NULL,
                category_id INTEGER,
                amount REAL,
                created_on TIMESTAMP,
                FOREIGN KEY(category_id) REFERENCES categories(id))''')
            db.commit()
    except Exception as error:
        db.rollback()
        print(f"Error: {error}")
