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
### (3) **👋 Go back to Welcome Page**
'''

hometxt = '''
# 💼 Welcome to the Expense Tracker

---

## 🏠 Home Page

### Choose an Option:
1. ➕ **Add a New Expense**
2. 📜 **View All Expenses**
3. 🔍 **Search for an Expense (Using note or date)**
4. ❌ **Delete an Expense**
5. 📊 **Generate Expense Report**
6. 🚪 **Logout**

---
'''

searchtext = '''
# Please select search type -

**(1) Search by date 📅**

**(2) Search by note 📝**

**(3) Go back to Home Page 🏠**

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
from rich.progress import track
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

monthMap = {1: "January", 2: "February", 3: "March", 4: "April", 
          5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 
          10: "October", 11: "November", 12: "December"}

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

# Welcome Page
def welcome():
    cls()
    console.print(Markdown(welcometxt))
    input("\nPress Enter to continue to the login page...")
    login()

# Checking is user is registered
def isRegistered(username):
    with open(dataFile, "r", newline = "") as file:
        rdr = csv.reader(file)
        for row in rdr:
            if row[0] == username:
                return True
    return False

# Formats date to required format for storage
def formatDate(date):
    day, month, year = date.split("/")
    
    formatted_day = f"{int(day):02}"
    formatted_month = f"{int(month):02}"
    
    return f"{formatted_day}/{formatted_month}/{year}"

# Formats the category type from raw storage type to something fancier
def formatCategory(cat):
    if cat == "food":
        return "🍕 Food & Dining"
    elif cat == "transport":
        return "🚗 Transport"
    elif cat == "housing":
        return "🏠 Housing & Utilities"
    elif cat == "health":
        return "🏋️ Health & Fitness"
    elif cat == "leisure":
        return "🎉 Fun & Leisure"
    else:
        return "🛠️ Others"

# Saves data to CSV file
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

