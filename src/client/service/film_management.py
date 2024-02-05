import os

def main(user_info):
    while True:
        print("please choose yor movie")
        
        # input(a list of available movies)
        
        # if input in available movies :
        #     show details (name min age rating length sans comments num, buy ticket)
            #   input(buy ticket (runs buy_ticket.py staring in line 12 showing sans instead of making user choose a movie , comment (runs commenting.py)))




        #========================Please Check The Code =======================
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
print("List of available movies:")
for movie in movies:
    print("- " + movie['name'])

movie_name = input("Enter the movie name: ")

for movie in movies:
    if movie_name == movie['name']:
        print("Name: " + movie['name'])
        print("Min age: " + str(movie['min_age']))
        print("Rating: " + str(movie['rating']))
        print("Length: " + str(movie['length']))
        print("Sans:")
        for day in ['sat', 'Sunday', 'Friday', 'Thursday', 'Wednesday', 'Tuesday', 'Monday']:
            day_count = 0
            sans_count = 0
            sans_times = []
            for i, s in enumerate(movie['sans']):
                if s['day'].lower() == day.lower():
                    sans_count += 1
                    day_count += 1
                    sans_times.append(f"{day_count}. {1}.{sans_count} {s['start_time']} to {s['end_time']} (price {movie['ticket price']})")
                else:
                    continue
            if sans_times:
                print(f"{day}:")
                print("  " + '\n  '.join(sans_times))
            else:
                continue
        print("Comments number: " + str(movie['comments number']))
        print("Ticket price: " + str(movie['ticket price']))
        break
else:
    print("Movie not found!")
  #   input(buy ticket (runs buy_ticket.py staring in line 12 showing sans instead of making user choose a movie , comment (runs commenting.py)))

