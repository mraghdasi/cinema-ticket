import os


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
            os.system("cls")
            break

        # some code to connect to db and stuff
        some_validations = ''
        user_info = 'f'

        if some_validations == '':
            os.system('cls')
            return user_info


if __name__ == '__main__':
    main()
