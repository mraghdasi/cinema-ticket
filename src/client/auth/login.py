import os


def main():
    while True:
        username = input('Enter Username:')

        if username == '1':
            os.system('clear')
            break

        print(username)
