import sqlite3
import random
import datetime
import re
import hashlib
import os
import sys

# --- Constants ---
DATABASE_FILE = "bank.db"

# ----------------- Helper Functions ----------------- #

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def log_transaction(cursor, acc_no, txn_type, amount, balance, details=""):
    """Logs a transaction to the database."""
    timestamp = datetime.datetime.now()
    try:
        cursor.execute("""
            INSERT INTO transactions (account_number, transaction_type, details, amount, current_balance, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (acc_no, txn_type, details, amount, balance, timestamp))
    except sqlite3.Error as e:
        # This error is critical but shouldn't stop the main transaction from committing.
        print(f"Warning: Failed to log transaction. {e}")

# ----------------- Object-Oriented Core ----------------- #

class Account:
    """Represents a single bank account, holding its data and operations."""
    def __init__(self, account_number, name, mail, mobile_num, address, balance, pin_hash):
        self.account_number = account_number
        self.name = name
        self.mail = mail
        self.mobile_num = mobile_num
        self.address = address
        self.balance = int(balance)
        self.pin_hash = pin_hash

    def deposit(self, amount):
        """Updates the balance in memory. Does NOT commit to DB."""
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return False
        self.balance += amount
        return True

    def withdraw(self, amount):
        """Updates the balance in memory. Does NOT commit to DB."""
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return False
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return False
        self.balance -= amount
        return True

    def authenticate(self, pin):
        """Hashes the provided pin and compares it to the stored hash."""
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        return hashed_pin == self.pin_hash

class Bank:
    """Manages all accounts and database interactions."""
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row # Allows accessing columns by name
        self.cursor = self.conn.cursor()
        self._create_tables()
        self.accounts = self._load_accounts()

    def _create_tables(self):
        """Creates the database tables if they don't exist."""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    mail TEXT UNIQUE NOT NULL,
                    mobile_num TEXT UNIQUE NOT NULL,
                    address TEXT,
                    balance INTEGER NOT NULL,
                    pin_hash TEXT NOT NULL
                )
            ''')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_number TEXT NOT NULL,
                    transaction_type TEXT NOT NULL,
                    details TEXT,
                    amount INTEGER NOT NULL,
                    current_balance INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (account_number) REFERENCES accounts (account_number)
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database Error: Could not create tables. {e}")
            sys.exit(1)

    def _load_accounts(self):
        """Loads all accounts from the database into a dictionary of Account objects."""
        accounts = {}
        try:
            self.cursor.execute("SELECT * FROM accounts")
            rows = self.cursor.fetchall()
            for row in rows:
                acc = Account(**dict(row))
                accounts[acc.account_number] = acc
        except sqlite3.Error as e:
            print(f"Database Error: Could not load accounts. {e}")
            sys.exit(1)
        return accounts
    
    def _commit_change(self, query, params=()):
        """Executes a query and commits it. Generic helper for single operations."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            self.conn.rollback()
            return False

    def _insert_account(self, account):
        """Inserts a new account object into the database."""
        query = """
            INSERT INTO accounts (account_number, name, mail, mobile_num, address, balance, pin_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            account.account_number, account.name, account.mail,
            account.mobile_num, account.address, account.balance, account.pin_hash
        )
        return self._commit_change(query, params)
    
    def _delete_account_record(self, account_number):
        """Deletes an account and its transactions from the database."""
        self._commit_change("DELETE FROM transactions WHERE account_number = ?", (account_number,))
        return self._commit_change("DELETE FROM accounts WHERE account_number = ?", (account_number,))

    def find_account(self, acc_no):
        return self.accounts.get(acc_no)

    def create_account(self):
        # ... (User input gathering is the same as the OOP version) ...
        clear_screen()
        print("--- Create New Bank Account ---")
        name = input("Enter your name: ")
        while True:
            mail = input("Enter your email-id: ")
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail):
                print("❌ Invalid email format.")
            elif any(acc.mail == mail for acc in self.accounts.values()):
                print("❌ This email is already registered.")
            else: break
        while True:
            mobile_num = input("Enter your 10-digit mobile number: ")
            if not (mobile_num.isdigit() and len(mobile_num) == 10):
                print("❌ Invalid mobile number. Must be 10 digits.")
            elif any(acc.mobile_num == mobile_num for acc in self.accounts.values()):
                print("❌ This mobile number is already registered.")
            else: break
        while True:
            pin = input("Create a 4-digit PIN for your account: ")
            if pin.isdigit() and len(pin) == 4:
                pin_hash = hashlib.sha256(pin.encode()).hexdigest()
                break
            else: print("❌ PIN must be exactly 4 digits.")
        address = input("Enter your address: ")
        while True:
            try:
                balance = int(input("Enter the initial deposit amount (>= 0): "))
                if balance >= 0: break
                else: print("❌ Initial deposit cannot be negative.")
            except ValueError: print("❌ Invalid amount.")
        account_number = str(random.randint(1000000000, 9999999999))
        
        new_account = Account(account_number, name, mail, mobile_num, address, balance, pin_hash)
        
        if self._insert_account(new_account):
            self.accounts[account_number] = new_account
            log_transaction(self.cursor, account_number, "Account Created", balance, balance)
            self.conn.commit()
            print(f"\n✅ Account created successfully! Your Account Number is {account_number}")
        else:
            print("❌ Failed to create account in database.")

    def close_account(self, account):
        confirm = input(f"Are you sure you want to close account {account.account_number}? (yes/no): ").lower()
        if confirm != "yes":
            print("❌ Account closure cancelled.")
            return

        if self._delete_account_record(account.account_number):
            del self.accounts[account.account_number]
            print(f"✅ Account {account.account_number} closed permanently.")
        else:
            print("❌ Error closing account.")
            
    def transfer_money(self, source_account):
        dest_acc_no = input("Enter the destination account number: ").strip()
        if dest_acc_no == source_account.account_number:
            print("❌ You cannot transfer money to your own account.")
            return
        dest_account = self.find_account(dest_acc_no)
        if not dest_account:
            print("❌ Destination account not found.")
            return
        try:
            amount = int(input("Enter amount to transfer: "))
            if amount <= 0:
                print("❌ Transfer amount must be positive.")
                return
            if amount > source_account.balance:
                print("❌ Insufficient balance for this transfer.")
                return
        except ValueError:
            print("❌ Invalid amount entered.")
            return

        # --- Atomic Transaction Starts Here ---
        try:
            # 1. Update balances in memory first for logging
            source_account.balance -= amount
            dest_account.balance += amount
            
            # 2. Execute both updates in the database
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (source_account.balance, source_account.account_number))
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (dest_account.balance, dest_account.account_number))
            
            # 3. Log both transactions
            log_transaction(self.cursor, source_account.account_number, "Transfer Out", amount, source_account.balance, f"To: {dest_acc_no}")
            log_transaction(self.cursor, dest_acc_no, "Transfer In", amount, dest_account.balance, f"From: {source_account.account_number}")
            
            # 4. Commit ONLY after all operations succeed
            self.conn.commit()
            print(f"✅ Successfully transferred {amount} to account {dest_acc_no}.")

        except sqlite3.Error as e:
            # 5. If any step fails, roll everything back
            self.conn.rollback()
            source_account.balance += amount # Revert in-memory changes too
            dest_account.balance -= amount
            print(f"❌ Transaction failed and has been rolled back: {e}")

    def branch_manager_report(self):
        # ... (This function remains largely the same) ...
        clear_screen()
        print("\n🏦 Branch Manager Report")
        print("-----------------------")
        if not self.accounts:
            print("No accounts in the bank yet.")
            return
        print(f"Total Accounts: {len(self.accounts)}")
        total_balance = sum(acc.balance for acc in self.accounts.values())
        print(f"Total Balance in Bank: {total_balance}")
        print("-----------------------")
        
# ----------------- Main Application UI ----------------- #

def main():
    the_bank = Bank(DATABASE_FILE)
    
    while True:
        clear_screen()
        print("\n===== Banking System Menu =====")
        print("1. Create New Account")
        print("2. Access Your Account")
        print("3. Branch Manager Report")
        print("4. Exit")
        
        main_choice = input("Enter choice: ").strip()

        if main_choice == "1":
            the_bank.create_account()
        elif main_choice == "2":
            acc_no = input("Enter your account number: ").strip()
            account = the_bank.find_account(acc_no)
            
            if not account:
                print("❌ Account not found.")
            else:
                pin = input("Enter your 4-digit PIN: ")
                if account.authenticate(pin):
                    # --- Logged-in User Menu ---
                    while True:
                        clear_screen()
                        print(f"\nWelcome, {account.name} (Acc: {account.account_number})")
                        print("-------------------------")
                        print("1. Deposit Money")
                        print("2. Withdraw Money")
                        print("3. Transfer Money")
                        print("4. Check Balance")
                        print("5. Transaction History")
                        print("6. Close Account")
                        print("7. Logout")
                        user_choice = input("Enter choice: ").strip()

                        if user_choice == "1":
                            try:
                                amount = int(input("Enter amount to deposit: "))
                                if account.deposit(amount):
                                    query = "UPDATE accounts SET balance = ? WHERE account_number = ?"
                                    if the_bank._commit_change(query, (account.balance, account.account_number)):
                                        log_transaction(the_bank.cursor, account.account_number, "Deposit", amount, account.balance)
                                        the_bank.conn.commit()
                                        print(f"✅ Deposit successful. New Balance: {account.balance}")
                                    else:
                                        account.balance -= amount # Rollback in-memory
                            except ValueError:
                                print("❌ Invalid amount.")
                        elif user_choice == "2":
                            try:
                                amount = int(input("Enter amount to withdraw: "))
                                if account.withdraw(amount):
                                    query = "UPDATE accounts SET balance = ? WHERE account_number = ?"
                                    if the_bank._commit_change(query, (account.balance, account.account_number)):
                                        log_transaction(the_bank.cursor, account.account_number, "Withdrawal", amount, account.balance)
                                        the_bank.conn.commit()
                                        print(f"✅ Withdrawal successful. New Balance: {account.balance}")
                                    else:
                                        account.balance += amount # Rollback in-memory
                            except ValueError:
                                print("❌ Invalid amount.")
                        elif user_choice == "3":
                            the_bank.transfer_money(account)
                        elif user_choice == "4":
                            print(f"💰 Current Balance: {account.balance}")
                        elif user_choice == "5":
                            display_transaction_history(the_bank.cursor, account.account_number)
                        elif user_choice == "6":
                            the_bank.close_account(account)
                            break
                        elif user_choice == "7":
                            print("👋 Logging out...")
                            break
                        else:
                            print("❌ Invalid choice.")
                        input("\nPress Enter to continue...")
                else:
                    print("❌ Authentication failed. Incorrect PIN.")
        elif main_choice == "3":
            the_bank.branch_manager_report()
        elif main_choice == "4":
            the_bank.conn.close()
            print("👋 Thank you for using the Banking System!")
            break
        else:
            print("❌ Invalid choice, please try again.")
        
        input("\nPress Enter to return to the main menu...")

def display_transaction_history(cursor, acc_no):
    print("\n📜 Transaction History:")
    try:
        cursor.execute(
            "SELECT * FROM transactions WHERE account_number = ? ORDER BY timestamp DESC",
            (acc_no,)
        )
        transactions = cursor.fetchall()
        if not transactions:
            print("  No transactions found for this account.")
            return

        for row in transactions:
            print(f"  - Time: {row['timestamp']}")
            print(f"    Type: {row['transaction_type']}, Amount: {row['amount']}, Balance: {row['current_balance']}")
            if row['details']:
                print(f"    Details: {row['details']}")
    except sqlite3.Error as e:
        print(f"Could not retrieve transaction history: {e}")

if __name__ == "__main__":
    main()

