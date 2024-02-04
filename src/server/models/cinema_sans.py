from datetime import datetime

from src.db.db_operations import DBOperation, Manager


class CinemaSans(DBOperation):
    """
            Class To Make Cinema_sans Instances.
    """
    start_time: datetime.time
    end_time: datetime.time
    film_id: int
    hall_id: int
    price: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'cinema_sans')

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


CinemaSans.set_manager()
