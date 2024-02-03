from datetime import datetime

from src.db.db_operations import DBOperation


class Subscription(DBOperation):
    """
        Class To Make Subscription Instances. 
    """
    user_id: int
    package_id: int
    expire_at: datetime

    def __init__(self, user_id, package_id, expire_at):
        """
        Initialize Instance (Constructor Method)
        """
        self.user_id = user_id
        self.package_id = package_id
        self.expire_at = expire_at

    def __str__(self):
        return f'User Id: {self.user_id} | Package Id: {self.package_id} | Expire At: {self.expire_at}'

    def create(self, **kwargs):
        """
        Create New Row Of Subscription in Subscription Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('subscription', kwargs.get(
            'columns', None), kwargs.get('values', None))

    def read(self, **kwargs):
        """
        Get An Existing Subscription From Subscription Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'subscription', kwargs.get(
            'condition', None), kwargs.get('order', None))

    def update(self, **kwargs):
        """
        Update An Existing Subscription In Subscription Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('subscription', kwargs.get(
            'columns', None), kwargs.get('condition', None))

    def delete(self, **kwargs):
        """
        Delete An Existing Subscription From Subscription Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('subscription', kwargs.get('condition', None))
