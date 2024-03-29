import json
import sys

from prettytable import PrettyTable

from src.client.service import movie_management, sans_management, hall_management, buy_ticket, buy_subscription, \
    film_management, banking, user_modification

from src.utils.utils import clear_terminal


def main(client):
    while True:
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
        table = PrettyTable(["What do you want to do today ?"])
        table.align["What do you want to do today ?"] = "l"
        table.add_rows([['1.Buy tickets'], ['2.Buy A Subscription'], ['3.Check Available Movies'],
                        ['4.Banking'], ['5.Modify Account'], ['6.Quit']])
        if user['role'] == 0:
            table.add_rows([['7. Movies'], ['8. Sans'], ['9. Halls']])

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
        else:
            if user["role"] == 0:
                if user_input == '7' or user_input == 'movies':
                    clear_terminal()
                    movie_management.main(client)
                elif user_input == '8' or user_input == 'sans':
                    clear_terminal()
                    sans_management.main(client)
                elif user_input == '9' or user_input == 'halls':
                    clear_terminal()
                    hall_management.main(client)
                else:
                    continue
            else:
                continue


if __name__ == "__main__":
    main()
