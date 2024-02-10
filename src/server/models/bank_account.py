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
    objects: Manager

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'user_bank_account')

    def __init__(self, user_id, title, card_number, password, cvv2, expire_date, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        self.user_id = user_id
        self.title = title
        self.card_number = card_number
        self.password = password
        self.cvv2 = cvv2
        self.amount = 5000
        self.minimum_amount = 5000
        self.user_id = user_id
        self.expire_date = expire_date
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Bank Account Card Number: {self.card_number} | Amount: {self.amount} | Title: {self.title}'


UserBankAccount.set_manager()
