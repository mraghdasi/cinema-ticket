from datetime import date
from datetime import datetime
from hmac import compare_digest

from src.db.db_operations import DBOperation
from src.utils.custom_exceptions import UserPasswordNotCorrect
from src.utils.custom_exceptions import NewPasswordsNotSame
from src.utils.utils import hash_string

from src.utils.custom_validators import Validator


class UserBankAccount(DBOperation):
    """
        Class To Make UserBankAccount Instances.
    """
    user_id: int
    title: str
    card_number: str
    password: str
    cvv2: str
    amount: int
    minimum_amount: int
    expire_date: date

    def __init__(self, user_id, title, card_number, password, cvv2, amount, minimum_amount):
        """
        Initialize Instance (Constructor Method)
        """
        validate_card_number = Validator.len_validator(card_number, 16)
        if isinstance(validate_card_number, bool):
            self.card_number = card_number
        else:
            raise Exception(validate_card_number)

        validate_cvv2 = Validator.len_validator(cvv2, 16)
        if isinstance(validate_cvv2, bool):
            self.cvv2 = cvv2
        else:
            raise Exception(validate_cvv2)

        validate_amount = Validator.value_validator(amount, 1000)
        if isinstance(validate_amount, bool):
            self.amount = amount
        else:
            raise Exception(validate_amount)

        validate_minimum_amount = Validator.value_validator(minimum_amount, 1000)
        if isinstance(validate_minimum_amount, bool):
            self.minimum_amount = minimum_amount
        else:
            raise Exception(validate_minimum_amount)

        self.user_id = user_id
        self.title = title
        self.password = hash_string(password)

    def __str__(self):
        return f'Bank Account Card Number: {self.card_number} | Amount: {self.amount} | Title: {self.title}'

    def create(**kwargs):
        """
        Create New Row Of User in UserBankAccount Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('user_bank_account', kwargs.get('columns', None), kwargs.get('values', None))

    def read(**kwargs):
        """
        Get An Existing User From UserBankAccount Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'user_bank_account', kwargs.get(
            'condition', None), kwargs.get('order', None))

    def update(**kwargs):
        """
        Update An Existing User In UserBankAccount Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('user_bank_account', kwargs.get('columns', None), kwargs.get('condition', None))

    def delete(**kwargs):
        """
        Delete An Existing User From UserBankAccount Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('user_bank_account', kwargs.get('condition', None))