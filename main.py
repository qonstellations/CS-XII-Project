'''

Expense Tracker made for Grade XII - CBSE Computer Science Project

'''

welcometxt = '''
# 🎉 Welcome to the Expense Tracker! 🎉

## 📊 Overview
The Expense Tracker is a simple and efficient tool designed to help you manage your personal finances.
You can easily track your expenses, categorize them, and review your spending habits over time.

## 🛠️ Features
- **User-Friendly Interface**: Navigate through the application with ease.
- **Categorization**: Organize your expenses into major categories:
  - Food & Dining
  - Transport
  - Housing & Utilities
  - Health & Fitness
  - Fun & Leisure
- **Custom Notes**: Add specific notes to each expense for better tracking.
- **Reports**: Generate monthly and yearly reports to analyze your spending patterns.
'''

loginmain = '''
# 🔐 Login Page

## Welcome to the Expense Tracker!

Please log in to your account or create a new account to get started.

---

### (1) **👤 Login with Existing User**
### (2) **🆕 Create a New User**
'''

hometxt = '''
# 💼 Welcome to the Expense Tracker

---

## 🏠 Home Page

### Choose an Option:
1. ➕ **Add a New Expense**
2. 📜 **View All Expenses**
3. 🔍 **Search for an Expense**
4. ❌ **Delete an Expense**
5. 📊 **Generate Expense Report**
6. 🚪 **Logout**

---
'''

categories = '''
# Pick a category of expense

### 1. 🍕 Food & Dining
### 2. 🚗 Transport
### 3. 🏠 Housing & Utilities
### 4. 🏋️ Health & Fitness
### 5. 🎉 Fun & Leisure
### 6. 🛠️ Others
'''

import csv
import os
import ast
import matplotlib.pyplot as plt

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from datetime import datetime

currentDate = datetime.now()
currentMMYY = currentDate.strftime("%m/%Y")
currentUser = None
currentData = {}
dataFile = "./data.csv"
recFile = "./records.csv"

defaultdata = {currentMMYY :
               {"total" : 0, 
                "food" : 0, "transport" : 0, "housing" : 0, 
                "health" : 0, "leisure" : 0, "other" : 0,
                "transacs" : []}
                }

months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5,
          "june": 6, "july": 7, "august": 8, "september": 9, "october": 10,
          "november": 11, "december": 12}


console = Console()

# Creating Required Files
if not os.path.exists(dataFile):
    with open(dataFile, "a", newline = "") as file:
        pass
if not os.path.exists(recFile):
    with open(recFile, "a", newline = "") as file:
        pass

# Clearing the Terminal
def cls():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For MacOS and Linux
        os.system('clear')

# Checking is user is registered
def isRegistered(username):
    with open(dataFile, "r", newline = "") as file:
        rdr = csv.reader(file)
        for row in rdr:
            if row[0] == username:
                return True
    return False

def formatDate(date):
    day, month, year = date.split("/")
    
    formatted_day = f"{int(day):02}"
    formatted_month = f"{int(month):02}"
    
    return f"{formatted_day}/{formatted_month}/{year}"

def saveDataToCSV():
    global currentUser, currentData
    rows = []
    user_found = False

    with open(recFile, "r", newline="") as file:
        rdr = csv.reader(file)
        for row in rdr:
            if row[0] == currentUser:
                rows.append([currentUser, currentData])
                user_found = True
            else:
                rows.append(row)

    if not user_found:
        rows.append([currentUser, currentData])

    with open(recFile, "w", newline="") as file:
        wtr = csv.writer(file)
        wtr.writerows(rows)

