import json
import os

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
        user = response['profile']
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

            # input (1.username ...)
        try:
            select_option = input(
                "Which Setting Do You Want To Change ?: ").lower().split()
            if select_option == '1' or 'username':
                new_username = input("Enter New Username: ")
                # Validation ?
                User.objects.update({"username": new_username}, f"id={user.id}")
                print("Username has been updated successfully!")

            elif select_option == '2' or 'email':
                new_email = input("Enter New Email: ").lower().split()
                # Validation ?
                User.objects.update({"email": new_email}, f"id={user.id}")
                print("Email has been updated successfully!")

            elif select_option == '3' or 'phone number':
                new_phone_number = int(input('Enter New Phone Number :'))
                # Validation ?
                User.objects.update(
                    {"phone number": new_phone_number}, f"id={user.id}")
                print("Phone number has been updated successfully!")

            elif select_option == '4' or 'password':
                password = input("Enter Current Password: ")
                new_password = input("Enter New Password: ")
                confirm_new_password = input("Confirm New Password: ")
                if (new_password == confirm_new_password) and (password == user.password):
                    # hash string and Validator ?
                    User.objects.update({"password": new_password}, f"id={user.id}")
                    print("Password has been updated successfully!")
                else:
                    print("Password could not be updated due to invalid input or verification error.")

        except ValueError:
            print("Invalid input! Please enter a valid option number.")

            request_data = json.dumps({
                'payload': {
                    'user_id': user.id,
                },
                'url': 'user_modification'
            })
            client.send(request_data.encode('utf-8'))
            response = client.recv(5 * 1024).decode('utf-8')
            response = json.loads(response)


            if response['status_code'] == 200:
                pass
            else:
                print(response['msg'])
                continue
        break


        # where is the else statement and error handling ?
        # success message
        # ctrl+c for exiting the loop

        # change username, email, phone no (change or add) , pass


if __name__ == '__main__':
    main('m')
