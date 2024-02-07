import os
import sys

<<<<<<< HEAD
users = {
    1: {'id': '2354', 'name': 'John', 'wallet': 20, 'subscription': 'bronze'},
    2: {'id': '756', 'name': 'Amy', 'wallet': 50, 'subscription': 'bronze'},
    3: {'id': '23', 'name': 'David', 'wallet': 60, 'subscription': 'bronze'}
}
=======

# incoming : package and subscription details
# outgoing : banking process and updating user

def main(user_info):
    # package = bronze , silver , gold

    # if package == one of the packages
>>>>>>> 088e7274ade2f7231d3e28287bed02c373c4ab9f

    # payment stuff and changes in db (should use other modules and db)

<<<<<<< HEAD
def main(user_input):
    # package = bronze , silver , gold

    # if package == one of the packages

    # payment stuff and changes in db (should use othere modules and db)

    # returns user_info

=======
    # returns user_info

>>>>>>> 088e7274ade2f7231d3e28287bed02c373c4ab9f
    # ===========================Please Check my Code==========================

    # check buy_ticket.py and card_registration.py


    def search_user(user_input):
        for _, user_info in users.items():
            if user_input == user_info['id'] or user_input == user_info['name']:
                return user_info
        return None

    # Defining update_wallet function inside main
    def update_wallet(user_id, new_amount):
        user_info = search_user(user_id)
        if user_info is None:
            print("User not found.")
            return False

        user_info['wallet'] = new_amount
        return True

    # Defining buy_subscription function inside main
    def buy_subscription(user_id):
        user_info = search_user(user_id)
        if user_info is None:
            print("User not found.")
            return

<<<<<<< HEAD
        print(f"Welcome {user_info['name']}!")

        while True:
            print("Please choose your subscription:")
            print(" **Bronze (ّFree basic service)**")
            print("1. Silver (20% cashback on up to 3 future purchases)")
            print("2. Gold (50% cashback on next purchase + free drink)")
            print("Q. Quit")

            choice = input("Enter your choice (1-2, or Q to quit): ")
            if choice.lower() == "q":
                print("Goodbye!")
                sys.exit()  # Exit the program if user enters "q" or "Q"
            if choice not in ["1", "2"]:
                print("Invalid choice.")
                continue

            subscription_type = ""
            duration = 0

            if choice == "1":
                subscription_type = "Silver"
                duration = 30
            elif choice == "2":
                subscription_type = "Gold"
                duration = 30

            print(f"You selected {subscription_type} subscription for {duration} days.")

            amount = 0

            if subscription_type == "Silver":
                amount = 20

            elif subscription_type == "Gold":
                amount = 50

            while True:
                pay = input("Would you like to pay now? (Y/N): ").lower()
                if pay == "y":
                    print("Redirecting to WALLET MANAGEMENT.PY...")
                    return
                elif pay == "n":
                    print("Goodbye!")
                    sys.exit()  # Exit the program if user does not want to pay
                else:
                    print("Invalid choice.")
                    continue

    user_info = search_user(user_input)
    if user_info is None:
        print("User not found.")
        return

    buy_subscription(user_info['id'])


if __name__ == '__main__':
    main('2354')
=======

user_info = {'name': 'John', 'email': 'john@example.com'}
main(user_info)
>>>>>>> 088e7274ade2f7231d3e28287bed02c373c4ab9f
