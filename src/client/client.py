import json
import socket

#
# def main():
#     while True:
#         user_input = input('1.Login\n2.Register\n3.Quit\n\n:').lower().strip()
#
#         if user_input == '3' or user_input == 'quit':
#             clear_terminal()
#             sys.exit('*\n**\n***\nHave A Nice Day :)\n***\n**\n*')
#         elif user_input == '1' or user_input == 'login':
#             clear_terminal()
#             user_info = login.main()
#             if user_info != '':
#                 print("\nWelcome <Username> :)\n")
#                 user_info = main_menu.main(user_info)
#             continue
#         elif user_input == '2' or user_input == 'Register':
#             clear_terminal()
#             user_info = register.main()
#             if user_info != '':
#                 print("\nWelcome to our app <Username> :)\n")
#                 user_info = main_menu.main(user_info)
#             continue
#         else:
#             clear_terminal()
#             print('\nPlease enter valid input!\n')
#             continue
#
#
# main()
import sys

from src.client import main_menu
from src.client.auth import login, register
from src.utils.utils import clear_terminal

HOST = '127.0.0.1'
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    user_input = input('1.Login\n2.Register\n3.Quit\n\n:').lower().strip()

    if user_input == '3' or user_input == 'quit':
        clear_terminal()
        sys.exit('*\n**\n***\nHave A Nice Day :)\n***\n**\n*')
    elif user_input == '1' or user_input == 'login':
        clear_terminal()
        while True:
            request_data = login.main()
            client.send(request_data.encode('utf-8'))
            response = json.loads(client.recv(1024).decode('utf-8'))
            if response['status_code'] == 200:
                print("\nWelcome <Username> :)\n")
                user_info = main_menu.main(user_info)
            else:
                print(response['msg'])

    elif user_input == '2' or user_input == 'Register':
        clear_terminal()
        user_info = register.main()
        if user_info != '':
            print("\nWelcome to our app <Username> :)\n")
            user_info = main_menu.main(user_info)
        continue
    else:
        clear_terminal()
        print('\nPlease enter valid input!\n')
        continue

    # option = input('Get Data From User: ')
    # if option == "1":
    #     payload = {'username': 'soroush', 'password': 'a_hashed_string'}  # Gathered Data
    #     route = 'login'  # Address of Views
    # elif option == "2":
    #     payload = {'username': 'soroush',
    #                'phone_number': '09390468833', 'password': 'a_hashed_string', 'birthday': '2024-01-16', 'email': 'sakdadshnadsi@asddjas.casd'}
    #     route = 'register'
    # elif option == "3":
    #     payload = {}
    #     route = 'show_profile'
    # else:
    #     continue
    #
    # js = {
    #     'payload': payload,
    #     'url': route
    # }
    # js = json.dumps(js)
    # print('Request Sent')
    # client.send(js.encode('utf-8'))
    #
    # response = client.recv(1024).decode('utf-8')
    # print(response)
