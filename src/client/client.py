import os

import auth.login as login


def main():
    while True:
        input_str = input('1.Login\n2.Register\n3.quit\n\n:')

        if input_str == '3':
            break

        if input_str == '1':
            os.system('clear')
            login.main()
            continue

        if input_str != '1' or input_str != '2':
            print('Please enter valid input')


if __name__ == '__main__':
    main()
