import json
import os
from src.utils.custom_validators import Validator
import signal

from src.server.models.user import User


# incoming : account info
# outgoing : updates on account


def main(client):
    request_data = json.dumps({
        'payload': {},
        'url': 'user_modification'
    })
    client.send(request_data.encode('utf-8'))
    response = client.recv(5 * 1024).decode('utf-8')
    response = json.loads(response)

    if response['status_code'] == 200:
        user = response['user_info']
    else:
        print(response['msg'])

    while True:
        # use \n for spacing and you should use one print
        print(f'1.Username: {user["username"]}')
        print(f'2.Email: {user["email"]}')
        print(f'3.Phone Number: {user["phone_number"]}')
        print(f'4.Password: Can\'t be shown due to security reasons')
        print(f'5.Birth Date: {user["birthday"]}')
        print(f'6.Created At: {user["created_at"]}')
        print(f'7.Subscription: {user["subscription"]}')
        print(f'8.Quit')

        # input (1.username ...)
        try:
            select_option = input(
                "Which Setting Do You Want To Change ?: ").lower().strip()
            payload = {}
            if select_option == '1' or select_option == 'username':
                new_username = input("Enter New Username: ")
                # Validation ?
                if not Validator.username_validator(new_username):
                    raise ValueError("Invalid username format.")
                payload['username'] = new_username

            elif select_option == '2' or select_option == 'email':
                new_email = input("Enter New Email: ").lower().strip()
                # Validation ?
                if not Validator.email_validator(new_email):
                    raise ValueError("Invalid email format.")
                payload['email'] = new_email

            elif select_option == '3' or select_option == 'phone number':
                new_phone_number = int(input('Enter New Phone Number :'))
                # Validation ?
                if not Validator.phone_number_validator(new_phone_number):
                    raise ValueError("Invalid phone number format.")
                payload['phone number'] = new_phone_number

            elif select_option == '4' or select_option == 'password':
                password = input("Enter Current Password: ")
                new_password = input("Enter New Password: ")
                confirm_new_password = input("Confirm New Password: ")
                if (new_password == confirm_new_password) and (password == user.password):
                    # hash string and Validator ?
                    if not Validator.password_validator(new_password):
                        raise ValueError("Invalid password format.")
                    payload['password'] = new_password
                else:
                    print(
                        "Password could not be updated due to invalid input or verification error.")
                    continue

            elif select_option == '8' or select_option == 'quit':
                print("\nExiting program...")
                exit()

            request_data = json.dumps({
                'payload': payload,
                'url': 'user_modification'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)

            if response['status_code'] == 200:
                user = response['user_info']
                print("User information has been updated successfully!")
                break
            else:
                print(response['msg'])
                continue

        except KeyboardInterrupt:
            print("\nExiting program...")
            exit()

        except Exception as e:
            print("Error occurred: ", e)
        continue


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main('m')