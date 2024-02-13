import sys

import service.banking as banking
import service.buy_subscription as buy_subscription
import service.buy_ticket as buy_ticket
import service.film_management as film_management
import service.user_modification as user_modification
from src.utils.utils import clear_terminal
from prettytable import PrettyTable


def main(client):
    while True:
        table = PrettyTable(["What do you want to do today ?"])
        table.align["What do you want to do today ?"] = "l"
        table.add_rows([['1.Buy tickets'], ['2.Buy A Subscription'], ['3.Check Available Movies'],
                        ['4.Banking'], ['5.Modify Account'], ['6.Quit']])

        print(table)
        user_input = input('Choose One Option:').lower().strip()

        if user_input == '6' or user_input == 'quit':
            clear_terminal()
            sys.exit('*\n**\n***\nHave A Nice Day :)\n***\n**\n*')
        elif user_input == '1' or user_input == 'buy tickets':
            clear_terminal()
            buy_ticket.main(client)
        elif user_input == '2' or user_input == 'buy a subscription':
            clear_terminal()
            buy_subscription.main(client)
        elif user_input == '3' or user_input == 'check available movies':
            clear_terminal()
            film_management.main(client)
        elif user_input == '4' or user_input == 'banking':
            clear_terminal()
            banking.main(client)
        elif user_input == '5' or user_input == 'modify account':
            clear_terminal()
            user_modification.main(client)


if __name__ == "__main__":
    main()
