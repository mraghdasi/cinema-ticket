import json
import os

from prettytable import PrettyTable

from src.client import card_operations
from src.utils.transaction import TransactionType
from src.utils.utils import clear_terminal


def main(client):
    while True:

        table = PrettyTable(["Your Wallet Operations:"])
        table.align["Your Wallet Operations:"] = "l"
        table.add_rows([["1.Charge wallet"], ["2.Check balance"], ["3.Quit"]])
        print(table)

        choice = input('Please Choose One Option:').strip().lower()

        if choice == '3' or choice.lower() == 'quit':
            clear_terminal()
            break
        elif choice == '1' or choice == 'charge wallet':
            amount = card_operations.main(client, "withdraw")
            if not amount:
                clear_terminal()
                print("Cart Operation Error")
                continue
            request_data = json.dumps({
                'payload': {
                    'amount': amount,
                    'transaction_log_type': TransactionType.DEPOSIT_WALLET.value
                },
                'url': 'wallet_deposit'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)

            if response['status_code'] == 200:
                clear_terminal()
                print('Wallet charged successfully.')
            else:
                print(response['msg'])
                continue

        elif choice == '2':
            request_data = json.dumps({
                'payload': {},
                'url': 'show_profile'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)
            clear_terminal()
            if response['status_code'] == 200:
                user = response['user']
            else:
                print(response['msg'])
                continue
            print(f"Balance: {user['balance']} Toman")

        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
