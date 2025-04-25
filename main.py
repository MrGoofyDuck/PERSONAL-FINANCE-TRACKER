import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QDialog, QLineEdit, QComboBox, QDateEdit,
    QMessageBox, QTableWidget, QTableWidgetItem, QDialogButtonBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from controls import FinanceController

ICON_MAP = {
    "Delete Account": "❎",
    "Accounts": "🏦",
    "Transaction": "➕",
    "Goal": "🚩",
    "Delete History": "🗑️",
    "View Summary": "📊",
    "Remove Goal": "❌",
    "Set New Goal": "⭘",
    "View Tables": "🧾"
}

class SetGoalDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Set Goal")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #1e1235; color: #ffe5ec;")

        layout = QVBoxLayout()

        self.goal_name_input = QLineEdit()
        self.goal_name_input.setPlaceholderText("Goal Name")
        layout.addWidget(QLabel("Goal Name:"))
        layout.addWidget(self.goal_name_input)

        self.goal_amount_input = QLineEdit()
        self.goal_amount_input.setPlaceholderText("Goal Amount")
        layout.addWidget(QLabel("Goal Amount:"))
        layout.addWidget(self.goal_amount_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.set_goal)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def set_goal(self):
        name = self.goal_name_input.text()
        try:
            amount = float(self.goal_amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount.")
            return
        self.controller.set_goal(name, amount)
        income = sum(t[3] for t in self.controller.get_transactions() if t[4] == "Income")
        if income >= amount:
            QMessageBox.information(self, "Goal Completed", f"Congratulations! You reached your goal: {name}")
        income = sum(t[3] for t in self.controller.get_transactions() if t[4] == "Income")
        if income >= amount:
                    QMessageBox.information(self, "Goal Set", f"Goal '{name}' set for {amount}.")
        self.parent().update_goal_label()
        self.accept()


class TransactionDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Add Transaction")
        self.setFixedSize(300, 250)
        self.setStyleSheet("background-color: #1e1235; color: #ffe5ec;")

        layout = QVBoxLayout()

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense"])
        layout.addWidget(QLabel("Type:"))
        layout.addWidget(self.type_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.add_transaction)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def add_transaction(self):
        goal = self.controller.get_goal()
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.text()
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number.")
            return
        trans_type = self.type_input.currentText()
        self.controller.add_transaction(date, category, amount, trans_type)
        if goal:
            income = sum(t[3] for t in self.controller.get_transactions() if t[4] == "Income")
            if income >= goal[1]:
                QMessageBox.information(self, "Goal Completed", f"Congratulations! You reached your goal: {goal[0]}")
        self.parent().update_balance_label()
        self.parent().update_goal_label()
        self.accept()


class FinanceMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.setFixedSize(500, 750)
        self.setStyleSheet("background-color: #1e1235; color: #ffe5ec;")

        self.controller = FinanceController()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        header = QLabel("Personal Finance Tracker")
        header.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        header.setStyleSheet("color: #fcd5ce;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        balance_label = QLabel("Balance")
        balance_label.setFont(QFont("Arial", 16))
        balance_label.setStyleSheet("color: #b197fc;")
        balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(balance_label)

        self.balance_value = QLabel("$0.00")
        self.balance_value.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.balance_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.balance_value)

        self.goal_label = QLabel("No goal set.")
        self.goal_label.setFont(QFont("Arial", 14))
        self.goal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.goal_label)

        layout.addSpacing(20)

        button_data = [
            ("Delete Account", self.delete_account_dialog),
            ("Accounts", self.open_account_dialog),
            ("Transaction", self.open_transaction_dialog),
            ("Goal", self.open_goal_dialog),
            ("Delete History", self.delete_history),
            ("View Summary", self.show_summary),
            ("Remove Goal", self.remove_goal),
                        ("View Tables", self.open_view_tables_dialog),
        ]

        button_rows = [button_data[i:i + 2] for i in range(0, len(button_data), 2)]
        for row in button_rows:
            row_layout = QHBoxLayout()
            for label, func in row:
                button = QPushButton(f"{ICON_MAP[label]}\n{label}")
                button.setFixedSize(160, 90)
                button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2c1a4a;
                        color: #ffe5ec;
                        border: none;
                        border-radius: 20px;
                    }
                    QPushButton:hover {
                        background-color: #3e2a5f;
                    }
                """)
                button.clicked.connect(func)
                row_layout.addWidget(button)
            layout.addLayout(row_layout)

        layout.addStretch()
        central_widget.setLayout(layout)
        self.update_balance_label()
        self.update_goal_label()

    def open_transaction_dialog(self):
        dialog = TransactionDialog(self.controller, self)
        dialog.exec()

    def open_goal_dialog(self):
        dialog = SetGoalDialog(self.controller, self)
        dialog.exec()

    def open_view_tables_dialog(self):
        class ViewTablesDialog(QDialog):
            def __init__(self, controller, parent=None):
                super().__init__(parent)
                self.controller = controller
                self.setWindowTitle("View Tables")
                self.setFixedSize(700, 500)
                self.setStyleSheet("background-color: #1e1235; color: #ffe5ec;")

                layout = QVBoxLayout()

                self.button_layout = QHBoxLayout()
                self.accounts_button = QPushButton("Accounts")
                self.transactions_button = QPushButton("Transactions")
                self.goals_button = QPushButton("Goals")

                for btn in [self.accounts_button, self.transactions_button, self.goals_button]:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #2c1a4a;
                            color: #ffe5ec;
                            border-radius: 10px;
                            padding: 6px 12px;
                        }
                        QPushButton:hover {
                            background-color: #3e2a5f;
                        }
                    """)
                    self.button_layout.addWidget(btn)

                layout.addLayout(self.button_layout)

                self.table = QTableWidget()
                layout.addWidget(self.table)
                self.setLayout(layout)

                self.accounts_button.clicked.connect(self.show_accounts_table)
                self.transactions_button.clicked.connect(self.show_transactions_table)
                self.goals_button.clicked.connect(self.show_goals_table)

                def delete_account(self, acc_id):
                    confirm = QMessageBox.question(self, "Confirm Delete", f"Delete account ID {acc_id}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if confirm == QMessageBox.StandardButton.Yes:
                        self.controller.account_dao.delete_account(acc_id)
                        QMessageBox.information(self, "Deleted", f"Account ID {acc_id} deleted.")
                        self.show_accounts_table()

                self.show_transactions_table()

            def show_accounts_table(self):
                data = self.controller.get_all_accounts()
                self.table.setRowCount(len(data))
                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(["ID", "Account Name", "Balance", "Actions"])
                for row, (id, name, balance) in enumerate(data):
                    self.table.setItem(row, 0, QTableWidgetItem(str(id)))
                    self.table.setItem(row, 1, QTableWidgetItem(str(name)))
                    self.table.setItem(row, 2, QTableWidgetItem(str(balance)))
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, acc_id=id: self.delete_account(acc_id))
                    self.table.setCellWidget(row, 3, delete_button)

            def show_transactions_table(self):
                data = self.controller.get_transactions()
                self.table.setRowCount(len(data))
                self.table.setColumnCount(4)
                self.table.setHorizontalHeaderLabels(["Date", "Category", "Amount", "Type"])
                for row_num, row_data in enumerate(data):
                    for col, item in enumerate(row_data[1:]):
                        self.table.setItem(row_num, col, QTableWidgetItem(str(item)))

            def show_goals_table(self):
                goal = self.controller.get_goal()
                self.table.setRowCount(1 if goal else 0)
                self.table.setColumnCount(2)
                self.table.setHorizontalHeaderLabels(["Goal Name", "Target Amount"])
                if goal:
                    name, amount = goal
                    self.table.setItem(0, 0, QTableWidgetItem(name))
                    self.table.setItem(0, 1, QTableWidgetItem(str(amount)))

        dialog = ViewTablesDialog(self.controller, self)
        dialog.exec()

    def delete_history(self):
        self.controller.delete_all_transactions()
        self.update_balance_label()
        self.update_goal_label()
        QMessageBox.information(self, "History Deleted", "Transaction history and goals have been deleted.")

    def show_summary(self):
        income = sum(t[3] for t in self.controller.get_transactions() if t[4] == "Income")
        expense = sum(t[3] for t in self.controller.get_transactions() if t[4] == "Expense")
        QMessageBox.information(self, "Summary", f"Income: {income}\nExpense: {expense}\nNet: {income - expense}")

    def remove_goal(self):
        self.controller.remove_goal()
        self.controller.goal_dao.delete()  # Make sure delete() exists in goal_dao
        self.update_goal_label()
        QMessageBox.information(self, "Goal Removed", "Goal has been removed.")

    def update_balance_label(self):
        balance = sum(t[3] if t[4] == "Income" else -t[3] for t in self.controller.get_transactions())
        self.balance_value.setText(f"${balance:.2f}")

    def open_account_dialog(self):
        class AddAccountDialog(QDialog):
            def __init__(self, controller, parent=None):
                super().__init__(parent)
                self.controller = controller
                self.setWindowTitle("Add Account")
                self.setFixedSize(300, 200)
                self.setStyleSheet("background-color: #1e1235; color: #ffe5ec;")

                layout = QVBoxLayout()

                self.name_input = QLineEdit()
                self.name_input.setPlaceholderText("Account Name")
                layout.addWidget(QLabel("Account Name:"))
                layout.addWidget(self.name_input)

                self.balance_input = QLineEdit()
                self.balance_input.setPlaceholderText("Initial Balance")
                layout.addWidget(QLabel("Initial Balance:"))
                layout.addWidget(self.balance_input)

                buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
                buttons.accepted.connect(self.save_account)
                buttons.rejected.connect(self.reject)
                layout.addWidget(buttons)

                self.setLayout(layout)

            def save_account(self):
                name = self.name_input.text()
                try:
                    balance = float(self.balance_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Input Error", "Please enter a valid balance.")
                    return
                self.controller.account_dao.insert_account(name, balance)
                QMessageBox.information(self, "Account Added", f"Account '{name}' with balance ${balance:.2f} added.")
                self.accept()

        dialog = AddAccountDialog(self.controller, self)
        dialog.exec()


    def delete_account_dialog(self):
        class DeleteAccountDialog(QDialog):
            def __init__(self, controller, parent=None):
                super().__init__(parent)
                self.controller = controller
                self.setWindowTitle("Delete Account")
                self.setFixedSize(300, 150)
                self.setStyleSheet("background-color: #1e1235; color: #ffe5ec;")

                layout = QVBoxLayout()

                self.account_id_input = QLineEdit()
                self.account_id_input.setPlaceholderText("Enter Account ID to delete")
                layout.addWidget(QLabel("Account ID:"))
                layout.addWidget(self.account_id_input)

                buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
                buttons.accepted.connect(self.confirm_delete)
                buttons.rejected.connect(self.reject)
                layout.addWidget(buttons)

                self.setLayout(layout)

            def confirm_delete(self):
                try:
                    acc_id = int(self.account_id_input.text())
                except ValueError:
                    QMessageBox.warning(self, "Input Error", "Please enter a valid numeric Account ID.")
                    return

                confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete account ID {acc_id}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if confirm == QMessageBox.StandardButton.Yes:
                    self.controller.account_dao.delete_account(acc_id)
                    QMessageBox.information(self, "Deleted", f"Account ID {acc_id} has been deleted.")
                    self.accept()

        dialog = DeleteAccountDialog(self.controller, self)
        dialog.exec()


    def update_goal_label(self):
        goal = self.controller.get_goal()
        if goal:
            income = sum(t[3] for t in self.controller.get_transactions() if t[4] == "Income")
            percent = min((income / goal[1]) * 100, 100)
            self.goal_label.setText(f"Goal: {goal[0]} - ${goal[1]:.2f} ({percent:.1f}%)")
        else:
            self.goal_label.setText("No goal set.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceMainWindow()
    window.show()
    sys.exit(app.exec())
