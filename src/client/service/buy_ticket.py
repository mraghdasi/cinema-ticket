import os


def main(user_info, movie=None):
    while True:
        print("please choose yor movie")

        # {'spiderman': {'sat' : ['2 to 4 (price)' , '5 to 7 (price)'] , 'sun' : ['4 to 6 (price)']} ,
        # 'batman' : {...} , 'joker' : {...} , ...}
        # available_movies = "this should be read from somewhere"
        # user_input = input(f"Here should be a list of <available_movies.keys>")

        # if user_input == one of the movies :
        #     print("choose the session and day"):
        #         print(available_movies[one of the movies] as key values)
        #               1. sat : 1.2 to 4 (price)
        #                        2.5 to 7 (price)
        #               2. sun : 1.4 to 6 (price)
        #               3. ...
        #               4. ...
        # 
        #         user_input = input("a list of available sessions for the movie")
        #                      input should be like 1-2 (sat 5 to 7)
        # 
        #         if user_input == one of the sessions:
        #             payment stuff  and changes in db (should use other modules and db)
        # 
        # returns user_info

        # ======================Please Check my Code =========================

        # near perfect execution it misses a few key stuff: (check below)

        movies = [
            {
                'name': 'spiderman',
                'min_age': 12,
                'rating': 8.8,
                'length': 148,
                'sans': [
                    {'day': 'sat', 'start_time': '14:00', 'end_time': '16:00'},
                    {'day': 'sat', 'start_time': '18:00', 'end_time': '20:00'},
                    {'day': 'Wednesday', 'start_time': '21:00', 'end_time': '23:00'},
                    {'day': 'Wednesday', 'start_time': '19:00', 'end_time': '20:00'},
                    {'day': 'Thursday', 'start_time': '14:00', 'end_time': '16:00'},
                    {'day': 'Thursday', 'start_time': '21:00', 'end_time': '23:00'}
                ],
                'comments number': 1050,
                'ticket price': 12
            },
            {
                'name': 'batman',
                'min_age': 13,
                'rating': 9.0,
                'length': 152,
                'sans': [
                    {'day': 'Friday', 'start_time': '15:00', 'end_time': '17:00'},
                    {'day': 'Saturday', 'start_time': '12:00', 'end_time': '14:00'},
                    {'day': 'Sunday', 'start_time': '18:00', 'end_time': '20:00'}
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
                movies_dict[name] = {'sat': [], 'sun': [], 'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': []}
            for san in sans:
                day = san['day'].lower()[:3]
                start_time = san['start_time']
                end_time = san['end_time']
                time_range = f"{start_time} to {end_time} (price {movie['ticket price']})"
                movies_dict[name][day].append(time_range)

        print("List of available movies:")
        i = 1
        for movie in movies:
            print(f"{i}.{movie['name']}")
            i += 1

        # ----------------

        # here user should be able to type the movie name or the movie number on menu 1.spiderman
        # the correct input is either 1 or spiderman
        # and you should use .strip() and .lower() on this types of inputs

        movie_name = input("Enter movie name: ")

        # --------------

        if movie_name in movies_dict:
            showtimes = movies_dict[movie_name]
            print("{0}:".format(movie_name))
            days_with_showtimes = []
            for day, times in showtimes.items():
                if times:
                    days_with_showtimes.append(day)
            for day_number, day in enumerate(days_with_showtimes, 1):
                print("{0}. {1}:".format(day_number, day))
                times = showtimes[day]
                for i, t in enumerate(times):
                    print("  {0}. {1}".format(i + 1, t))
            # -----------

            # you didn't check for correct input here
            # first check for correct format (x-y)
            # second check if the indexing is right

            # opt1 : use try except
            # opt2 : use if elif else

            selected_time = input("Enter day and time number: ")

            # -----------
            day_number, time_number = map(int, selected_time.split('-'))
            day = days_with_showtimes[day_number - 1]
            selected_time = showtimes[day][time_number - 1]
            print("Selected time: {0} - {1}".format(day, selected_time))
            print("***At this step the user should be taken to the payment page***")
        else:
            print("Movie not found.")


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