# Add a new expense
def addExpense():
    cls()
    global currentUser, currentData, monthMap

    try:
        ddmmyy = formatDate(str(input("Enter date (eg - 25/05/2025 for 25 May 2025): ")))
        day, month, year = map(int, ddmmyy.split("/"))
    except (ValueError, IndexError):
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return addExpense()

    if month < 1 or month > 12:
        console.print(Panel("Please enter a valid month (1-12)...", 
                            title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return addExpense()
    
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
    try:
        cat = int(input("Enter category number : "))
        if cat < 1 or cat > 6:
            console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
            input("\nPress Enter to try again...")
            return addExpense()
    except:
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return addExpense()

    category_key = ['food', 'transport', 'housing', 'health', 'leisure', 'other'][cat - 1]
    currentData[mmyy][category_key] += cost

    cls()
    note = str(input("Enter note for transaction (leave blank for empty) : "))
    newtransac = {"date": day, "amt" : cost, "category": category_key, "note": note if note != "" else None}

    currentData[mmyy]['transacs'].append(newtransac)
    saveDataToCSV()

    console.print(Panel("Expense added successfully!", title="Success!", style="bold green"))
    input("\nPress Enter to return to the homepage...")
    return home()

# View Expenses
def viewExpense():
    cls()
    global currentUser, currentData

    try:
        mmyy = formatDate("00/"+str(input("Enter month to view expenses for (eg - 05/2025 for May 2025) : ")))[3:]
        month, year = map(int, mmyy.split("/"))
    except (ValueError, IndexError):
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return viewExpense()

    if month < 1 or month > 12:
        console.print(Panel("Please enter a valid month (1-12)...", 
                            title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return viewExpense()
    
    if mmyy not in currentData:
        console.print(Panel("Records for this month do not exist!", title="Message!", style="bold red"))
        input("\nPress Enter to go to home page...")
        return home()
    
    currentTransacs = currentData[mmyy]["transacs"]
    
    table = Table(title=f"{monthMap[month]} {year} Detailed Summary", title_style="bold cyan")

    table.add_column("Date", style="bold green", overflow="wrap")
    table.add_column("Amount", style="yellow", overflow="wrap")
    table.add_column("Category", style="yellow", overflow="wrap")
    table.add_column("Note", style="purple", overflow="wrap")

    for record in currentTransacs:
        table.add_row(str(record["date"]), str(record["amt"]), 
                        formatCategory(record["category"]), record["note"])
    
    console.print(table)
    console.print(Panel(f"Would you like to view transactions from another month?", 
                        title="Message!", style="bold yellow"))
    res = input("\nRespond with (y) to confirm or (n) to cancel: ")
    if res.lower() == "y":
        return viewExpense()
    else:
        return home()

# Search for an expense
def searchExpense():
    cls()
    global currentUser, currentData

    console.print(Markdown(searchtext))
    ans = int(input("\nEnter your input: "))

    if ans == 1:
        cls()
        try:
            ddmmyy = formatDate(str(input("Enter date of expense (eg - 25/05/2025 for 25 May 2025) : ")))
            date, month, year = map(int, ddmmyy.split("/"))
        except (ValueError, IndexError):
            console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
            input("\nPress Enter to try again...")
            return searchExpense()

        if month < 1 or month > 12:
            console.print(Panel("Please enter a valid month (1-12)...", 
                                title="Message!", style="bold red"))
            input("\nPress Enter to try again...")
            return searchExpense()
        
        if ddmmyy[3:] not in currentData:
            console.print(Panel(f"No search results found for {ddmmyy}", title="Message!", style="bold red"))
            input("\nPress Enter to go to home page...")
            return home()
        
        currentTransacs = currentData[ddmmyy[3:]]["transacs"]
        found = False

        table = Table(title=f"Search Results for {ddmmyy}", title_style="bold cyan")

        table.add_column("Date", style="bold green", overflow="wrap")
        table.add_column("Amount", style="yellow", overflow="wrap")
        table.add_column("Category", style="yellow", overflow="wrap")
        table.add_column("Note", style="purple", overflow="wrap")

        for record in currentTransacs:
            if record["date"] == date:
                table.add_row(formatDate(str(record["date"]) + "/" + ddmmyy[3:]), str(record["amt"]), 
                        formatCategory(record["category"]), record["note"])
                found = True
        
        if found:
            console.print(table)
            console.print(Panel(f"Would you like to search for another transaction?", 
                        title="Message!", style="bold yellow"))
            ans2 = input("\nRespond with (y) to confirm or (n) to cancel: ")
            if ans2.lower() == "y":
                return searchExpense()
            else:
                return home()
        else:
            console.print(Panel(f"No search results found for {ddmmyy}", title="Message!", style="bold red"))
            input("\nPress Enter to go to home page...")
            return home()
    
    elif ans == 2:
        cls()
        query = str(input("\nPlease enter search query : "))

        cls()
            
        table2 = Table(title=f"Search Results for \"{query}\"", title_style="bold cyan")

        table2.add_column("Date", style="bold green", overflow="wrap")
        table2.add_column("Amount", style="yellow", overflow="wrap")
        table2.add_column("Category", style="yellow", overflow="wrap")
        table2.add_column("Note", style="purple", overflow="wrap")

        found2 = False

        for item2 in currentData:
            transacs = currentData[item2]["transacs"]

            for record2 in transacs:
                if query in record2["note"]:
                    table2.add_row(formatDate(str(record2["date"]) + "/" + item2), str(record2["amt"]), 
                    formatCategory(record2["category"]), record2["note"])
                    found2 = True

        if found2:
            console.print(table2)
            console.print(Panel(f"Would you like to search for another transaction?", 
                        title="Message!", style="bold yellow"))
            ans3 = input("\nRespond with (y) to confirm or (n) to cancel: ")
            if ans3.lower() == "y":
                return searchExpense()
            else:
                return home()
        else:
            console.print(Panel(f"No search results found for {query}", title="Message!", style="bold red"))
            input("\nPress Enter to try again...")
            return searchExpense()

    elif ans == 3:
        return home()
    
    else:
        cls()
        console.print(Panel(f"Invalid Input!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to home page...")
        return home()

# Delete Expense
def deleteExpense():
    cls()
    global currentUser, currentData

    try:
        mmyy = str(input("Enter month for deletion (eg - 05/2025 for May 2025): "))
        mmyy = formatDate("00/" + mmyy)[3:]
        if mmyy not in currentData:
            cls()
            console.print(Panel("No records found for this month!", title="Message!", style="bold red"))
            input("\nPress Enter to return to home page...")
            return home()
    except:
        cls()
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return deleteExpense()

    currentTransacs = currentData[mmyy]["transacs"]
    if not currentTransacs:
        cls()
        console.print(Panel("No records to delete!", title="Message!", style="bold red"))
        input("\nPress Enter to return to the homepage...")
        return home()

    table = Table(title=f"Delete Expense", title_style="bold cyan")
    table.add_column("Index", style="cyan")
    table.add_column("Date", style="magenta")
    table.add_column("Amount (₹)", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Note", style="blue")

    index = 1
    for t in currentTransacs:
        table.add_row(str(index), str(t["date"]), str(t["amt"]), formatCategory(t["category"]), str(t["note"] or ""))
        index += 1

    console.print(table)
    try:
        deleteIndex = int(input("Enter index of transaction to delete: ")) - 1
        if deleteIndex < 0 or deleteIndex >= len(currentTransacs):
            raise ValueError
    except ValueError:
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return deleteExpense()

    deleted = currentTransacs.pop(deleteIndex)
    currentData[mmyy]["total"] -= deleted["amt"]
    category_key = deleted["category"]
    currentData[mmyy][category_key] -= deleted["amt"]
    saveDataToCSV()

    console.print(Panel("Expense deleted successfully!", title="Success!", style="bold green"))
    input("\nPress Enter to return to the homepage...")
    return home()

def expenseReport():
    cls()
    global currentUser, currentData
    console.print(Markdown("# 📊 Expense Report"))

    try:
        mmyy = str(input("\nEnter month/year for report (eg - 05/2025 for May 2025): "))
        mmyy = formatDate("00/" + mmyy)[3:]
        if mmyy not in currentData:
            console.print(Panel("No records found for this month!", title="Message!", style="bold red"))
            input("\nPress Enter to return to home page...")
            return home()
    except:
        console.print(Panel("Please enter a valid input...", title="Message!", style="bold red"))
        input("\nPress Enter to try again...")
        return expenseReport()

    total_expenses = currentData[mmyy]["total"]
    categories = {
        "Food & Dining": currentData[mmyy]["food"],
        "Transport": currentData[mmyy]["transport"],
        "Housing & Utilities": currentData[mmyy]["housing"],
        "Health & Fitness": currentData[mmyy]["health"],
        "Fun & Leisure": currentData[mmyy]["leisure"],
        "Others": currentData[mmyy]["other"]
    }

    table3 = Table(title=f"Expense Report for {monthMap[int(mmyy[:2])]} {mmyy[3:]}", title_style="bold cyan")
    table3.add_column("Category", style="bold green")
    table3.add_column("Amount (₹)", style="yellow")

    for category, amount in categories.items():
        table3.add_row(category, str(amount))

    table3.add_row("\nTotal", "\n" + str(total_expenses))

    cls()
    console.print(table3)

    console.print(Panel("Would you like to generate a graphical report?", title="Message!", style="bold yellow"))
    res4 = input("\nRespond with (y) to confirm or (n) to cancel: ")

    while True:
        cls()
        if res4.lower() == "y":
            console.print(Markdown("# Choose the representation format:"))
            console.print(Markdown("1. 📊 Bar Chart\n2. 📈 Line Graph\n3. 🍰 Pie Chart"))
            
            try:
                choice = int(input("\nEnter your choice : "))
            except ValueError:
                cls()
                console.print(Panel("Invalid input! Please enter a number (1, 2, or 3).", title="Message!", style="bold red"))
                return home()

            if choice == 1:
                plt.figure(figsize=(12, 6))
                colors = ['#FF5733', '#33FF57', '#3357FF', '#FFC300', '#DAF7A6', '#FF33F6']
                bars = plt.bar(list(categories.keys()), list(categories.values()), color=colors, width=0.4)

                plt.xlabel("Categories", fontsize=14, fontweight='bold')
                plt.ylabel("Amount (₹)", fontsize=14, fontweight='bold')
                plt.title(f"Expense Report for {monthMap[int(mmyy[:2])]} {mmyy[3:]}", fontsize=16, fontweight='bold')
                plt.xticks(rotation=15)
                plt.yticks(fontsize=12)
                plt.grid(axis='y', linestyle='--', alpha=0.7)

                for bar in bars:
                    yval = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, int(yval), ha='center', va='bottom', fontsize=10)

                plt.tight_layout()
                plt.show()

            elif choice == 2:
                plt.figure(figsize=(12, 6))
                plt.plot(list(categories.keys()), list(categories.values()), marker='o', linestyle='-', color='b')

                plt.xlabel("Categories", fontsize=14, fontweight='bold')
                plt.ylabel("Amount (₹)", fontsize=14, fontweight='bold')
                plt.title(f"Expense Report for {monthMap[int(mmyy[:2])]} {mmyy[3:]}", fontsize=16, fontweight='bold')
                plt.xticks(rotation=15)
                plt.grid()

                plt.tight_layout()
                plt.show()

            elif choice == 3:
                plt.figure(figsize=(5, 5))

                labelList = []
                for thing in categories.keys():
                    if categories[thing] != 0:
                        labelList.append(thing)
                
                valueList = []
                for item2 in categories.values():
                    if item2 != 0:
                        valueList.append(item2)

                plt.pie(valueList, labels = labelList, autopct='%1.1f%%', startangle=140)

                plt.title(f"Expense Distribution for {monthMap[int(mmyy[:2])]} {mmyy[3:]}", fontsize=16, fontweight='bold')
                plt.axis('equal')

                plt.tight_layout()
                plt.show()

            else:
                console.print(Panel("Invalid choice! Please select 1, 2, or 3.", title="Message!", style="bold red"))

            cls()
            console.print(Markdown("# Please enter your choice - "))
            console.print(Markdown("### Type 'y' to view data in another format"))
            console.print(Markdown("### Type 'n' to exit to home page"))
            response = input("\nEnter your choice : ")
            if response.lower() != "y":
                break
        else:
            return home()
        
    return home()

# Creating a new user account
def createAccount():
    cls()

    details = {"Username" : "", "Email" : "", "Phone Number" : 0, "Password" : ""}

    #Filling Values in dictionary from user input
    for key in details.keys():
        try:
            if key == "Phone Number" : details[key] = int(input(f"\nEnter {key} : "))
            else : details[key] = str(input(f"\nEnter {key} : "))
        except ValueError:
            cls()
            console.print(Panel(f"Please Enter a valid 10 digit phone number...", 
                        title="Message!", style="bold red"))
            input("\nPress Enter to go back to login menu...")
            return login()

    # Check Empty Fields 
    if details["Username"] == "" or details["Email"] == "" or details["Password"] == "":
        cls()
        console.print(Panel(f"Some fields are left blank, please try again!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        return login()

    username = details["Username"]

    # Checking if the username already exists
    check = isRegistered(details["Username"])
    if check:
        console.print(Panel(f"User {username} already exists", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        return login()

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
        return login()

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
    return login()

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
        return login()

    if res == 1:
        pass
    elif res == 2:
        createAccount()
        return login()
    elif res == 3:
        return welcome()
    else:
        console.print(Panel(f"Please enter a valid input!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        return login()

    cls()

    try:
        username = str(input("\nPlease enter your username : "))
    except:
        cls()
        console.print(Panel(f"Please enter a valid input!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        return login()

    # Checking if user is registered or not
    check = isRegistered(username)
    if check == False:
        console.print(Panel(f"User {username} is not registered!", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to go back to login menu...")
        return login()
    
    # Verifying login and redirecting to homepage
    cls()
    password = str(input(f"\nHey {username}, please enter your password : "))

    with open(dataFile, "r", newline = "") as file:
        rdr = csv.reader(file)
        for row in rdr:
            if row[0] == username and row[3] == password:
                currentUser = username
                with open(recFile, "r", newline = "") as file:
                    rdr = csv.reader(file)
                    for row in rdr:
                        if row[0] == username:
                            currentData = ast.literal_eval(row[1])
                            break
                console.print(Panel(f"User {username} successfully logged in!", 
                        title="Message!", style="bold green"))
                input("\nPress Enter to go to the homepage...")
                return home()
            
            elif row[0] == username and row[3] != password:
                console.print(Panel(f"Incorrect password entered!", 
                        title="Message!", style="bold red"))
                input("\nPress Enter to back to the login page again...")
                return login()

# User Logout
def logout():
    global currentUser, currentData

    currentUser = None
    currentData = {}
    return main()

# Homepage for the app
def home():
    cls()
    global currentUser

    console.print(Markdown(hometxt))

    try:
        res = int(input("\nEnter your input : "))

        if res == 1:
            return addExpense()
        elif res == 2:
            return viewExpense()
        elif res == 3:
            return searchExpense()
        elif res == 4:
            return deleteExpense()
        elif res == 5:
            return expenseReport()
        elif res == 6:
            return logout()
        else:
            cls()
            console.print(Panel(f"Invalid Input Entered...(Only 1, 2, 3, 6 working for now)", 
                            title="Message!", style="bold red"))
            input("\nPress Enter to back to the home page again...")
            return home()
    
    except:
        cls()
        console.print(Panel(f"Invalid Input Entered...(Only 1 and 6 working for now)", 
                        title="Message!", style="bold red"))
        input("\nPress Enter to back to the home page again...")
        return home()
    
# Parent Function of all Functions
def main():

    welcome()

    login()

main()