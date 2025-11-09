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
                _ = input("\033[2m~\033[0m \033[1;32m$\033[0m\033[33mdbankite3 \033[2m:\033[0m ACTION [1-8] \033[34m>>\033[0m " ) ; print("\033c")

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
                        ...
                    case '7':
                        ...
                    case '8':
                        break
                    case _:
                        print()



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
            print(print("\n\033[1;32mWITHDRAW SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mWITHDRAW UNSUCCESSFUL!\033[0m\n"))
        
        def transfer(self) -> None:
            amount = float(input('\nENTER AMOUNT: \033[1;33m$ ')) ; print('\033[0m')
            _to = input('\nSEND TO <enter username> : \033[1;33m ') ; print('\033[0m')
            _ = dbankite3ServerQL.traversal().isUserExist(_to)
            
            if not _:
                print("\033[1;31mdbankite3: USER DOES NOT EXIST\033[0m")
                return
            
            _ = dbankite3ServerQL.transactions().transfer(self.username, _to, amount)
            print(print("\n\033[1;32mTRANSFER SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mTRANSFER UNSUCCESSFUL!\033[0m\n"))

        def close_account(self) -> bool:
            _ = input(f"\n\033[1;31mUNDONE EVENT: Are you sure? (YES/NO) : \033[0m\n")
            if _ == 'YES':
                _password = input("\nENTER PASSWORD TO CONFIRM: ")
                
                if dbankite3ServerQL.authentication(self.username, _password).authenticate_password():
                    _ = dbankite3ServerQL.accountactions().delete_account(self.username)
                    print("\n\033[1;32mDELETION SUCCESSFUL!\033[0m\n" if _ else "\n\033[1;31mDELETION UNSUCCESSFUL!\033[0m\n")
                    return _
            
            print("\n\033[1;32mDELETION UNSUCCESSFUL!\033[0m\n")
            return False