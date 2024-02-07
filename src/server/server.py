import json
import socket
import threading
from datetime import date
from datetime import datetime
from secrets import compare_digest

from dotenv import load_dotenv

from src.server.models.user import User
from src.server.views import login, register, show_profile
from src.utils.custom_exceptions import DBError

load_dotenv()


def login_required(func):
    def wrapper(request):
        if request.session.user:
            return func(request)
        else:
            def login_required_error():
                return {'msg': 'Login Required', 'status_code': 401}
            return login_required_error()
    return wrapper


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

    def __init__(self, data: str, session: object):
        self.session = session

        data = json.loads(data.decode('utf-8'))
        self.payload = data['payload']
        self.url = data['url']


class Response:
    """
    A Class To Handle Responses From Server Side to Client Side
    """
    payload: str

    def __init__(self, payload: str):
        self.payload = json.dumps(payload).encode('utf-8')


urls = {
    'login': login,
    'register': register,
    'show_profile': show_profile,
}

HOST = '127.0.0.1'
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f'[*] Server is listening on {HOST}:{PORT}')


def handle_client(client_socket):
    session = Session(client_socket)
    try:
        while True:
            command = session.connection.recv(1024)
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


while True:
    client_socket, addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
