import os

#!
#!
#!
#! We must run validators in this file! I'll change it myself (Behdad)
#!
#!
#!


def main():
    while True:
        try:
            print('\nHi! we are very happy to have you on our app please fill in the fields and pay attention to the requirements for each field\n')

            username = input(
                'Username*(must contain lower and uppercase letters and numbers at least 3 characters):').strip()

            email = input('Email*(example@example.example):').strip()

            phone_number = input('Phone number(09121231234):').strip()

            password = input(
                'Password*(at least 2 uppercase letters, numbers and special characters):').strip()

            password_confirm = ''
            
            while password != password_confirm:
                if password_confirm != '':
                    print('\nPasswords Do Not Match!\n')
                password_confirm = input('Confirm Password*:').strip()

            birthday = input('Birthday*(yyyy-mm-dd):')
            

        except KeyboardInterrupt:
            os.system("cls")
            break
        # except Validator errors:
        #   ...
        # except Validator errors:
        #   ...
        # except Validator errors:
        #   ...
        # except Validator errors:
        #   ...

        # some code to connect to db and stuff
        
        user_info = ''
        os.system('cls')
        return user_info
