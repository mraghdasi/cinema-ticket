import json
from datetime import datetime

from prettytable import PrettyTable
from prettytable import ORGMODE

from src.utils import custom_exceptions

from src.utils.transaction import TransactionType

from src.utils.utils import clear_terminal

import src.utils.custom_validators as Validators


def cancel_ticket(client):
    while True:
        request_data = json.dumps({
            'payload': {},
            'url': 'check_tickets'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            ticket_list = response['payload']
            if len(ticket_list) == 0:
                print('You have no tickets!\n')
                break
        # Check if the selected ticket is found
        if selected_ticket:
            # Find the time difference for the selected ticket
            ticket_time = datetime.strptime(selected_ticket['premiere_date'], '%Y-%m-%d')
            system_time = datetime.now()
            time_diff_hours = (ticket_time - system_time).total_seconds() / 3600
            refund_amount = 0

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
                wallet_deposit_payload = json.dumps({
                    'payload': {
                        'amount': refund_amount,
                        'transaction_log_type': TransactionType.CANCEL_TICKET.value
                    },
                    'url': 'wallet_deposit'
                })
                client.send(wallet_deposit_payload.encode('utf-8'))
                response = client.recv(5 * 1024).decode('utf-8')
                response = json.loads(response)
                print(response['msg'])

                break
            else:
                clear_terminal()
                print(response['msg'])
        else:
            print(response['msg'])
            return False

        ticket_list = sorted(ticket_list, key=lambda x: x['id'], reverse=True)

        table = PrettyTable(['Id', 'Seat', 'Ticket Data', 'Movie', 'Price'])

        for ticket in ticket_list:
            table.add_row(
                [ticket['id'], ticket['sit_number'], f"{ticket['start_time']} {ticket['end_time']}", ticket['title'],
                 ticket['price']])

        clear_terminal()
        while True:
            print(table)

            ticket_id = input("Enter the ID of the ticket you want to cancel: ").strip().lower()

            if ticket_id == 'quit':
                return True

            selected_ticket = None
            for ticket in ticket_list:
                if str(ticket['id']) == ticket_id:
                    selected_ticket = ticket
                    break
            if selected_ticket:
                ticket_time = datetime.strptime(selected_ticket['premiere_date'], '%Y-%m-%d')
                system_time = datetime.now()
                time_diff_hours = (ticket_time - system_time).total_seconds() / 3600

                if time_diff_hours > 1:
                    refund_amount = selected_ticket['price']
                    print(f"Cancelled successfully. The refund amount is {refund_amount} Toman.")
                    print(f'{refund_amount} can pass to wallet_management.py')
                elif 0 <= time_diff_hours <= 1:
                    refund_amount = int(selected_ticket['price'] * 0.82)
                    print(f"Cancelled successfully. The refund amount is {refund_amount} Toman.")
                    print(f'{refund_amount} can pass to wallet_management.py')
                else:
                    refund_amount = 0
                    print("Sorry, ticket has been expired")

                # $$$$$$$ Foroutan $$$$$$$
                # Payment Method

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


def main(client):
    while True:
        table = PrettyTable(['Number', 'Option'])
        table.add_row(['1', 'Buy Ticket'])
        table.add_row(['2', 'Cancel Ticket'])
        table.add_row(['3', 'Quit'])
        print(table)

        action_choice = input("\n:").strip().lower()
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
                continue

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

        request_data = json.dumps({
            'payload': {},
            'url': 'show_profile'
        })

        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            user = response['user']
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

        movies_title_list = [title['title'] for title in movies]
        while True:
            table = PrettyTable(['Number', 'Title'])

            print("Please choose your movie:")
            for i, m in enumerate(movies_title_list, start=1):
                table.add_row([str(i), m.capitalize()])
            table.add_row(['', ''], divider=True)
            table.add_row(['Other Options', 'Functionality'], divider=True)
            table.add_row([(len(movies) + 1), 'Quit'])
            print(table)
            movie_choice = input("Enter movie name or number: ").strip().lower()

            if movie_choice == f'{len(movies) + 1}' or movie_choice == 'quit':
                clear_terminal()
                break
            elif movie_choice.isdigit():
                try:
                    clear_terminal()
                    movie = movies[int(movie_choice) - 1]
                except IndexError:
                    clear_terminal()
                    print("Invalid input. Please try again.")
                    continue
            elif movie_choice in movies_title_list:
                clear_terminal()
                movie = movies[movies_title_list.index(movie_choice)]
            else:
                clear_terminal()
                print("Invalid input. Please try again.")
                continue

            try:
                Validators.Validator.min_age_validator(movie['min_age'], user['birthday'])
            except custom_exceptions.MinAgeValidationError:
                clear_terminal()
                print(str(custom_exceptions.MinAgeValidationError()))
                continue

            show_times = movies_dict[movie['title']]
            print(f"\n{movie['title'].capitalize()}:")

            while True:
                table = PrettyTable(['Id', 'Day', 'Show Times'])
                i = 1
                for day, times in show_times.items():
                    for t in times:
                        table.add_row(
                            [f"{t['id']}", f"{day}",
                             f"{t['start_time']} to {t['end_time']} (price {t['price']} Toman)"])
                        i += 1
                table.add_row(['', '', ''], divider=True)
                table.add_row(['Other Options', 'Functionality', ''], divider=True)
                table.add_row([str(i), 'Quit', ''])
                print(table)

                selected_time = input("Enter id number: ").strip().lower()

                if selected_time == 'quit':
                    clear_terminal()
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
                    table = PrettyTable([f'Seats for {payload["hall"]["title"]}'])
                    seats = [[str((d * 10) + (y + 1)).zfill(2) for y in range(10)] for d in
                             range(payload['hall']['capacity'] // 10)]
                    reserved_tickets_seats = [ticket['sit_number'] for ticket in payload['sans_tickets']]
                    for seat_number in reserved_tickets_seats:
                        seats[(seat_number // 10) if (seat_number % 10) != 0 else (seat_number // 10) - 1][
                            (seat_number % 10) - 1] = '**'
                    for seat in seats:
                        table.add_row([seat], divider=True)
                    table.set_style(ORGMODE)
                    clear_terminal()
                    print(table)

                    seat_to_reserve_input = input(
                        'Enter the seat you want(type quit to exit this part): ').lower().strip()
                    if seat_to_reserve_input == 'quit':
                        clear_terminal()
                        break
                    elif seat_to_reserve_input not in [seat.zfill(2) for seat in
                                                       map(str, range(1, payload['hall']['capacity'] + 1))]:
                        clear_terminal()
                        print('This seat number is not valid')
                        continue

                    reserved_seats = [seat.zfill(2) for seat in map(str, reserved_tickets_seats)]
                    if seat_to_reserve_input in reserved_seats:
                        clear_terminal()
                        print('This seat has been reserved')
                        continue
                    while True:
                        print(
                            f"\n============================\n"
                            f"      Movie Name: {movie['title']}\n"
                            f"{selected_sans['premiere_date']} {selected_sans['start_time']} to {selected_sans['end_time']}\n"
                            f"      Price: {selected_sans['price']} Toman\n")

                        payment_choice = input("1.Confirm Payment   2.Quit\n\n:").strip().lower()
                        if payment_choice == '2' or payment_choice == 'quit':
                            clear_terminal()
                            break
                        elif payment_choice == '1' or payment_choice == 'confirm payment':
                            clear_terminal()
                            print("Payment successful. Thank you for your purchase!")
                            request_data = json.dumps({
                                'payload': {},
                                'url': 'check_subscription'})
                            client.send(request_data.encode('utf-8'))
                            response = client.recv(5 * 1024).decode('utf-8')
                            response = json.loads(response)
                            if response['status_code'] == 200:
                                cash_back_amount = 0
                                package = response['package']
                                if package['title'] == 'Gold':
                                    cash_back_amount = selected_sans['price'] * (int(package['cash_back']) / 100)
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
                                            cash_back_amount = selected_sans['price'] * (
                                                    int(package['cash_back']) / 100)
                                        else:
                                            cash_back_amount = 0
                                    else:
                                        print(response['msg'])
                                        continue
                            else:
                                print(response['msg'])
                                continue
                            wallet_deposit_payload = json.dumps({
                                'payload': {
                                    'amount': cash_back_amount,
                                    'transaction_log_type': TransactionType.DEPOSIT_WALLET.value
                                },
                                'url': 'wallet_deposit'
                            })
                            client.send(wallet_deposit_payload.encode('utf-8'))
                            response = client.recv(5 * 1024).decode('utf-8')
                            response = json.loads(response)
                            if response['status_code'] == 200:
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
                                    clear_terminal()
                                    print(
                                        f"Ticket Id: {ticket['id']} For {selected_sans['premiere_date']}"
                                        f" {selected_sans['start_time']} to {selected_sans['end_time']}\n "
                                        f"Seat Number: {ticket['sit_number']}")
                                    return 'Payed'
                                else:
                                    clear_terminal()
                                    print(response['msg'])
                            else:
                                clear_terminal()
                                print(response['msg'])
                                continue
                        else:
                            clear_terminal()
                            print("Invalid input. Please enter a valid choice.")
                            continue


if __name__ == '__main__':
    main()
