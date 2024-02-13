# Commenting.py
import json

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
        if selected_movie not in map(str, [movie['id'] for movie in movies]):
            clear_terminal()
            print("Invalid Movie Id")
            continue
        elif selected_movie == 'quit':
            break

        user_input = input(
            '\n1. Show Sans\n2. Add Sans\n3. Delete Sans\n4. Update Sans\n5. Quit\n\n:').strip().lower()

        if user_input == '5' or user_input == 'quit':
            clear_terminal()
            break
        elif user_input == '1' or user_input == 'show sans':
            while True:

                request_data = json.dumps({
                    'payload': {
                        'movie_id': selected_movie['id'],
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
                                 sans['hall_id'], sans['price']] for sans in sansses])
                print(table)
                break

        elif user_input == '2' or user_input == 'add sans':
            while True:
                description = input("Enter a description: ").strip()

                request_data = json.dumps({
                    'payload': {
                        'description': description,
                        'movie_id': movie['id'],
                    },
                    'url': 'add_comment'
                })
                client.send(request_data.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                if response['status_code'] == 200:
                    comment = response['comment']
                    print("Sans Added!")
                    print(
                        f"Comment ID: {comment['id']} \nDescription: {comment['description']}\nCreated At: {comment['created_at']}")
                    break
                else:
                    clear_terminal()
                    print(response['msg'])
                    continue

        elif user_input == '3' or user_input == 'delete sans':
            while True:
                selected_comment = show_user_comments(client, movie)
                if not selected_comment:
                    break

                request_data = json.dumps({
                    'payload': {
                        'comment_id': selected_comment,
                    },
                    'url': 'delete_comment'
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
                selected_comment = show_user_comments(client, movie)
                if not selected_comment:
                    break
                new_description = input('Enter New Description: ').strip()

                if not new_description:
                    clear_terminal()
                    print('Invalid Description')
                    continue

                request_data = json.dumps({
                    'payload': {
                        'comment_id': selected_comment,
                        'new_description': new_description
                    },
                    'url': 'update_comment'
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
