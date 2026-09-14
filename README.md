# Expense and Budget Manager

A Python-based command-line application for managing personal expenses and monthly budgets.

The application allows users to record, view, edit, and delete expenses, create and manage category-based budgets, track spending, and receive budget notifications.

## Features

### Expense Management

* Add new expenses
* View expenses grouped by category
* Edit existing expenses
* Delete expenses
* Save expenses to a JSON file
* Load saved expenses when the application starts

### Budget Management

* Add monthly budgets by category
* View all budgets
* View budgets by year
* View budgets by month
* View budgets by category
* Modify existing budgets
* Delete budgets
* Save budgets to a JSON file
* Load saved budgets when the application starts

### Budget Tracking

* Automatically calculate spending for each budget category
* Display remaining budget
* Compare expenses against monthly budgets
* Generate notifications when spending reaches the configured threshold
* Alert when a budget is exceeded

## Project Structure

```text
Expense-and-Budget-Management/
│
├── main.py          # Main application and user interface
├── Expense.py       # Expense and ExpenseManager classes
├── Budget.py        # Budget and BudgetManager classes
├── Data.json        # Stored expense data
├── Budget.json      # Stored budget data
├── .gitignore       # Files and folders ignored by Git
└── README.md        # Project documentation
```

## Technologies Used

* Python
* JSON
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

### 3. Run the application

```bash
python main.py
```

## Data Storage

The application uses JSON files for persistent storage:

* `Data.json` stores expense information.
* `Budget.json` stores budget information.

The application loads the saved data when it starts and updates the files when the user chooses the corresponding save options.

## Budget Notifications

The budget manager uses a configurable notification threshold.

When spending reaches or exceeds the threshold, the application displays a warning. If spending exceeds the allocated budget, an alert is displayed.

## Project Status

**Completed**

The core expense management, budget management, persistence, budget tracking, notifications, input validation, and dataflow have been implemented and tested.

## Future Improvements

Possible improvements for future versions include:

* Improved command-line interface
* More detailed spending reports
* Expense search and filtering
* Graphs and visualizations
* Exporting reports
* Improved input handling
* Additional automated tests

## Author

**G.Sri Bhargava**
