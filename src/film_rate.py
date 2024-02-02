from src.db.db_operations import DBOperation
from src.utils.custom_validators import Validator


class FilmRate(DBOperation):
    """
        Class To Make Film Rate Instances. 
    """
    film_id: int
    rate: int
    user_id: int

    def __init__(self, film_id, rate, user_id):
        """
        Initialize Instance (Constructor Method)
        """
        self.film_id = film_id
        self.rate = rate
        self.user_id = user_id

        validate_min_age = Validator.validate(rate, (Validator.rate_validator,))
        if isinstance(validate_min_age, bool):
            self.min_age = validate_min_age
        else:
            raise Exception(validate_min_age)

    def __str__(self):
        return f'Film Id: {self.film_id} | Rate: {self.rate} | User Id: {self.user_id}'

    @staticmethod
    def create(**kwargs):
        """
        Create New Row Of Film Rate in Film Rate Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('film_rate', kwargs.get(
            'columns', None), kwargs.get('values', None))

    @staticmethod
    def read(**kwargs):
        """
        Get An Existing Film Rate From Film Rate Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'film_rate', kwargs.get(
            'condition', None), kwargs.get('order', None))

    @staticmethod
    def update(**kwargs):
        """
        Update An Existing Film Rate In Film Rate Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('film_rate', kwargs.get(
            'columns', None), kwargs.get('condition', None))

    @staticmethod
    def delete(**kwargs):
        """
        Delete An Existing Film Rate From Film Rate Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('film_rate', kwargs.get('condition', None))
