import os

# incoming : wallet info
# outgoing : any update

def main(user_info):
    # charge wallet , check balance

    # check balance is for wallet we don't need to get the card info

    # user_info  # lowercase vars please
    CARD_LIST = [
        {'card_number': '2656435571048868', 'cvv2': '333', 'password': '1234', 'expiration_year': '02',
         'expiration_month': '11'},
        {'card_number': '7988634497364006', 'cvv2': '333', 'password': '1234', 'expiration_year': '02',
         'expiration_month': '12'},
        {'card_number': '8765435571048868', 'cvv2': '333', 'password': '1234', 'expiration_year': '02',
         'expiration_month': '10'},
        {'card_number': '1234334497364006', 'cvv2': '333', 'password': '1234', 'expiration_year': '02',
         'expiration_month': '11'}
    ]

    # user info (dummy data)
    USER_INFO = {'account_number': '1234567890', 'password': 'password123'}

    # initial wallet balance is 0
    WALLET_BALANCE = 0

    def check_card_info():
        # Check for each input and don't make the user write the correct ones again
        card_num = input('Enter card number:')
        cvv2 = input('Enter CVV2 code:')
        password = input('Enter password:')
        expire_year = input('Enter expiration year (e.g. 02 for 2002):')
        expire_month = input('Enter expiration month (e.g. 11 for November):')

        # check if card is available
        for card in CARD_LIST:
            if (
                    card['card_number'], card['cvv2'], card['password'], card['expiration_year'],
                    card['expiration_month']) == (
                    card_num, cvv2, password, expire_year, expire_month):
                return card

        return None

    while True:
        print('Please choose your wallet management operation:')
        print('1. Charge wallet')
        print('2. Check balance')
        print('3. Quit')

        choice = input('Enter your choice (1, 2, or 3):')

        if choice == '1':  # charge wallet

            card_info = check_card_info()
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

            card_info = check_card_info()
            if card_info is None:
                print('Invalid card info.')
            else:
                print('Balance:', card_info.get('balance', 0), 'Toman')

        elif choice == '3':  # quit
            print('Goodbye!')
            break

        else:  # invalid choice
            print('Invalid choice. Please try again.')


user_info = {'account_number': '1234567890', 'password': 'password123'}
main(user_info)
