from datetime import date
import json
import os
class Expense:

    def __init__(self,Date:date,Category,name,Amount):
        self.Date=Date
        self.Category=Category
        self.Amount=Amount
        self.Name=name

class ExpenseManager:
    def __init__(self):
          self.expense={}

    def addExpense(self,obj:Expense):
                #Adding expense if category exists
                if obj.Category in self.expense:
                    a={"Date":obj.Date,"Name":obj.Name,"Amount":obj.Amount}
                    self.expense[obj.Category].append(a)
                    
                else:
                    #Creating new category and adding expense
                    self.expense[obj.Category]=[]
                    a={"Date":obj.Date,"Name":obj.Name,"Amount":obj.Amount}
                    self.expense[obj.Category].append(a)    

    def viewExpense(self):
         for category in self.expense:
              print("=====",category,"====\n")
              for i in range(len(self.expense[category])):
                    k=self.expense[category][i]
                    print((i+1),". ",k["Name"],"   Rs.",k["Amount"],"  ",k["Date"])
         
    def deleteExpense(self,Category,Expense_number):
                if Category in self.expense:
                    if 1<=Expense_number<=len(self.expense[Category]):
                      del self.expense[Category][Expense_number - 1]
                    else:
                        print("Expense does not exist")
                else:
                    print("Category not found")

    def editExpense(self,Category,Expense_number):
          if Category in self.expense:
                 if 1<=Expense_number<=len(self.expense[Category]):
                       print("What do you want to change?")
                       print("Enter (Date,Amount,Name) exactly to change date,amount,name ")
                       a=input()
                       if a=="Date":
                             while True:
                                try:
                                  k=input("Enter date(YYYY-MM-DD): ")
                                  x=date.fromisoformat(k)
                                  self.expense[Category][Expense_number-1]["Date"]=x
                                  break
                                except ValueError:
                                     print("Invalid date")
                       elif a=="Amount":
                             while True:
                                  try:
                                     k=float(input("Enter Amount: "))
                                     self.expense[Category][Expense_number-1]["Amount"]=k
                                     break
                                  except ValueError:
                                          print("Invalid input")
                       elif a=="Name":
                             k=input("Enter name of the expense: ")
                             self.expense[Category][Expense_number-1]["Name"]=k
                 else:
                       print("Expense number is invalid")  
          else:
                print("Category not found")
                                     
                
    def store(self):
                with open("Data.json","w") as file:
                  json.dump(self.expense,file,indent=4,default=str) # Chnages date into string to save in Json file

    def load(self):
         if os.path.exists("Data.json"):
              with open("Data.json","r") as file:
                 self.expense=json.load(file)
                 for category in self.expense:
                      for expense in self.expense[category]:
                           expense["Date"]=date.fromisoformat(expense["Date"])
         else:
              with open("Data.json","w") as file:
                   json.dump(self.expense,file,indent=4,default=str)

    def getCategoryTotal(self,Category,month,year):
         total=0  
         if Category in self.expense:
            for i in range(len(self.expense[Category])):
                  k=self.expense[Category][i]
                  if k["Date"].month==month and k["Date"].year==year:
                       total+=k["Amount"]
            if total==0:
                  print("There are no expenses in ",month," of ",year)           
         else:
            print("Category does not exist") 
         return total
              

#To convert every date key back to date format:

# for category in self.expense:
#     for expense in self.expense[category]:
#         expense["Date"] = date.fromisoformat(expense["Date"]) 
    


