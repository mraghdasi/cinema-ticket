import json

# incoming : package and subscription details
# outgoing : banking process and updating user
from prettytable import PrettyTable

from src.utils.utils import clear_terminal


def main(client):
    # package = bronze , silver , gold

    # if package == one of the packages

    # payment stuff and changes in db (should use other modules and db)

    # returns user_info

    # ===========================Please Check my Code==========================

    # check buy_ticket.py and card_registration.py

    while True:
        print('Please choose your package:\n')

        # Get Packages From Server

        request_data = json.dumps({
            'payload': {},
            'url': 'get_packages'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            packages = response['packages']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        table = PrettyTable(['Id', 'Package Title'])

        for package in packages:
            table.add_row([package['id'], package['title']])
        print(table)

        selected_package = input('Enter Id of Package: ').strip().lower()
        if selected_package in map(str, [package['id'] for package in packages]):
            selected_package = [package for package in packages if str(package['id']) == selected_package][0]
        elif selected_package == 'quit':
            break
        else:
            clear_terminal()
            print('Invalid Package ID')
            continue

        user_package = selected_package['title']

        clear_terminal()
        print(f"You selected {user_package.capitalize()} package.")
        # print("At this step the user should be taken to the payment stuff and changes in the database.")

        # $$$$$$$ Foroutan $$$$$$$
        # Payment Method
        request_data = json.dumps({
            'payload': {
                'user_package': user_package,
            },
            'url': 'buy_subscription'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            payload = response['subscription']
            print(
                f"Subscription Id: {payload['id']}\nPackage Title: {response['package']['title']}\nExpires At: {payload['expire_at']}")
            break
        else:
            print(response['msg'])
            continue


if __name__ == '__main__':
    main()
