**Simple Banking System**
1. Project Overview
This project is a command-line based banking management system written in Python. It allows users to perform basic banking operations such as creating accounts, depositing and withdrawing money, checking balances, and viewing transaction histories. The system stores all account and transaction data persistently in local CSV files. It's designed to be simple and robust, with built-in validation for user inputs like email and mobile numbers.

2. Features
The application supports the following features:

Create New Account: Allows a new user to create a bank account with their name, email, mobile number, and address.

Input Validation:

Ensures email addresses are in a valid format.

Ensures mobile numbers are exactly 10 digits.

Checks for uniqueness to prevent duplicate accounts with the same email or mobile number.

Validates that deposit/withdrawal amounts are positive numbers.

Deposit Money: Add funds to an existing account.

Withdraw Money: Withdraw funds from an existing account, with a check for sufficient balance.

Check Balance: View the current balance of a specific account.

Transaction History: Display a log of all transactions for a given account.

Close Account: Securely remove an account from the system.

Branch Manager Report: A special feature to view a summary of all accounts, including the total number of accounts and the cumulative balance in the bank.

3. File Structure
The system uses two CSV files to store data:

bank_accounts.csv: This file acts as the main database for all customer accounts. Each row represents a unique account.

Columns: account_number, name, mail, mobile_num, address, amount

transactions.csv: This file logs every transaction that occurs in the system, providing a complete audit trail.

Columns: account_number, transaction_type, amount, current_balance, timestamp

4. How to Run the Application
Save the code as a Python file (e.g., banking_system.py).

Open a terminal or command prompt.

Navigate to the directory where you saved the file.

Run the script using the command: python banking_system.py

The main menu will be displayed, and you can interact with the system by entering the number corresponding to your choice.

5. Functions Reference
Helper Functions
log_transaction(acc_no, txn_type, amount, balance): Logs a single transaction to transactions.csv. It records the account number, transaction type (e.g., "Deposit", "Withdraw"), the amount of the transaction, the new balance, and a timestamp.

find_account(acc_no): Searches bank_accounts.csv for an account matching the provided acc_no. Returns the account details as a list if found, otherwise returns None.

update_account(acc_no, new_balance): Updates the balance of a specific account in bank_accounts.csv. It reads all data, modifies the specific account's balance, and writes the entire dataset back to the file.

is_valid_email(email): Uses regular expressions (re module) to validate if the provided string is a valid email format.

is_valid_mobile(mobile): Checks if the mobile number is a string of exactly 10 digits.

is_field_unique(column_index, value): A crucial validation function that checks if a given value (like an email or mobile number) already exists in a specific column_index of bank_accounts.csv.

Core Feature Functions
create_account(): Prompts the user for personal details. It uses the validation helper functions to ensure the email and mobile number are valid and unique before creating a new account and logging the initial deposit.

deposit_money(acc_no): Handles the logic for depositing money into an account.

withdraw_money(acc_no): Manages withdrawals, including checking for insufficient funds.

check_balance(acc_no): Fetches and displays the current balance for an account.

transaction_history(acc_no): Reads transactions.csv and prints all entries corresponding to the given account number.

branch_manager_report(): Calculates and displays aggregate data about all accounts in the bank.

close_account(acc_no): Removes an account from bank_accounts.csv after user confirmation. It logs this action in the transaction file.

main(): The primary function that runs the application loop, displays the menu, and calls the appropriate functions based on user input.
