import json
import re
from datetime import datetime

from prettytable import PrettyTable

from src.utils.utils import clear_terminal


def main(client):
    while True:
        request_data = json.dumps({
            'payload': {},
            'url': 'get_movies'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            movies = response['payload']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        table = PrettyTable(['Id', 'title', 'min_age'])

        for movie in movies:
            table.add_row([movie['id'], movie['title'],
                           movie['min_age']])
        print(table)
        selected_movie = input('Enter Id of Movie: ').strip().lower()
        if selected_movie == 'quit':
            break
        elif selected_movie not in map(str, [movie['id'] for movie in movies]):
            clear_terminal()
            print("Invalid Movie Id")
            continue
        while True:
            user_input = input(
                '\n1. Show Sans\n2. Add Sans\n3. Delete Sans\n4. Update Sans\n5. Quit\n\n:').strip().lower()

            if user_input == '5' or user_input == 'quit':
                clear_terminal()
                break
            elif user_input == '1' or user_input == 'show sans':
                while True:

                    request_data = json.dumps({
                        'payload': {
                            'movie_id': selected_movie,
                        },
                        'url': 'get_movie_sans'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    if response['status_code'] == 200:
                        sansses = response['sansses']
                    else:
                        clear_terminal()
                        print(response['msg'])
                        continue

                    table = PrettyTable(['Id', 'Premiere Date', 'Start Time', 'End Time', 'Hall Id', 'Price'])
                    table.add_rows([[sans['id'], sans['premiere_date'], sans['start_time'], sans['end_time'],
                                     sans['title'], sans['price']] for sans in sansses])
                    print(table)
                    break

            elif user_input == '2' or user_input == 'add sans':
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

                    premier_date = input("Enter Premier Date: ")
                    try:
                        datetime.strptime(premier_date, "%Y-%m-%d")
                    except:
                        clear_terminal()
                        print("Invalid Premier Date")
                        continue

                    def check_time(string):
                        return re.search(r'[0-9]{2}:[0-9]{2}:[0-9]{2}', string)

                    start_time = input("Enter Start Time: ")
                    if not check_time(start_time):
                        clear_terminal()
                        print("Invalid Start Time")
                        continue
                    end_time = input("Enter End Time: ")
                    if not check_time(end_time):
                        clear_terminal()
                        print("Invalid End Time")
                        continue
                    price = input("Enter Price: ")
                    if not price.isdigit():
                        clear_terminal()
                        print("Invalid Price")
                        continue
                    request_data = json.dumps({
                        'payload': {
                            'film_id': selected_movie,
                            'hall_id': selected_hall,
                            'premiere_date': premier_date,
                            'start_time': start_time,
                            'end_time': end_time,
                            'price': price,
                        },
                        'url': 'add_sans'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    if response['status_code'] == 200:
                        print("Sans Added Successfully")
                        break
                    else:
                        clear_terminal()
                        print(response['msg'])
                        continue

            elif user_input == '3' or user_input == 'delete sans':
                while True:
                    request_data = json.dumps({
                        'payload': {
                            'movie_id': selected_movie,
                        },
                        'url': 'get_movie_sans'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    if response['status_code'] == 200:
                        sansses = response['sansses']
                    else:
                        clear_terminal()
                        print(response['msg'])
                        continue

                    table = PrettyTable(['Id', 'Premiere Date', 'Start Time', 'End Time', 'Hall Id', 'Price'])
                    table.add_rows([[sans['id'], sans['premiere_date'], sans['start_time'], sans['end_time'],
                                     sans['title'], sans['price']] for sans in sansses])
                    print(table)

                    selected_sans = input("Enter Sans Id: ")
                    if selected_sans == 'quit':
                        break
                    elif selected_sans not in map(str, [sans['id'] for sans in sansses]):
                        clear_terminal()
                        print("Wrong Sans Id")
                        continue

                    request_data = json.dumps({
                        'payload': {
                            'sans_id': selected_sans,
                        },
                        'url': 'delete_sans'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    if response['status_code'] == 200:
                        print('Sans Deleted Successfully')
                        break
                    else:
                        clear_terminal()
                        print(response['msg'])
                        continue

            elif user_input == '4' or user_input == 'update sans':
                while True:
                    request_data = json.dumps({
                        'payload': {
                            'movie_id': selected_movie,
                        },
                        'url': 'get_movie_sans'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    if response['status_code'] == 200:
                        sansses = response['sansses']
                    else:
                        clear_terminal()
                        print(response['msg'])
                        continue

                    table = PrettyTable(['Id', 'Premiere Date', 'Start Time', 'End Time', 'Hall Id', 'Price'])
                    table.add_rows([[sans['id'], sans['premiere_date'], sans['start_time'], sans['end_time'],
                                     sans['title'], sans['price']] for sans in sansses])
                    print(table)

                    selected_sans = input("Enter Sans Id: ")
                    if selected_sans == 'quit':
                        break
                    elif selected_sans not in map(str, [sans['id'] for sans in sansses]):
                        clear_terminal()
                        print("Wrong Sans Id")
                        continue

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

                    premier_date = input("Enter Premier Date: ")
                    try:
                        datetime.strptime(premier_date, "%Y-%m-%d")
                    except:
                        clear_terminal()
                        print("Invalid Premier Date")
                        continue

                    def check_time(string):
                        return re.search(r'[0-9]{2}:[0-9]{2}:[0-9]{2}', string)

                    start_time = input("Enter Start Time: ")
                    if not check_time(start_time):
                        clear_terminal()
                        print("Invalid Start Time")
                        continue
                    end_time = input("Enter End Time: ")
                    if not check_time(end_time):
                        clear_terminal()
                        print("Invalid End Time")
                        continue
                    price = input("Enter Price: ")
                    if not price.isdigit():
                        clear_terminal()
                        print("Invalid Price")
                        continue
                    request_data = json.dumps({
                        'payload': {'data': {
                            'film_id': selected_movie,
                            'hall_id': selected_hall,
                            'premiere_date': premier_date,
                            'start_time': start_time,
                            'end_time': end_time,
                            'price': price,
                        }, 'sans_id': selected_sans},
                        'url': 'update_sans'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    if response['status_code'] == 200:
                        print('Sans Updated Successfully')
                        break
                    else:
                        clear_terminal()
                        print(response['msg'])
                        continue


if __name__ == "__main__":
    main()
