from base_dao import BaseDAO

class AccountDAO(BaseDAO):
    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS accounts")  # Force recreate
        self.cursor.execute("""
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance INTEGER DEFAULT 0
            )
        """)
        self.commit()

    def insert_account(self, name, balance=0.0):
        self.cursor.execute("""
            INSERT INTO accounts (name, balance)
            VALUES (?, ?)
        """, (name, balance))
        self.commit()

    def get_all_accounts(self):
        self.cursor.execute("SELECT id, name, balance FROM accounts")
        return self.cursor.fetchall()

    def update_balance(self, account_id, new_balance):
        self.cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE id = ?
        """, (new_balance, account_id))
        self.commit()

    def delete_account(self, account_id):
        self.cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        self.commit()
