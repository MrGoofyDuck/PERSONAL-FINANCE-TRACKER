from base_dao import BaseDAO

class GoalDAO(BaseDAO):
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY,
                name TEXT,
                target_amount REAL
            )
        """)
        self.commit()

    def set_goal(self, name, amount):
        self.cursor.execute("DELETE FROM goals")  # одна цель
        self.cursor.execute("INSERT INTO goals (name, target_amount) VALUES (?, ?)", (name, amount))
        self.commit()

    def get_goal(self):
        self.cursor.execute("SELECT name, target_amount FROM goals LIMIT 1")
        return self.cursor.fetchone()
    
    def delete(self):
        self.cursor.execute("DELETE FROM goals")
        self.commit()

    def remove_goal(self, name=None):
        if name:
            self.goal = None
            print(f"Goal '{name}' removed.")

        self.goal = None

    def set_new_goal(self, name, amount):
        self.goal = (name, amount)