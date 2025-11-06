import sqlite3
import logging
from CaesarCipher import Encryption

log = logging.FileHandler(r'dbankite3\dbankite3.logs')

# Database Connection
connection = sqlite3.connect(r'dbankite3\db\dbankite3.sqlite3')


class dbankite3ServerQL:

    cursor = connection.cursor()

    def __init__(self):
        # self.cursor = connection.cursor()
        ...

    def close_connection(self):
        self.cursor.close()
        connection.close()

    class table_definitions:

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor
        
        def define_user_table(self) -> None:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(25) NOT NULL,
                    balance REAL DEFAULT 0,
                    recovery_code CHAR(6)
                )
            ''')
            connection.commit()

        def define_administrator_table(self) -> None:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS administrators (
                    admin_name VARCHAR(50) PRIMARY KEY,
                    admin_password VARCHAR(25) NOT NULL
                )
            ''')
            connection.commit()

    class authentication:

        def __init__(self, username: str, password: str) -> None:
            self.cursor = dbankite3ServerQL.cursor
            self.username = username
            self.password = password

        def authenticate_password(self) -> bool:
            self.cursor.execute('''
                SELECT password FROM users WHERE username = ?
            ''', (self.username,))
            return self.cursor.fetchone()[0] == Encryption(self.password, shift = 8, alterNumbers = True).encrypt()

    class transactions:

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def balance_inquiry(self, username: str) -> float:
            self.cursor.execute('''
                SELECT balance FROM users WHERE username = ?
            ''', (username,))
            balance = self.cursor.fetchone()
            return balance[0] if balance else 0.0

        def deposit(self, username: str, amount: float) -> bool:
            self.cursor.execute('''
                UPDATE users SET balance = balance + ? WHERE username = ?
            ''', (amount, username))
            connection.commit()
            return self.cursor.rowcount > 0

        def withdraw(self, username: str, amount: float) -> bool:
            self.cursor.execute('''
                UPDATE users SET balance = balance - ? WHERE username = ?
            ''', (amount, username))
            connection.commit()
            return self.cursor.rowcount > 0
    
    class administrator:

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def authenticate_admin(self, admin_name: str, admin_password: str) -> bool:
            self.cursor.execute('''
                SELECT admin_password FROM administrators WHERE admin_name = ?
            ''', (admin_name,))

            return self.cursor.fetchone()[0] == Encryption(admin_password, shift = 53, alterNumbers = True).encrypt()