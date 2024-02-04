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