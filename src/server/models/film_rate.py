from src.db.db_operations import DBOperation, Manager
from src.utils.custom_validators import Validator


class FilmRate(DBOperation):
    """
        Class To Make Film Rate Instances. 
    """
    film_id: int
    rate: int
    user_id: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'film_rate')

    def __init__(self, film_id, rate, user_id):
        """
        Initialize Instance (Constructor Method)
        """
        self.film_id = film_id

        validate_rate = Validator.validate(rate, (Validator.rate_validator,))
        if isinstance(validate_rate, bool):
            self.rate = validate_rate
        else:
            raise Exception(validate_rate)

        self.user_id = user_id

    def __str__(self):
        return f'Film Id: {self.film_id} | Rate: {self.rate} | User Id: {self.user_id}'


FilmRate.set_manager()
