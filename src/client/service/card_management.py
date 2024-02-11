# import os
import json
import sys
from secrets import compare_digest
from datetime import date
from prettytable import PrettyTable

from src.utils import custom_exceptions
from src.utils.custom_validators import Validator
from src.utils.utils import clear_terminal, hash_string


def edit_card_number(card_list, new_card):
    try:
        if new_card.isdigit() and Validator.len_validator(new_card, 16):
            return True
        clear_terminal()
        print('Card number should be all numbers')
    except custom_exceptions.LenValidationError:
        clear_terminal()
        print(custom_exceptions.LenValidationError())


def change_cvv2(new_cvv2):
    try:
        if new_cvv2.isdigit() and Validator.len_bound_validator(new_cvv2, 3, 4):
            return True
        clear_terminal()
        print('Cvv2 should be all numbers')
    except custom_exceptions.LenBoundValidationError:
        clear_terminal()
        print(custom_exceptions.LenBoundValidationError())


def change_expiration_date(new_date):
    try:
        if Validator.date_format_validator(new_date):
            current_date = date.today()
            new_date = date.fromisoformat(new_date)

            if current_date < new_date:
                return True

            clear_terminal()
            print("New expiration date has already been passed")
    except custom_exceptions.DateValidationError:
        clear_terminal()
        print(custom_exceptions.DateValidationError())
    print(f"Expiration date updated. New expiration date is {new_date}.")


def validate_password(password):
    try:
        if password.isdigit() and Validator.len_bound_validator(password, 4, 10):
            return True
        clear_terminal()
        print('Password should be all numbers')
    except custom_exceptions.LenBoundValidationError:
        clear_terminal()
        print(custom_exceptions.LenBoundValidationError())


def main(client):
    while True:
        request_data = json.dumps({
            'payload': {},
            'url': 'get_cards'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            available_cards = list(response['cards'])
            card_creds = response['cards']
        elif response['status_code'] == 400:
            clear_terminal()
            sys.exit(response['msg'])
        else:
            clear_terminal()
            print(response['msg'])

        i = 1
        print('Your Cards:')
        table = PrettyTable(['#', 'Card Number'])
        for card in available_cards:
            table.add_row([i, card])
            i += 1

        print(table, f'\n{i}.Quit')
        user_input = input("\nPlease Select Your Card:").replace(" ", "").lower()
        if user_input == str(i) or user_input == 'quit':
            clear_terminal()
            break
        try:
            if len(user_input) == 1:
                clear_terminal()
                selected_card = available_cards[int(user_input) - 1]
            else:
                if user_input in available_cards:
                    clear_terminal()
                    selected_card = available_cards[available_cards.index(user_input)]
                else:
                    clear_terminal()
                    print(f'\n{user_input} is not one of the available cards.\n')
                    continue
        except IndexError:
            clear_terminal()
            print(f'\n{user_input} is not one of the menu options')
            continue

        clear_terminal()
        print("Selected card: ", selected_card)

        while True:
            user_input = input(
                "You can choose one of the following options:\n1. Edit card number\n2. Change CVV2\n3. Change expiration date\n4. Change password\n5. Quit\n6. Confirm Changes\n\n:").strip().lower()

            if user_input == '5' or user_input == 'quit':
                clear_terminal()
                break
            elif user_input == '6' or user_input == 'confirm changes':
                request_data = json.dumps({
                    'payload': card_creds[selected_card],
                    'url': 'update_cards'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    clear_terminal()
                    print(f"All Changes Were Made")
                    continue
                elif response['status_code'] == 400:
                    print("The Card Number Is Already In Our Database")
                else:
                    print(response['msg'])
                    continue
            elif user_input == '1' or user_input == 'edit card number':
                new_card = input("Enter new card number: ")
                if new_card == card_creds[selected_card]['card_number']:
                    clear_terminal()
                    print(f"You can't change you card number to the same one")
                    continue
                if edit_card_number(available_cards, new_card):
                    card_creds[selected_card]['card_number'] = new_card
                    clear_terminal()
                    continue
            elif user_input == '2' or user_input == 'change cvv2':
                new_cvv2 = input("Enter new CVV2: ")
                if new_cvv2 == card_creds[selected_card]['cvv2']:
                    clear_terminal()
                    print("You can't change your CVV2 to the same number")
                    continue
                if change_cvv2(new_cvv2):
                    card_creds[selected_card]['cvv2'] = new_cvv2
                    clear_terminal()
                    continue
            elif user_input == '3' or user_input == 'change expiration date':
                new_date = input("Enter new expiration date (YYYY-MM-DD): ")
                if new_date == card_creds[selected_card]['expire_date']:
                    clear_terminal()
                    print("You can't change your expiration date to the same one")
                    continue
                if change_expiration_date(new_date):
                    card_creds[selected_card]['expire_date'] = new_date
                    clear_terminal()
                    continue
            elif user_input == '4' or user_input == 'change password':
                current_password = input("Please enter your current password: ")
                if validate_password(current_password):
                    current_password = hash_string(current_password)
                    if compare_digest(current_password, card_creds[selected_card]['password']):
                        new_password = input("Please enter your new password: ")
                        if compare_digest(hash_string(new_password), card_creds[selected_card]['password']):
                            clear_terminal()
                            print("You Can't change your password to the same one")
                            continue
                        if validate_password(new_password):
                            confirm_new_password = input("Please confirm your new password: ")
                            if compare_digest(new_password, confirm_new_password):
                                card_creds[selected_card]['password'] = hash_string(new_password)
                                clear_terminal()
                                continue
            else:
                clear_terminal()
                print("Invalid selection. Please try again.\n")
                continue


if __name__ == '__main__':
    main()
