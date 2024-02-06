# import os

# def main(user_info):
#     while True:
#         print('please choose your card')
        
#         input(list of cards)
        
#         if input in list of cards :
            
#             management options : change pass change exp date change cvv2
#             input(management options)
        
#         return user_info




#=========================***Please check My Code:***===============MRY=================

# check buy_ticket.py and card_registration.py

import sys

card_list = ['2656435571048868', '7988634497364006', '4328353309086601', '2498525345064556', '3500037762653692', '3971687107588513', '8353272705341641', '7215425071807050', '6715821371280480', '7644452566589771']
if not card_list:
    print("There is no card in your profile.")
else:
    print("Your cards:")
    for i, card in enumerate(card_list, start=1):
        print(f"{i}.{card}")
    selected = input("Please choose a card number: ")
    try:
        index = int(selected) - 1
        selected_card = card_list[index]
        print("Selected card: ", selected_card)
        while True:
            print("You can choose one of the following options:")
            print("1. Edit card number")
            print("2. Change CVV2")
            print("3. Change expiration date")
            #-------

            # password ?

            #-------
            print("4. Cancel")
            choice = input("Please choose an option: ")
            if choice == '1':
                print("Going to update.py...")
                sys.exit()
            elif choice == '2':
                print("Going to update.py...")
                sys.exit()
            elif choice == '3':
                print("Going to update.py...")
                sys.exit()
            elif choice == '4':
                print("Canceled.")
                break
            else:
                print("Invalid selection. Please try again.")
    except (ValueError, IndexError):
        print("Invalid selection.")



