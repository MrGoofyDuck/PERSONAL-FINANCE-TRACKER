# PERSONAL-FINANCE-TRACKER

A simple desktop application for tracking your personal finances, built with Python, PyQt6, and SQLite. It allows users to record income and expenses, set savings goals, and monitor progress toward financial targets.

## ⚙️ Features

- 📅 Add transactions with date, category, amount, and type (Income/Expense)
- 📊 View all transactions in a table
- 📈 Automatic calculation of goal progress
- 🧾 Delete goals or all transaction history
- 📋 View overall financial summary (Income, Expense, Balance)

---

## 🛠️ Technologies Used

- Python 3.10+
- PyQt6
- SQLite3

## 📂 Project Structure

```
📁 finance-tracker/
├── main.py               # GUI implementation using PyQt6
├── controls.py           # Controller connecting GUI and data logic
├── base_dao.py           # Base DAO class for database operations
├── transaction_dao.py    # Handles 'transactions' table
├── goal_dao.py           # Handles 'goals' table (multiple goals supported)
├── account_dao.py        # (Optional) handles 'accounts' table
└── finance.db            # SQLite database file (auto-generated)
```

---

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   pip install PyQt6
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. The app will create a local SQLite database named `finance.db` automatically.

---

