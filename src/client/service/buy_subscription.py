import os

def main(user_info):
    while True:
        print('please choose your package')
        
        # package = bronze , silver , gold
        
        # if package == one of the packages
        
        # payment stuff and changes in db (should use othere modules and db)
        
        # returns user_info



    #===========================Please Check my Code==========================

    # check buy_ticket.py and card_registration.py

    while True:
        print('please choose your package:\n  1. silver\n  2. gold')

        user_choice = input("Enter package number (1/2) or 'q' to quit: ")
        if user_choice == 'q':
            print('Exiting the program...')
            break
        elif user_choice == '1':
            user_package = 'silver'
        elif user_choice == '2':
            user_package = 'gold'
        else:
            user_package = 'bronze'

        # else can be 100000000000000000 other stuff . use elif and have bronze in opts

        if user_choice in {'1', '2'}:
            print("You selected", user_package)
            print('At this step the user should be taken to Payment stuff and changes in db')
            break
        else:
            print("Invalid package number. Please try again.")