# Commenting.py
import json

from prettytable import PrettyTable

from src.server.models.film import Film
from src.utils.utils import clear_terminal


def main(client):
    while True:
        user_input = input(
            '\n1. Show Movies\n2. Add Movie\n3. Delete Movie\n4. Update Movie\n5. Quit\n\n:').strip().lower()

        if user_input == '5' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'show movies':
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
                break

        elif user_input == '2' or user_input == 'add movie':
            while True:
                title = input("Enter a title: ").strip()
                min_age = input("Enter a min age: ").strip()
                if min_age.isdigit():
                    min_age = int(min_age)
                else:
                    clear_terminal()
                    continue
                request_data = json.dumps({
                    'payload': {
                        'title': title,
                        'min_age': min_age,
                    },
                    'url': 'add_movie'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    film = response['film']
                    print("Movie Added!")
                    print(
                        f"Film ID: {film['id']} \nTitle: {film['title']}\nMin Age: {film['min_age']}")
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '3' or user_input == 'delete movie':
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
                if selected_movie not in map(str, [movie['id'] for movie in movies]):
                    clear_terminal()
                    print("Invalid Movie Id")
                    continue
                elif selected_movie == 'quit':
                    break
                request_data = json.dumps({
                    'payload': {
                        'movie_id': selected_movie,
                    },
                    'url': 'delete_movie'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Movie Deleted Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '4' or user_input == 'update movie':
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
                if selected_movie not in map(str, [movie['id'] for movie in movies]):
                    clear_terminal()
                    print('Invalid Movie ID')
                    continue
                elif selected_movie == 'quit':
                    break

                new_title = input("Enter New Title: ")
                new_min_age = input("Enter New Min Age: ")
                if new_min_age.isdigit():
                    new_min_age = int(new_min_age)
                else:
                    clear_terminal()
                    print("Wrong New Min Age")
                    continue
                request_data = json.dumps({
                    'payload': {
                        'movie_id': selected_movie,
                        'fields': {
                            'title': new_title,
                            'min_age': new_min_age
                        }
                    },
                    'url': 'update_movie'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    print('Movie Updated Successfully')
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue


if __name__ == "__main__":
    main()
