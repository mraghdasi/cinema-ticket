import os
from datetime import datetime
from prettytable import PrettyTable


# ======================```============install  PrettyTable library ============```=============

def cancel_ticket():
    # movie date and movie time please
    ticket_list = [
        {
            'ticket_id': 1,
            'movie': 'Batman',
            'quantity': 2,
            'price': 22,
            'total_price': 44,
            'purchase_date': '2021-09-04',
            'time': '19:00'
        },
        {
            'ticket_id': 2,
            'movie': 'Spiderman',
            'quantity': 3,
            'price': 36,
            'total_price': 108,
            'purchase_date': '2021-09-05',
            'time': '14:00'
        },
        {
            'ticket_id': 3,
            'movie': 'Batman',
            'quantity': 1,
            'price': 11,
            'total_price': 11,
            'purchase_date': '2025-08-31',
            'time': '15:00'
        },
        {
            'ticket_id': 4,
            'movie': 'Spiderman',
            'quantity': 2,
            'price': 24,
            'total_price': 48,
            'purchase_date': '2025-08-30',
            'time': '19:00'
        },
        {
            'ticket_id': 5,
            'movie': 'Spiderman',
            'quantity': 1,
            'price': 12,
            'total_price': 12,
            'purchase_date': '2021-08-29',
            'time': '21:00'
        }
    ]

    # Sort the ticket_list by purchase date and time
    ticket_list = sorted(ticket_list,
                         key=lambda x: datetime.strptime(x['purchase_date'] + ' ' + x['time'], '%Y-%m-%d %H:%M'))

    # Create a new table with the desired columns
    table = PrettyTable(['Ticket ID', 'Movie', 'Quantity', 'Price', 'Total Price', 'Purchase Date', 'Time'])

    # Add each ticket's data as a row to the table
    for ticket in ticket_list:
        table.add_row([ticket['ticket_id'], ticket['movie'], ticket['quantity'], ticket['price'], ticket['total_price'],
                       ticket['purchase_date'], ticket['time']])

    # Print the table and ask for a ticket_id to cancel
    print(table)
    # Error handling
    # And a quit option
    ticket_id = int(input("Enter the ID of the ticket you want to cancel: "))

    # Find the selected ticket by ticket_id
    selected_ticket = None
    for ticket in ticket_list:
        if ticket['ticket_id'] == ticket_id:
            selected_ticket = ticket
            break

    # Check if the selected ticket is found
    if selected_ticket is not None:
        # Find the time difference for the selected ticket
        ticket_time = datetime.strptime(selected_ticket['purchase_date'] + ' ' + selected_ticket['time'],
                                        '%Y-%m-%d %H:%M')
        system_time = datetime.now()
        time_diff_hours = (ticket_time - system_time).total_seconds() / 3600

        # Calculate refund amount based on time difference
        if time_diff_hours > 1:
            refund_amount = selected_ticket['price'] * selected_ticket['quantity']
            print(f"Cancelled successfully. The refund amount is {refund_amount} Toman.")
            print(f'{refund_amount} can pass to wallet_management.py')
            # 0 <= time_diff_hours <= 1 , no need for and XD
        elif time_diff_hours >= 0 and time_diff_hours <= 1:
            refund_amount = selected_ticket['price'] * selected_ticket['quantity'] * 0.82
            print(f"Cancelled successfully. The refund amount is {refund_amount} Toman.")
            print(f'{refund_amount} can pass to wallet_management.py')
        else:
            refund_amount = 0
            print("Sorry, ticket has been expired")

        # add_to_wallet(refund_amount)
    else:
        print("Sorry, the ticket with the given ID could not be found.")

    return refund_amount


def main(user_info, movie=None):
    # Create dictionary to map day codes to numeric values
    day_codes = {'Sat': 1, 'Sun': 2, 'Mon': 3, 'Tue': 4, 'Wed': 5, 'Thu': 6, 'Fri': 7}
    while True:
        print("Please choose your action:")
        print("1. Buy")
        print("2. Cancel ticket")
        print("q. Quit")
        # Get user input for action choice
        action_choice = input("Enter your choice (1 or 2 or q): ").strip()
        if action_choice == '2':
            cancel_ticket()
            print("Exiting the program...")
            break
        elif action_choice != '1' and action_choice != 'q':
            print("Invalid input. Please enter a valid choice.")
            continue

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
                time_range = f"{start_time} to {end_time} (price {movie['ticket price']} Toman)"
                movies_dict[name][day] = movies_dict[name].get(day, []) + [time_range]

        # Print available movies
        print("List of available movies:")
        for i, m in enumerate(movies, start=1):
            print(f"{i}. {m['name']}")
        print("q. Quit")

        # Get user input for movie choice
        movie_choice = input("Enter movie name or number: ").strip().lower()
        if movie_choice == 'q':
            print('Exiting the program...')
            break
        elif movie_choice not in [str(i) for i in range(1, len(movies) + 1)] + [movie['name'].lower() for movie in
                                                                                movies]:
            print("Invalid movie. Please try again.")
            continue

        if movie_choice.isdigit():
            movie = movies[int(movie_choice) - 1]

            # ----------------

            # here user should be able to type the movie name or the movie number on menu 1.spiderman
            # the correct input is either 1 or spiderman                            *
            # and you should use .strip() and .lower() on this types of inputs

            # ------------------

        else:
            for m in movies:
                if m['name'].lower() == movie_choice:
                    movie = m
                    break

        showtimes = movies_dict[movie['name']]

        # Print available showtimes
        print(f"\n{movie['name']}:")
        while True:
            table = PrettyTable(['Day', 'Showtimes'])
            for day, times in showtimes.items():
                if not times:
                    continue
                for i, t in enumerate(times, start=1):
                    table.add_row([f"{day_codes[day]}. {day}", f"{i}. {t}"])
            print(table)

            # Get user input for showtime choice
            selected_time = input("Enter day and time number (e.g. 1-2): ").strip().lower()

            if selected_time == 'q':
                break

            # Validate user input for showtime choice
            try:
                day_number, time_number = map(int, selected_time.split('-'))
            except ValueError:
                print("Invalid input. Please enter day and time number like '1-2'.")
                continue

            if not 1 <= day_number <= len(list(showtimes.keys())) or not 1 <= time_number <= len(
                    showtimes[list(showtimes.keys())[day_number - 1]]):
                print("Invalid input. Please enter a valid day and time number.")
                continue

            day = list(showtimes.keys())[day_number - 1]
            selected_time = showtimes[day][time_number - 1]

            print("Selected time: {0} - {1}".format(day, selected_time))

            # Print payment information
            while True:
                print("\n============================")
                print(f"Movie Name: {movie['name']}")
                print(f"{day} {selected_time}")
                print(f"Price: {movie['ticket price']} Toman")
                print("\n1. Confirm Payment")
                print("2. Go back")
                print("q. Quit")

                # Get user input for payment choice
                payment_choice = input("Enter your choice (1, 2, or q): ").strip()

                if payment_choice == '1':
                    print("Payment successful. Thank you for your purchase!")
                    return user_info

                elif payment_choice == '2':
                    break
                    # -----------

                    # you didn't check for correct input here
                    # first check for correct format (x-y)
                    # second check if the indexing is right

                    # opt1 : use try except
                    # opt2 : use if elif else
                elif payment_choice == 'q':
                    print('Exiting the program...')
                    return user_info

                else:
                    print("Invalid input. Please enter a valid choice.")
                    continue

            if payment_choice == '1' or payment_choice == 'q':
                break


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

#sansegit pull origin m
if __name__ == '__main__':
    main('m', 'm')
