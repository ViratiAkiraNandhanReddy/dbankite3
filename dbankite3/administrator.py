from .dbankite3ServerQL import dbankite3ServerQL

class administrator:
    
    def __init__(self):
        pass

    class login:

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

        def __init__(self) -> None:
            
            while True:

                _ = input("\033[2m~\033[0m \033[1;32m$\033[0m\033[33mdbankite3 \033[2m:\033[0m ADMIN ACTION [1-8] \033[34m>>\033[0m ") ; print("\033c")
