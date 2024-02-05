import os


def main(user_info, movie=None):
    # Create dictionary to map day codes to numeric values
    day_codes = {'Sat': 1, 'Sun': 2, 'Mon': 3, 'Tue': 4, 'Wed': 5, 'Thu': 6, 'Fri': 7}
    while True:
        print("Please choose your movie")

        # Available movies
        movies = [
            {
                'name': 'Spiderman',
                'min_age': 12,
                'rating': 8.8,
                'length': 148,
                'sans': [
                    {'day': 'Sat', 'start_time': '14:00', 'end_time': '16:00'},
                    {'day': 'Sat', 'start_time': '18:00', 'end_time': '20:00'},
                    {'day': 'Wed', 'start_time': '21:00', 'end_time': '23:00'},
                    {'day': 'Wed', 'start_time': '19:00', 'end_time': '20:00'},
                    {'day': 'Thu', 'start_time': '14:00', 'end_time': '16:00'},
                    {'day': 'Thu', 'start_time': '21:00', 'end_time': '23:00'}
                ],
                'comments number': 1050,
                'ticket price': 12
            },
            {
                'name': 'Batman',
                'min_age': 13,
                'rating': 9.0,
                'length': 152,
                'sans': [
                    {'day': 'Fri', 'start_time': '15:00', 'end_time': '17:00'},
                    {'day': 'Sat', 'start_time': '12:00', 'end_time': '14:00'},
                    {'day': 'Sun', 'start_time': '18:00', 'end_time': '20:00'}
                ],
                'comments number': 876,
                'ticket price': 11
            }
        ]

        movies_dict = {}

        for movie in movies:
            name = movie['name']
            sans = movie['sans']
            if name not in movies_dict:
                movies_dict[name] = {'Sat': [], 'Sun': [], 'Mon': [], 'Tue': [], 'Wed': [], 'Thu': [], 'Fri': []}
            for san in sans:
                day = san['day'][:3]
                start_time = san['start_time']
                end_time = san['end_time']
                time_range = f"{start_time} to {end_time} (price {movie['ticket price']} USD)"
                movies_dict[name][day] = movies_dict[name].get(day, []) + [time_range]

        # Print available movies
        print("List of available movies:")
        for i, movie in enumerate(movies, start=1):
            print(f"{i}. {movie['name']}")
        print("q. Quit")

        # Get user input for movie choice
        movie_choice = input("Enter movie name or number: ").strip().lower()
        # ----------------

        # here user should be able to type the movie name or the movie number on menu 1.spiderman
        # the correct input is either 1 or spiderman                            *
        # and you should use .strip() and .lower() on this types of inputs

        # ------------------

        if movie_choice == 'q':
            print('Exiting the program...')
            break

        if movie_choice not in [str(i) for i in range(1, len(movies) + 1)] + [movie['name'].lower() for movie in movies]:
            print("Invalid movie. Please try again.")
            continue

        if movie_choice.isdigit():
            movie = movies[int(movie_choice) - 1]
        else:
            for m in movies:
                if m['name'].lower() == movie_choice:
                    movie = m
                    break

        showtimes = movies_dict[movie['name']]

        # Print available showtimes
        print("\n{0}:".format(movie['name']))

        for day, times in showtimes.items():
            if not times:
                continue
            numerized_day = day_codes[day]
            print("{0}. {1}:".format(numerized_day, day))
            for i, t in enumerate(times, start=1):
                print("  {0}. {1}".format(i, t))

        while True:
            # Get user input for showtime choice
            selected_time = input("Enter day and time number (e.g. 1-2): ").strip()

            if selected_time == 'q':
                break

            # Validate user input for showtime choice
            try:
                day_number, time_number = map(int, selected_time.split('-'))
            except ValueError:
                print("Invalid input. Please enter day and time number like '1-2'.")
                continue

            if not 1 <= day_number <= len(showtimes) or not 1 <= time_number <= len(
                    showtimes[list(showtimes.keys())[day_number - 1]]):
                print("Invalid input. Please enter a valid day and time number.")
                continue

            day = list(showtimes.keys())[day_number - 1]
            selected_time = showtimes[day][time_number - 1]

            print("Selected time: {0} - {1}".format(day, selected_time))

            # Print payment information
            print("\n============================")
            print("Movie Name: {0}".format(movie['name']))
            print("{0} {1}".format(day, selected_time))
            print("Price: {0} USD".format(movie['ticket price']))
            print("\n1. Confirm Payment")
            print("2. Go back to movie selection")
            print("q. Quit")

            # Get user input for payment choice
            payment_choice = input("Enter your choice (1, 2, or q): ").strip()

            if payment_choice == '1':
                print("Payment successful. Thank you for your purchase!")
                return user_info
            # -----------

            # you didn't check for correct input here
            # first check for correct format (x-y)
            # second check if the indexing is right

            # opt1 : use try except
            # opt2 : use if elif else

            elif payment_choice == '2':
                break

            elif payment_choice == 'q':
                print('Exiting the program...')
                return user_info

# -------------------

# A few other comments on this file :
# 1.you have to have a quit option for you menu
# 2.you have to have a test payment menu for ex:
# ========
#       Movie Name
#
#     date sans hall
#
#          price
#
# 1.confirm(this will go for payment stuff)
# 2.quit(the user should be able to check other sans or other movies in this file (basically run the loop again))
# =========
#
# 3.pay attention that if something goes wrong you should not always run the loop again
#       for example if user gave invalid input when choosing sans you should only get the sans input another time
# 4. pay attention that if everything goes ok the program should stop working

# -------------------



main('m', 'm')