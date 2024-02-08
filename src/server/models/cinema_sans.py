from datetime import datetime
from datetime import date

from src.db.db_operations import Manager


class CinemaSans:
    """
            Class To Make Cinema_sans Instances.
    """
    premiere_date: date
    start_time: datetime.time
    end_time: datetime.time
    film_id: int
    hall_id: int
    price: int
    objects: Manager

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'cinema_sans')

    def __init__(self, premiere_date, start_time, end_time, film_id, hall_id, price, **kwargs):
        """
                Initialize Instance (Constructor Method)
        """
        self.premiere_date = premiere_date
        self.start_time = start_time
        self.end_time = end_time
        self.film_id = film_id
        self.hall_id = hall_id
        self.price = price

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return (f'Start Time:{self.start_time} | End Time:{self.end_time} |'
                f' Film ID:{self.film_id} | Hall ID:{self.hall_id} | Price:{self.price}')


CinemaSans.set_manager()
