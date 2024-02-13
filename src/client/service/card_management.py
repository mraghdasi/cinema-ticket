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
            card_creds = response['cards']
        else:
            clear_terminal()
            print(response['msg'])
            break

        i = 1
        table = PrettyTable(['Number', 'Title', 'Card Number'])
        for card in card_creds:
            table.add_row([i, card, card_creds[card]['card_number']])
            i += 1
        table.add_row(['', '', ''], divider=True)
        table.add_row(['Other Options', 'Functionality', ''], divider=True)
        table.add_row([str(i), 'Quit', ''])
        print(table)

        available_cards = [card for card in card_creds]

        user_input = input("\nPlease Select Your Card:").strip()
        if user_input == str(i) or user_input == 'quit':
            clear_terminal()
            break
        try:
            if len(user_input) == 1:
                clear_terminal()
                selected_card = available_cards[int(user_input) - 1]
            else:
                if user_input in [card for card in card_creds]:
                    clear_terminal()
                    selected_card = user_input
                elif user_input in [card_creds[card]['card_number'] for card in card_creds]:
                    clear_terminal()
                    selected_card = [card for card in card_creds if card_creds[card]['card_number'] == user_input][0]
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

            table = PrettyTable(["Numbers", "Your Credentials", "Current Value Of Your Credential"])
            table.add_rows([['1', 'Card number', f'{card_creds[selected_card]["card_number"]}'],
                            ['2', 'CVV2', f'{card_creds[selected_card]["cvv2"]}'],
                            ['3', 'Expiration Date', f'{card_creds[selected_card]["expire_date"]}'],
                            ['4', 'Password', 'Can\'t show password due to privacy reasons']])
            table.add_row(['', '', ''], divider=True)
            table.add_row(['Other Options', 'Functionality', ''], divider=True)
            table.add_row(['5', 'Quit', ''])
            table.add_row(['6', 'Confirm Changes', ''])
            print(table)

            user_input = input("PLease Choose One Of The Options:").strip().lower()

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
                new_card = input("Enter new card number (length must be 16): ")
                if new_card == card_creds[selected_card]['card_number']:
                    clear_terminal()
                    print(f"You can't change you card number to the same one")
                    continue
                if edit_card_number(available_cards, new_card):
                    card_creds[selected_card]['card_number'] = new_card
                    clear_terminal()
                    continue
            elif user_input == '2' or user_input == 'change cvv2':
                new_cvv2 = input("Enter new CVV2 (length must be 3 or 4): ")
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
                        new_password = input("Please enter your new password (length must be 4 to 10): ")
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
