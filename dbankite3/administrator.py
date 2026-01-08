"""Administrator CLI utilities for dbankite3.

Provides an interactive administrator panel to inspect users,
send notices, change admin password, and manage user accounts.
"""

from .dbankite3ServerQL.SQLite3 import dbankite3ServerQL
import subprocess, time

class administrator:
    """Container for administrator login and action flows.

    Nested classes implement authentication and the interactive
    administrator menu.
    """
    
    def __init__(self):
        pass

    class login:
        """Prompt for the administrator password and authenticate.

        On successful authentication it launches `administrator.actions`.
        """

        def __init__(self) -> None:

            self.password = input("PASSWORD: ")
            
            if not self.password:
                print("\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m")
                return

            if not dbankite3ServerQL.administrator().authenticate_admin(self.password):
                print("\033[1;31mdbankite3: INVALID PASSWORD\033[0m")
                return
            
            administrator.actions()

    class actions:
        """Interactive administrator menu and helper actions.

        Methods include showing all accounts, sending notices, changing
        the admin password, and removing user accounts.
        """

        def __init__(self) -> None:
            
            while True:

                print('''\033[34m
1. CONTACT DEVELOPER - GITHUB
2. SHOW ALL USERS
3. NOTICE
4. CHANGE ADMINISTRATOR PASSWORD
5. FORCE REMOVE A USER ACCOUNT (ONE AT A TIME)
6. DELETE ALL USER ACCOUNTS
7. QUIT DBANKITE3
8. LOGOUT FROM ADMINISTRATOR PANEL
                      \033[0m''')

                _ = input("\033[2m~\033[0m \033[1;32m$\033[0m\033[33mdbankite3 \033[2m:\033[0m ADMINISTRATOR ACTION [1-8] \033[34m>>\033[0m ") ; print("\033c")

                match _:
                    case '1':
                        print(f"\n\033[1;32m OPENING GITHUB...\033[0m\n")
                        subprocess.run("start https://github.com/ViratiAkiraNandhanReddy", shell = True)
                    case '2':
                        self.show_all_accounts()
                    case '3':
                        self.notice()
                    case '4':
                        self.change_admin_password()
                    case '5':
                        self.force_remove_user_account()
                    case '6':
                        self.delete_all_user_accounts()
                    case '7':
                        print('\n\033[1;31mEXITING DBANKITE3...\033[0m\n')
                        time.sleep(2)
                        exit()
                    case '8':
                        break
                    case _:
                        print('\nINVALID ACTION\n')

        def show_all_accounts(self) -> None:
            """Print all registered users and their balances."""
            users = dbankite3ServerQL.traversal().fetch_all_users()
            if not users:
                print('\n\033[1;31mNO USERS FOUND IN DATABASE\033[0m\n')
                return
            
            print('\n\033[1;32mALL REGISTERED USERS:\033[0m\n')
            for index, user in enumerate(users, start = 1):
                print(f'{index} - USERNAME: \033[1;32m{user[0]}\033[0m ~ BALANCE: ${user[1]}')
            print()
        
        def notice(self) -> None:
            """Prompt for a notice message and publish it to the administrators table."""
            msg = input('ENTER NOTICE MESSAGE: ')
            password = input('ENTER ADMINISTRATOR PASSWORD TO CONFIRM: ')
            if not dbankite3ServerQL.administrator().authenticate_admin(password):
                print("\n\033[1;31mdbankite3: INVALID PASSWORD - NOTICE NOT SENT\033[0m\n")
                return
            _ = dbankite3ServerQL.administrator().notifications(msg)
            print("\n\033[1;32mNOTICE SENT SUCCESSFULLY!\033[0m\n" if _ else "\n\033[1;31mNOTICE SENDING FAILED!\033[0m\n")
        
        def change_admin_password(self) -> None:
            """Change the administrator account password after confirmation."""
            
            def pw_avoidnesting(password: str) -> bool:
                """Basic validation helper for administrator passwords."""
                if not password:
                    print("\n\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m") ; return False
                
                if len(password) < 6:
                    print("\n\033[1;31mdbankite3: PASSWORD MUST BE ATLEAST 6 CHARS\033[0m") ; return False
                
                return True

            for i in range(5, 0, -1):
                print(f'\n#{i} ATTEMPT\'S LEFT')
                _new_password = input('\nENTER NEW ADMINISTRATOR PASSWORD: ')

                if not pw_avoidnesting(_new_password):
                    continue

                password = input('ENTER CURRENT ADMINISTRATOR PASSWORD TO CONFIRM: ')
            
                if not dbankite3ServerQL.administrator().authenticate_admin(password):
                    print("\n\033[1;31mdbankite3: INVALID PASSWORD - PASSWORD NOT CHANGED\033[0m\n")
                    return
                
                _ = dbankite3ServerQL.administrator().change_password(_new_password)
                print("\n\033[1;32mPASSWORD CHANGED SUCCESSFULLY!\033[0m\n" if _ else "\n\033[1;31mPASSWORD CHANGE FAILED!\033[0m\n")

                break

        def force_remove_user_account(self) -> None:
            """Remove a given user's account after admin confirmation."""
            username = input('ENTER USERNAME TO REMOVE ACCOUNT: ')

            if not dbankite3ServerQL.traversal().isUserExist(username):
                print("\n\033[1;31mdbankite3: USER DOES NOT EXIST - ACCOUNT NOT REMOVED\033[0m\n")
                return

            password = input('ENTER ADMINISTRATOR PASSWORD TO CONFIRM: ')
            
            if not dbankite3ServerQL.administrator().authenticate_admin(password):
                print("\n\033[1;31mdbankite3: INVALID PASSWORD - ACCOUNT NOT REMOVED\033[0m")
                return
            
            _ = dbankite3ServerQL.accountactions().delete_account(username)
            print("\n\033[1;32mACCOUNT REMOVED SUCCESSFULLY!\033[0m" if _ else "\n\033[1;31mACCOUNT REMOVAL FAILED!\033[0m")

        def delete_all_user_accounts(self) -> None:
            """Delete all user accounts from the database after admin confirmation."""
            _password = input('ENTER ADMINISTRATOR PASSWORD TO CONFIRM: ')
            if not dbankite3ServerQL.administrator().authenticate_admin(_password):
                print("\n\033[1;31mdbankite3: INVALID PASSWORD - ACTION ABORTED\033[0m")
                return
            _ = dbankite3ServerQL.administrator().delete_all_user_accounts()
            print("\n\033[1;32mALL USER ACCOUNTS DELETED SUCCESSFULLY!\033[0m" if _ else "\n\033[1;31mACTION FAILED!\033[0m")