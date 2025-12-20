"""User interface components for dbankite3.

This module exposes `UserInterface` which contains interactive
subclasses for user login and account actions used by the CLI.

Classes
- `UserInterface.login`: prompts for username/password and authenticates.
- `UserInterface.actions`: interactive account actions for an authenticated user.
"""

from . import Greeting
from .dbankite3ServerQL import dbankite3ServerQL

class UserInterface:
    """Top-level container for CLI user interaction helpers.

    The nested classes implement specific UI flows: `login` to sign in
    and `actions` to perform account operations.
    """

    class login:
        """Prompt for username and password and authenticate the user.

        On successful authentication this class launches
        `UserInterface.actions` for the authenticated user.
        """

        def __init__(self) -> None:

            self.username = input("USERNAME: ")

            if not self.username:
                print("\033[1;31mdbankite3: USERNAME CANNOT BE EMPTY\033[0m")
                return 

            if not dbankite3ServerQL.traversal().isUserExist(self.username):
                print("\033[1;31mdbankite3: USER DOES NOT EXIST\033[0m")
                return
            
            self.password = input("PASSWORD: ")

            if not self.password:
                print("\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m")
                return

            if not dbankite3ServerQL.authentication(self.username, self.password).authenticate_password():
                print("\033[1;31mdbankite3: INVALID PASSWORD\033[0m")
                return
            
            UserInterface.actions(self.username)

    class actions:
        """Interactive menu for an authenticated user's account actions.

        Methods implement balance inquiry, deposit, withdraw, transfer,
        account closure, password change, and username change flows.
        """

        def __init__(self, username: str) -> None:
            
            self.username = username
            query = False
            while True:
                
                print(f'\n{Greeting}, {self.username}!\n') if not query else lambda: None

                print('''\033[34m
1. BALANCE
2. DEPOSIT
3. WITHDRAW
4. TRANSFER
5. CLOSE ACCOUNT
6. CHANGE PASSWORD
7. CHANGE USERNAME
8. LOGOUT
                      \033[0m''')
                _ = input("\033[2m~\033[0m \033[1;32m$\033[0m\033[33mdbankite3 \033[2m:\033[0m ACTION [1-8] \033[34m>>\033[0m ") ; print("\033c")

                match _:
                    case '1':
                        self.balance()
                    case '2':
                        self.deposit()
                    case '3':
                        self.withdraw()
                    case '4':
                        self.transfer()
                    case '5':
                        _ = self.close_account()
                        if _: break
                    case '6':
                        _ = self.change_passwd()
                        if _: break
                    case '7':
                        self.change_username()
                    case '8':
                        break
                    case _:
                        print('\nINVALID ACTION\n')
                        query = False
                        continue
                    
                query = True

        def balance(self) -> None:
            """Print the current balance for the user.

            Uses the database transactions API to fetch the balance and
            prints it with color-coded severity.
            """
            balance = dbankite3ServerQL.transactions().balance_inquiry(self.username)

            if balance >= 1000: # green
                print(f"\nBALANCE:\033[1;32m $ {balance}\033[0m\n")

            elif 0 < balance < 1000 : # yellow
                print(f"\nBALANCE:\033[1;33m $ {balance}\033[0m\n")

            else: # red
                print(f"\nBALANCE:\033[1;31m $ {balance}\033[0m\n")
        
        def deposit(self) -> None:
            """Prompt for an amount and deposit it into the user's account."""
            amount = float(input('\nENTER AMOUNT: \033[1;32m$ ')) ; print('\033[0m')
            _ = dbankite3ServerQL.transactions().deposit(self.username, amount)
            print("\n\033[1;32mDEPOSIT SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mDEPOSIT UNSUCCESSFUL!\033[0m\n")

        def withdraw(self) -> None:
            """Prompt for an amount and withdraw it from the user's account."""
            amount = float(input('\nENTER AMOUNT: \033[1;33m$ ')) ; print('\033[0m')
            _ = dbankite3ServerQL.transactions().withdraw(self.username, amount)
            print("\n\033[1;32mWITHDRAW SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mWITHDRAW UNSUCCESSFUL!\033[0m\n")
        
        def transfer(self) -> None:
            """Transfer funds from the current user to another user.

            Prompts for recipient username and amount, and performs checks
            before attempting the transfer.
            """
            amount = float(input('\nENTER AMOUNT: \033[1;33m$ ')) ; print('\033[0m')
            _to = input('\nSEND TO <enter username> : \033[1;33m ') ; print('\033[0m')
            _ = dbankite3ServerQL.traversal().isUserExist(_to)
            
            if not _:
                print("\033[1;31mdbankite3: USER DOES NOT EXIST\033[0m")
                return
            
            _ = dbankite3ServerQL.transactions().transfer(self.username, _to, amount)
            print("\n\033[1;32mTRANSFER SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mTRANSFER UNSUCCESSFUL!\033[0m\n")

        def close_account(self) -> bool:
            """Prompt to confirm and delete the current user's account.

            Returns True when the account was deleted successfully.
            """
            _ = input(f"\n\033[1;31mUNDONE EVENT: Are you sure? (YES/NO) : \033[0m")
            if _ == 'YES':
                _password = input("\nENTER PASSWORD TO CONFIRM: ")
                
                if dbankite3ServerQL.authentication(self.username, _password).authenticate_password():
                    _ = dbankite3ServerQL.accountactions().delete_account(self.username)
                    print("\n\033[1;32mDELETION SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mDELETION UNSUCCESSFUL!\033[0m\n")
                    return _
            
            print("\n\033[1;32mDELETION UNSUCCESSFUL!\033[0m\n")
            return False
        
        def change_passwd(self) -> bool:
            """Change the authenticated user's password after confirmation.

            Returns True on success.
            """

            def pw_avoidnesting(password: str) -> bool:
                """Validate a candidate password for a password-change flow.

                Returns True if the password meets minimal length requirements.
                """
                if not password:
                    print("\n\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m") ; return False
                
                if len(password) < 6:
                    print("\n\033[1;31mdbankite3: PASSWORD MUST BE ATLEAST 6 CHARS\033[0m") ; return False

                return True

            _ = input(f"\n\033[1;31mUNDONE EVENT: Are you sure? (YES/NO) : \033[0m")
            if _ == 'YES':

                for i in range(5, 0, -1):
                    
                    print(f'\n#{i} ATTEMPT\'S LEFT')
                    newPassword =  input(f'\nENTER NEW PASSWORD : ')
                    
                    if not pw_avoidnesting(newPassword.strip()) :
                        continue
                    
                    _ = dbankite3ServerQL.accountactions().change_password(self.username, newPassword)
                    print("\n\033[1;32mPASSWORD CHANGE SUCCESSFUL!\033[0m" if _ else "\n\033[1;31mPASSWORD CHANGE UNSUCCESSFUL!\033[0m")
                    return _

            print("\n\033[1;32mPASSWORD CHANGE UNSUCCESSFUL!\033[0m\n")
            return False
        
        def change_username(self) -> None:
            """Change the authenticated user's username after validation."""
            
            def un_avoidnesting(username: str) -> bool:
                """Return True if the proposed username is not already taken."""
                if dbankite3ServerQL.traversal().isUserExist(username):
                    print("\n\033[1;31mdbankite3: USER ALREADY EXIST\033[0m") ; return False
                return True

            for i in range(5, 0, -1):

                print('** TYPE `EXIT` IN NEW USERNAME TO CANCEL **')
                print(f'\n#{i} ATTEMPT\'S LEFT')
                newUsername = input('\nNEW USERNAME: ')
                
                if newUsername == 'EXIT':
                    break

                if not un_avoidnesting(newUsername) :
                    continue
                
                _ = dbankite3ServerQL.accountactions().change_username(self.username, newUsername)
                print("\n\033[1;32mUSERNAME CHANGE SUCCESSFUL!\033[0m" if _ else "\n\033[1;31mUSERNAME CHANGE UNSUCCESSFUL!\033[0m")
                if _: self.username = newUsername

                return
            
            print("\n\033[1;32mUSERNAME CHANGE UNSUCCESSFUL!\033[0m\n")
