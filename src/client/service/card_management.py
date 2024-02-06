# import os

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

from prettytable import PrettyTable


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


def main(card_list):
    if not card_list:
        print("There is no card in your profile.")
    else:
        print("Your cards:")
        table = PrettyTable(['#', 'Card Number'])
        for i, card in enumerate(card_list, start=1):
            table.add_row([i, card])
        print(table)
        while True:
            selected = input("Please choose a card number: ")
            try:
                index = int(selected) - 1
                selected_card = card_list[index]
                break
            except (ValueError, IndexError):
                print("Invalid selection.")

        print("Selected card: ", selected_card)
        while True:
            print("You can choose one of the following options:")
            print("1. Edit card number")
            print("2. Change CVV2")
            print("3. Change expiration date")

            # Option to change password
            print("4. Change password")

            print("5. Cancel")
            choice = input("Please choose an option: ")
            if choice == '1':
                edit_card_number(card_list, selected_card)
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

    return card_list


if __name__ == '__main__':
    card_list = ['2656435571048868', '7988634497364006', '4328353309086601', '2498525345064556', '3500037762653692',
                 '3971687107588513', '8353272705341641', '7215425071807050', '6715821371280480', '7644452566589771']
    card_list = main(card_list)
