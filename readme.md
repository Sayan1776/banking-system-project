Command-Line Banking System
Version: 2.0
Author: Sayan
Date: October 7, 2025

1. Introduction
    This project is a command-line based banking application developed in Python. It simulates the core functionalities of a modern bank, built upon a robust Object-Oriented Programming (OOP) architecture and a reliable SQLite database for data persistence.

    The application allows users to securely manage their finances through a simple and intuitive interface. All sensitive operations are protected by a hashed PIN, and all transactions are atomic, ensuring data integrity.

2. Key Features
    Secure Account Management:

    Create Account: Securely create a new bank account with unique email and mobile number validation.

    Close Account: Permanently delete an existing bank account and its associated transactions.

    Atomic Transactions:

    PIN Authentication: All account operations are protected by a 4-digit PIN, which is securely stored using a SHA-256 hash.

    Deposit & Withdraw: Add or remove funds from an account.

    Money Transfer: Atomically transfer funds between two accounts. The system guarantees that if any part of the transfer fails, the entire transaction is rolled back, preventing data corruption.

    Account Information:

    Check Balance: Instantly view the current account balance.

    Transaction History: View a complete, timestamped log of all transactions, sorted from most recent to oldest.

    Administrative Functions:

    Branch Manager Report: View a high-level summary of the bank's health, including the total number of accounts and the total funds under management.

3. How to Run the Application
    Prerequisites
    Python 3.x installed on your system.

    Setup and Execution
    Save the Code: Save the provided Python code as a file named banking_system.py.

    Open a Terminal: Open a command prompt or terminal in the same directory as the file.

    Run the Script: Execute the script using the following command:

    "python banking_system.py"

    First Time Use: The application will automatically create a single database file named bank.db in the same directory. This file will contain all the application's data.

4. How It Works
    Architecture: Object-Oriented Programming (OOP)
    The application is built using an OOP design, which organizes the code into logical, reusable components.

    Account Class: Represents a single bank account. This object holds all the data for one user (name, balance, etc.) and contains the methods to perform operations on that data (e.g., deposit(), withdraw(), authenticate()).

    Bank Class: Acts as the central controller for the entire application. It manages the collection of all Account objects, handles the connection to the SQLite database, and contains the high-level logic for operations like creating accounts and transferring money.

    This class-based structure makes the code clean, scalable, and easy to maintain.

    Data Storage: SQLite Database
    All application data is stored in a single, lightweight database file named bank.db. This is a professional and efficient alternative to using plain text files.

    The database contains two main tables:

    accounts: Stores the primary information for each user account.

    account_number (PRIMARY KEY)

    name, mail, mobile_num, address

    balance

    pin_hash (The secure SHA-256 hash of the user's PIN)

    transactions: Provides a complete audit trail of every action taken.

    id (PRIMARY KEY)

    account_number (FOREIGN KEY to the accounts table)

    transaction_type, details, amount

    current_balance, timestamp

    This database structure ensures data integrity, efficiency, and allows for atomic transactions that cannot be corrupted.

5. How to View the Database
    The bank.db file is a binary file and cannot be opened with a normal text editor. To view the data inside, you need a specialized tool.

    Recommended Tool: The "SQLite" extension for Visual Studio Code.

    How to Use:

    Install the "SQLite" extension from the VS Code Marketplace.

    Open the Command Palette (Ctrl+Shift+P).

    Type and select SQLite: Open Database.

    Choose your bank.db file.

    A "SQLITE EXPLORER" tab will appear in your sidebar, allowing you to browse the accounts and transactions tables and see their data in a clean, spreadsheet-like view.

6. Future Improvements
    Unit Testing: Implement automated tests using Python's unittest module to verify the correctness of each function and method.

    Web API: Build a simple web API using a framework like Flask or FastAPI to expose the banking logic, allowing it to be used by a web or mobile front-end.

    GUI: Develop a graphical user interface (GUI) using a library like Tkinter or PyQt to make the application more accessible to non-technical users.