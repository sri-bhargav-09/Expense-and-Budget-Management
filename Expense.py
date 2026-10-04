import math
from datetime import date
import mysql.connector
from database import db, cursor

MAX_AMOUNT = 99_999_999.99  
MAX_TEXT_LEN = 50           

def validate_text(value, field="Value"):
    """Strip and validate a name/category. Raises ValueError with a user-friendly message."""
    if not isinstance(value, str):
        raise ValueError(f"{field} must be text.")
    value = value.strip()
    if not value:
        raise ValueError(f"{field} cannot be empty.")
    if len(value) > MAX_TEXT_LEN:
        raise ValueError(f"{field} cannot be longer than {MAX_TEXT_LEN} characters.")
    return value

def validate_amount(value):
    """Convert to a float rounded to 2 decimals. Must be finite, > 0 and <= MAX_AMOUNT."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")
    if not math.isfinite(amount):
        raise ValueError("Amount must be a valid number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")
    if amount > MAX_AMOUNT:
        raise ValueError(f"Amount cannot exceed {MAX_AMOUNT:,.2f}.")
    return round(amount, 2)

def validate_date(value):
    """Accept a date object only (not a datetime)."""
    if isinstance(value, date) and not hasattr(value, "hour"):
        return value
    raise ValueError("Invalid date.")

def _db_error_message(e, action):
    """Map a MySQL error to a user-friendly message."""
    if e.errno == 3819:
        return "Invalid amount."
    if e.errno == 1062:
        return "Expense already exists."
    if e.errno == 1406:
        return f"Name or category is too long (max {MAX_TEXT_LEN} characters)."
    if e.errno in (1264, 1366):
        return "Amount or value is out of range."
    return f"Unable to {action} expense."


class Expense:

    def __init__(self, Date: date, Category, name, Amount):
        self.Date = Date
        self.Category = Category
        self.Amount = Amount
        self.Name = name


class ExpenseManager:

    def addExpense(self, obj: Expense):
        try:
            name = validate_text(obj.Name, "Name")
            category = validate_text(obj.Category, "Category")
            amount = validate_amount(obj.Amount)
            expense_date = validate_date(obj.Date)
        except ValueError as e:
            return False, str(e)

        try:
            cursor.execute(
                "INSERT INTO Expense(name,category_name,amount,expense_date) "
                "VALUES(%s,%s,%s,%s)",
                (name, category, amount, expense_date),
            )
            db.commit()
            expense_id = cursor.lastrowid
            return True, f"Expense added successfully. Expense ID: {expense_id}"
        except mysql.connector.Error as e:
            db.rollback()
            return False, _db_error_message(e, "add")

    def viewExpense(self):
        try:
            cursor.execute(
                "SELECT expense_id, name, category_name, amount, expense_date "
                "FROM Expense ORDER BY expense_date, expense_id"
            )
            expenses = cursor.fetchall()
        except mysql.connector.Error:
            print("Unable to fetch expenses.")
            return

        if not expenses:
            print("No expenses found.")
            return

        print()
        print("=" * 85)
        print(
            f"{'ID':<6}{'Name':<22}{'Category':<20}"
            f"{'Amount':>12}{'Date':>15}"
        )
        print("-" * 85)
        for expense_id, name, category, amount, expense_date in expenses:
            print(
                f"{expense_id:<6}{name:<22}{category:<20}"
                f"{float(amount):>12.2f}{str(expense_date):>15}"
            )
        print("=" * 85)
        print()

    def deleteExpense(self, Expense_id):
        try:
            cursor.execute("DELETE FROM Expense WHERE expense_id=%s", (Expense_id,))
            if cursor.rowcount == 0:
                db.rollback()
                return False, f"Expense with id {Expense_id} does not exist."
            db.commit()
            return True, "Expense successfully deleted."
        except mysql.connector.Error:
            db.rollback()
            return False, "Unable to delete expense."

    def editExpense(self, expense_id, name=None, category=None, amount=None, new_date=None):
        updates = []
        values = []

        try:
            if name is not None:
                updates.append("name = %s")
                values.append(validate_text(name, "Name"))
            if category is not None:
                updates.append("category_name = %s")
                values.append(validate_text(category, "Category"))
            if amount is not None:
                updates.append("amount = %s")
                values.append(validate_amount(amount))
            if new_date is not None:
                updates.append("expense_date = %s")
                values.append(validate_date(new_date))
        except ValueError as e:
            return False, str(e)

        if not updates:
            return False, "No changes specified."

        values.append(expense_id)
        query = "UPDATE Expense SET " + ", ".join(updates) + " WHERE expense_id = %s"

        try:
            cursor.execute(query, tuple(values))
            if cursor.rowcount == 0:
                # Either the id does not exist, or the new values equal the old ones.
                cursor.execute("SELECT 1 FROM Expense WHERE expense_id = %s", (expense_id,))
                exists = cursor.fetchone() is not None
                db.rollback()
                if not exists:
                    return False, "Expense does not exist."
                return True, "No changes made (values are the same as before)."

            db.commit()
            return True, "Expense updated successfully."
        except mysql.connector.Error as e:
            db.rollback()
            return False, _db_error_message(e, "update")

    def getCategoryTotal(self, Category, month, year):
        """Total spent in a category for a month. Always returns a float."""
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        start_date = f"{year}-{month:02d}-01"
        end_date = f"{next_year}-{next_month:02d}-01"

        cursor.execute(
            "SELECT SUM(amount) FROM Expense "
            "WHERE category_name = %s "
            "AND expense_date >= %s "
            "AND expense_date < %s",
            (Category, start_date, end_date),
        )
        result = cursor.fetchone()
        if result is None or result[0] is None:
            return 0.0
        return float(result[0])