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
        movie_list = [('spiderman', 'sat', '2 to 4 (price)'), ('spiderman', 'sat', '5 to 7 (price)'),
                      ('spiderman', 'sun', '4 to 6 (price)'), ('batman', 'sat', '3 to 5 (price)'),
                      ('batman', 'sat', '6 to 8 (price)'), ('batman', 'sun', '5 to 7 (price)'),
                      ('joker', 'sat', '4 to 6 (price)'), ('joker', 'sat', '7 to 9 (price)'),
                      ('joker', 'sun', '6 to 8 (price)')]

        movies_dict = {}

        for m, d, t in movie_list:
            if m not in movies_dict:
                movies_dict[m] = {'sat': [], 'sun': []}
            movies_dict[m][d].append(t)

        movie_name = input("Enter movie name: ")
        if movie_name in movies_dict:
            showtimes = movies_dict[movie_name]
            print("{0}:".format(movie_name))
            for day_number, (day, times) in enumerate(showtimes.items(), 1):
                print("{0}. {1}:".format(day_number, day))
                for i, t in enumerate(times):
                    print("  {0}. {1}".format(i + 1, t))

            selected_time = input("Enter day and time number: ")
            day_number, time_number = map(int, selected_time.split('-'))
            day = list(showtimes.keys())[day_number - 1]
            selected_time = showtimes[day][time_number - 1]
            print("Selected time: {0} - {1}".format(day, selected_time))
            print("***At this step the user should be taken to the payment page***")
        else:
            print("Movie not found.")