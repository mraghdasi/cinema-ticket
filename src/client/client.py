import json
import socket

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
            response = json.loads(client.recv(5 * 1024).decode('utf-8'))
            if response['status_code'] == 200:
                print(f"\nWelcome <{response['user']['username']}> :)\n")
                main_menu.main(client)
            else:
                print(response['msg'])

    elif user_input == '2' or user_input == 'Register':
        clear_terminal()
        while True:
            request_data = register.main()
            client.send(request_data.encode('utf-8'))
            response = json.loads(client.recv(5 * 1024).decode('utf-8'))

            if response['status_code'] == 200:
                print(f"\nWelcome to our app <{response['user']['username']}> :)\n")
                main_menu.main(client)
            else:
                print(response['msg'])
    else:
        clear_terminal()
        print('\nPlease enter valid input!\n')

