from base_dao import BaseDAO

class TransactionDAO(BaseDAO):
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                date TEXT,
                category TEXT,
                amount INTEGER,
                type TEXT
            )
        """)
        self.commit()

    def insert_transaction(self, date, category, amount, trans_type):
        self.cursor.execute("""
            INSERT INTO transactions (date, category, amount, type)
            VALUES (?, ?, ?, ?)
        """, (date, category, amount, trans_type))
        self.commit()

    def get_all_transactions(self):
        self.cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        return self.cursor.fetchall()

    def get_summary(self):
        self.cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
        return dict(self.cursor.fetchall())
    
    def delete_all_transactions(self):
        self.cursor.execute("DELETE FROM transactions")
        self.commit()


