from datetime import date

from Expense import (
    Expense,
    ExpenseManager,
    validate_text,
    validate_amount,
)
from Budget import (
    Budget,
    BudgetManager,
    validate_budget,
    MIN_YEAR,
    MAX_YEAR,
)
from database import db, cursor


# ---------- Menus ----------

def printMainMenu():
    print("====Expense and Budget manager===")
    print("1. Expense management")
    print("2. Budget management")
    print("3. Exit")


def printBudgetMenu():
    print("Select your choice from the menu :")
    print("======Budget Manager=====")
    print(" 1. Add Budget")
    print(" 2. View Budgets")
    print(" 3. Modify Budget")
    print(" 4. Delete Budget")
    print(" 5. Notifications")
    print(" 6. Exit")


def printExpenseMenu():
    print("Select your choice from the menu :")
    print("======Expense and Budget Manager=====")
    print(" 1. Add Expense")
    print(" 2. View Expenses")
    print(" 3. Delete Expense")
    print(" 4. Edit Expense")
    print(" 5. Exit")


# ---------- Input helpers ----------

def askToContinue():
    return input("Do you want to continue(y/n)? ").strip().lower() == "y"


def read_int(prompt, low=None, high=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue
        if (low is not None and value < low) or (high is not None and value > high):
            if low is not None and high is not None:
                print(f"Please enter a value between {low} and {high}.")
            elif low is not None:
                print(f"Please enter a value of at least {low}.")
            else:
                print(f"Please enter a value of at most {high}.")
            continue
        return value


def read_text(prompt, field, optional=False):
    while True:
        raw = input(prompt)
        if optional and raw.strip() == "":
            return None
        try:
            return validate_text(raw, field)
        except ValueError as e:
            print(e)


def read_number(prompt, validator, optional=False):
    while True:
        raw = input(prompt).strip()
        if optional and raw == "":
            return None
        try:
            return validator(raw)
        except ValueError as e:
            print(e)


def read_date(prompt, optional=False):
    while True:
        raw = input(prompt).strip()
        if optional and raw == "":
            return None
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Invalid date. Please enter a valid date in YYYY-MM-DD format.")


# ---------- Expense management ----------

def expense_menu(manager):
    while True:
        printExpenseMenu()
        a = read_int("Enter your choice(1,2,3,4,5): ", 1, 5)

        if a == 1:
            print("Enter details of the expense: ")
            t = read_date("Enter date(YYYY-MM-DD) : ")
            category = read_text("Enter Category of expense: ", "Category")
            name = read_text("Enter name of the expense: ", "Name")
            amount = read_number("Enter amount: ", validate_amount)
            success, message = manager.addExpense(Expense(t, category, name, amount))
            print(message)

        elif a == 2:
            manager.viewExpense()

        elif a == 3:
            manager.viewExpense()
            while True:
                raw = input("Enter the expense_id to delete (press Enter to cancel): ").strip()
                if raw == "":
                    break
                try:
                    expense_id = int(raw)
                except ValueError:
                    print("Invalid input. Please enter a valid expense Id.")
                    continue
                result, message = manager.deleteExpense(expense_id)
                print(message)
                if result:
                    break

        elif a == 4:
            manager.viewExpense()
            expense_id = read_int("Enter the expense_id of the expense to edit: ", 1)
            name = read_text("Enter new name (press Enter to keep current): ", "Name", optional=True)
            category = read_text("Enter new category (press Enter to keep current): ", "Category", optional=True)
            amount = read_number(
                "Enter new amount (press Enter to keep current): ", validate_amount, optional=True
            )
            new_date = read_date(
                "Enter new date (YYYY-MM-DD) (press Enter to keep current): ", optional=True
            )
            result, message = manager.editExpense(
                expense_id, name=name, category=category, amount=amount, new_date=new_date
            )
            print(message)

        elif a == 5:
            break

        if not askToContinue():
            break


# ---------- Budget management ----------

def budget_menu(budgetmanager):
    while True:
        printBudgetMenu()
        b = read_int("Enter your option(1,2,3,4,5,6): ", 1, 6)

        if b == 1:
            print("Enter details of budget: ")
            category = read_text("Enter category: ", "Category")
            year = read_int(f"Enter year ({MIN_YEAR}-{MAX_YEAR}): ", MIN_YEAR, MAX_YEAR)
            month = read_int("Enter month (1-12): ", 1, 12)
            amount = read_number("Enter budget: ", validate_budget)
            budgetmanager.addBudget(Budget(category, amount, month, year))

        elif b == 2:
            budgetmanager.viewBudget()

        elif b == 3:
            category = read_text("Enter category: ", "Category")
            year = read_int(f"Enter year ({MIN_YEAR}-{MAX_YEAR}): ", MIN_YEAR, MAX_YEAR)
            month = read_int("Enter month (1-12): ", 1, 12)
            amount = read_number("Enter new budget: ", validate_budget)
            budgetmanager.modifyBudget(year, month, category, amount)

        elif b == 4:
            category = read_text("Enter category: ", "Category")
            year = read_int(f"Enter year ({MIN_YEAR}-{MAX_YEAR}): ", MIN_YEAR, MAX_YEAR)
            month = read_int("Enter month (1-12): ", 1, 12)
            budgetmanager.deleteBudget(year, month, category)

        elif b == 5:
            budgetmanager.notifications()

        elif b == 6:
            break


# ---------- Entry point ----------

def main():
    manager = ExpenseManager()
    budgetmanager = BudgetManager(manager, 75)

    try:
        while True:
            printMainMenu()
            opt = read_int("Enter your option(1,2,3): ", 1, 3)

            if opt == 1:
                expense_menu(manager)
            elif opt == 2:
                budget_menu(budgetmanager)
            elif opt == 3:
                break
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
    finally:
        try:
            cursor.close()
            db.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()