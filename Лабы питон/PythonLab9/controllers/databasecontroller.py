import sqlite3
from typing import List, Dict, Any

class DatabaseConnection:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            PRAGMA foreign_keys = ON;
        """)
        cursor.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value REAL,
                nominal INTEGER
            );
        """)
        cursor.execute("""
            CREATE TABLE user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    def get_connection(self):
        return self.conn


class CurrencyRatesCRUD:
    def __init__(self, db: DatabaseConnection):
        self.db = db.conn

    def create(self, data: Dict[str, Any]):
        sql = """
            INSERT INTO currency(num_code, char_code, name, value, nominal)
            VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        cursor = self.db.cursor()
        cursor.execute(sql, data)
        self.db.commit()
        return cursor.lastrowid

    def read_all(self) -> List[sqlite3.Row]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM currency")
        return cursor.fetchall()

    def read_by_char_code(self, char_code: str) -> sqlite3.Row:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM currency WHERE char_code = ?", (char_code,))
        return cursor.fetchone()

    def update(self, char_code: str, value: float):
        cursor = self.db.cursor()
        cursor.execute("UPDATE currency SET value = ? WHERE char_code = ?", (value, char_code))
        self.db.commit()

    def delete(self, currency_id: int):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.db.commit()


class UserCRUD:
    def __init__(self, db: DatabaseConnection):
        self.db = db.conn

    def create(self, name: str):
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO user(name) VALUES(?)", (name,))
        self.db.commit()
        return cursor.lastrowid

    def read_all(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM user")
        return cursor.fetchall()

    def read_by_id(self, user_id: int):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def delete(self, user_id: int):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
        self.db.commit()


class UserCurrencyCRUD:
    def __init__(self, db: DatabaseConnection):
        self.db = db.conn

    def subscribe(self, user_id: int, currency_id: int):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO user_currency(user_id, currency_id) VALUES (?, ?)",
            (user_id, currency_id)
        )
        self.db.commit()

    def get_subscriptions(self, user_id: int):
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT c.* FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        """, (user_id,))
        return cursor.fetchall()