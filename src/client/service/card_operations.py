import os

import src.utils.custom_validators as Validators

from src.utils.utils import clear_terminal


def main(user_info, op):
    while True:
        print('\nCard operations\n')

        # input(available cards)
        # if op == deposit : ...
        # if op == withdraw : ...
        # if op == card_to_card : ...

        # return user info

        availabel_cards = ['6104337387924085', '5859831112974042', '6037701540936439']
        card_creds = {'6104337387924085': {'expire_date': '27-05', 'cvv2': '5498', 'password': '2020'},
                      '5859831112974042': {'expire_date': '24-05', 'cvv2': '1298', 'password': '1234'},
                      '6037701540936439': {'expire_date': '27-09', 'cvv2': '9876', 'password': '7894'},
                      }
        i = 1
        for card in availabel_cards:
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
                selected_card = availabel_cards[int(user_input) - 1]
            else:
                if user_input in availabel_cards:
                    selected_card = availabel_cards[availabel_cards.index(user_input)]
                else:
                    clear_terminal()
                    print(f'\n{user_input} is not one of the available cards.\n')
                    continue
        except IndexError:
            clear_terminal()
            print(f'\n{user_input} is not one of the menu options')

        card_creds_input = {'expire_date': '', 'cvv2': '', 'password': ''}

        if op == 'deposit':

            deposit_amount = input('\nHow much money you want to deposit:')

            if Validators.Validator.deposit_amount_validator(deposit_amount):
                while True:
                    try:
                        expire_date = ''

                        while expire_date != card_creds[selected_card]['expire_date']:

                            expire_date = input('\nPlease enter your card\'s expire date 20YY-MM:')

                            if expire_date != card_creds[selected_card]['expire_date']:
                                clear_terminal()
                                print(f'\nExpiration date: {expire_date} for card: {selected_card} is not correct')

                            card_creds_input['expire_date'] = expire_date

                        cvv2 = ''

                        while cvv2 != card_creds[selected_card]['cvv2']:

                            cvv2 = input('\nPlease enter your card\'s Cvv2:')

                            if cvv2 != card_creds[selected_card]['cvv2']:
                                clear_terminal()
                                print(f'\nExpiration date: {cvv2} for card: {selected_card} is not correct')

                            card_creds_input['cvv2'] = cvv2

                        password = ''

                        while password != card_creds[selected_card]['password']:

                            password = input('\nPlease enter your card\'s password:')

                            if password != card_creds[selected_card]['password']:
                                clear_terminal()
                                print(f'\nExpiration date: {password} for card: {selected_card} is not correct')

                            card_creds_input['password'] = password

                    except KeyboardInterrupt:
                        clear_terminal()
                        break
            continue

        elif op == 'withdraw':
            ...
        elif op == 'transfer':
            ...

        break


if __name__ == '__main__':
    main('m', 'deposit')
