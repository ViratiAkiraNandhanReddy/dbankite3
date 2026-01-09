"""Database access layer for dbankite3.

This module provides a thin wrapper around a MySQL database used by
the application. It exposes the `dbankite3ServerQL` class which contains
nested helper classes for table definitions, authentication, registration,
account actions, transactions and administrator operations.

All public methods are documented with short Markdown-style docstrings.
"""

import mysql.connector
from CaesarCipher import Encryption

# Database Connection
connection = mysql.connector.connect(
    host="localhost",
    user="YOUR_USERNAME_HERE",
    password="YOUR_PASSWORD_HERE",
    database="dbankite3"
)

class dbankite3ServerQL:
    """Top-level container for DB operations and helpers.

    The nested classes implement specific areas of DB functionality such
    as table creation, authentication, registration, transactions and
    administrator actions.
    """

    cursor = connection.cursor()

    def __init__(self):
        ...

    def close_connection(self):
        """Close the shared database connection."""
        connection.close()
    
    @classmethod
    def table_exists(cls) -> bool:
        """Return True if the expected tables exist in the database."""
        try:
            cls.cursor.execute('SELECT 1 FROM users LIMIT 1')
            return True
        except: return False

    class table_definitions:

        """Provide methods to create required database tables."""

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor
        
        def define_user_table(self) -> None:
            """Create the `users` table if it does not already exist."""
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password VARCHAR(25) NOT NULL,
                    balance DOUBLE DEFAULT 0
                )
            ''')
            connection.commit()

        def define_administrator_table(self) -> None:
            """Create the administrators table and initialize a default admin password."""
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS administrators (
                    password VARCHAR(25) NOT NULL,
                    notices TEXT)''')
            self.cursor.execute('''
                INSERT INTO administrators (password) VALUES ('333333')
            ''')
            connection.commit()

    class authentication:

        """Authenticate a user's credentials against stored values."""

        def __init__(self, username: str, password: str) -> None:
            """Initialize with `username` and `password` to authenticate."""
            self.cursor = dbankite3ServerQL.cursor
            self.username = username
            self.password = password

        def authenticate_password(self) -> bool:
            """Return True if the provided password matches the stored hash."""
            self.cursor.execute('''
                SELECT password FROM users WHERE username = %s
            ''', (self.username,))
            return self.cursor.fetchone()[0] == Encryption(self.password, shift = 8, alterNumbers = True).encrypt()  # type: ignore  -->  escaping type checker warning.

    class traversal:

        """Utility methods for reading user records and existence checks."""

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def isUserExist(self, username: str) -> bool:
            """Return True if a user with `username` exists."""
            self.cursor.execute('''
                SELECT COUNT(*) FROM users WHERE username = %s
            ''', (username,))
            return self.cursor.fetchone()[0] > 0  # type: ignore  -->  escaping type checker warning.

        def fetch_all_users(self) -> list[tuple]:
            """Return a list of (username, balance) tuples for all users."""
            self.cursor.execute('''
                SELECT username, balance FROM users
            ''')
            return self.cursor.fetchall()  # type: ignore  -->  escaping type checker warning.

    class registration:

        """Register new users into the `users` table."""

        def __init__(self, username: str, password: str) -> None:
            """Initialize a registration helper for `username`/`password`."""
            self.cursor = dbankite3ServerQL.cursor
            self.username = username
            self.password = password

        def register_user(self) -> bool:
            """Insert a new user record. Returns True on success, False on conflict."""
            try:
                self.cursor.execute('''
                    INSERT INTO users (username, password)
                    VALUES (%s, %s)
                ''', (
                    self.username,
                    Encryption(self.password, shift = 8, alterNumbers = True).encrypt(),
                ))
                connection.commit()
                return True
            except mysql.connector.IntegrityError:
                return False
    
    class accountactions:

        """Account modification operations like change password/username/delete."""

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def change_password(self, username: str, new_password: str) -> bool:
            """Set a new password for `username`. Returns True on success."""
            password: str = Encryption(new_password, shift = 8, alterNumbers = True).encrypt()
            self.cursor.execute('''
                UPDATE users SET password = %s WHERE username = %s
            ''', (password, username))
            connection.commit()
            return self.cursor.rowcount > 0
        
        def change_username(self, old_username: str, new_username: str) -> bool:
            """Rename a user's username. Returns True on success."""
            self.cursor.execute('''
                UPDATE users SET username = %s WHERE username = %s
            ''', (new_username, old_username))
            connection.commit()
            return self.cursor.rowcount > 0
        
        def delete_account(self, username: str) -> bool:
            """Delete the user account identified by `username`. Returns True on success."""
            self.cursor.execute('''
                DELETE FROM users WHERE username = %s
            ''', (username,))
            connection.commit()
            return self.cursor.rowcount > 0

    class transactions:

        """Financial transaction helpers for balance inquiries, deposits, withdrawals and transfers."""

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def balance_inquiry(self, username: str) -> float:
            """Return the current balance for `username` (0.0 if not found)."""
            self.cursor.execute('''
                SELECT balance FROM users WHERE username = %s
            ''', (username,))
            balance = self.cursor.fetchone()
            return balance[0] if balance else 0.0  # type: ignore  -->  escaping type checker warning.

        def deposit(self, username: str, amount: float) -> bool:
            """Add `amount` to the user's balance. Returns True on success."""
            self.cursor.execute('''
                UPDATE users SET balance = balance + %s WHERE username = %s
            ''', (amount, username))
            connection.commit()
            return self.cursor.rowcount > 0

        def withdraw(self, username: str, amount: float) -> bool:
            """Subtract `amount` from the user's balance. Returns True on success."""
            self.cursor.execute('''
                UPDATE users SET balance = balance - %s WHERE username = %s
            ''', (amount, username))
            connection.commit()
            return self.cursor.rowcount > 0
        
        def transfer(self, _from: str, _to: str, amount: float) -> bool:
            """Transfer `amount` from `_from` to `_to`. Returns True on success."""
            self.cursor.execute('''
                UPDATE users SET balance = balance - %s WHERE username = %s
            ''', (amount, _from))
            connection.commit()

            self.cursor.execute('''
                UPDATE users SET balance = balance + %s WHERE username = %s
            ''', (amount, _to))
            connection.commit()
            return self.cursor.rowcount > 0
            
    class administrator:

        """Administrator-specific DB operations (auth, notices, cleanup)."""

        def __init__(self) -> None:
            self.cursor = dbankite3ServerQL.cursor

        def authenticate_admin(self, admin_password: str) -> bool:
            """Return True if `admin_password` matches the stored administrator password."""
            self.cursor.execute('''
                SELECT password FROM administrators LIMIT 1
            ''')

            return self.cursor.fetchone()[0] == Encryption(admin_password, shift = 53, alterNumbers = True).encrypt()  # type: ignore  -->  escaping type checker warning.
        
        def change_password(self, _password: str) -> bool:
            """Change the administrator password. Returns True on success."""
            password: str = Encryption(_password, shift = 53, alterNumbers = True).encrypt()
            self.cursor.execute('''
                UPDATE administrators SET password = %s
            ''', (password,))
            connection.commit()
            return self.cursor.rowcount > 0
        
        def notifications(self, msg: str) -> bool:
            """Store a short notification message for administrators."""
            self.cursor.execute('''
                UPDATE administrators SET notices = %s
            ''', (msg,))
            connection.commit()
            return self.cursor.rowcount > 0

        def fetch_notifications(self) -> str:
            """Return the current administrator notice string."""
            self.cursor.execute('''
                SELECT notices FROM administrators LIMIT 1
            ''')
            return self.cursor.fetchone()[0]  # type: ignore  -->  escaping type checker warning.
        
        def delete_all_user_accounts(self) -> bool:
            """Remove all user records. Returns True when rows were deleted."""
            self.cursor.execute('''
                DELETE FROM users
            ''')
            connection.commit()
            return self.cursor.rowcount > 0
