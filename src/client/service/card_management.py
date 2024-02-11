# import os
import json
import sys

# def main(user_info):
#     while True:
#         print('please choose your card')

#         input(list of cards)

#         if input in list of cards :

#             management options : change pass change exp date change cvv2
#             input(management options)

#         return user_info


# =========================***Please check My Code:***===============MRY=================

# check buy_ticket.py and card_registration.py

# incoming : card info
# outgoing : any updates

from prettytable import PrettyTable

from src.utils.utils import clear_terminal


def edit_card_number(card_list, selected_card):
    while True:
        new_card = input("Enter new card number: ")
        if len(new_card) == 16:
            if new_card in card_list:
                print("This card is already in your profile.")
            else:
                print(f"Card number updated. New card number is {new_card}.")
                card_list[card_list.index(selected_card)] = new_card
            break
        else:
            print("Invalid card number. Please enter a 16-digit card number.")


def change_cvv2():
    while True:
        new_cvv2 = input("Enter new CVV2: ")
        if len(new_cvv2) in (3, 4) and new_cvv2.isnumeric():
            print(f"CVV2 updated. New CVV2 is {new_cvv2}.")
            break
        print("Invalid CVV2. Please enter a 3 or 4-digit number.")


def change_expiration_date():
    new_date = input("Enter new expiration date (mm/yy): ")
    print(f"Expiration date updated. New expiration date is {new_date}.")


def main(client):
    request_data = json.dumps({
        'payload': {},
        'url': 'get_cards'
    })
    client.send(request_data.encode('utf-8'))
    response = client.recv(5 * 1024).decode('utf-8')
    response = json.loads(response)
    if response['status_code'] == 200:
        available_cards = list(response['cards'])
        card_creds = response['cards']
    elif response['status_code'] == 400:
        clear_terminal()
        sys.exit(response['msg'])
    else:
        clear_terminal()
        print(response['msg'])

    while True:
        i = 1
        print('Your Cards:')
        table = PrettyTable(['#', 'Card Number'])
        for card in available_cards:
            table.add_row([i, card])
            i += 1

        print(table + f'\n{i}.Quit')
        user_input = input("Please Select Your Card").replace(" ", "").lower()
        if user_input == str(i) or user_input == 'quit':
            clear_terminal()
            break
        try:
            if len(user_input) == 1:
                selected_card = available_cards[int(user_input) - 1]
                break
            else:
                if user_input in available_cards:
                    selected_card = available_cards[available_cards.index(user_input)]
                    break
                else:
                    clear_terminal()
                    print(f'\n{user_input} is not one of the available cards.\n')
                    continue
        except IndexError:
            clear_terminal()
            print(f'\n{user_input} is not one of the menu options')
            continue

    clear_terminal()
    print("Selected card: ", selected_card)

    while True:
        print("You can choose one of the following options:")
        print("1. Edit card number")
        print("2. Change CVV2")
        print("3. Change expiration date")
        print("4. Change password")
        print("5. Cancel")

        choice = input("Please choose an option: ")
        if choice == '1':
            edit_card_number(available_cards, selected_card)
        elif choice == '2':
            change_cvv2()
        elif choice == '3':
            change_expiration_date()
        elif choice == '4':
            current_password = input("Please enter your current password: ")
            if current_password == "1234":
                new_password = input("Please enter your new password: ")
                print("Password changed successfully!")
            else:
                print("Incorrect password. Please try again.")
        elif choice == '5':
            print("Canceled.")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == '__main__':
    main('client')
