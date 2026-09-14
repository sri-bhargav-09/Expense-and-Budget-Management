import json
import os
import Expense
from datetime import datetime

class Budget:
    def __init__(self,category,budget):
        self.month=datetime.now().month
        self.year=datetime.now().year
        self.Category=category
        self.Budget=budget

class BudgetManager:
    def __init__(self,expense_manager:Expense.ExpenseManager,threshold=80):
        self.expensemanager=expense_manager
        self.Budget={}
        if(50<=threshold<=100):
            self.Threshold=threshold
        else:
             self.Threshold=80

    def addBudget(self,obj:Budget,):
        #Adding budget if Year exist:
        if obj.year in self.Budget:       #Checks year exists in Budget dictionary or not
            if obj.month in self.Budget[obj.year]:    #Checks month exists in budget or not
                    if obj.Category in self.Budget[obj.year][obj.month]:
                         print("Budget already exists for this category.Please use the Modify Budget option to change it.")
                    else:     
                         self.Budget[obj.year][obj.month][obj.Category]=obj.Budget    
            else:
                 #Adding month in the dictionary    
                 self.Budget[obj.year].update({obj.month:{obj.Category:obj.Budget}})
        else:
             #Adding year in the dictionary
             self.Budget.update({obj.year:{obj.month:{obj.Category:obj.Budget}}})

    def viewBudget(self):
         while True:
              print("====Budget Menu====")
              print("1. View all budgets")
              print("2. View by year")
              print("3. View by month")
              print("4. View by category")
              print("5. Exit")

              p=input("Enter your option: ")
              if p=="1":
                   for year in self.Budget:
                        print("====",year,"====")
                        for month in self.Budget[year]:
                             print("----",month,"----")
                             for category in self.Budget[year][month]:
                                  k=self.expensemanager.getCategoryTotal(category,month,year)
                                  a=self.Budget[year][month][category]
                                  print(category,"  Budget:",a,"  Spent:",k,"  Remaining:",a-k)

              elif p == "2":
               try:
                 x = int(input("Enter year: "))
 
                 if x not in self.Budget:
                    print("Year doesn't exist")
                    continue

                 print("====", x, "====")

                 for month in self.Budget[x]:
                    print("----", month, "----")
                    for category in self.Budget[x][month]:
                       k = self.expensemanager.getCategoryTotal(category, month, x)
                       a = self.Budget[x][month][category]
                       print(category, "  Budget:", a,"  Spent:", k,"  Remaining:", a-k)
               except ValueError:
                  print("Invalid year")

              elif p == "3":
               try:
                 x = int(input("Enter year: "))
                 if x not in self.Budget:
                   print("Year doesn't exist")
                   continue
                 y = int(input("Enter month: "))
                 if y not in self.Budget[x]:
                  print("Month doesn't exist")
                  continue
                 print("====", x, "====")
                 print("----", y, "----")
                 for category in self.Budget[x][y]:
                  k = self.expensemanager.getCategoryTotal(category, y, x)
                  a = self.Budget[x][y][category]
                  print(category, "  Budget:", a,"  Spent:", k,"  Remaining:", a-k)
               except ValueError:
                  print("Invalid input")

              elif p == "4":
               try:
                  x = int(input("Enter year: "))

                  if x not in self.Budget:
                    print("Year doesn't exist")
                    continue

                  y = int(input("Enter month: "))

                  if y not in self.Budget[x]:
                      print("Month doesn't exist")
                      continue

                  z = input("Enter category: ")

                  if z not in self.Budget[x][y]:
                     print("Invalid category")
                     continue
                  print("====", x, "====")
                  print("----", y, "----")
                  k = self.expensemanager.getCategoryTotal(z, y, x)
                  a = self.Budget[x][y][z]

                  print(z,"  Budget:", a,"  Spent:", k,"  Remaining:", a - k)
               except ValueError:
                  print("Invalid input")
                                  
              elif p=="5":
                   break

              else:
                      print("Invalid input")            
 
    def modifyBudget(self,year,month,category,budget):
         if year in self.Budget:
              if month in self.Budget[year]:
                   if category in self.Budget[year][month]:
                        self.Budget[year][month][category]=budget
                   else:
                        print("Category does not exist")
              else:
                    print("Month does not exist")
         else:
               print("Year does not exist")

    def deleteBudget(self,year,month,category):
          if year in self.Budget:
                if month in self.Budget[year]:
                     if category in self.Budget[year][month]:
                          del self.Budget[year][month][category]
                     else:
                           print("Category does not exist")
                else:
                               print("Month does not exist")
          else:
                 print("Year does not exist")  

    def storeBudget(self):
         with open("Budget.json","w") as file:
              json.dump(self.Budget,file,indent=4,default=str)

    def loadBudget(self):
         if os.path.exists("Budget.json"):
              with open("Budget.json","r") as file:
                   self.Budget=json.load(file)
                   newBudget = {}
                   for year in self.Budget:
                      newBudget[int(year)] = {}
                      for month in self.Budget[year]:
                        newBudget[int(year)][int(month)] = self.Budget[year][month]
              self.Budget = newBudget
         else:
              with open("Budget.json","w") as file:
                   json.dump(self.Budget,file,default=str)

    def notifications(self):
         for year in self.Budget:
              for month in self.Budget[year]:
                   for category in self.Budget[year][month]:
                        a=self.expensemanager.getCategoryTotal(category,month,year)
                        k=self.Budget[year][month][category]
                        if(a>k):
                            print(f"❌ Alert: You have exceeded your {category} budget for {month}/{year}. You have spent Rs. {a:.2f}, which is Rs. {a-k:.2f} over your budget of Rs. {k:.2f}.")
                        elif(a>=(float(k*self.Threshold)/100)):
                           x=float(((a*100)/k))
                           print(f"⚠️ Warning: You have used {x:.2f}% of your {category} budget for {month}/{year}. Only Rs. {k-a:.2f} remains.")