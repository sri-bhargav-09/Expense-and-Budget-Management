
from Expense import Expense,ExpenseManager
from Budget import Budget,BudgetManager
from datetime import date

manager=ExpenseManager()
manager.load()
budgetmanager=BudgetManager(manager,75)
budgetmanager.loadBudget()

def printBudgetMenu():
    print("Select your choice from the menu :")
    print("======Budget Manager=====")
    print(" 1. Add Budget")
    print(" 2. View Budgets")
    print(" 3. Modify Budget")
    print(" 4. Delete Budget")
    print(" 5. Save Budgets")
    print(" 6. Notifications")
    print(" 7. Exit")

def printExpenseMenu():
        print("Select your choice from the menu :")
        print("======Expense and Budget Manager=====")
        print(" 1. Add Expense")
        print(" 2. View Expenses")
        print(" 3. Delete Expense")
        print(" 4. Edit Expense")
        print(" 5. Save Expenses")
        print(" 6. Exit")

def askToContinue():
    x=input("Do you want to continue(y/n)? ")
    if(x=="y"):
         return True
    else:
         return False
         
while True:
     print("====Expense and Budget manager===")
     print("1. Expense management")
     print("2. Budget management")
     print("3. Exit")

     try:
         opt=int(input("Enter your option(1,2,3): "))
     except ValueError:
         print("Invalid input. Please enter an integer.")
         continue

     #Expense management
     if opt==1:
          while(True):
            printExpenseMenu()

            try:
                a=int(input("Enter your choice(1,2,3,4,5,6): "))
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue

            if(a==6):
               break

            elif a==1:
               print("Enter details of the expense: ")
               while True:
                 try:
                   p=input("Enter date(YYYY-MM-DD) : ")
                   t=date.fromisoformat(p)
                   break
                 except ValueError:
                    print("Invaild date.Please enter a valid date in YYYY-MM-DD format")
               r=input("Enter Category of expense: ") 
               q=input("Enter name of the expense: ")
               while True:
                 try:
                   s=float(input("Enter amount: "))
                   break
                 except ValueError:
                   print("Invalid input. ")
               obj=Expense(t,r,q,s)
               manager.addExpense(obj)

            elif a==2:
               manager.viewExpense()

            elif a==3:
               manager.viewExpense()
               print("Enter details of expense to delete: ")
               x=input("Enter Category: ")
               while True:
                try:
                  y=int(input("Enter expense number in the category: "))
                  break
                except ValueError:
                  print("Invalid input. ")
               manager.deleteExpense(x,y)

            elif a==4:
               manager.viewExpense()
               print("Enter details of expense to edit: ")
               x=input("Enter Category: ")
               while True:
                 try:
                   y=int(input("Enter expense number in the category: "))
                   break
                 except ValueError:
                   print("Invalid input. ")
               manager.editExpense(x,y)

            elif a==5:
               manager.store() 

            else:
              print("Invalid input")

            if not askToContinue():
             break

     #Budget management
     elif opt==2:
        while True:
           printBudgetMenu()

           try:
               b=int(input("Enter you option(1,2,3,4,5,6,7): "))
           except ValueError:
               print("Invalid input. Please enter an integer.")
               continue

           if(b==1):
              print("Enter details of budget: \n")
              x=input("Enter category: ")
              while True:
                 try:
                    y=float(input("Enter budget: "))
                    break
                 except ValueError:
                    print("Invalid input")
              obj=Budget(x,y)
              budgetmanager.addBudget(obj)

           elif(b==2):
              budgetmanager.viewBudget()

           elif(b == 3):
             try:
               x = int(input("Enter year: "))

               if x not in budgetmanager.Budget:
                  print("Year doesn't exist")
                  continue

               y = int(input("Enter month: "))

               if y not in budgetmanager.Budget[x]:
                  print("Month doesn't exist")
                  continue

               z = int(input("Enter budget: "))

               if z <= 0:
                 print("Invalid budget")
                 continue

               cat = input("Enter category: ")

               if cat not in budgetmanager.Budget[x][y]:
                  print("Invalid category")
                  continue

               budgetmanager.modifyBudget(x, y, cat, z)

             except ValueError:
                print("Invalid input")

           elif(b == 4):
              try:
                x = int(input("Enter year: "))

                if x not in budgetmanager.Budget:
                  print("Year doesn't exist")
                  continue

                y = int(input("Enter month: "))

                if y not in budgetmanager.Budget[x]:
                    print("Month doesn't exist")
                    continue

                cat = input("Enter category: ")

                if cat not in budgetmanager.Budget[x][y]:
                    print("Invalid category")
                    continue

                budgetmanager.deleteBudget(x, y, cat)

              except ValueError:
                  print("Invalid input")

           elif(b==5):
               budgetmanager.storeBudget()

           elif(b==6):
               budgetmanager.notifications()

           elif(b==7):
              break

           else:
              print("Invalid input")

     elif opt==3:
        break

     else:
        print("Invalid option")

