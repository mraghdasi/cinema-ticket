from src.db.db_operations import DBOperation
from datetime import datetime


class Comment(DBOperation):

    description: str
    film_id: int
    user_id: int
    created_at: datetime
    reply_to: int

    def __init__(self, description, film_id, user_id, created_at, reply_to=None):
        """
        Initialize Instance (Constructor Method)
        """
        
        self.description = description
        self.film_id = film_id
        self.user_id = user_id
        self.created_at = created_at
        self.reply_to = reply_to
        
    
    def create(**kwargs):
        """
        Create New Row Of Comment in Comment Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('comment', kwargs.get('columns', None), kwargs.get('values', None))
        
    def read(**kwargs):
        """
        Get An Existing Comment From Comment Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'comment', kwargs.get(
            'condition', None), kwargs.get('order', None))
        
    def update(**kwargs):
        """
        Update An Existing Comment In Comment Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('comment', kwargs.get('columns', None), kwargs.get('condition', None))
        
    def delete(**kwargs):
        """
        Delete An Existing Comment From Comment Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('comment', kwargs.get('condition', None))

    def __str__(self):
        return f'User : {self.user_id} Description : {self.description} Film id : {self.film_id} Created at : {self.created_at}'