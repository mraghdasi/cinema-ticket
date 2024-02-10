import json

# incoming : package and subscription details
# outgoing : banking process and updating user
from src.utils.utils import clear_terminal


def main(client):
    # package = bronze , silver , gold

    # if package == one of the packages

    # payment stuff and changes in db (should use other modules and db)

    # returns user_info

    # ===========================Please Check my Code==========================

    # check buy_ticket.py and card_registration.py

    while True:
        print('Please choose your package:\n  1. Bronze\n  2. Silver\n  3. Gold\n 4. Quit')

        user_choice = input("Enter package number (1/2/3) or 4 to quit: ").strip().lower()

        if user_choice == '4' or user_choice == 'quit':
            print('Exiting the program...')
            break
        elif user_choice == '1' or user_choice == 'bronze':
            user_package = 'Bronze'
        elif user_choice == '2' or user_choice == 'silver':
            user_package = 'Silver'
        elif user_choice == '3' or user_choice == 'gold':
            user_package = 'Gold'
            # else can be 100000000000000000 other stuff . use elif and have bronze in opts
            # edited.
        else:
            print("Invalid package number. Please try again.")
            continue

        clear_terminal()
        print(f"You selected {user_package} package.")
        # print("At this step the user should be taken to the payment stuff and changes in the database.")

        # $$$$$$$ Foroutan $$$$$$$
        # Payment Method
        request_data = json.dumps({
            'payload': {
                'user_package': user_package,
            },
            'url': 'buy_subscription'
        })
        client.send(request_data.encode('utf-8'))
        response = client.recv(5 * 1024).decode('utf-8')
        response = json.loads(response)
        if response['status_code'] == 200:
            payload = response['subscription']
            print(
                f"Subscription Id: {payload['id']}\nPackage Title: {response['package']['title']}\nExpired At: {payload['expire_at']}")
            break
        else:
            print(response['msg'])
            continue


if __name__ == '__main__':
    main()
