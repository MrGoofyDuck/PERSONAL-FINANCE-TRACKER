from account_dao import AccountDAO
from transaction_dao import TransactionDAO
from goal_dao import GoalDAO

class FinanceController:
    def __init__(self):
        self.goal_dao = GoalDAO()
        self.transaction_dao = TransactionDAO()
        self.goal_dao.create_table()
        self.transaction_dao.create_table()
        self.account_dao = AccountDAO()
        self.account_dao.create_table()

    def add_transaction(self, date, category, amount, trans_type):
        self.transaction_dao.insert_transaction(date, category, amount, trans_type)

    def get_transactions(self):
        return self.transaction_dao.get_all_transactions()

    def delete_all_transactions(self):
        return self.transaction_dao.delete_all_transactions()

    def get_summary(self):
        return self.transaction_dao.get_summary()

    def set_goal(self, name, amount):
        self.goal_dao.set_goal(name, amount)

    def get_goal(self):
        return self.goal_dao.get_goal()

    def get_all_accounts(self):
        return self.account_dao.get_all_accounts()

    def remove_goal(self):
        self.goal_dao.remove_goal()

    def set_new_goal(self, name, amount):
        return self.goal_dao.set_goal(name, amount)
