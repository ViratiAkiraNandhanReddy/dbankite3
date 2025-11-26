from .dbankite3ServerQL import dbankite3ServerQL

class UserInterface:

    class login:

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

        def __init__(self, username: str) -> None:
            
            self.username = username
            
            while True:

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

        def balance(self) -> None:
            balance = dbankite3ServerQL.transactions().balance_inquiry(self.username)

            if balance >= 1000: # green
                print(f"\nBALANCE:\033[1;32m $ {balance}\033[0m\n")

            elif 0 < balance < 1000 : # yellow
                print(f"\nBALANCE:\033[1;33m $ {balance}\033[0m\n")

            else: # red
                print(f"\nBALANCE:\033[1;31m $ {balance}\033[0m\n")
        
        def deposit(self) -> None:
            amount = float(input('\nENTER AMOUNT: \033[1;32m$ ')) ; print('\033[0m')
            _ = dbankite3ServerQL.transactions().deposit(self.username, amount)
            print("\n\033[1;32mDEPOSIT SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mDEPOSIT UNSUCCESSFUL!\033[0m\n")

        def withdraw(self) -> None:
            amount = float(input('\nENTER AMOUNT: \033[1;33m$ ')) ; print('\033[0m')
            _ = dbankite3ServerQL.transactions().withdraw(self.username, amount)
            print("\n\033[1;32mWITHDRAW SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mWITHDRAW UNSUCCESSFUL!\033[0m\n")
        
        def transfer(self) -> None:
            amount = float(input('\nENTER AMOUNT: \033[1;33m$ ')) ; print('\033[0m')
            _to = input('\nSEND TO <enter username> : \033[1;33m ') ; print('\033[0m')
            _ = dbankite3ServerQL.traversal().isUserExist(_to)
            
            if not _:
                print("\033[1;31mdbankite3: USER DOES NOT EXIST\033[0m")
                return
            
            _ = dbankite3ServerQL.transactions().transfer(self.username, _to, amount)
            print("\n\033[1;32mTRANSFER SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mTRANSFER UNSUCCESSFUL!\033[0m\n")

        def close_account(self) -> bool:
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

            def pw_avoidnesting(password: str) -> bool:
                
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
            
            def un_avoidnesting(username: str) -> bool:
                if dbankite3ServerQL.traversal().isUserExist(username):
                    print("\n\033[1;31dbankite3: USER ALREADY EXIST\033[0m") ; return False
                return True

            for i in range(5, 0, -1):

                print('** TYPE `EXIT` IN NEW USERNAME TO CANCEL **')
                newUsername = input('\nNEW USERNAME: ')
                    
                print(f'\n#{i} ATTEMPT\'S LEFT')
                
                if newUsername == 'EXIT':
                    break

                if not un_avoidnesting(newUsername) :
                    continue
                
                _ = dbankite3ServerQL.accountactions().change_username(self.username, newUsername)
                print("\n\033[1;32mUSERNAME CHANGE SUCCESSFUL!\033[0m" if _ else "\n\033[1;31mUSERNAME CHANGE UNSUCCESSFUL!\033[0m")
                if _: self.username = newUsername

                return
            
            print("\n\033[1;32mUSERNAME CHANGE UNSUCCESSFUL!\033[0m\n")
