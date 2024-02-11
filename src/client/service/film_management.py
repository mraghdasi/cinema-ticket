import json

from src.client.service import commenting, rating
from src.utils.utils import clear_terminal


def main(client):
    while True:
        print("Please choose your movie:")
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

        # Print available movies
        print("List of available movies:")
        for i, m in enumerate(movies, start=1):
            print(f"{i}. {m['title']}")
        print(f"{len(movies) + 1}. Quit")

        # Get user input for movie choice
        movie_choice = input("Enter movie name or number: ").strip().lower()
        if movie_choice == (len(movies) + 1) or movie_choice == 'quit':
            print('Exiting the program...')
            break
        elif movie_choice not in [str(i) for i in range(1, len(movies) + 1)] + [movie['title'].lower() for movie in
                                                                                movies]:
            print("Invalid movie. Please try again.")
            continue

        if movie_choice.isdigit():
            movie = movies[int(movie_choice) - 1]
        else:
            for m in movies:
                if m['title'].lower() == movie_choice:
                    movie = m
                    break
            else:
                continue

        # please do all this in one print statement (use multi line str)
        print("\n" + "=" * 50)
        print(movie['title'])
        print("=" * 50)
        print(f"Minimum Age: {movie['min_age']}")

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

        print(f"Rating: {film_rating:.1f}/10")

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

        print(f"Number of rates: {len(film_rates)}")

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

        print(f"Number of comments: {len(film_comments)}")
        print("\nPlease select one of the options below:")
        print("1) Leave a comment")
        print("2) Rate film")
        print("3) Quit")

        selected_option = input("Enter your choice: ")
        if selected_option == '3' or selected_option == 'quit':
            print("Thanks for using our app!")
            break
        elif selected_option == '1' or selected_option == 'leave a comment':
            commenting.main(client, movie)
        elif selected_option == '2' or selected_option == 'rate film':
            rating.main(client, movie)
        else:
            clear_terminal()
            print("Invalid option selected!")
            continue


if __name__ == "__main__":
    main('client')

# input(buy ticket (runs buy_ticket.py staring in line 12 showing sans instead of making user choose a movie ,
# comment (runs commenting.py)))
