import mysql.connector

from Expense import ExpenseManager, validate_text, validate_amount
from database import db

cursor = db.cursor()

MIN_YEAR = 2000
MAX_YEAR = 2100


# ---------- Validation helpers (also used by the main menu file) ----------

def validate_month(value):
    try:
        month = int(value)
    except (TypeError, ValueError):
        raise ValueError("Month must be a whole number.")
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")
    return month


def validate_year(value):
    try:
        year = int(value)
    except (TypeError, ValueError):
        raise ValueError("Year must be a whole number.")
    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ValueError(f"Year must be between {MIN_YEAR} and {MAX_YEAR}.")
    return year


def validate_budget(value):
    try:
        return validate_amount(value)
    except ValueError as e:
        raise ValueError(str(e).replace("Amount", "Budget"))


def _ask_int(prompt, low, high):
    """Ask for an int in [low, high]. Returns None (after a message) if invalid."""
    try:
        value = int(input(prompt).strip())
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return None
    if not low <= value <= high:
        print(f"Please enter a value between {low} and {high}.")
        return None
    return value


def _fetch(query, params=()):
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except mysql.connector.Error:
        print("Database error: unable to fetch budgets.")
        return None


# ---------- Models ----------

class Budget:
    def __init__(self, category, budget, month, year):
        self.month = month
        self.year = year
        self.Category = category
        self.Budget = budget


