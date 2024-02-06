from datetime import date

from src.db.db_operations import Manager


class UserBankAccount:
    """
        Class To Make UserBankAccount Instances.
    """
    title: str
    card_number: str
    password: str
    cvv2: str
    amount: int
    minimum_amount: int
    expire_date: date
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'user_bank_account')

    def __init__(self, user_id, title, card_number, password, cvv2, amount, minimum_amount, expire_date, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        # validate_card_number = Validator.len_validator(card_number, 16)
        # if isinstance(validate_card_number, bool):
        #     self.card_number = card_number
        # else:
        #     raise Exception(validate_card_number)
        #
        # validate_cvv2 = Validator.len_validator(cvv2, 16)
        # if isinstance(validate_cvv2, bool):
        #     self.cvv2 = cvv2
        # else:
        #     raise Exception(validate_cvv2)
        #
        # validate_amount = Validator.value_validator(amount, 1000)
        # if isinstance(validate_amount, bool):
        #     self.amount = amount
        # else:
        #     raise Exception(validate_amount)
        #
        # validate_minimum_amount = Validator.value_validator(minimum_amount, 1000)
        # if isinstance(validate_minimum_amount, bool):
        #     self.minimum_amount = minimum_amount
        # else:
        #     raise Exception(validate_minimum_amount)

        self.title = title
        self.card_number = card_number
        self.password = password
        self.cvv2 = cvv2
        self.amount = amount
        self.minimum_amount = minimum_amount
        self.user_id = user_id
        self.expire_date = expire_date
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Bank Account Card Number: {self.card_number} | Amount: {self.amount} | Title: {self.title}'


UserBankAccount.set_manager()
