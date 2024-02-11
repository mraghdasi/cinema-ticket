import os

from src.client.service import card_operations, card_registeration


# outgoing : urls

def main(client):
    while True:
        print('please choose your banking op')

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

        card_registeration.main(client)


if __name__ == '__main__':
    main('m')
