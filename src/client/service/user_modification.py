import os

from ...server.models.user import User


def main(user_info):
    user_id = 10
    while True:
        user = User.objects.read(f"id={user_id}")[0]
        print(f'Username: {user.username}')
        print(f'Email: {user.email}')
        print(f'Phone Number: {user.phone_number}')
        print(f'Birth Date: {user.birthday.strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'Created At: {user.created_at.strftime}')
        print(f'Subscription: {user.subscription.strftime}')

        # input (1.username ...)
        select_option = input(
            "Witch Setting Do You Want To Change ?: ").lower().split()
        if select_option == '1' or 'username':
            new_username = input("Enter New Username: ")
            User.objects.update({"username": new_username}, f"id={user.id}")

        elif select_option == '2' or 'email':
            new_email = input("Enter New Email: ").lower().split()
            User.objects.update({"email": new_email}, f"id={user.id}")

        elif select_option == '3' or 'phone number':
            new_phone_number = int(input('Enter New Phone Number :'))
            User.objects.update(
                {"phone number": new_phone_number}, f"id={user.id}")

        elif select_option == '4' or 'password':
            password = input()
            new_password = input()
            confirm_new_password = input()
            if (new_password == confirm_new_password) and (password == user.password):
                User.objects.update(
                    {"password": new_password}, f"id={user.id}")

        # change username, email, phone no (change or add) , pass ,birthday
