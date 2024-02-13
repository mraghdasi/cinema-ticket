import hashlib
import hmac
import json
import os

from dotenv import load_dotenv

load_dotenv()


def hash_string(string):
    """
    Return A Hashed String From An Input String
    :param string:
    :return:
        Hashed String
    """

    return hmac.new(os.getenv('SECRET_KEY').encode('utf-8'), string.encode('utf-8'), hashlib.sha256).hexdigest()


def input_client(msg):
    return input(msg).strip()


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_user_info(client):
    request_data = json.dumps({
        'payload': {},
        'url': 'show_profile'
    })
    client.send(request_data.encode('utf-8'))
    response = client.recv(5 * 1024).decode('utf-8')
    response = json.loads(response)

    if response['status_code'] == 200:
        return response['user']
    return None
