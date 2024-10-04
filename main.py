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

import csv
import os
import matplotlib.pyplot as plt

from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

currentUser = None
dataFile = "./data.csv"
recFile = "./records.csv"

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
            console.print(Markdown('''### **Please Enter a valid 10 digit phone number.**'''))
            input("\nPress Enter to go back to login menu...")
            login()

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
    console.print(Markdown('''### **Would you like to confirm account creation?**'''))
    console.print(final)
    res = input("\nRespond with (y) to confirm or (n) to cancel: ")
    if res.lower() != "y":
        login()

    # Register user details to backend
    with open(dataFile, "a+", newline = "") as file:
        wtr = csv.writer(file)
        wtr.writerow(details.values())
    
    with open(recFile, "a+", newline = "") as file:
        wtr = csv.writer(file)

        defaultdict = {"total" : 0, 
                       "food" : 0, "transport" : 0, "housing" : 0, "health" : 0, "leisure" : 0,
                       "details" : []}
        
        wtr.writerow([details["Username"], defaultdict])

    # Print Completion
    username = details["Username"]
    console.print(Panel(f"User {username} successfully registered!", 
                        title="Message!", style="bold green"))
    input("\nPress Enter to go back to login menu...")
    login()

# User Login
def login():
    cls()
    console.print(Markdown(loginmain))
    res = int(input("\nEnter your input : "))

    if res == 1:
        pass
    elif res == 2:
        createAccount()
        login()
    else:
        console.print(Markdown('''### **Please enter a valid input**'''))
        input("\nPress Enter to go back to login menu...")
        login()

    cls()
    username = str(input("\nPlease enter your username : "))

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
                console.print(Panel(f"User {username} successfully logged in!", 
                        title="Message!", style="bold green"))
                input("\nPress Enter to go to the homepage...")
                return
            elif row[0] == username and row[3] != password:
                console.print(Panel(f"Incorrect password entered!", 
                        title="Message!", style="bold red"))
                input("\nPress Enter to back to the login page again...")
                login()

# Parent Function of all Functions
def main():

    cls()
    console.print(Markdown(welcometxt))
    input("\nPress Enter to continue to the login page...")

    login()
    
    #Continue to build homepage after this

main()