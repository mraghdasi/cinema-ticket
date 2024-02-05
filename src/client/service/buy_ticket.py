import os

def main(user_info,movie=None):
    while True:
        print("please choose yor movie")
        
        # {'spiderman': {'sat' : ['2 to 4 (price)' , '5 to 7 (price)'] , 'sun' : ['4 to 6 (price)']} , 'batman' : {...} , 'joker' : {...} , ...}
        # availabel_movies = "this should be read from somewhere"
        # user_input = input(f"Here should be a list of <availabel_movies.keys>")
        
        # if user_input == one of the movies :
        #     print("choose the session and day"):
        #         print(availabel_movies[one of the movies] as key values) 
        #               1. sat : 1.2 to 4 (price)
        #                        2.5 to 7 (price)
        #               2. sun : 1.4 to 6 (price)
        #               3. ...
        #               4. ...
        # 
        #         user_input = input("a list of availabel sessions for the movie")
        #                      input should be like 1-2 (sat 5 to 7)
        # 
        #         if user_input == one of the sessions:
        #             payment stuff  and changes in db (should use othere modules and db)
        # 
        # returns user_info





        #======================Please Check my Code =========================
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
        for movie in movies:
            print("- " + movie['name'])

        movie_name = input("Enter movie name: ")
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

            selected_time = input("Enter day and time number: ")
            day_number, time_number = map(int, selected_time.split('-'))
            day = days_with_showtimes[day_number - 1]
            selected_time = showtimes[day][time_number - 1]
            print("Selected time: {0} - {1}".format(day, selected_time))
            print("***At this step the user should be taken to the payment page***")
        else:
            print("Movie not found.")