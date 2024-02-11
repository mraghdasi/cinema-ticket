import json

from prettytable import PrettyTable

from src.utils.utils import clear_terminal


def get_rate():
    while True:
        selected_rate = input('Enter Rate (0-10) or quit: ').strip().lower()
        if selected_rate in map(str, range(11)):
            return selected_rate
        elif selected_rate == 'quit':
            break
        else:
            clear_terminal()
            print('Invalid Rating')
            continue


def show_rate(client, movie):
    while True:
        request_data = json.dumps({
            'payload': {
                'movie_id': movie['id'],
            },
            'url': 'get_user_rates'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            rates = response['rates']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        table = PrettyTable(['Id', 'Rate'])

        for rate in rates:
            table.add_row([rate['id'], rate['rate']])
        print(table)

        selected_rate = input('Enter Id of Rate: ').strip().lower()
        if selected_rate in map(str, [rate['id'] for rate in rates]):
            return selected_rate
        elif selected_rate == 'quit':
            break
        else:
            clear_terminal()
            print('Invalid Rate ID')
            continue


def main(client, movie):
    while True:
        user_input = input(
            '\n1. Add Rate\n2. Delete Rate\n3. Update Rate\n4. Quit\n\n:').strip().lower()

        if user_input == '4' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'add rate':
            while True:
                rate = get_rate()
                if not rate:
                    break
                request_data = json.dumps({
                    'payload': {
                        'rate': rate,
                        'movie_id': movie['id'],
                    },
                    'url': 'add_rate'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    rate = response['rate']
                    print("Rate Added!")
                    print(f"Rate ID: {rate['id']} \nRate: {rate['rate']}")
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '2' or user_input == 'delete comment':
            while True:
                selected_rate = show_rate(client, movie)
                if not selected_rate:
                    break

                request_data = json.dumps({
                    'payload': {
                        'rate_id': selected_rate,
                    },
                    'url': 'delete_rate'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Rate Deleted Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '3' or user_input == 'update comment':
            while True:
                selected_rate = show_rate(client, movie)

                if not selected_rate:
                    break

                new_rate = get_rate()
                if not new_rate:
                    break

                if not new_rate:
                    clear_terminal()
                    print('Invalid Rate')
                    continue

                request_data = json.dumps({
                    'payload': {
                        'rate_id': selected_rate,
                        'new_rate': new_rate
                    },
                    'url': 'update_rate'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Rate Updated Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue


if __name__ == "__main__":
    main()
