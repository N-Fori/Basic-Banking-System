from abc import ABC, abstractmethod


class Transaction:
    def __init__(self, transaction_type, amount, account):
        self.transaction_type = transaction_type
        self.amount = amount
        self.account = account

    def __str__(self):
        return f"{self.transaction_type.title()} - ${self.amount:.2f}"


class Account(ABC):
    def __init__(self, account_number, owner_name, balance=0):
        self.account_number = account_number
        self.owner_name = owner_name
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount <= 0:
            return False, "Deposit amount must be positive"

        self.balance += amount
        transaction = Transaction("deposit", amount, self)
        self.transaction_history.append(transaction)
        return True, f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}"

    @abstractmethod
    def withdraw(self, amount):
        pass

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history


class SavingsAccount(Account):
    def __init__(self, account_number, owner_name, balance=0, interest_rate=0.01, min_balance=100):
        super().__init__(account_number, owner_name, balance)
        self.interest_rate = interest_rate
        self.min_balance = min_balance

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be positive"

        if self.balance - amount < self.min_balance:
            return False, f"Cannot withdraw below minimum balance of ${self.min_balance:.2f}"

        self.balance -= amount
        transaction = Transaction("withdrawal", amount, self)
        self.transaction_history.append(transaction)
        return True, f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        transaction = Transaction("interest", interest, self)
        self.transaction_history.append(transaction)
        return True, f"Applied interest: ${interest:.2f}. New balance: ${self.balance:.2f}"


class CheckingAccount(Account):
    def __init__(self, account_number, owner_name, balance=0, overdraft_limit=100):
        super().__init__(account_number, owner_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be positive"

        if self.balance - amount < -self.overdraft_limit:
            return False, f"Cannot exceed overdraft limit of ${self.overdraft_limit:.2f}"

        self.balance -= amount
        transaction = Transaction("withdrawal", amount, self)
        self.transaction_history.append(transaction)

        if self.balance < 0:
            return True, f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f} (Overdraft)"
        return True, f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, account_type, account_number, owner_name, initial_balance=0, **kwargs):
        if account_number in self.accounts:
            return False, "Account number already exists"

        if account_type.lower() == "savings":
            account = SavingsAccount(account_number, owner_name, initial_balance, **kwargs)
        elif account_type.lower() == "checking":
            account = CheckingAccount(account_number, owner_name, initial_balance, **kwargs)
        else:
            return False, "Invalid account type"

        self.accounts[account_number] = account
        return True, f"{account_type.title()} account created successfully"

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def transfer(self, from_account_number, to_account_number, amount):
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)

        if not from_account or not to_account:
            return False, "One or both accounts not found"

        # Try to withdraw from source account
        success, message = from_account.withdraw(amount)
        if not success:
            return False, f"Transfer failed: {message}"

        # Deposit to destination account
        to_account.deposit(amount)
        return True, f"Transferred ${amount:.2f} from {from_account_number} to {to_account_number}"

# Example usage:
# bank = Bank("MyBank")
# bank.create_account("savings", "S123", "Alice", 500, interest_rate=0.02)
# bank.create_account("checking", "C456", "Bob", 1000, overdraft_limit=200)
# bank.transfer("C456", "S123", 300)