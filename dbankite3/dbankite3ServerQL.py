import sqlite3
from CaesarCipher import Encryption

# Database Connection
connection = sqlite3.connect(r'dbankite3\db\dbankite3.sqlite3')

class dbankite3ServerQL:

    cursor = connection.cursor()

    def __init__(self):
        ...

    def close_connection(self):
        connection.close()
    
    @classmethod
    def table_exists(cls) -> bool:
        try:
            dbankite3ServerQL.cursor.execute('SELECT * FROM users')
            return True
        except: return False

    class table_definitions:

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor
        
        def define_user_table(self) -> None:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(25) NOT NULL,
                    balance REAL DEFAULT 0
                )
            ''')
            connection.commit()

        def define_administrator_table(self) -> None:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS administrators (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(25) NOT NULL)
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

    class traversal:

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def isUserExist(self, username: str) -> bool:
            self.cursor.execute('''
                SELECT COUNT(*) FROM users WHERE username = ?
            ''', (username,))
            return self.cursor.fetchone()[0] > 0

    class registration:

        def __init__(self, username: str, password: str) -> None:
            self.cursor = dbankite3ServerQL.cursor
            self.username = username
            self.password = password

        def register_user(self) -> bool:
            try:
                self.cursor.execute('''
                    INSERT INTO users (username, password)
                    VALUES (?, ?)
                ''', (
                    self.username,
                    Encryption(self.password, shift = 8, alterNumbers = True).encrypt(),
                ))
                connection.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    class accountactions:

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def change_password(self, username: str, new_password: str) -> bool:
            password: str = Encryption(new_password, shift = 8, alterNumbers = True).encrypt()
            self.cursor.execute('''
                UPDATE users SET password = ? WHERE username = ?
            ''', (password, username))
            connection.commit()
            return self.cursor.rowcount > 0
        
        def change_username(self, old_username: str, new_username: str) -> bool:
            self.cursor.execute('''
                UPDATE users SET username = ? WHERE username = ?
            ''', (new_username, old_username))
            connection.commit()
            return self.cursor.rowcount > 0
        
        def delete_account(self, username: str) -> bool:
            self.cursor.execute('''
                DELETE FROM users WHERE username = ?
            ''', (username,))
            connection.commit()
            return self.cursor.rowcount > 0

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
        
        def transfer(self, _from: str, _to: str, amount: float) -> bool:
            self.cursor.execute('''
                UPDATE users SET balance = balance - ? WHERE username = ?
            ''', (amount, _from))
            connection.commit()

            self.cursor.execute('''
                UPDATE users SET balance = balance + ? WHERE username = ?
            ''', (amount, _to))
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
        