class BudgetManager:
    def __init__(self, expense_manager: ExpenseManager, threshold=80):
        self.expensemanager = expense_manager
        if 50 <= threshold <= 100:
            self.Threshold = threshold
        else:
            self.Threshold = 80

    def addBudget(self, obj: Budget):
        try:
            category = validate_text(obj.Category, "Category")
            month = validate_month(obj.month)
            year = validate_year(obj.year)
            amount = validate_budget(obj.Budget)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        query = """
            INSERT INTO Budget
            (category_name, month, year, budget_amount)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (category, month, year, amount))
            db.commit()
            print("Budget added successfully.")
            return True
        except mysql.connector.Error as e:
            db.rollback()
            if e.errno == 1062:
                print(
                    "A budget already exists for this category in this month and year. "
                    "Please use the Modify Budget option to change it."
                )
            elif e.errno == 3819:
                print("Invalid budget or month.")
            elif e.errno == 1406:
                print("Category is too long (max 50 characters).")
            elif e.errno in (1264, 1366):
                print("Budget value is out of range.")
            else:
                print("Unable to add budget.")
            return False

    def viewBudget(self):
        while True:
            print("==== Budget Menu ====")
            print("1. View all budgets")
            print("2. View by year")
            print("3. View by month")
            print("4. View by category")
            print("5. Exit")

            p = input("Enter your option: ").strip()

            if p == "1":
                rows = _fetch("""
                    SELECT category_name, month, year, budget_amount
                    FROM Budget
                    ORDER BY year, month, category_name
                """)
                self._show(rows, "No budgets found.")

            elif p == "2":
                year = _ask_int("Enter year: ", MIN_YEAR, MAX_YEAR)
                if year is None:
                    continue
                rows = _fetch("""
                    SELECT category_name, month, year, budget_amount
                    FROM Budget
                    WHERE year = %s
                    ORDER BY month, category_name
                """, (year,))
                self._show(rows, f"No budget found in year {year}")

            elif p == "3":
                year = _ask_int("Enter year: ", MIN_YEAR, MAX_YEAR)
                if year is None:
                    continue
                month = _ask_int("Enter month: ", 1, 12)
                if month is None:
                    continue
                rows = _fetch("""
                    SELECT category_name, month, year, budget_amount
                    FROM Budget
                    WHERE year = %s AND month = %s
                    ORDER BY category_name
                """, (year, month))
                self._show(rows, f"No budget found in month {month} of year {year}")

            elif p == "4":
                year = _ask_int("Enter year: ", MIN_YEAR, MAX_YEAR)
                if year is None:
                    continue
                month = _ask_int("Enter month: ", 1, 12)
                if month is None:
                    continue
                try:
                    category = validate_text(input("Enter category: "), "Category")
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
                rows = _fetch("""
                    SELECT category_name, month, year, budget_amount
                    FROM Budget
                    WHERE year = %s AND month = %s AND category_name = %s
                """, (year, month, category))
                self._show(
                    rows,
                    f"No budget found in month {month} of year {year} "
                    f"with category {category}",
                )

            elif p == "5":
                break

            else:
                print("Invalid input")

    def _show(self, rows, empty_message):
        if rows is None:          # database error already reported
            return
        if not rows:
            print(empty_message)
            return
        self.displayBudgets(rows)

    def displayBudgets(self, budgets):
        print()
        print("=" * 85)
        print("                              BUDGET REPORT")
        print("=" * 85)

        print(
            f"{'Category':<20}"
            f"{'Month':<10}"
            f"{'Year':<10}"
            f"{'Budget':>12}"
            f"{'Spent':>12}"
            f"{'Remaining':>15}"
        )
        print("-" * 85)

        for row in budgets:
            category = row[0]
            month = row[1]
            year = row[2]
            budget = float(row[3])

            try:
                spent = self.expensemanager.getCategoryTotal(category, month, year)
            except mysql.connector.Error:
                print(f"{category:<20}{month:<10}{year:<10}  (unable to read expenses)")
                continue

            remaining = budget - spent

            print(
                f"{category:<20}"
                f"{month:<10}"
                f"{year:<10}"
                f"{budget:>12.2f}"
                f"{spent:>12.2f}"
                f"{remaining:>15.2f}"
            )

        print("=" * 85)
        print()

    def modifyBudget(self, year, month, category, budget):
        try:
            category = validate_text(category, "Category")
            month = validate_month(month)
            year = validate_year(year)
            budget = validate_budget(budget)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        query = (
            "UPDATE Budget SET budget_amount=%s "
            "WHERE year=%s AND month=%s AND category_name=%s"
        )
        try:
            cursor.execute(query, (budget, year, month, category))

            if cursor.rowcount == 0:
                # Either the budget does not exist, or the new value equals the old one.
                cursor.execute(
                    "SELECT 1 FROM Budget WHERE year=%s AND month=%s AND category_name=%s",
                    (year, month, category),
                )
                exists = cursor.fetchone() is not None
                db.rollback()
                if not exists:
                    print("Error: Budget does not exist")
                    return False
                print("No changes made (budget is the same as before).")
                return True

            db.commit()
            print("Successfully modified the budget")
            return True
        except mysql.connector.Error as e:
            db.rollback()
            if e.errno in (1264, 1366):
                print("Budget value is out of range.")
            else:
                print("Unable to modify budget.")
            return False

    def deleteBudget(self, year, month, category):
        try:
            category = validate_text(category, "Category")
            month = validate_month(month)
            year = validate_year(year)
        except ValueError as e:
            print(f"Error: {e}")
            return False

        query = "DELETE FROM Budget WHERE year=%s AND month=%s AND category_name=%s"
        try:
            cursor.execute(query, (year, month, category))
            if cursor.rowcount == 0:
                db.rollback()
                print("Error: Budget does not exist")
                return False
            db.commit()
            print("Successfully deleted the budget")
            return True
        except mysql.connector.Error:
            db.rollback()
            print("Unable to delete budget.")
            return False

    def notifications(self):
        rows = _fetch("""
            SELECT category_name, month, year, budget_amount
            FROM Budget
            ORDER BY year, month, category_name
        """)
        if rows is None:
            return

        alerts = 0

        for row in rows:
            category = row[0]
            month = row[1]
            year = row[2]
            budget = float(row[3])

            try:
                spent = round(self.expensemanager.getCategoryTotal(category, month, year), 2)
            except mysql.connector.Error:
                print(f"Unable to check expenses for {category} ({month}/{year}).")
                continue

            remaining = budget - spent

            if spent > budget:
                alerts += 1
                print(
                    f"Alert: You have exceeded your {category} "
                    f"budget for {month}/{year}. "
                    f"You have spent Rs. {spent:.2f}, which is "
                    f"Rs. {abs(remaining):.2f} over your budget "
                    f"of Rs. {budget:.2f}."
                )

            elif budget > 0 and spent + 1e-9 >= budget * self.Threshold / 100:
                alerts += 1
                percentage = (spent * 100) / budget
                print(
                    f"Warning: You have used {percentage:.2f}% "
                    f"of your {category} budget for {month}/{year}. "
                    f"Only Rs. {remaining:.2f} remains."
                )

        if alerts == 0:
            print("No alerts. All your budgets are within limits.")