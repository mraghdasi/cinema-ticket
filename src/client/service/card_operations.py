import json
import sys

import src.utils.custom_exceptions as custom_exceptions
import src.utils.custom_validators as Validators
from src.utils.utils import clear_terminal, hash_string


def op_manager(client, op, selected_card, card_creds):
    op_amount = input(f'\nHow much money you want to {op}? ')

    card_creds_input = {'expire_date': '', 'cvv2': '', 'password': ''}

    try:
        if Validators.Validator.card_op_amount_validator(op_amount):
            while True:
                try:
                    if op == 'transfer':
                        destination_card = input('\nPlease enter the destination card:')
                        if destination_card == selected_card:
                            clear_terminal()
                            print('\nYou can\'t transfer money to the origin card')
                            break

                        request_data = json.dumps({
                            'payload': {'destination_card': destination_card},
                            'url': 'check_db_for_transfer'
                        })
                        client.send(request_data.encode('utf-8'))
                        response = client.recv(5 * 1024).decode('utf-8')
                        response = json.loads(response)
                        if response['status_code'] == 200:
                            destination_card = response['destination_card_obj']
                        else:
                            print(response['msg'])
                            break

                    expire_date = ''
                    expire_date_tries = 0

                    while expire_date != card_creds[selected_card]['expire_date']:
                        if expire_date_tries == 3:
                            clear_terminal()
                            sys.exit('\nYou have failed to enter correct input 3 times terminating operation...')
                        expire_date_tries += 1

                        expire_date = input('\nPlease enter your card\'s expire date YYYY-MM-DD:')

                        if expire_date != card_creds[selected_card]['expire_date']:
                            clear_terminal()
                            print(f'\nExpiration date: {expire_date} for card: {selected_card} is not correct')

                        card_creds_input['expire_date'] = expire_date

                    cvv2 = ''
                    cvv2_tries = 0

                    while cvv2 != card_creds[selected_card]['cvv2']:
                        if cvv2_tries == 3:
                            clear_terminal()
                            sys.exit('\nYou have failed to enter correct input 3 times terminating operation...')
                        cvv2_tries += 1

                        cvv2 = input('\nPlease enter your card\'s Cvv2:')

                        if cvv2 != card_creds[selected_card]['cvv2']:
                            clear_terminal()
                            print(f'\nExpiration date: {cvv2} for card: {selected_card} is not correct')

                        card_creds_input['cvv2'] = cvv2

                    password = ''
                    password_tries = 0

                    while password != card_creds[selected_card]['password']:
                        if password_tries == 3:
                            clear_terminal()
                            sys.exit('\nYou have failed to enter correct input 3 times terminating operation...')
                        password_tries += 1

                        password = hash_string(input('\nPlease enter your card\'s password:'))

                        if password != card_creds[selected_card]['password']:
                            clear_terminal()
                            print(f'\nExpiration date: {password} for card: {selected_card} is not correct')

                        card_creds_input['password'] = password

                except KeyboardInterrupt:
                    clear_terminal()
                    break

                min_check = (card_creds[selected_card]['amount'] - int(op_amount)) < card_creds[selected_card][
                    'minimum_amount']

                if op == 'deposit':
                    card_creds[selected_card]['amount'] += int(op_amount)
                elif op == 'withdraw':

                    if min_check:
                        clear_terminal()
                        print(f'\nNot enough money, your balance : {card_creds[selected_card]["amount"]}')
                        break

                    card_creds[selected_card]['amount'] -= int(op_amount)
                elif op == 'transfer':
                    if min_check:
                        clear_terminal()
                        print(f'\nNot enough money, your balance : {card_creds[selected_card]["amount"]}')
                        break
                    card_creds[selected_card]['amount'] -= int(op_amount)
                    card_creds[destination_card]['amount'] += int(op_amount)

                clear_terminal()

                if op == 'transfer':
                    request_data = json.dumps({
                        'payload': {'selected_card': selected_card,
                                    'destination_card': destination_card},
                        'url': 'do_transfer'
                    })
                else:
                    request_data = json.dumps({
                        'payload': {'selected_card': selected_card},
                        'url': 'do_card_op'
                    })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    pass
                else:
                    print(response['msg'])
                    break

                if op != 'transfer':
                    print(
                        f"""\n{op_amount} is {op}ed to {selected_card}\n
            your current balance: {card_creds[selected_card]['amount']}""")
                else:
                    print(
                        f"""\n{op_amount} is {op}ed to {destination_card}\n
            your current balance: {card_creds[selected_card]['amount']}""")

                break

    except custom_exceptions.CardOpAmountValueError:
        clear_terminal()
        print(str(custom_exceptions.CardOpAmountValueError()))


def main(client, op):
    while True:
        print('\nCard operations\n')

        # input(available cards)
        # if op == deposit : ...
        # if op == withdraw : ...
        # if op == card_to_card : ...

        # return user info

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
        else:
            print(response['msg'])
            break

        i = 1
        for card in available_cards:
            print(f'{i}.{card}')
            i += 1
        print(f'{i}.Quit')

        user_input = input('\nPlease select one of your cards:').lower().replace(" ", "")

        if user_input == f'{i}' or user_input == 'quit':
            clear_terminal()
            break

        selected_card = ''

        try:
            if len(user_input) == 1:
                selected_card = available_cards[int(user_input) - 1]
            else:
                if user_input in available_cards:
                    selected_card = available_cards[available_cards.index(user_input)]
                else:
                    clear_terminal()
                    print(f'\n{user_input} is not one of the available cards.\n')
                    continue
        except IndexError:
            clear_terminal()
            print(f'\n{user_input} is not one of the menu options')

        op_manager(client, op, selected_card, card_creds)

        break


if __name__ == '__main__':
    main('m', 'transfer')
