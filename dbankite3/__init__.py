__ascii_art__ = r'''

       /$$ /$$                           /$$       /$$   /$$                /$$$$$$ 
      | $$| $$                          | $$      |__/  | $$               /$$__  $$
  /$$$$$$$| $$$$$$$   /$$$$$$  /$$$$$$$ | $$   /$$ /$$ /$$$$$$    /$$$$$$ |__/  \ $$
 /$$__  $$| $$__  $$ |____  $$| $$__  $$| $$  /$$/| $$|_  $$_/   /$$__  $$   /$$$$$/
| $$  | $$| $$  \ $$  /$$$$$$$| $$  \ $$| $$$$$$/ | $$  | $$    | $$$$$$$$  |___  $$
| $$  | $$| $$  | $$ /$$__  $$| $$  | $$| $$_  $$ | $$  | $$ /$$| $$_____/ /$$  \ $$
|  $$$$$$$| $$$$$$$/|  $$$$$$$| $$  | $$| $$ \  $$| $$  |  $$$$/|  $$$$$$$|  $$$$$$/
 \_______/|_______/  \_______/|__/  |__/|__/  \__/|__/   \___/   \_______/ \______/ 
                                                                                    
'''

from .dbankite3ServerQL import dbankite3ServerQL
from datetime import datetime

if not dbankite3ServerQL.table_exists():
    
    print('\n\033[1;31m ~ NO DATABASE FOUND IN YOUR SERVER\033[0m\n')
    _ = input('DO YOU WANT TO INITIALIZE DATABASE <YES/NO> : ')
    
    match _:
        case 'YES':

            dbankite3ServerQL.table_definitions().define_user_table()
            dbankite3ServerQL.table_definitions().define_administrator_table()

            def pw_avoidnesting(password: str) -> bool:
                if not password:
                    print("\n\033[1;31mdbankite3: PASSWORD CANNOT BE EMPTY\033[0m") ; return False
                
                if len(password) < 6:
                    print("\n\033[1;31mdbankite3: PASSWORD MUST BE ATLEAST 6 CHARS\033[0m") ; return False
                
                return True

            print('\n ~ ~ SET A PASSWORD FOR ADMINISTRATOR ~ ~\n')
            while True:
                    
                password =  input(f'NEW PASSWORD FOR `ADMINISTRATOR`: ')
                
                if not pw_avoidnesting(password.strip()) :
                    continue
                
                _ = dbankite3ServerQL.administrator().change_password(password)
                print("\n\033[1;32mSUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mUNSUCCESSFUL!\033[0m")
                break
            
        case _:
            print('\n\033[1;31dbankite3: INITIALIZE DATABASE UNSUCCESSFUL - EXITING...\033[0m')
            exit()

currentDateTime = datetime.now()
time24hrsFormat = int(currentDateTime.strftime('%H'))

if time24hrsFormat >= 0 and time24hrsFormat < 12:
    Greeting = 'Good morning'

elif time24hrsFormat >= 12 and time24hrsFormat < 16:
    Greeting = 'Good afternoon'

elif time24hrsFormat >= 16:
    Greeting = 'Good evening'
