import os

from src.server.models.user import User


def main(user_info):
    user_id = 1
    while True:
        user = User.objects.read(f"id={user_id}")[0]
        # use \n for spacing and you should use one print
        print(f'1.Username: {user.username}')
        print(f'2.Email: {user.email}')
        print(f'3.Phone Number: {user.phone_number}')
        print(f'4.Password: Can\'t be shown due to security reasons')
        print(f'Birth Date: {user.birthday.strftime("%Y-%m-%d")}')
        print(f'Created At: {user.created_at.strftime("%Y-%m-%d %H:%M")}')
        print(f'Subscription: {user.subscription_id}')

        # input (1.username ...)
        select_option = input(
            "Which Setting Do You Want To Change ?: ").lower().split()
        if select_option == '1' or 'username':
            new_username = input("Enter New Username: ")
            # Validation ?
            User.objects.update({"username": new_username}, f"id={user.id}")

        elif select_option == '2' or 'email':
            new_email = input("Enter New Email: ").lower().split()
            # Validation ?
            User.objects.update({"email": new_email}, f"id={user.id}")

        elif select_option == '3' or 'phone number':
            new_phone_number = int(input('Enter New Phone Number :'))
            # Validation ?
            User.objects.update(
                {"phone number": new_phone_number}, f"id={user.id}")

        elif select_option == '4' or 'password':
            password = input()
            new_password = input()
            confirm_new_password = input()
            if (new_password == confirm_new_password) and (password == user.password):
                # hash string and Validator ?
                User.objects.update(
                    {"password": new_password}, f"id={user.id}")

        # where is the else statement and error handling ?
        # success message
        # ctrl+c for exiting the loop

        # change username, email, phone no (change or add) , pass


if __name__ == '__main__':
    main('m')
