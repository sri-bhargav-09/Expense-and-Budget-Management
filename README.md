# Expense and Budget Manager

A Python-based command-line application for managing personal expenses and monthly budgets.

The application allows users to record, view, edit, and delete expenses, create and manage category-based budgets, track spending, and receive budget notifications.

## Features

### Expense Management

* Add new expenses
* View all expenses
* Edit existing expenses
* Delete expenses
* Validate expense names, categories, dates, and amounts
* Store expense data in MySQL

### Budget Management

* Add monthly budgets by category
* View all budgets
* View budgets by year
* View budgets by month
* View budgets by category
* Modify existing budgets
* Delete existing budgets
* Validate budget categories, months, years, and amounts
* Store budget data in MySQL

### Budget Tracking

* Automatically calculate spending for each budget category
* Display remaining budget
* Compare expenses against monthly budgets
* Generate notifications when spending reaches the configured threshold
* Alert when a budget is exceeded

### Database Management

* MySQL database used for persistent data storage
* Centralized database connection
* Parameterized SQL queries
* Transaction handling with commit and rollback
* Database constraints and application-level validation

## Project Structure

```text
Expense-and-Budget-Management/
│
├── main.py          # Main application and user interface
├── Expense.py       # Expense and ExpenseManager classes
├── Budget.py        # Budget and BudgetManager classes
├── database.py      # MySQL database connection
├── .gitignore       # Files and folders ignored by Git
└── README.md        # Project documentation
```

## Technologies Used

* Python
* MySQL
* mysql-connector-python
* Git
* GitHub

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sri-bhargav-09/Expense-and-Budget-Management.git
```

### 2. Navigate to the project directory

```bash
cd Expense-and-Budget-Management
```

### 3. Install the required Python package

```bash
pip install mysql-connector-python
```

### 4. Configure the database

Create a MySQL database named:

```text
Expense_and_Budget_Manager
```

Create the required `Expense` and `Budget` tables according to the project's database schema.

Update the MySQL connection settings in `database.py` and provide the password through the `MYSQL_PASSWORD` environment variable.

For example, in PowerShell:

```powershell
$env:MYSQL_PASSWORD="YOUR_MYSQL_PASSWORD"
```

### 5. Run the application

```bash
python main.py
```

## Data Storage

The application uses **MySQL** for persistent data storage.

Expense and budget information is stored in the MySQL database rather than local JSON files.

The application connects to the database through `database.py`, while `ExpenseManager` and `BudgetManager` perform the required database operations.

## Budget Notifications

The budget manager uses a configurable notification threshold.

When spending reaches or exceeds the configured threshold, the application displays a warning.

If spending exceeds the allocated budget, an alert is displayed.

## Project Status

**Completed**

The core expense management, budget management, MySQL persistence, budget tracking, notifications, input validation, transaction handling, and dataflow have been implemented and tested.

## Future Improvements

Possible improvements for future versions include:

* Improved command-line interface
* More detailed spending reports
* Expense search and filtering
* Graphs and visualizations
* Exporting reports
* Improved automated test coverage
* Additional database features

## Author

**G.Sri Bhargava**
