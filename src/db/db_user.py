from datetime import date, datetime

from db_main import db_manager
from src.utils.utils import username_validator, email_validator, phone_number_validator


class User:
    """
        Class To Make User Instances, It's a Basic User Without Any Specification.
    """
    USER_ID_COUNTER = 1
    user_id: int
    username: str
    email: str
    phone_number: str
    password: str
    birthday: date
    last_login: None
    created_at: datetime
    subscription_id: int
    wallet_id: int

    def __init__(self, username, email, phone_number, password, birthday, last_login, created_at, subscription_id,
                 wallet_id):
        """
        Initialize Instance (Constructor Method)
        :param username:
        :param email:
        :param phone_number:
        :param password:
        :param birthday:
        :param last_login:
        :param created_at:
        :param subscription_id:
        :param wallet_id:
        """
        self.user_id = self.return_user_id()
        self.username = username_validator(username)
        self.email = email_validator(email)
        self.phone_number = phone_number_validator(phone_number)
        self.password = password
        self.birthday = birthday
        self.last_login = last_login
        self.created_at = created_at
        self.subscription_id = subscription_id
        self.wallet_id = wallet_id

    def return_user_id(self):
        """
        Get Last Used Id
        :return:
            counter
        """
        counter = self.USER_ID_COUNTER
        self.USER_ID_COUNTER += 1
        return counter

    def save(self):
        """
        Insert User Instance to Database, Table User
        :return:
            True Or False
        """

        query = f'''
        INSERT INTO user (id, username, email, phone_number, password, birthday, last_login, created_at, subscription_id, wallet_id)
        VALUES ({self.user_id}, {self.username}, {self.email}, {self.phone_number}, {self.password}, {self.birthday}, {self.last_login}, {self.created_at}, {self.subscription_id}, {self.wallet_id});
        '''
        return db_manager.execute_query(query)

