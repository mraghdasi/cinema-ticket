import json
import socket
import threading

from dotenv import load_dotenv

from src.server.views import do_login, register, get_movies, add_ticket, check_seats, check_tickets, cancel_ticket, \
    buy_subscription, check_subscription, get_cards, register_cards, check_db_for_transfer, do_transfer, do_card_op

load_dotenv()


# Classes
class Session:
    """
    A Class To Connect Socket Connection and User (Authentication)
    """
    connection: object
    user: object

    def __init__(self, connection: object, user=None):
        self.connection = connection
        self.user = user


class Request:
    """
    A Class To Handle Requests From Client Side
    """
    data: str
    session: object

    def __init__(self, data: bytes, session: object):
        self.session = session

        data = json.loads(data.decode('utf-8'))
        self.payload = data['payload']
        self.url = data['url']


class Response:
    """
    A Class To Handle Responses From Server Side to Client Side
    """
    payload: bytes

    def __init__(self, payload: dict):
        self.payload = json.dumps(payload).encode('utf-8')


# Urls
urls = {
    'login': do_login,
    'register': register,
    'get_movies': get_movies,
    'add_ticket': add_ticket,
    'check_seats': check_seats,
    'check_tickets': check_tickets,
    'cancel_ticket': cancel_ticket,
    'buy_subscription': buy_subscription,
    'check_subscription': check_subscription,
    'register_cards': register_cards,
    'get_cards': get_cards,
    'check_db_for_transfer': check_db_for_transfer,
    'do_transfer': do_transfer,
    'do_card_op': do_card_op,
}

HOST = '127.0.0.1'
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f'[*] Server is listening on {HOST}:{PORT}')


# User Thread Handling
def handle_client(client_socket):
    session = Session(client_socket)
    try:
        while True:
            command = session.connection.recv(5 * 1024)
            if command:
                # Convert Received Data To Request Instance
                request = Request(command, session)

                # Send Request To View Function
                response = Response(urls[request.url](request))
                # Send Response To Client Connection
                session.connection.send(response.payload)
            else:
                raise ConnectionAbortedError()

    except ConnectionAbortedError:
        print('[!] Connection aborted by client.')
    except ConnectionResetError:
        print('[!] Connection reset by client.')
    finally:
        print('[!] Connection Closed.')
        client_socket.close()


# Add New Thread Per User
while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
