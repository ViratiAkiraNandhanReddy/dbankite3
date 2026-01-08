"""dbankite3 command-line entrypoint.

This module implements the interactive CLI loop used to run dbankite3.

Features
- Prints ASCII art and a greeting.
- Provides options to login, register, or perform administrator login.

Usage
```py
python main.py
```
"""

import dbankite3, time
from dbankite3.interface import UserInterface
from dbankite3.administrator import administrator
from dbankite3.dbankite3ServerQL.SQLite3 import dbankite3ServerQL

while True:
    
    print('\n\033[1;33mREDIRECTING...\033[0m')
    time.sleep(4)
    print("\033c")
    print(f'\033[1;32m{dbankite3.__ascii_art__}\033[0m')
    print('dbankite3 (tags/v1.0, DEC-20-2025, 23:45:53) - https://github.com/ViratiAkiraNandhanReddy/dbankite3\n\n~~ PRESS CTRL + C TO EXIT PROGRAM $')
    
    print('\n\033[1;31mNOTICE: ' + dbankite3ServerQL.administrator().fetch_notifications() + '\033[0m') if dbankite3ServerQL.administrator().fetch_notifications() else None

    print('''\033[1;32m
          1. USER LOGIN
          2. REGISTER USER
          3. ADMIN LOGIN
          \033[0m''')
    
    _ = input("\033[2m~\033[0m \033[1;32m$\033[0m\033[33mdbankite3 \033[2m:\033[0m ACTION [1-3] \033[34m>>\033[0m ") ; print()
    
    match _:
        case '1': UserInterface.login()
        case '2':
            
            def un_avoidnesting(username: str) -> bool:
                """Check whether a username is available.

                Args:
                    username: Candidate username.

                Returns:
                    True if username is not present in the database, False otherwise.
                """
                if dbankite3ServerQL.traversal().isUserExist(username):
                    print("\n\033[1;31mdbankite3: USER ALREADY EXIST\033[0m\n") ; return False
                
                if not username:
                    print("\n\033[1;31mdbankite3: USERNAME CANNOT BE EMPTY\033[0m\n") ; return False
                
                return True
            
            def pw_avoidnesting(password: str) -> bool:
                """Validate a candidate password.

                Args:
                    password: Candidate password string.

                Returns:
                    True if password meets basic requirements, False otherwise.
                """
                if not password:
                    print("\n\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m") ; return False
                
                if len(password) < 6:
                    print("\n\033[1;31mdbankite3: PASSWORD MUST BE ATLEAST 6 CHARS\033[0m") ; return False
                
                return True
            
            while True:
                
                print('** TYPE `EXIT` IN NEW USERNAME TO CANCEL **')
                username = input('\nNEW USERNAME: ')
                
                if username == 'EXIT':
                    break

                if not un_avoidnesting(username.strip()) :
                    continue
                
                for i in range(5, 0, -1):
                    
                    print(f'\n#{i} ATTEMPT\'S LEFT')
                    password =  input(f'\nNEW PASSWORD FOR `{username}`: ')
                    
                    if not pw_avoidnesting(password.strip()) :
                        continue
                    
                    _ = dbankite3ServerQL.registration(username, password).register_user()
                    print("\n\033[1;32mSUCCESSFUL!\033[0m" if _ else "\n\033[1;31mUNSUCCESSFUL!\033[0m")
                    break

                else:
                    continue

                break
                
        case '3': administrator.login()
        case _: print('INVALID ACTION\n')
