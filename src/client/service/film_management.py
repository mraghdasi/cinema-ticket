import json

from src.client.service import commenting, rating
from src.utils.utils import clear_terminal
from prettytable import PrettyTable


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

        movies_dict = {}

        for movie in movies:
            name = movie['title']
            sans = movie['sans']
            if name not in movies_dict:
                movies_dict[name] = {'Sat': [], 'Sun': [], 'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': []}
            for san in sans:
                day = san['premiere_date'][:3]
                movies_dict[name][day] = movies_dict[name].get(day, []) + [san]

        print("List of available movies:")

        table = PrettyTable(['Number', 'Title'])

        for i, m in enumerate(movies, start=1):
            table.add_row([str(i), m['title'].capitalize()])
        table.add_row(['', ''], divider=True)
        table.add_row(['Other Options', 'Functionality'], divider=True)
        table.add_row([(len(movies) + 1), 'Quit'])
        print(table)

        movie_choice = input("Enter movie name or number: ").strip().lower()
        if movie_choice == (len(movies) + 1) or movie_choice == 'quit':
            clear_terminal()
            break
        elif movie_choice not in [str(i) for i in range(1, len(movies) + 1)] + [movie['title'].lower() for movie in
                                                                                movies]:
            clear_terminal()
            print("Invalid movie. Please try again.")
            continue

        if movie_choice.isdigit():
            clear_terminal()
            movie = movies[int(movie_choice) - 1]
        else:
            clear_terminal()
            for m in movies:
                if m['title'].lower() == movie_choice:
                    movie = m
                    break
            else:
                continue

        request_data = json.dumps({
            'payload': {'id': movie['id']},
            'url': 'get_movie_rating'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            film_rating = response['payload']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        request_data = json.dumps({
            'payload': {'id': movie['id']},
            'url': 'get_movie_rates'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            film_rates = response['rates']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        request_data = json.dumps({
            'payload': {'id': movie['id']},
            'url': 'get_movie_comments'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            film_comments = response['comments']
        else:
            clear_terminal()
            print(response['msg'])
            continue

        table = PrettyTable([movie['title'].capitalize()])
        table.add_rows([[f"Minimum Age: {movie['min_age']}"], [f"Rating: {film_rating:.1f}/10"],
                       [f"Number of rates: {len(film_rates)}"], [f"Number of comments: {len(film_comments)}"]])
        print(table, '\n', sep=None)

        table = PrettyTable(["Please select one of the options below:"])
        table.align["Please select one of the options below:"] = 'l'
        table.add_rows([["1.Comments"], ["2.Rate film"], ["3.Quit"]])
        print(table)

        selected_option = input("Enter your choice: ").lower().strip()

        if selected_option == '3' or selected_option == 'quit':
            clear_terminal()
            break
        elif selected_option == '1' or selected_option == 'comments':
            clear_terminal()
            commenting.main(client, movie)
            break
        elif selected_option == '2' or selected_option == 'rate film':
            clear_terminal()
            rating.main(client, movie)
            break
        else:
            clear_terminal()
            print("Invalid option selected!")
            continue


if __name__ == "__main__":
    main('client')

# input(buy ticket (runs buy_ticket.py staring in line 12 showing sans instead of making user choose a movie ,
# comment (runs commenting.py)))
