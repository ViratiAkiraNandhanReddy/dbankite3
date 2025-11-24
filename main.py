'''

'''

import dbankite3, time
from dbankite3.interface import UserInterface
from dbankite3.administrator import administrator
from dbankite3.dbankite3ServerQL import dbankite3ServerQL

while True:
    
    time.sleep(4)
    print("\033c")
    print(f'\033[1;32m{dbankite3.__ascii_art__}\033[0m')
    print('dbankite3 (tags/v, MMM DD YYYY, HH:MM:SS) - https://github.com/ViratiAkiraNandhanReddy/dbankite3')
    
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
                if dbankite3ServerQL.traversal().isUserExist(username):
                    print("\033[1;31dbankite3: USER ALREADY EXIST\033[0m") ; return False
                return True
            
            def pw_avoidnesting(password: str) -> bool:
                if not password:
                    print("\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m") ; return False
                
                if len(password) < 6:
                    print("\033[1;31mdbankite3: PASSWORD MUST BE ATLEAST 6 CHARS\033[0m") ; return False
                
                return True
            
            while True:
                
                print('** TYPE `EXIT` IN NEW USERNAME TO CANCEL **')
                username = input('\nNEW USERNAME: ')
                
                if username == 'EXIT':
                    break

                if not un_avoidnesting(username) :
                    continue
                
                for i in range(5, 0, -1):
                    
                    print(f'\n#{i} ATTEMPT\'S LEFT')
                    password =  input(f'\nNEW PASSWORD FOR `{username}`: ')
                    
                    if not pw_avoidnesting(password) :
                        continue
                    
                    _ = dbankite3ServerQL.registration(username, password).register_user()
                    print("\n\033[1;32mSUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mUNSUCCESSFUL!\033[0m\n")
                    break

                else:
                    continue

                break
                
        case '3': administrator.login()
        case _: print('INVALID ACTION\n')