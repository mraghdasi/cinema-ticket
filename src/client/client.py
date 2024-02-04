import sys

import auth.login as login
import auth.register as register
import main_menu
from src.utils.utils import clear_terminal


def main():
    while True:
        user_input = input('1.Login\n2.Register\n3.Quit\n\n:').lower().strip()

        if user_input == '3' or user_input == 'quit' :
            clear_terminal()
            sys.exit('*\n**\n***\nHave A Nice Day :)\n***\n**\n*')
        elif user_input == '1' or user_input == 'login':
            clear_terminal()
            user_info = login.main()
            if user_info != '':
                print("\nWelcome <Username> :)\n")
                user_info = main_menu.main(user_info)
            continue
        elif user_input == '2' or user_input == 'Register':
            clear_terminal()
            user_info = register.main()
            if user_info != '':
                print("\nWelcome to our app <Username> :)\n")
                user_info = main_menu.main(user_info)
            continue
        else:
            clear_terminal()
            print('\nPlease enter valid input!\n')
            continue


if __name__ == '__main__':
    main()
