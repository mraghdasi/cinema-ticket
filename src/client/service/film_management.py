import os
from prettytable import PrettyTable


# ======================```============install  PrettyTable library ============```=============

def main(user_info):
    movies = [
        {
            'name': 'Spiderman',
            'min_age': 12,
            'rating': 8.8,
            'length': 148,
            'shows': [
                {'day': 'Saturday', 'start_time': '14:00', 'end_time': '16:00'},
                {'day': 'Saturday', 'start_time': '18:00', 'end_time': '20:00'},
                {'day': 'Wednesday', 'start_time': '21:00', 'end_time': '23:00'},
                {'day': 'Wednesday', 'start_time': '19:00', 'end_time': '20:00'},
                {'day': 'Thursday', 'start_time': '14:00', 'end_time': '16:00'},
                {'day': 'Thursday', 'start_time': '21:00', 'end_time': '23:00'}
            ],
            'comments_number': 1050,
            'ticket_price': 12
        },
        {
            'name': 'Batman',
            'min_age': 13,
            'rating': 9.0,
            'length': 152,
            'shows': [
                {'day': 'Friday', 'start_time': '15:00', 'end_time': '17:00'},
                {'day': 'Saturday', 'start_time': '12:00', 'end_time': '14:00'},
                {'day': 'Sunday', 'start_time': '18:00', 'end_time': '20:00'}
            ],
            'comments_number': 876,
            'ticket_price': 11
        }
    ]

    while True:
        print("Please choose your movie:")

        # input(a list of available movies)

        # if input in available movies :
        #     show details (name min age rating length sans comments num, buy ticket)
        #     input
        #     (buy ticket (runs buy_ticket.py staring in line 12 showing sans instead of making user choose a movie ,
        #     comment (runs commenting.py)))

        # ========================Please Check The Code =======================

        # Display a list of available movies
        movie_dict = {}
        for i, movie in enumerate(movies):
            movie_dict[str(i + 1)] = movie
            print(f"{i + 1}. {movie['name'].title()}")

        selected_movie = input("Enter the name or number of the movie: ").title()
        selected_movie_details = None
        if selected_movie.isdigit():
            selected_movie_details = movie_dict.get(selected_movie)
        else:
            for movie in movies:
                if movie['name'].title() == selected_movie:
                    selected_movie_details = movie
                    break

        if selected_movie_details:
            # please do all this in one print statement (use multi line str)
            print("\n" + "=" * 50)
            print(selected_movie_details['name'])
            print("=" * 50)
            print(f"Minimum Age: {selected_movie_details['min_age']}")
            print(f"Rating: {selected_movie_details['rating']:.1f}/10")
            print(f"Duration: {selected_movie_details['length']} minutes")

            # Create a table for the movie schedule
            table = PrettyTable()
            table.field_names = ["Day", "Time", "Price"]
            for show in selected_movie_details['shows']:
                day = show['day']
                start_time = show['start_time']
                end_time = show['end_time']
                price = selected_movie_details['ticket_price']
                table.add_row([day, f"{start_time}-{end_time}", f"{price} Toman"])

            print("Showtimes:")
            print(table)

            print(f"Number of comments: {selected_movie_details['comments_number']}")
            print(f"Ticket price: {selected_movie_details['ticket_price']} Toman")
            print("\nPlease select one of the options below:")
            print("1) Buy ticket")
            print("2) Leave a comment")
            print("3) Quit")

            selected_option = input("Enter your choice: ")
            if selected_option.isdigit():
                selected_option = int(selected_option)

                # A very fun and cool approach to use os.system, but we have to import these files
                # Keep in mind that buying ticket (from this file) and commenting both have an input called movie name
                # you have to pass movie name to them
                # don't forget that we have to clear terminal in some cases, and we have a function for it in utils
                # options should be selected by numbers or names selected_option == 1 or  selected_option == 'Buy'

                if selected_option == 1:
                    os.system("python buy_ticket.py")
                elif selected_option == 2:
                    os.system("python commenting.py")
                elif selected_option == 3:
                    print("Thanks for using our app!")
                    break
                else:
                    print("Invalid option selected!")
                    break
            else:
                print("Invalid input! Please enter a valid number")


if __name__ == "__main__":
    main('m')

# input(buy ticket (runs buy_ticket.py staring in line 12 showing sans instead of making user choose a movie ,
# comment (runs commenting.py)))
