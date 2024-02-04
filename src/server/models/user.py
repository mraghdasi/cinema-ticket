from datetime import date
from datetime import datetime
from hmac import compare_digest

from src.db.db_operations import DBOperation
from src.utils.custom_exceptions import UserPasswordNotCorrect
from src.utils.custom_exceptions import NewPasswordsNotSame
from src.utils.utils import hash_string

from src.utils.custom_validators import Validator


class User(DBOperation):
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
    role: str
    is_logged_in: int

    def __init__(self, username, email, phone_number, password, birthday):
        """
        Initialize Instance (Constructor Method)
        """
        validate_username = Validator.validate(
            username, (Validator.username_validator,))
        if isinstance(validate_username, bool):
            self.username = username
        else:
            raise Exception(validate_username)

        validate_email = Validator.validate(
            email, (Validator.email_validator,))
        if isinstance(validate_email, bool):
            self.email = email
        else:
            raise Exception(validate_email)

        validate_phone_number = Validator.validate(
            phone_number, (Validator.phone_number_validator,))
        if isinstance(validate_phone_number, bool):
            self.phone_number = phone_number
        else:
            raise Exception(validate_phone_number)

        validate_password = Validator.validate(
            password, (Validator.password_validator,))
        if isinstance(validate_password, bool):
            self.password = hash_string(password)
        else:
            raise Exception(validate_password)

        validate_birthday = Validator.validate(
            birthday, (Validator.birthday_format_validator,))
        if isinstance(validate_birthday, bool):
            self.birthday = birthday
        else:
            raise Exception(validate_birthday)

        self.last_login = None
        self.created_at = None
        self.subscription_id = None
        self.wallet_id = None
        self.balance = None
        self.role = None
        self.is_logged_in = 0

    def __str__(self):
        return f'Username: {self.username} | Email: {self.email} | Role: {self.role}'

    def create(self, **kwargs):
        """
        Create New Row Of User in User Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('user', kwargs.get('columns', None), kwargs.get('values', None))

    def read(self, **kwargs):
        """
        Get An Existing User From User Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'user', kwargs.get(
            'condition', None), kwargs.get('order', None))

    def update(self, **kwargs):
        """
        Update An Existing User In User Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('user', kwargs.get('columns', None), kwargs.get('condition', None))

    def delete(self, **kwargs):
        """
        Delete An Existing User From User Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('user', kwargs.get('condition', None))

    def change_password(self, password, new_password, confirm_new_password):
        """
        Change Password Of User, If New Password And Confirm New Password Are The Same, and Password is correct
        Updates User Password to New Password
        :param password:
        :param new_password:
        :param confirm_new_password:
        :return:
            True Or Raise Exception
        """
        if compare_digest(new_password, confirm_new_password):
            hashed_password = hash_string(password)
            user = self.read(
                **{'columns': '*', 'condition': f'username = {self.username} AND password = {hashed_password}'})
            if user:
                validate_password = Validator.validate(
                    new_password, (Validator.password_validator,))
                if isinstance(validate_password, bool):
                    hashed_new_password = hash_string(new_password)
                    self.password = hashed_new_password
                    self.update(
                        **{'columns': f'password = {hashed_new_password}', 'condition': f'id = {user.id}'})
                    return True
                else:
                    raise Exception(validate_password)
            else:
                return str(UserPasswordNotCorrect())
        else:
            return str(NewPasswordsNotSame())

    def set_user_logged_in(self):
        self.is_logged_in = 1

    def set_user_logged_out(self):
        self.is_logged_in = 0
