import getpass
import json
from datetime import date
import sys

from src.utils import custom_exceptions
from src.utils.custom_validators import Validator
import sys

from src.utils.utils import clear_terminal, hash_string


def get_input(prompt, validation_func, is_password=False):
    while True:
        if is_password:
            user_input = getpass.getpass(prompt)
        else:
            user_input = input(prompt)
        if validation_func(user_input):
            clear_terminal()
            return user_input


def validate_title(title):
    try:
        if not title.isdigit() and Validator.len_bound_validator(title, 3, 100):
            return True
        clear_terminal()
        print("Title Can't be all numbers")
    except custom_exceptions.LenBoundValidationError:
        clear_terminal()
        print(custom_exceptions.LenBoundValidationError())


def validate_card_number(card_number):
    try:
        if card_number.isdigit() and Validator.len_validator(card_number, 16):
            return True
        clear_terminal()
        print('Card number should be all numbers')
    except custom_exceptions.LenValidationError:
        clear_terminal()
        print(custom_exceptions.LenValidationError())


def validate_password(password):
    try:
        if password.isdigit() and Validator.len_bound_validator(password, 4, 10):
            confirm_password = getpass.getpass("Enter your password again: ").strip()
            if password == confirm_password:
                return True
            clear_terminal()
            print('Passwords does not match')
            return False
        clear_terminal()
        print('Password should be all numbers')
    except custom_exceptions.LenBoundValidationError:
        clear_terminal()
        print(custom_exceptions.LenBoundValidationError())


def validate_cvv2(cvv2):
    try:
        if cvv2.isdigit() and Validator.len_bound_validator(cvv2, 3, 4):
            return True
        clear_terminal()
        print('Cvv2 should be all numbers')
    except custom_exceptions.LenBoundValidationError:
        clear_terminal()
        print(custom_exceptions.LenBoundValidationError())


def validate_expire_date(expire_date):
    try:
        if Validator.date_format_validator(expire_date):
            current_date = date.today()
            expire_date = date.fromisoformat(expire_date)

            if current_date < expire_date:
                return True

            clear_terminal()
            print("Your Card is expired")
    except custom_exceptions.DateValidationError:
        clear_terminal()
        print(custom_exceptions.DateValidationError())


def main(client):
    card_creds_input = {'user_id': '', 'title': '', 'card_number': '', 'password': '', 'cvv2': '', 'expire_date': ''}
    while True:
        try:
            print('Please Fill In The Fields (press ctrl+c to quit)\n')
            if card_creds_input['title'] == '':
                card_creds_input['title'] = get_input('Card Title Between 3 to 100 Chars: ', validate_title)
            else:
                print(card_creds_input['title'])

            if card_creds_input['card_number'] == '':
                card_creds_input['card_number'] = get_input("Enter card number (16 digits): ",
                                                            validate_card_number)
            else:
                print(card_creds_input['card_number'])

            if card_creds_input['password'] == '':
                card_creds_input['password'] = hash_string(
                    get_input("Enter password (4 to 10 digits): ", validate_password, True))
            else:
                print('Password Has Already Been Set')

            if card_creds_input['cvv2'] == '':
                card_creds_input['cvv2'] = get_input("Enter CVV2 code (3-4 digits): ", validate_cvv2)
            else:
                print(card_creds_input['cvv2'])

            if card_creds_input['expire_date'] == '':
                card_creds_input['expire_date'] = get_input("Enter card expiration date yyyy-mm-dd: ",
                                                            validate_expire_date)
            else:
                print(card_creds_input['expire_date'])
        except KeyboardInterrupt:
            clear_terminal()
            break

        request_data = json.dumps({
            'payload': card_creds_input,
            'url': 'register_cards'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            clear_terminal()
            print('Your Card Has Been Registered')
            break
        elif response['status_code'] == 400:
            print("The Card Already Exists In Our Database")
            break
        else:
            print(response['msg'])
            break


if __name__ == '__main__':
    main()
