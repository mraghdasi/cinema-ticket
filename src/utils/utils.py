import hashlib
import hmac

from main import secret_key

def hash_string(string):
    """
    Return A Hashed String From An Input String
    :param string:
    :return:
        Hashed String
    """
    return hmac.new(secret_key.encode('utf-8'), string.encode('utf-8'), hashlib.sha256).hexdigest()