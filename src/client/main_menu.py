import json
import sys

import service.banking as banking
import service.buy_subscription as buy_subscription
import service.buy_ticket as buy_ticket
import service.film_management as film_management
import service.user_modification as user_modification
from src.client.service import movie_management, sans_management
from src.utils.utils import clear_terminal


# outgoing : just the url for the next file

def main(client):
    while True:
        print("What do you want to do today ?\n")
        while True:
            request_data = json.dumps({
                'payload': {},
                'url': 'show_profile'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)

            if response['status_code'] == 200:
                user = response['user']
                break
            else:
                print(response['msg'])
                continue
        extra_option = "\n7. Movies\n8. Sans\n\n:" if user["role"] == 0 else ""
        user_input = input(
            '1.Buy tickets\n2.Buy A Subscription\n3.Check Available Movies\n4.Banking\n5.Modify Account\n6.Quit\n\n:' + extra_option).lower().strip()

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
        else:
            if user["role"] == 0:
                if user_input == '7' or user_input == 'movies':
                    clear_terminal()
                    movie_management.main(client)
                elif user_input == '8' or user_input == 'sans':
                    clear_terminal()
                    sans_management.main(client)
                else:
                    continue
            else:
                continue


if __name__ == "__main__":
    main()
