import json

from prettytable import PrettyTable

from src.utils.utils import clear_terminal


def main(client):
    while True:
        user_input = input(
            '\n1. Show Halls\n2. Add Hall\n3. Delete Hall\n4. Update Hall\n5. Quit\n\n:').strip().lower()

        if user_input == '5' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'show halls':
            while True:
                request_data = json.dumps({
                    'payload': {},
                    'url': 'get_halls'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    halls = response['halls']
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

                table = PrettyTable(['Id', 'Title', 'Capacity'])
                table.add_rows([[hall['id'], hall['title'], hall['capacity']] for hall in halls])
                print(table)
                break

        elif user_input == '2' or user_input == 'add hall':
            while True:
                title = input("Enter a title: ").strip()
                capacity = input("Enter a capacity: ").strip()
                if capacity.isdigit():
                    capacity = int(capacity)
                else:
                    clear_terminal()
                    print("Wrong Capacity")
                    continue
                request_data = json.dumps({
                    'payload': {
                        'title': title,
                        'capacity': capacity,
                    },
                    'url': 'add_hall'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print("Hall Added!")
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '3' or user_input == 'delete hall':
            while True:
                request_data = json.dumps({
                    'payload': {},
                    'url': 'get_halls'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    halls = response['halls']

                else:
                    clear_terminal()
                    print(response['msg'])
                    continue
                table = PrettyTable(['Id', 'Title', 'Capacity'])
                table.add_rows([[hall['id'], hall['title'], hall['capacity']] for hall in halls])
                print(table)

                selected_hall = input("Enter Hall Id: ")
                if selected_hall == 'quit':
                    break
                elif selected_hall not in map(str, [hall['id'] for hall in halls]):
                    clear_terminal()
                    print("Wrong Hall Id")
                    continue

                request_data = json.dumps({
                    'payload': {
                        'hall_id': selected_hall,
                    },
                    'url': 'delete_hall'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Hall Deleted Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '4' or user_input == 'update hall':
            while True:
                request_data = json.dumps({
                    'payload': {},
                    'url': 'get_halls'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    halls = response['halls']

                else:
                    clear_terminal()
                    print(response['msg'])
                    continue
                table = PrettyTable(['Id', 'Title', 'Capacity'])
                table.add_rows([[hall['id'], hall['title'], hall['capacity']] for hall in halls])
                print(table)

                selected_hall = input("Enter Hall Id: ")
                if selected_hall == 'quit':
                    break
                elif selected_hall not in map(str, [hall['id'] for hall in halls]):
                    clear_terminal()
                    print("Wrong Hall Id")
                    continue

                new_title = input("Enter a title: ").strip()
                new_capacity = input("Enter a capacity: ").strip()
                if new_capacity.isdigit():
                    new_capacity = int(new_capacity)
                else:
                    clear_terminal()
                    print("Wrong Capacity")
                    continue
                request_data = json.dumps({
                    'payload': {'data': {
                        'title': new_title,
                        'capacity': new_capacity,
                    }, 'hall_id': selected_hall},
                    'url': 'update_hall'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Hall Updated Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue


if __name__ == "__main__":
    main()
