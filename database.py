import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="REMOVED_PASSWORD",
    database="Expense_and_Budget_Manager"
)

cursor = db.cursor()