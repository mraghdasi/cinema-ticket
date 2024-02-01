from datetime import datetime

from src.db.db_operations import DBOperation


class Package(DBOperation):
    """
        Class To Make Package Instances. 
    """
    title: str
    cash_bank: int
    price: int

    def __init__(self, title, price, cash_bank=0):
        """
        Initialize Instance (Constructor Method)
        """
        self.title = title
        self.cash_bank= cash_bank
        self.price = price

    def __str__(self):
        return f'Title: {self.title} | Cash Bank: {self.cash_bank} | Price: {self.price}'

    def create(**kwargs):
        """
        Create New Row Of Package in Package Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('Package', kwargs.get(
            'columns', None), kwargs.get('values', None))

    def read(**kwargs):
        """
        Get An Existing Package From Package Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'package', kwargs.get(
            'condition', None), kwargs.get('order', None))

    def update(**kwargs):
        """
        Update An Existing Package In Package Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('package', kwargs.get(
            'columns', None), kwargs.get('condition', None))

    def delete(**kwargs):
        """
        Delete An Existing Package From Package Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('package', kwargs.get('condition', None))
