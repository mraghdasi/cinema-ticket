import os

from src.client.service import card_operations, card_management, card_registeration, wallet_management
from src.utils.utils import clear_terminal


def main(client):
    while True:

        user_input = input(
            "Please choose your action:\n1.Card Management\n2.Card Registration\n3.Card Operations\n4.Wallet "
            "Management\n5.Quit\n\n:").strip().lower()

        if user_input == '5' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'card management':
            clear_terminal()
            card_management.main(client)
        elif user_input == '2' or user_input == 'card registration':
            clear_terminal()
            card_registeration.main(client)
        elif user_input == '3' or user_input == 'card operations':
            clear_terminal()

            while True:
                op = input(
                    "Please Choose your operation:\n1.Deposit\n2.Withdraw\n3.Transfer\n4.Quit\n\n:").strip().lower()

                if op == '4' or op == 'quit':
                    clear_terminal()
                    break
                elif op == '1' or op == 'deposit':
                    operation = 'deposit'
                elif op == '2' or op == 'withdraw':
                    operation = 'withdraw'
                elif op == '3' or op == 'transfer':
                    operation = 'transfer'
                else:
                    clear_terminal()
                    print("Invalid input. Please try again.")
                    continue

                clear_terminal()
                card_operations.main(client, operation)
        elif user_input == '4' or user_input == 'wallet management':
            clear_terminal()
            wallet_management.main(client)
        else:
            clear_terminal()
            print("Invalid input. Please try again.")
            continue


if __name__ == '__main__':
    main('m')
