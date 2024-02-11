import os

from src.client.service import card_operations, card_management, card_registeration, wallet_management
from src.utils.utils import clear_terminal


# outgoing : urls

def main(client):
    while True:
        # show my cards(runs card_management.py)
        # add a card(runs card_registration.py)
        # wallet management (runs wallet_management.py)
        # (deposit , withdraw , card to card(IDK what this called in eng XD) (runs card_operations.py))

        # return user info

        # 4.card op
        # depo
        # with
        # transfer

        # 4 or card op

        print("Please choose your action:\n1. Card Management\n2. Card Registration\n3. Wallet Management\n4. Quit")
        # Get user input for action choice
        action_choice = input("Enter your choice (1 or 2 or 3): ").strip().lower()
        if action_choice == '4' or action_choice == 'quit':
            clear_terminal()
            break
        elif action_choice == '1' and action_choice == 'card management':
            clear_terminal()
            card_management.main()
        elif action_choice == '2' or action_choice == 'card registration':
            clear_terminal()
            card_registeration.main(client)
        elif action_choice == '3' or action_choice == 'wallet management':
            clear_terminal()
            card_operations.main(client, input('input card operation (deposit, withdraw, card_to_card) : '))
        else:
            clear_terminal()
            continue


if __name__ == '__main__':
    main('m')
