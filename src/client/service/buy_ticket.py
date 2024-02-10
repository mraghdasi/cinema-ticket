import json
from datetime import datetime

from prettytable import PrettyTable

# incoming data : available movies and show_times , list of bought tickets (if available) , wallet info
# outgoing data : a ticket that user bought (the ticket itself , wallet updating , lowering the capacity for that sans,
# if wallet doesn't have enough money it should be charged , checking for birthday discount , cash back check)
from src.utils.utils import clear_terminal


# ======================```============install  PrettyTable library ============```=============


def cancel_ticket(client):
    # movie date and movie time please

    request_data = json.dumps({
        'payload': {},
        'url': 'check_tickets'
    })
    client.send(request_data.encode('utf-8'))
    response = client.recv(5 * 1024).decode('utf-8')
    response = json.loads(response)
    if response['status_code'] == 200:
        ticket_list = response['payload']
    else:
        print(response['msg'])
        return False

    # ticket_list = [
    #     {
    #         'ticket_id': 1,
    #         'movie': 'Batman',
    #         'quantity': 2,
    #         'price': 22,
    #         'total_price': 44,
    #         'purchase_date': '2021-09-04',
    #         'time': '19:00'
    #     },
    #     {
    #         'ticket_id': 2,
    #         'movie': 'Spiderman',
    #         'quantity': 3,
    #         'price': 36,
    #         'total_price': 108,
    #         'purchase_date': '2021-09-05',
    #         'time': '14:00'
    #     },
    #     {
    #         'ticket_id': 3,
    #         'movie': 'Batman',
    #         'quantity': 1,
    #         'price': 11,
    #         'total_price': 11,
    #         'purchase_date': '2025-08-31',
    #         'time': '15:00'
    #     },
    #     {
    #         'ticket_id': 4,
    #         'movie': 'Spiderman',
    #         'quantity': 2,
    #         'price': 24,
    #         'total_price': 48,
    #         'purchase_date': '2025-08-30',
    #         'time': '19:00'
    #     },
    #     {
    #         'ticket_id': 5,
    #         'movie': 'Spiderman',
    #         'quantity': 1,
    #         'price': 12,
    #         'total_price': 12,
    #         'purchase_date': '2021-08-29',
    #         'time': '21:00'
    #     }
    # ]

    # Sort the ticket_list by purchase date and time
    ticket_list = sorted(ticket_list, key=lambda x: x['id'], reverse=True)

    # Create a new table with the desired columns
    table = PrettyTable(['Id', 'Seat', 'Ticket Data', 'Movie', 'Price'])

    # Add each ticket's data as a row to the table
    for ticket in ticket_list:
        table.add_row(
            [ticket['id'], ticket['sit_number'], f"{ticket['start_time']} {ticket['end_time']}", ticket['title'],
             ticket['price']])

    clear_terminal()
    while True:
        # Print the table and ask for a ticket_id to cancel
        print(table)
        # Error handling
        # And a quit option
        ticket_id = input("Enter the ID of the ticket you want to cancel: ").strip().lower()

        if ticket_id == 'quit':
            return True

        # Find the selected ticket by ticket_id
        selected_ticket = None
        for ticket in ticket_list:
            if str(ticket['id']) == ticket_id:
                selected_ticket = ticket
                break
        # Check if the selected ticket is found
        if selected_ticket:
            # Find the time difference for the selected ticket
            ticket_time = datetime.strptime(selected_ticket['premiere_date'], '%Y-%m-%d')
            system_time = datetime.now()
            time_diff_hours = (ticket_time - system_time).total_seconds() / 3600

            # Calculate refund amount based on time difference
            if time_diff_hours > 1:
                refund_amount = selected_ticket['price']
                print(f"Cancelled successfully. The refund amount is {refund_amount} Toman.")
                print(f'{refund_amount} can pass to wallet_management.py')
                # 0 <= time_diff_hours <= 1 , no need for and XD
            elif 0 <= time_diff_hours <= 1:
                refund_amount = int(selected_ticket['price'] * 0.82)
                print(f"Cancelled successfully. The refund amount is {refund_amount} Toman.")
                print(f'{refund_amount} can pass to wallet_management.py')
            else:
                refund_amount = 0
                print("Sorry, ticket has been expired")

            request_data = json.dumps({
                'payload': {'ticket_id': selected_ticket['id']},
                'url': 'cancel_ticket'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)
            if response['status_code'] == 200:
                clear_terminal()
                # add_to_wallet(refund_amount)
                break
            else:
                clear_terminal()
                print(response['msg'])
        else:
            clear_terminal()
            print("Sorry, the ticket with the given ID could not be found.")


def main(client, movie=None):
    # Create dictionary to map day codes to numeric values
    while True:
        print("Please choose your action:\n1. Buy Ticket\n2. Cancel ticket\n3. Quit")
        # Get user input for action choice
        action_choice = input("Enter your choice (1 or 2 or 3): ").strip().lower()
        if action_choice == '3' or action_choice == 'quit':
            clear_terminal()
            break
        elif action_choice == '1' and action_choice == 'buy ticket':
            clear_terminal()
            pass
        elif action_choice == '2' or action_choice == 'cancel ticket':
            clear_terminal()
            if cancel_ticket(client):
                clear_terminal()
                break
            else:
                clear_terminal()
                continue

        print("Please choose your movie")
        # Available movies
        request_data = json.dumps({
            'payload': {},
            'url': 'get_movies'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            movies = response['payload']
            movies = [movie for movie in movies if len(movie['sans']) != 0]

        else:
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
        if movie_choice == 'q':
            print('Exiting the program...')
            break
        elif movie_choice not in [str(i) for i in range(1, len(movies) + 1)] + [movie['title'].lower() for movie in
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
                if m['title'].lower() == movie_choice:
                    movie = m
                    break

        show_times = movies_dict[movie['title']]
        # Print available show_times
        print(f"\n{movie['title']}:")
        while True:
            table = PrettyTable(['Id', 'Day', 'Show Times'])
            for day, times in show_times.items():
                for t in times:
                    table.add_row(
                        [f"{t['id']}", f"{day}", f"{t['start_time']} to {t['end_time']} (price {t['price']} Toman)"])
            print(table)

            # Get user input for showtime choice
            selected_time = input("Enter id number: ").strip().lower()

            if selected_time == 'q':
                break
            try:
                selected_sans = [sans for sans in movie['sans'] if selected_time == str(sans['id'])][0]
            except IndexError:
                clear_terminal()
                print('Wrong id entered!')
                continue

            request_data = json.dumps({
                'payload': {
                    'hall_id': selected_sans['hall_id'],
                    'sans_id': selected_sans['id'],
                },
                'url': 'check_seats'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)
            if response['status_code'] == 200:
                payload = response['payload']
            else:
                print(response['msg'])
                continue
            while True:
                seats = [[str((d * 10) + (y + 1)).zfill(2) for y in range(10)] for d in
                         range(payload['hall']['capacity'] // 10)]
                reserved_tickets_seats = [ticket['sit_number'] for ticket in payload['sans_tickets']]
                for seat_number in reserved_tickets_seats:
                    seats[(seat_number // 10) if (seat_number % 10) != 0 else (seat_number // 10) - 1][
                        (seat_number % 10) - 1] = '**'
                for seat in seats:
                    print(seat)

                seat_to_reserve_input = input('Enter the seat you want: ')

                # Validate Valid Seat Number
                if seat_to_reserve_input not in [seat.zfill(2) for seat in
                                                 map(str, range(1, payload['hall']['capacity'] + 1))]:
                    clear_terminal()
                    print('This seat number is not valid')
                    continue

                # Validate Not Reserved
                reserved_seats = map(str, reserved_tickets_seats)
                if seat_to_reserve_input in reserved_seats:
                    clear_terminal()
                    print('This seat has been reserved')
                    continue
                break

            clear_terminal()
            while True:
                print("\n============================")
                print(f"Movie Name: {movie['title']}")
                print(f"{selected_sans['premiere_date']} {selected_sans['start_time']} to {selected_sans['end_time']}")
                print(f"Price: {selected_sans['price']} Toman")
                print("\n1. Confirm Payment")
                print("2. Go back")
                print("3. Quit")

                # Get user input for payment choice
                payment_choice = input("Enter your choice: ").strip().lower()
                if payment_choice == '3' or payment_choice == 'quit':
                    print('Exiting the program...')
                    return 'Quited'
                elif payment_choice == '1' or payment_choice == 'confirm payment':
                    clear_terminal()
                    # $$$$$$$ Foroutan $$$$$$$
                    # Payment Method
                    print("Payment successful. Thank you for your purchase!")
                    request_data = json.dumps({
                        'payload': {
                            'sans_id': selected_sans['id'],
                            'sit': seat_to_reserve_input
                        },
                        'url': 'add_ticket'
                    })
                    client.send(request_data.encode('utf-8'))
                    response = client.recv(5 * 1024).decode('utf-8')
                    response = json.loads(response)
                    ticket = response['payload']
                    if response['status_code'] == 200:
                        print(
                            f"Ticket Id: {ticket['id']} For {selected_sans['premiere_date']} {selected_sans['start_time']} to {selected_sans['end_time']}\n Seat Number: {ticket['sit_number']}")

                        # Check Subscription
                        request_data = json.dumps({
                            'payload': {},
                            'url': 'check_subscription'
                        })
                        client.send(request_data.encode('utf-8'))
                        response = client.recv(5 * 1024).decode('utf-8')
                        response = json.loads(response)
                        if response['status_code'] == 200:
                            package = response['package']
                            if package['title'] == 'Gold':
                                cash_back_amount = selected_sans['price'] * 0.5
                                print(f'Cash Back Amount: {cash_back_amount}')
                                print('You Have A Free Cocktail!')
                            elif package['title'] == 'Silver':
                                request_data = json.dumps({
                                    'payload': {},
                                    'url': 'check_tickets'
                                })
                                client.send(request_data.encode('utf-8'))
                                response = client.recv(5 * 1024).decode('utf-8')
                                response = json.loads(response)
                                if response['status_code'] == 200:
                                    ticket_list = response['payload']
                                    if len(ticket_list) < 3:
                                        cash_back_amount = selected_sans['price'] * 0.2
                                    else:
                                        cash_back_amount = 0
                                else:
                                    print(response['msg'])
                                    continue
                                print(f'Cash Back Amount: {cash_back_amount}')
                            else:
                                pass
                            return 'Payed'
                        else:
                            print(response['msg'])
                            continue
                    else:
                        print(response['msg'])
                        continue

                elif payment_choice == '2':
                    break

                else:
                    print("Invalid input. Please enter a valid choice.")
                    continue


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

# sansegit pull origin m
if __name__ == '__main__':
    main('m', 'm')
