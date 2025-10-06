Command-Line Banking System
Version: 1.0
Author: Sayan Paul
Date: October 7, 2025

1. Introduction
This project is a command-line based banking application developed in Python. It simulates the basic functionalities of a bank, allowing users to create accounts, perform transactions, and check their financial details. The application is designed to be simple and robust, storing all user and transaction data locally in CSV files. It features a secure authentication system using a 4-digit PIN for all sensitive operations.

2. Key Features
Account Management:

Create Account: Securely create a new bank account with unique email and mobile number validation.

Close Account: Permanently delete an existing bank account after confirmation.

Secure Transactions:

PIN Authentication: All account operations (deposit, withdrawal, balance check, etc.) are protected by a 4-digit PIN. PINs are securely stored using SHA-256 hashing.

Deposit: Add funds to an account.

Withdraw: Withdraw funds from an account, with checks to prevent overdrawing.

Account Information:

Check Balance: View the current balance of an account.

Transaction History: View a complete, timestamped log of all transactions for an account.

Administrative Functions:

Branch Manager Report: An admin-level feature to view a summary of all accounts, including the total number of accounts and the total funds held by the bank.

3. How to Run the Application
Prerequisites
Python 3.x installed on your system.

Setup and Execution
Save the Code: Save the provided Python code as a file named banking_system.py.

Open a Terminal: Open a command prompt or terminal.

Navigate to the Directory: Use the cd command to navigate to the folder where you saved the banking_system.py file.

cd path/to/your/project/folder

Run the Script: Execute the script using the following command:

python banking_system.py

First Time Use: The application will automatically create two files in the same directory: bank_accounts.csv and transactions.csv. You can start by creating a new account.

4. How It Works
Data Storage
The application uses two separate CSV files for data persistence:

bank_accounts.csv: This file acts as the main database for all user accounts. It stores the following information for each user:

account_number: A unique, randomly generated 10-digit number.

name: The full name of the account holder.

mail: The user's unique email address.

mobile_num: The user's unique 10-digit mobile number.

address: The physical address of the user.

amount: The current balance in the account.

pin_hash: The SHA-256 hash of the user's 4-digit PIN for secure storage.

transactions.csv: This file logs every single transaction that occurs in the system. Each log entry includes:

account_number: The account associated with the transaction.

transaction_type: The type of transaction (e.g., "Account Created", "Deposit", "Withdraw", "Account Closed").

amount: The amount involved in the transaction.

current_balance: The account balance after the transaction.

timestamp: The exact date and time the transaction occurred.

Security
Security is a key aspect of this application. Instead of storing user PINs in plain text, the program uses the SHA-256 hashing algorithm. When a user creates a PIN, it is immediately converted into a unique hash (a long string of characters). This hash is stored. When the user tries to log in, the PIN they enter is hashed again, and this new hash is compared to the stored one. This ensures that even if someone gains access to the bank_accounts.csv file, they cannot see the actual PINs.

5. Code Overview
The script is logically divided into three main sections:

Helper Functions: This section contains utility functions that perform common tasks like clearing the screen, initializing files, finding accounts, logging transactions, validating input (email, mobile, PIN), and authenticating users. Using csv.DictReader and csv.DictWriter makes the code readable and easy to maintain.

Core Features: This section contains the main logic for each banking feature, such as create_account(), deposit_money(), withdraw_money(), etc. These functions handle user interaction and data manipulation.

Main Menu: The main() function serves as the entry point of the application. It runs the main program loop, displays the user menus, and calls the appropriate functions based on user input.

6. Future Improvements
Database Integration: Replace the CSV file system with a more robust and efficient database like SQLite or PostgreSQL to handle larger amounts of data and more complex queries.

Money Transfer: Add a feature to allow users to transfer money from their account to another account within the bank.

Object-Oriented Programming (OOP): Refactor the code into classes (e.g., Account, Bank, Transaction) to better organize the logic and make the system more scalable.

Graphical User Interface (GUI): Develop a graphical interface using a library like Tkinter or PyQt to make the application more user-friendly.