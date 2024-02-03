from src.db.db_operations import DBOperation
from datetime import datetime


class Cinema_sans(DBOperation):
    """
            Class To Make Cinema_sans Instances.
    """
    start_time: datetime.time
    end_time: datetime.time
    film_id: int
    hall_id: int
    price: int

    def __init__(self, start_time, end_time, film_id, hall_id, price):
        """
                Initialize Instance (Constructor Method)
        """
        self.start_time = start_time
        self.end_time = end_time
        self.film_id = film_id
        self.hall_id = hall_id
        self.price = price

    def __str__(self):
        return (f'Start Time:{self.start_time} | End Time:{self.end_time} |'
                f' Film ID:{self.film_id} | Hall ID:{self.hall_id} | Price:{self.price}')

    def create(self, **kwargs):
        """
            Create New Row Of Cinema sans in cinema_sans Table in Database

        """
        super().create('cinema_sans', kwargs.get(
            'columns', None), kwargs.get('values', None))

    def read(self, **kwargs):
        """
        Get An Existing cinema sans From cinema_sans Table in Database
        """
        super().read(kwargs.get('columns', None), 'cinema_sans', kwargs.get(
            'condition', None), kwargs.get('order', None))

    def update(self, **kwargs):
        """
        Update An Existing Cinema Sans In cinema_sans Table in Database

        """
        super().update('cinema_sans', kwargs.get(
            'columns', None), kwargs.get('condition', None))

    def delete(self, **kwargs):
        """
        Delete An Existing cinema sans From cinema_sans Table in Database

        """
        super().delete('cinema_sans', kwargs.get('condition', None))
