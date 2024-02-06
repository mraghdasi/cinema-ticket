import socket
import threading

from dotenv import load_dotenv

load_dotenv()

HOST = '127.0.0.1'
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f'[*] Server is listening on {HOST}:{PORT}')


def handle_client(client_socket):
    try:
        client_socket.send(b'1.Login\n2.Register\n3.Quit\n')
        request = client_socket.recv(1024).decode('utf-8')
        print(f'[*] Received request: {request}')
        while request != 'quit':
            client_socket.send(b'ACK')
            request = client_socket.recv(1024).decode('utf-8')
            print(f'[*] Received request: {request}')
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
