import json
import os

from src.client.service import card_operations
from src.utils.utils import clear_terminal


def main(client):
    while True:
        print('Please choose your wallet management operation:')
        print('1. Charge wallet\n2. Check balance\n3. Quit')

        choice = input('Enter your choice (1, 2, or 3):').strip().lower()
        if choice == '3' or choice.lower() == 'quit':  # quit
            clear_terminal()
            print('Goodbye!')
            break

        elif choice == '1' or choice == 'charge wallet':  # charge wallet

            amount = card_operations.main(client, "withdraw")
            if not amount:
                clear_terminal()
                print("Cart Operation Error")
                continue
            request_data = json.dumps({
                'payload': {"amount": amount},
                'url': 'add_amount_to_wallet'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)

            if response['status_code'] == 200:
                print('Wallet charged successfully.')
            else:
                print(response['msg'])
                continue

        elif choice == '2':  # check balance
            request_data = json.dumps({
                'payload': {},
                'url': 'show_profile'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)

            if response['status_code'] == 200:
                user = response['user']
            else:
                print(response['msg'])
                continue
            print(f"Balance: {user['balance']} Toman")

        else:  # invalid choice
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
