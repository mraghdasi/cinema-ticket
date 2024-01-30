from datetime import date, datetime

from src.db.db_main import db_manager
from src.utils.utils import Validator


class User:
    """
        Class To Make User Instances, It's a Basic User Without Any Specification.
    """
    username: str
    email: str
    phone_number: str
    password: str
    birthday: date
    last_login: None
    created_at: datetime
    subscription_id: int
    balance: int

    def __init__(self, username, email, phone_number, password, birthday, last_login, created_at, subscription_id,
                 balance):
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
        :param balance:
        """
        # Validators for Username
        username_validators = [validate(username) for validate in [Validator.username_validator]]
        # self.username = username_validator(username)
        # self.email = email_validator(email)
        # self.phone_number = phone_number_validator(phone_number)
        self.password = password
        self.birthday = birthday
        self.last_login = last_login
        self.created_at = created_at
        self.subscription_id = subscription_id
        self.balance = balance

    def save(self):
        """
        Insert User Instance to Database, Table User
        :return:
            True Or False
        """

        query = f'''
        INSERT INTO user (username, email, phone_number, password, birthday, last_login, created_at, subscription_id, wallet_id)
        VALUES ({self.username}, {self.email}, {self.phone_number}, {self.password}, {self.birthday}, {self.last_login}, {self.created_at}, {self.subscription_id}, {self.wallet_id});
        '''
        return db_manager.execute_commit_query(query)

    def read(self):
        query = '''
        '''

