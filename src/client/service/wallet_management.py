import os

# incoming : wallet info
# outgoing : any update

def main(user_info):
    # charge wallet , check balance

    # check balance is for wallet we don't need to get the card info

    # user_info  # lowercase vars please
    CARD_LIST = [
        {'card_number': '2656435571048868', 'cvv2': '333', 'password': '123456', 'expiration_year': '02',
         'expiration_month': '11'},
        {'card_number': '7988634497364006', 'cvv2': '333', 'password': '123456', 'expiration_year': '02',
         'expiration_month': '12'},
        {'card_number': '8765435571048868', 'cvv2': '333', 'password': '123456', 'expiration_year': '02',
         'expiration_month': '10'},
        {'card_number': '1234334497364006', 'cvv2': '333', 'password': '123456', 'expiration_year': '02',
         'expiration_month': '11'}
    ]

    # initial wallet balance is 0
    WALLET_BALANCE = 0

    def check_card_info(charge_wallet=True):
        if not charge_wallet:
            # No need to get card information if charge_wallet is False
            return {'balance': WALLET_BALANCE}

        while True:
            card_num = input('Enter card number:')
            if not card_num.isdigit() or len(card_num) != 16:
                print('Invalid card number. Please try again.')
                continue

            cvv2 = input('Enter CVV2 code:')
            if not cvv2.isdigit() or len(cvv2) != 3:
                print('Invalid CVV2 code. Please try again.')
                continue

            password = input('Enter password:')
            # Check if password meets criteria (minimum length, etc.)
            if len(password) < 6:
                print('Password should be at least 6 characters long.')
                continue

            expire_year = input('Enter expiration year (e.g. 02 for 2002):')
            if not expire_year.isdigit() or len(expire_year) != 2:
                print('Invalid expiration year. Please try again.')
                continue

            expire_month = input('Enter expiration month (e.g. 11 for November):')
            if not expire_month.isdigit() or len(expire_month) != 2:
                print('Invalid expiration month. Please try again.')
                continue

            for card in CARD_LIST:
                if (card['card_number'], card['cvv2'], card['password'], card['expiration_year'],
                        card['expiration_month']) == (card_num, cvv2, password, expire_year, expire_month):
                    return card

            print('Invalid card info. Please try again.')

    while True:
        print('Please choose your wallet management operation:')
        print('1. Charge wallet')
        print('2. Check balance')
        print('3. Quit')

        choice = input('Enter your choice (1, 2, or 3):')

        if choice == '1':  # charge wallet

            card_info = check_card_info(charge_wallet=True)
            if card_info is None:
                print('Invalid card info.')
                continue

            amount = input('Enter the amount to charge:')
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                print('Invalid amount.')
                continue

            # charge wallet
            WALLET_BALANCE += amount
            print('Wallet charged successfully.')

        elif choice == '2':  # check balance

            card_info = check_card_info(charge_wallet=False)
            if card_info is None:
                print('Invalid card info.')
            else:
                print('Balance:', card_info.get('balance', 0), 'Toman')

        elif choice == '3' or choice.lower() == 'q':  # quit
            print('Goodbye!')
            break

        else:  # invalid choice
            print('Invalid choice. Please try again.')


user_info = {'account_number': '1234567890', 'password': 'password123'}
main(user_info)