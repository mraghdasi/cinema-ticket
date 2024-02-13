import json
import socket

import sys

import main_menu
from auth import login, register
from src.utils.utils import clear_terminal
from prettytable import PrettyTable

HOST = '127.0.0.1'
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    table = PrettyTable(["Hi Welcome to Our App!"])
    table.align["Hi Welcome to Our App!"] = "l"
    table.add_rows([['1.Login'], ['2.Register'], ['3.Quit']])
    print(table)

    user_input = input('Please Choose One Option:').lower().strip()

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
                print(f"\nWelcome {response['user']['username']} :)\n")
                main_menu.main(client)
            else:
                print(response['msg'])
                break
    elif user_input == '2' or user_input == 'Register':
        clear_terminal()
        while True:
            request_data = register.main()
            client.send(request_data.encode('utf-8'))
            response = json.loads(client.recv(5 * 1024).decode('utf-8'))

            if response['status_code'] == 200:
                print(f"\nWelcome to our app {response['user']['username']} :)\n")
                main_menu.main(client)
            elif response['status_code'] == 400:
                print("One or more of your unique fields exists in our database")
                break
            else:
                print(response['msg'])
                break
    else:
        clear_terminal()
        print('\nPlease enter valid input!\n')
