# 🏦 Basic Banking System in Python

This is a simple object-oriented banking system written in Python. It supports savings and checking accounts, deposits, withdrawals, transfers, interest application, and transaction history tracking.

## 📦 Features

- Create and manage different types of accounts:
  - **SavingsAccount** with interest and minimum balance
  - **CheckingAccount** with overdraft support
- Deposit and withdraw funds
- Enforce minimum balance and overdraft limits
- Transfer money between accounts
- View transaction history
- Track balance updates

## 🧱 Class Overview

### `Bank`
- `create_account(...)`: Create new accounts (savings or checking)
- `get_account(...)`: Get an account by its number
- `transfer(...)`: Transfer money between accounts

### `Account` *(Abstract Base Class)*
- Common logic for all account types
- `deposit(...)`, `get_balance()`, `get_transaction_history()`
- `withdraw(...)` must be implemented in subclasses

### `SavingsAccount(Account)`
- Withdrawals must not reduce balance below `min_balance`
- Automatically apply interest via `apply_interest()`

### `CheckingAccount(Account)`
- Allows overdraft up to a configurable limit

### `Transaction`
- Represents a single transaction (`deposit`, `withdrawal`, or `interest`)

## 🧪 Example Usage

```python
bank = Bank("MyBank")
bank.create_account("savings", "S123", "Alice", 500, interest_rate=0.02)
bank.create_account("checking", "C456", "Bob", 1000, overdraft_limit=200)

success, message = bank.transfer("C456", "S123", 300)
print(message)  # Transferred $300.00 from C456 to S123


Author
Created by Nándor Forgó
📧 nfori.coding@gmail.com
