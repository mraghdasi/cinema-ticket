from src.utils.utils import clear_terminal


# !
# !
# !
# !
# !
# !
# ! WE HAVE TO FIX IMPORTS
# !
# !
# !
# !
# !
# !

def main():
    while True:
        try:
            print(
                '\n Welcome! please enter your username and password (press ctrl+c to exit this menu)\n')
            username = input(
                'Username :').strip()
            password = input(
                'Password :').strip()

        except KeyboardInterrupt:
            clear_terminal()
            break

        # some code to connect to db and stuff
        some_validations = ''
        user_info = 'f'

        if some_validations == '':
            clear_terminal()
            return user_info


if __name__ == '__main__':
    main()
