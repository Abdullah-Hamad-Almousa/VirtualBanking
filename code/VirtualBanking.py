import random
from datetime import datetime

class Account:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.account_id = self._generate_unique_account_id()
        self.balance = initial_balance if initial_balance >= 0 else 0
        self.transaction_history = []
        self.payees = set()

        if initial_balance > 0:
            self._record_transaction("Deposit", initial_balance)

    def _generate_unique_account_id(self):
        return random.randint(10_000_000, 99_999_999)

    def _record_transaction(self, transaction_type, amount, description=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append({
            "timestamp": timestamp,
            "type": transaction_type,
            "amount": amount,
            "description": description
        })

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self._record_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance for withdrawal.")
        self.balance -= amount
        self._record_transaction("Withdrawal", amount)

    def add_payee(self, payee_account_id):
        if not isinstance(payee_account_id, int) or not (10_000_000 <= payee_account_id <= 99_999_999):
            raise ValueError("Invalid payee account ID: must be an 8-digit number.")
        self.payees.add(payee_account_id)

    def transfer(self, payee_account_id, amount, accounts):
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if payee_account_id not in self.payees:
            raise ValueError("Payee not added. Please add the payee before transferring.")
        if amount > self.balance:
            raise ValueError("Insufficient balance for transfer.")
        if payee_account_id not in accounts:
            raise ValueError("Payee account does not exist.")

        self.balance -= amount
        accounts[payee_account_id].balance += amount

        self._record_transaction("Transfer Out", amount, f"To {payee_account_id}")
        accounts[payee_account_id]._record_transaction("Transfer In", amount, f"From {self.account_id}")

    def view_transaction_history(self):
        if not self.transaction_history:
            print("No transactions yet.")
            return
        print(f"\n--- Transaction History for {self.name} (ID: {self.account_id}) ---")
        for tx in self.transaction_history:
            print(f"[{tx['timestamp']}] {tx['type']}: ${tx['amount']:.2f} {tx['description']}")

    def view_details(self):
        print(f"\n--- Account Details ---")
        print(f"Name: {self.name}")
        print(f"Account ID: {self.account_id}")
        print(f"Balance: ${self.balance:.2f}")
        print(f"Payees: {sorted(self.payees) if self.payees else 'None'}")


all_accounts = {}


def create_account():
    name = input("Enter account holder name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    try:
        initial = float(input("Enter initial balance (optional, default $0): ") or 0)
    except ValueError:
        print("Invalid balance. Setting to $0.")
        initial = 0

    while True:
        account = Account(name, initial)
        if account.account_id not in all_accounts:
            all_accounts[account.account_id] = account
            print(f"\nAccount created successfully!")
            print(f"Account ID: {account.account_id}")
            break


def get_account_by_input():
    try:
        acc_id = int(input("Enter your account ID: "))
    except ValueError:
        print("Invalid account ID.")
        return None
    if acc_id not in all_accounts:
        print("Account not found.")
        return None
    return all_accounts[acc_id]


def main():
    print("Welcome to the Virtual Banking Application!")

    while True:
        print("\n" + "="*50)
        print("1. Create an account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Add a payee")
        print("5. Transfer money")
        print("6. View account details")
        print("7. View transaction history")
        print("8. Exit")
        print("="*50)

        try:
            choice = input("Choose an option (1-8): ").strip()
        except EOFError:
            print("\nNo input received. Exiting application.")
            break

        try:
            if choice == "1":
                create_account()

            elif choice == "2":
                account = get_account_by_input()
                if account:
                    amount = float(input("Enter deposit amount: $"))
                    account.deposit(amount)
                    print(f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}")

            elif choice == "3":
                account = get_account_by_input()
                if account:
                    amount = float(input("Enter withdrawal amount: $"))
                    account.withdraw(amount)
                    print(f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}")

            elif choice == "4":
                account = get_account_by_input()
                if account:
                    payee_id = int(input("Enter payee's 8-digit account ID: "))
                    account.add_payee(payee_id)
                    print(f"Payee {payee_id} added.")

            elif choice == "5":
                account = get_account_by_input()
                if account:
                    payee_id = int(input("Enter payee's account ID: "))
                    amount = float(input("Enter transfer amount: $"))
                    account.transfer(payee_id, amount, all_accounts)
                    print(f"Transferred ${amount:.2f} to {payee_id}.")

            elif choice == "6":
                account = get_account_by_input()
                if account:
                    account.view_details()

            elif choice == "7":
                account = get_account_by_input()
                if account:
                    account.view_transaction_history()

            elif choice == "8":
                print("Thank you for using Virtual Banking! Goodbye.")
                break

            else:
                print("Invalid option. Please choose 1-8.")

        except EOFError:
            print("\nInput stream ended unexpectedly. Exiting.")
            break
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()