from datetime import date
from datetime import datetime

from src.db.db_operations import Manager


class User:
    """
        Class To Make User Instances, It's a Basic User Without Any Specification.
    """
    id: int
    username: str
    email: str
    phone_number: str
    password: str
    birthday: date
    last_login: None
    created_at: datetime
    balance: int
    role: int
    is_logged_in: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'user')

    def __init__(self, username, email, phone_number, password, birthday, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.birthday = birthday
        self.role = 1
        self.is_logged_in = 0
        self.balance = 0

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Username: {self.username} | Email: {self.email} | Role: {self.role}'

    def set_user_logged_in(self):
        self.is_logged_in = 1
        User.objects.update({'is_logged_in': '1'}, f'id={self.id}')

    def set_user_logged_out(self):
        self.is_logged_in = 0
        User.objects.update({'is_logged_in': '0'}, f'id={self.id}')


User.set_manager()