def addExpense():
    cls()
    global currentUser, currentData

    ddmmyy = formatDate(str(input("Enter date (eg - 25/05/2025 for 25 May 2025): ")))
    try:
        day, month, year = map(int, ddmmyy.split("/"))
    except (ValueError, IndexError):
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        addExpense()
        return

    if month < 1 or month > 12:
        console.print(Panel("Please enter a valid month (1-12)...", 
                            title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        addExpense()
        return
    
    mmyy = str(ddmmyy[3:])
    
    if mmyy not in currentData:
        currentData[mmyy] = {
            "total": 0, 
            "food": 0, 
            "transport": 0, 
            "housing": 0, 
            "health": 0, 
            "leisure": 0, 
            "other": 0,
            "transacs": []
        }

    cost = int(input("Enter amount spent : "))
    currentData[mmyy]["total"] += cost

    cls()
    console.print(Markdown(categories))
    cat = int(input("Enter category number : "))
    if cat < 1 or cat > 6:
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        addExpense()
        return

    category_key = ['food', 'transport', 'housing', 'health', 'leisure', 'other'][cat - 1]
    currentData[mmyy][category_key] += cost

    cls()
    note = str(input("Enter note for transaction (leave blank for empty) : "))
    newtransac = {"date": day, "amt" : cost, "category": category_key, "note": note if note != "" else None}

    currentData[mmyy]['transacs'].append(newtransac)
    saveDataToCSV()

    console.print(Panel("Expense added successfully!", title="Success!", style="bold green"))
    input("\nPress Enter to return to the homepage...")
    return


# Creating a new user account
def createAccount():
    cls()

    details = {"Username" : "", "Email" : "", "Phone Number" : 0, "Password" : ""}

    #Filling Values in dictionary from user input
    for key in details.keys():
        cls()
        try:
            if key == "Phone Number" : details[key] = int(input(f"\nEnter {key} : "))
            else : details[key] = str(input(f"\nEnter {key} : "))
        except ValueError:
            cls()
            console.print(Panel(f"Please Enter a valid 10 digit phone number...", 
                        title="Message!", style="bold red"))
            input("\nPress Enter to go back to login menu...")
            login()

    # Check Empty Fields 
    if details["Username"] == "" or details["Email"] == "" or details["Password"] == "":
        cls()
        console.print(Panel(f"Some fields are left blank, please try again!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        login()

    username = details["Username"]

    # Checking if the username already exists
    check = isRegistered(details["Username"])
    if check:
        console.print(Panel(f"User {username} already exists", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        login()

    # Confirm User Details
    final = Table(title="Expense Tracker", title_style="bold cyan")

    final.add_column("Details", style="bold green")
    final.add_column("Data Entered", style="yellow")

    for key in details.keys():
        final.add_row(str(key), str(details[key]))

    cls()
    console.print(Panel(f"Would you like to confirm account creation?", 
                        title="Message!", style="bold yellow"))
    console.print(final)
    res = input("\nRespond with (y) to confirm or (n) to cancel: ")
    if res.lower() != "y":
        login()

    # Register user details to backend
    with open(dataFile, "a+", newline = "") as file:
        wtr = csv.writer(file)
        wtr.writerow(details.values())
    
    with open(recFile, "a+", newline = "") as file:
        global defaultdata
        wtr = csv.writer(file)
        wtr.writerow([details["Username"], defaultdata])

    # Print Completion
    console.print(Panel(f"User {username} successfully registered!", 
                        title="Message!", style="bold green"))
    input("\nPress Enter to go back to login menu...")
    login()

# User Login
def login():
    cls()
    global currentUser, currentData

    console.print(Markdown(loginmain))

    try:
        res = int(input("\nEnter your input : "))
    except:
        cls()
        console.print(Panel(f"Please enter a valid input!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        login()

    if res == 1:
        pass
    elif res == 2:
        createAccount()
        login()
    else:
        console.print(Panel(f"Please enter a valid input!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        login()

    cls()

    try:
        username = str(input("\nPlease enter your username : "))
    except:
        cls()
        console.print(Panel(f"Please enter a valid input!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        login()

    # Checking if user is registered or not
    check = isRegistered(username)
    if check == False:
        console.print(Panel(f"User {username} is not registered!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        login()
    
    # Verifying login and redirecting to homepage
    cls()
    password = str(input(f"\nHey {username}, please enter your password : "))

    with open(dataFile, "r", newline = "") as file:
        rdr = csv.reader(file)
        for row in rdr:
            if row[0] == username and row[3] == password:
                currentUser = username
                console.print(Panel(f"User {username} successfully logged in!", 
                        title="Message!", style="bold green"))
                input("\nPress Enter to go to the homepage...")
                continue
            
            elif row[0] == username and row[3] != password:
                console.print(Panel(f"Incorrect password entered!", 
                        title="Message!", style="bold red"))
                input("\nPress Enter to back to the login page again...")
                login()
    
    with open(recFile, "r", newline = "") as file:
        rdr = csv.reader(file)
        for row in rdr:
            if row[0] == username:
                currentData = ast.literal_eval(row[1])
                break

def logout():
    global currentUser

    currentUser = None
    main()

# Homepage for the app
def home():
    cls()
    global currentUser

    console.print(Markdown(hometxt))

    res = int(input("\nEnter your input : "))

    if res == 1:
        addExpense()
    elif res == 6:
        logout()
    else:
        cls()
        console.print(Panel(f"Invalid Input Entered...(Only 1 and 6 working for now)", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to back to the home page again...")
        home()
    
# Parent Function of all Functions
def main():

    cls()
    console.print(Markdown(welcometxt))
    input("\nPress Enter to continue to the login page...")

    login()
    
    #Continue to homepage after login
    home()

main()