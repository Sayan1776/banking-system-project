import csv
import random
import datetime
import re

BANK_FILE = "bank_accounts.csv"
TXN_FILE = "transactions.csv"

# ----------------- Helper Functions ----------------- #

def log_transaction(acc_no, txn_type, amount, balance):
    """Logs a transaction to the transactions file."""
    try:
        # Create the file with headers if it doesn't exist
        try:
            with open(TXN_FILE, "x", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["account_number", "transaction_type", "amount", "current_balance", "timestamp"])
        except FileExistsError:
            pass # File already exists

        with open(TXN_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([acc_no, txn_type, amount, balance, datetime.datetime.now()])
    except IOError as e:
        print(f"Error logging transaction: {e}")

def find_account(acc_no):
    """Finds an account by account number and returns the row data."""
    acc_no = acc_no.strip()  # remove spaces/newlines
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for row in reader:
                # Check if row is not empty and the account number matches
                if row and row[0].strip() == acc_no:
                    return row
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred while finding the account: {e}")
    return None


def update_account(acc_no, new_balance):
    """Updates the balance for a specific account."""
    rows = []
    headers = []
    acc_no = acc_no.strip()
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row and row[0].strip() == acc_no:
                    row[5] = str(new_balance) # Update balance
                rows.append(row)

        with open(BANK_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)
    except FileNotFoundError:
        print(f"Error: {BANK_FILE} not found.")
    except Exception as e:
        print(f"An error occurred while updating the account: {e}")

def is_valid_email(email):
    """Checks if the email format is valid using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def is_valid_mobile(mobile):
    """Checks if the mobile number is 10 digits and contains only numbers."""
    return mobile.isdigit() and len(mobile) == 10

def is_field_unique(column_index, value):
    """Checks if a value in a specific column of the bank file is unique."""
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            for row in reader:
                if row and len(row) > column_index and row[column_index].strip() == value:
                    return False  # Value exists, so not unique
    except FileNotFoundError:
        return True  # File doesn't exist, so the value is unique
    return True # Value is unique

# ----------------- Core Features ----------------- #

def create_account():
    """Creates a new bank account with validation and saves it to the CSV file."""
    name = input("Enter your name: ")

    # Validate Email
    while True:
        mail = input("Enter your email-id: ")
        if not is_valid_email(mail):
            print("❌ Invalid email format. Please try again (e.g., user@example.com).")
            continue
        if not is_field_unique(2, mail):  # Column 2 is 'mail'
            print("❌ This email is already registered. Please use another email.")
            continue
        break

    # Validate Mobile Number
    while True:
        mobile_num = input("Enter your 10-digit mobile number: ")
        if not is_valid_mobile(mobile_num):
            print("❌ Invalid mobile number. Please enter exactly 10 digits.")
            continue
        if not is_field_unique(3, mobile_num):  # Column 3 is 'mobile_num'
            print("❌ This mobile number is already registered.")
            continue
        break

    address = input("Enter your address: ")
    account_number = str(random.randint(1000000000, 9999999999))
    
    while True:
        try:
            amount = int(input("Enter the initial deposit amount (must be >= 0): "))
            if amount >= 0:
                break
            else:
                print("❌ Initial deposit cannot be negative.")
        except ValueError:
            print("❌ Invalid amount. Please enter a number.")


    # Create the file with headers if it doesn't exist
    try:
        with open(BANK_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["account_number", "name", "mail", "mobile_num", "address", "amount"])
    except FileExistsError:
        pass  # file already exists, which is fine

    # Append the new account details
    with open(BANK_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([account_number, name, mail, mobile_num, address, amount])

    log_transaction(account_number, "Account Created", amount, amount)

    print(f"✅ Account created successfully! Your Account Number is {account_number}")

def deposit_money(acc_no):
    """Deposits money into a specified account."""
    account = find_account(acc_no)
    if not account:
        print("❌ Account not found.")
        return

    try:
        amount = int(input("Enter amount to deposit: "))
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return
            
        new_balance = int(account[5]) + amount
        update_account(acc_no, new_balance)
        log_transaction(acc_no, "Deposit", amount, new_balance)

        print(f"✅ Deposited {amount}. New Balance: {new_balance}")
    except ValueError:
        print("❌ Invalid amount entered.")

def withdraw_money(acc_no):
    """Withdraws money from a specified account."""
    account = find_account(acc_no)
    if not account:
        print("❌ Account not found.")
        return

    try:
        amount = int(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return

        balance = int(account[5])
        if amount > balance:
            print("❌ Insufficient balance.")
            return

        new_balance = balance - amount
        update_account(acc_no, new_balance)
        log_transaction(acc_no, "Withdraw", amount, new_balance)

        print(f"✅ Withdrawn {amount}. New Balance: {new_balance}")
    except ValueError:
        print("❌ Invalid amount entered.")

def check_balance(acc_no):
    """Checks and prints the balance of a specified account."""
    account = find_account(acc_no)
    if not account:
        print("❌ Account not found.")
        return
    print(f"💰 Current Balance: {account[5]}")

def transaction_history(acc_no):
    """Displays the transaction history for a specified account."""
    print("📜 Transaction History:")
    found = False
    try:
        with open(TXN_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None) # Skip header
            for row in reader:
                if row and row[0].strip() == acc_no.strip():
                    print(f"  - Type: {row[1]}, Amount: {row[2]}, Balance: {row[3]}, Time: {row[4]}")
                    found = True
        if not found:
            print("  No transactions found for this account.")
    except FileNotFoundError:
        print("❌ No transactions recorded yet.")

def branch_manager_report():
    """Provides a summary report of all accounts."""
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader) # Skip header
            accounts = list(reader)
            # Filter out empty rows that might exist in the CSV
            accounts = [acc for acc in accounts if acc] 
            if not accounts:
                print("No accounts in the bank yet.")
                return

            print("🏦 Branch Manager Report")
            print(f"Total Accounts: {len(accounts)}")
            total_balance = sum(int(acc[5]) for acc in accounts)
            print(f"Total Balance in Bank: {total_balance}")
    except FileNotFoundError:
        print("❌ No accounts file found.")
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")

def close_account(acc_no):
    """Closes an account by removing it from the bank file."""
    acc_no = acc_no.strip()
    account = find_account(acc_no)
    if not account:
        print("❌ Account not found.")
        return

    confirm = input(f"Are you sure you want to close account {acc_no}? (yes/no): ").lower()
    if confirm != "yes":
        print("❌ Account closure cancelled.")
        return

    rows = []
    headers = []
    with open(BANK_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        # Read all accounts except the one to be deleted
        for row in reader:
            if row and row[0].strip() != acc_no:
                rows.append(row)

    # Write the remaining accounts back to the file
    with open(BANK_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    final_balance = account[5]
    log_transaction(acc_no, "Account Closed", 0, final_balance)

    print(f"✅ Account {acc_no} closed successfully. Final Balance was {final_balance}.")

# ----------------- Main Menu ----------------- #

def main():
    """Main function to run the banking system menu."""
    while True:
        print("\n===== Banking System =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Branch Manager Report")
        print("7. Close Account")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice in ["2", "3", "4", "5", "7"]:
            acc_no = input("Enter account number: ").strip()
            if not acc_no:
                print("❌ Account number cannot be empty.")
                continue
            if choice == "2":
                deposit_money(acc_no)
            elif choice == "3":
                withdraw_money(acc_no)
            elif choice == "4":
                check_balance(acc_no)
            elif choice == "5":
                transaction_history(acc_no)
            elif choice == "7":
                close_account(acc_no)
        elif choice == "6":
            branch_manager_report()
        elif choice == "8":
            print("👋 Thank you for using the Banking System!")
            break
        else:
            print("❌ Invalid choice, please try again.")

if __name__ == "__main__":
    main()