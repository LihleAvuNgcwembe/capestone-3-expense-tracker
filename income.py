import sqlite3


class Income:
    def __init__(self, description, category, amount, created_on):
        self.description = description
        self.category = category
        self.amount = amount
        self.created_on = created_on


# Check and generate an incomes tables
def create_incomes_table():
    try:
        with sqlite3.connect('Expense_tracker.db') as db:
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS incomes(
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
