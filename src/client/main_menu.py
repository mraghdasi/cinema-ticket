import service.buy_ticket as buy_ticket
import service.buy_subscription as buy_subscription
import service.film_management as film_management
import service.banking as banking
import service.user_modification as user_modification
from src.utils.utils import clear_terminal


def main(user_info):
    while True:
        print("What do you want to do today ?\n")

        user_input = input('1.Buy tickets\n2.Buy A Subscription\n3.Check Available Movies\n4.Banking\n5.Modify Account\n6.Quit\n\n:').lower().strip()

        if user_input == '6' or user_input == 'quit':
            clear_terminal()
            return user_info
        elif user_input == '1' or user_input == 'buy tickets':
            clear_terminal()
            buy_ticket.main(user_info)
            continue
        elif user_input == '2' or user_input == 'buy a subscription':
            clear_terminal()
            buy_subscription.main(user_info)
            continue
        elif user_input == '3' or user_input == 'check available movies':
            clear_terminal()
            film_management.main(user_info)
            continue
        elif user_input == '4' or user_input == 'banking':
            clear_terminal()
            banking.main(user_info)
            continue
        elif user_input == '5' or user_input == 'modify account':
            clear_terminal()
            user_modification.main(user_info)
            continue