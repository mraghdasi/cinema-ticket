import json
from secrets import compare_digest

import src.utils.custom_exceptions as CustomException
import src.utils.custom_validators as Validators
from src.utils.utils import clear_terminal, hash_string
from src.utils.utils import input_client
import getpass

# outgoing data : validated user registration info :
# username email phone number password birthday


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
    print('\nHi! we are very happy to have you on our app.\n\nPlease fill in the fields.\n'
          'Pay attention to the requirements for each field (press Ctrl+C to quit)\n')

    while True:
        try:

            if creds['username'] == '':
                username = input(
                    'Username*(Must Contain lower and uppercase letters and numbers 3~100):').strip()

                if Validators.Validator.username_validator(username):
                    creds['username'] = username

            else:
                print(f'Username : {creds["username"]}')

            if creds['email'] == '':
                email = input_client('Email*(example@example.example):').strip().lower()

                if Validators.Validator.email_validator(email):
                    creds['email'] = email

            else:
                print(f'Email : {creds["email"]}')

            if creds['phone_number'] == '':
                phone_number = input('Phone number(09121231234):').replace(" ", "")

                if Validators.Validator.phone_number_validator(phone_number):
                    creds['phone_number'] = phone_number

            else:
                print(f'Phone Number : {creds["phone_number"]}')

            if creds['password'] == '':
                password = getpass.getpass(prompt=
                                           'Password*(at least 2 uppercase letters, numbers and special characters):').strip()

                if Validators.Validator.password_validator(password):

                    password_confirm = ''

                    while not compare_digest(password, password_confirm):
                        if password_confirm != '':
                            print('\nPasswords Do Not Match!\n')
                        password_confirm = getpass.getpass('Confirm Password*:').strip()

                    creds['password'] = hash_string(password)

            else:
                print(f'Password : Already set')

            if creds['birthday'] == '':
                birthday = input('Birthday*(yyyy-mm-dd):').strip()

                if Validators.Validator.date_format_validator(birthday) and Validators.Validator.min_date_validator(
                        birthday, '2013-01-01'):
                    creds['birthday'] = birthday

            else:
                print(f'Birthday : {creds["birthday"]}')

            data = {
                'payload': creds,
                'url': 'register'
            }
            js = json.dumps(data)
            clear_terminal()
            return js

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
        except CustomException.DateValidationError:
            clear_terminal()
            print('\n' + str(CustomException.DateValidationError()))
            continue
        except CustomException.MinDateValidationError:
            clear_terminal()
            print('\n' + str(CustomException.MinDateValidationError()))
            continue


if __name__ == '__main__':
    main()
