import json

from prettytable import PrettyTable

from src.utils.transaction import TransactionType
from src.utils.utils import clear_terminal


def main(client):
    while True:
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
            table.add_row([package['id'], package['title'].capitalize()])
        table.add_row(['', ''], divider=True)
        table.add_row(['Other Options', 'Functionality'], divider=True)
        table.add_row(['4', 'Quit'])
        print(table)

        selected_package = input('Enter the package you want: ').strip().lower()
        if selected_package == 'quit' or selected_package == '4':
            clear_terminal()
            break
        elif selected_package in list(map(str, [package['id'] for package in packages])):
            selected_package = [package for package in packages if str(package['id']) == selected_package][0]
        else:
            clear_terminal()
            print('Invalid Package ID')
            continue

        user_package = selected_package['title']

        clear_terminal()
        print(f"You selected {user_package.capitalize()} package.")
        request_data = json.dumps({
            'payload': {},
            'url': 'check_subscription'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            subscription = response['package']
            if subscription['title'] == user_package:
                clear_terminal()
                print('You Already Have This Subscription')
                continue
            elif subscription['title'] == 'Bronze':
                pass
            elif subscription['title'] == 'Silver' and user_package == 'Bronze':
                clear_terminal()
                print('You Have A Silver Subscription Can\'t Downgrade To Bronze')
                continue
            elif subscription['title'] == 'Gold':
                clear_terminal()
                print('You Already Have The Best Subscription Available, Can\'t Downgrade To Other Ones')
                continue
        else:
            clear_terminal()
            print(response['msg'])
            continue

        wallet_withdraw_payload = json.dumps({
            'payload': {
                'amount': selected_package['price'],
                'transaction_log_type': TransactionType.BUY_PACKAGE.value
            },
            'url': 'wallet_withdraw'
        })
        client.send(wallet_withdraw_payload.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
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
                clear_terminal()
                print(response['msg'])
                continue
        else:
            clear_terminal()
            print(response['msg'])
            continue


if __name__ == '__main__':
    main()
