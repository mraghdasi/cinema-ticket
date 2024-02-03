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
