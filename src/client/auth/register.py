from src.utils.utils import input_client
from src.utils.utils import clear_terminal

import src.utils.custom_validators as Validators
import src.utils.custom_exceptions as CustomException


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
    creds = {'username': '', 'email': '', 'phone_number': '', 'password': '', 'birthday': ''}
    while True:
        print(
            '''\nHi! we are very happy to have you on our app.
Please fill in the fields.
Pay attention to the requirements for each field (press Ctrl+C to quit)\n''')
        try:

            if creds['username'] == '':
                username = input(
                    'Username*(Must Contain lower/uppercase letters and numbers 3~100):').strip()

                if Validators.Validator.username_validator(username):
                    creds['username'] = username

            else:
                print(f'Username : {creds['username']}')

            if creds['email'] == '':
                email = input_client('Email*(example@example.example):')

                if Validators.Validator.email_validator(email):
                    creds['email'] = email

            else:
                print(f'Email : {creds['email']}')

            if creds['phone_number'] == '':
                phone_number = input('Phone number(09121231234):').strip()

                if Validators.Validator.phone_number_validator(phone_number):
                    creds['phone_number'] = phone_number

            else:
                print(f'Phone Number : {creds['phone_number']}')

            if creds['password'] == '':
                password = input(
                    'Password*(at least 2 uppercase letters, numbers and special characters):').strip()

                if Validators.Validator.password_validator(password):

                    password_confirm = ''

                    while password != password_confirm:
                        if password_confirm != '':
                            print('\nPasswords Do Not Match!\n')
                        password_confirm = input('Confirm Password*:').strip()

                    creds['password'] = password

            else:
                print(f'Password : {creds['password']}')

            if creds['birthday'] == '':
                birthday = input('Birthday*(yyyy-mm-dd):')

                if Validators.Validator.birthday_format_validator(birthday):
                    creds['birthday'] = birthday

            else:
                print(f'Birthday : {creds['birthday']}')

        except KeyboardInterrupt:
            clear_terminal()
            break
        except CustomException.UsernameValidationError:
            clear_terminal()
            print('\n' + str(CustomException.UsernameValidationError()))
            continue
        except CustomException.EmailValidationError:
            clear_terminal()
            print('\n' + str(CustomException.EmailValidationError()))
            continue
        except CustomException.PhoneNumberValidationError:
            clear_terminal()
            print('\n' + str(CustomException.PhoneNumberValidationError()))
            continue
        except CustomException.PasswordValidationError:
            clear_terminal()
            print('\n' + str(CustomException.PasswordValidationError()))
            continue
        except CustomException.BirthdayValidationError:
            clear_terminal()
            print('\n' + str(CustomException.BirthdayValidationError()))
            continue

        # some code to connect to db and stuff

        user_info = ''
        clear_terminal()
        return user_info


if __name__ == '__main__':
    main()
