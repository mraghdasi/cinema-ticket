import os


# incoming : package and subscription details
# outgoing : banking process and updating user

def main(user_info):
    # package = bronze , silver , gold

    # if package == one of the packages

    # payment stuff and changes in db (should use other modules and db)

    # returns user_info

    # ===========================Please Check my Code==========================

    # check buy_ticket.py and card_registration.py

    while True:
        print('Please choose your package:\n  1. Bronze\n  2. Silver\n  3. Gold')

        user_choice = input("Enter package number (1/2/3) or 'q' to quit: ")

        if user_choice == 'q':
            print('Exiting the program...')
            break
        elif user_choice == '1':
            user_package = 'Bronze'
        elif user_choice == '2':
            user_package = 'Silver'
        elif user_choice == '3':
            user_package = 'Gold'
            # else can be 100000000000000000 other stuff . use elif and have bronze in opts
            # edited.
        else:
            print("Invalid package number. Please try again.")
            continue

        print("You selected {0} package.".format(user_package))
        print("At this step the user should be taken to the payment stuff and changes in the database.")
        break

    return user_info


user_info = {'name': 'John', 'email': 'john@example.com'}
main(user_info)
