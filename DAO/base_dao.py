import sqlite3
import os

class BaseDAO:
    def __init__(self, db_name=None):
        if db_name is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_name = os.path.join(base_dir, "finance.db")
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

