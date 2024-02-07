import json

from src.utils.utils import clear_terminal, hash_string


# outgoing data : username and password to the User Table in DB


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

        password = hash_string(password)
        data = {
            'payload': {'username': username, 'password': password},
            'url': 'login'
        }
        js = json.dumps(data)
        clear_terminal()
        return js


if __name__ == '__main__':
    main()
