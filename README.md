# 🧾 Personal Finance Tracker

This repository contains a simple personal finance tracking application built in Python with a Graphical User Interface (GUI) using PyQt6 and an SQLite database.

---

## 👥 Our Team

- **Aralova Dariya**: 🧠 Code and logic.
- **Sadiev Aiman**: 🎨 Design and GUI.
- **Almazbekov Eldiiar** 🗄️ Databases and documentation.

---

## 📂 Structure

- `main.py` – Launches the application, defines GUI logic and handles user interaction.
- `controls.py` – Acts as a controller that connects GUI actions with the database (uses DAO classes).
- `base_dao.py` – Base Data Access Object class with shared methods for database connection and queries.
- `transaction_dao.py` – Handles operations on the `transactions` table (add, retrieve, summarize, delete).
- `goal_dao.py` – Handles saving goals (multiple goals supported), progress tracking, and deletion.
- `account_dao.py` – (Optional) Manages user account table (add, update, delete).
- `finance.db` – Local SQLite database file created automatically on first run.

---

## 💼 Core Classes

### 👤 TransactionDAO
Handles the logic for storing income and expense records.

**Methods**
- `insert_transaction(date, category, amount, type)`
- `get_all_transactions()`
- `get_summary()` – Returns total income and expenses
- `delete_all_transactions()`

### 🎯 GoalDAO
Allows users to set **multiple savings goals** and track progress.

**Methods**
- `set_goal(name, amount)` – Adds a new goal
- `get_goals()` – Returns all current goals
- `delete_goal_by_id(goal_id)` – Deletes specific goal

### 🧠 FinanceController
Acts as the **bridge between GUI and DAOs**.

**Methods**
- `add_transaction(...)`
- `get_transactions()`
- `get_summary()`
- `set_goal(...)`
- `get_goals()`

---

## 🖥️ GUI Features

- Add income or expense transactions
- View transaction history in a table
- View live progress (%) toward each goal
- Delete goals
- View financial summary: total income, expense, and current balance

---

## 🛠️ Installation and Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/finance-tracker.git
   cd finance-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install PyQt6
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

The application will create `finance.db` automatically in the working directory.

---

## 📊 Planned Features

- [ ] Export transactions to CSV
- [ ] Filter by date range
- [ ] Add support for categories and tags
- [ ] Multi-user login system
- [ ] Dark mode and theme switching

---

## 🖼️ Screenshots

_Add some screenshots here..._

---

## 📄 License

MIT License – free to use, modify, and share.


3. The app will create a local SQLite database named `finance.db` automatically.

---

