import hashlib
import hmac
import os


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