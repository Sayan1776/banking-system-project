import csv
import random
import datetime
import re
import hashlib
import os

# --- Constants ---
BANK_FILE = "bank_accounts.csv"
TXN_FILE = "transactions.csv"
ACCOUNT_HEADERS = ["account_number", "name", "mail", "mobile_num", "address", "amount", "pin_hash"]
TXN_HEADERS = ["account_number", "transaction_type", "amount", "current_balance", "timestamp"]

# ----------------- Helper Functions ----------------- #

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_files():
    """Creates the necessary CSV files with headers if they don't exist."""
    try:
        with open(BANK_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(ACCOUNT_HEADERS)
    except FileExistsError:
        pass # File already exists

    try:
        with open(TXN_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(TXN_HEADERS)
    except FileExistsError:
        pass # File already exists

def log_transaction(acc_no, txn_type, amount, balance):
    """Logs a transaction to the transactions file."""
    try:
        with open(TXN_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=TXN_HEADERS)
            writer.writerow({
                "account_number": acc_no,
                "transaction_type": txn_type,
                "amount": amount,
                "current_balance": balance,
                "timestamp": datetime.datetime.now()
            })
    except IOError as e:
        print(f"Error logging transaction: {e}")

def find_account(acc_no):
    """Finds an account by account number and returns the row data as a dictionary."""
    acc_no = acc_no.strip()
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['account_number'] == acc_no:
                    return row
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"An error occurred while finding the account: {e}")
    return None

def update_all_accounts(accounts):
    """Rewrites the entire bank file with the updated list of accounts."""
    try:
        with open(BANK_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=ACCOUNT_HEADERS)
            writer.writeheader()
            writer.writerows(accounts)
        return True
    except Exception as e:
        print(f"An error occurred while updating accounts: {e}")
        return False

def is_valid_email(email):
    """Checks if the email format is valid using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def is_valid_mobile(mobile):
    """Checks if the mobile number is 10 digits and contains only numbers."""
    return mobile.isdigit() and len(mobile) == 10
    
def is_valid_pin(pin):
    """Checks if the PIN is 4 digits."""
    return pin.isdigit() and len(pin) == 4

def is_field_unique(field_name, value):
    """Checks if a value in a specific column of the bank file is unique."""
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[field_name].strip() == value:
                    return False  # Value exists, so not unique
    except FileNotFoundError:
        return True  # File doesn't exist, so the value is unique
    return True # Value is unique

def authenticate_user(account):
    """Authenticates the user by asking for their PIN."""
    pin = input("Enter your 4-digit PIN to confirm: ")
    if not is_valid_pin(pin):
        print("❌ Invalid PIN format. Must be 4 digits.")
        return False
        
    hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
    if hashed_pin == account['pin_hash']:
        return True
    print("❌ Incorrect PIN.")
    return False

# ----------------- Core Features ----------------- #

def create_account():
    """Creates a new bank account with validation and saves it to the CSV file."""
    name = input("Enter your name: ")

    while True:
        mail = input("Enter your email-id: ")
        if not is_valid_email(mail):
            print("❌ Invalid email format. Please try again (e.g., user@example.com).")
        elif not is_field_unique('mail', mail):
            print("❌ This email is already registered. Please use another email.")
        else:
            break

    while True:
        mobile_num = input("Enter your 10-digit mobile number: ")
        if not is_valid_mobile(mobile_num):
            print("❌ Invalid mobile number. Please enter exactly 10 digits.")
        elif not is_field_unique('mobile_num', mobile_num):
            print("❌ This mobile number is already registered.")
        else:
            break
            
    while True:
        pin = input("Create a 4-digit PIN for your account: ")
        if is_valid_pin(pin):
            pin_hash = hashlib.sha256(pin.encode()).hexdigest()
            break
        else:
            print("❌ PIN must be exactly 4 digits.")

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

    new_account = {
        "account_number": account_number, "name": name, "mail": mail,
        "mobile_num": mobile_num, "address": address, "amount": amount, "pin_hash": pin_hash
    }

    try:
        with open(BANK_FILE, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=ACCOUNT_HEADERS)
            writer.writerow(new_account)
        log_transaction(account_number, "Account Created", amount, amount)
        print(f"\n✅ Account created successfully! Your Account Number is {account_number}")
    except Exception as e:
        print(f"❌ Could not create account: {e}")


def deposit_money(account):
    """Deposits money into a specified account."""
    try:
        amount = int(input("Enter amount to deposit: "))
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return

        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            accounts = list(reader)
        
        for acc in accounts:
            if acc['account_number'] == account['account_number']:
                new_balance = int(acc['amount']) + amount
                acc['amount'] = new_balance
                if update_all_accounts(accounts):
                    log_transaction(account['account_number'], "Deposit", amount, new_balance)
                    print(f"✅ Deposited {amount}. New Balance: {new_balance}")
                break
    except ValueError:
        print("❌ Invalid amount entered.")

def withdraw_money(account):
    """Withdraws money from a specified account."""
    try:
        amount = int(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return
            
        current_balance = int(account['amount'])
        if amount > current_balance:
            print("❌ Insufficient balance.")
            return

        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            accounts = list(reader)

        for acc in accounts:
            if acc['account_number'] == account['account_number']:
                new_balance = current_balance - amount
                acc['amount'] = new_balance
                if update_all_accounts(accounts):
                    log_transaction(account['account_number'], "Withdraw", amount, new_balance)
                    print(f"✅ Withdrawn {amount}. New Balance: {new_balance}")
                break
    except ValueError:
        print("❌ Invalid amount entered.")

def check_balance(account):
    """Checks and prints the balance of a specified account."""
    print(f"💰 Current Balance: {account['amount']}")

def transaction_history(account):
    """Displays the transaction history for a specified account."""
    print("📜 Transaction History:")
    found = False
    try:
        with open(TXN_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['account_number'] == account['account_number']:
                    print(f"  - Type: {row['transaction_type']}, Amount: {row['amount']}, Balance: {row['current_balance']}, Time: {row['timestamp']}")
                    found = True
        if not found:
            print("  No transactions found for this account.")
    except FileNotFoundError:
        print("❌ No transactions recorded yet.")

def branch_manager_report():
    """Provides a summary report of all accounts."""
    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            accounts = list(reader)
            
            if not accounts:
                print("No accounts in the bank yet.")
                return

            print("\n🏦 Branch Manager Report")
            print("-----------------------")
            print(f"Total Accounts: {len(accounts)}")
            total_balance = sum(int(acc['amount']) for acc in accounts)
            print(f"Total Balance in Bank: {total_balance}")
            print("-----------------------")
            
    except FileNotFoundError:
        print("❌ No accounts file found.")
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")

def close_account(account):
    """Closes an account by removing it from the bank file."""
    confirm = input(f"Are you sure you want to close account {account['account_number']}? This action is irreversible. (yes/no): ").lower()
    if confirm != "yes":
        print("❌ Account closure cancelled.")
        return

    try:
        with open(BANK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            # Read all accounts except the one to be deleted
            remaining_accounts = [acc for acc in reader if acc['account_number'] != account['account_number']]

        if update_all_accounts(remaining_accounts):
            final_balance = account['amount']
            log_transaction(account['account_number'], "Account Closed", 0, final_balance)
            print(f"✅ Account {account['account_number']} closed successfully. Final Balance was {final_balance}.")
    except Exception as e:
        print(f"An error occurred while closing the account: {e}")


# ----------------- Main Menu ----------------- #

def main():
    """Main function to run the banking system menu."""
    initialize_files()
    while True:
        clear_screen()
        print("\n===== Banking System Menu =====")
        print("1. Create New Account")
        print("2. Access Your Account")
        print("3. Branch Manager Report")
        print("4. Exit")
        
        main_choice = input("Enter choice: ")

        if main_choice == "1":
            create_account()
        elif main_choice == "2":
            acc_no = input("Enter your account number: ").strip()
            if not acc_no:
                print("❌ Account number cannot be empty.")
                input("\nPress Enter to continue...")
                continue
            
            account = find_account(acc_no)
            if not account:
                print("❌ Account not found.")
                input("\nPress Enter to continue...")
                continue
                
            if not authenticate_user(account):
                input("\nPress Enter to continue...")
                continue
            
            # --- Logged-in User Menu ---
            while True:
                clear_screen()
                print(f"\nWelcome, {account['name']} (Acc: {account['account_number']})")
                print("-------------------------")
                print("1. Deposit Money")
                print("2. Withdraw Money")
                print("3. Check Balance")
                print("4. Transaction History")
                print("5. Close Account")
                print("6. Logout")
                user_choice = input("Enter choice: ")

                if user_choice == "1":
                    deposit_money(account)
                elif user_choice == "2":
                    withdraw_money(account)
                elif user_choice == "3":
                    check_balance(account)
                elif user_choice == "4":
                    transaction_history(account)
                elif user_choice == "5":
                    close_account(account)
                    break # Exit user menu after closing account
                elif user_choice == "6":
                    print("👋 Logging out...")
                    break
                else:
                    print("❌ Invalid choice.")
                
                # Refresh account data in case of balance changes
                account = find_account(acc_no) 
                if not account: # If account was closed
                    break
                input("\nPress Enter to continue...")

        elif main_choice == "3":
            branch_manager_report()
        elif main_choice == "4":
            print("👋 Thank you for using the Banking System!")
            break
        else:
            print("❌ Invalid choice, please try again.")
        
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()