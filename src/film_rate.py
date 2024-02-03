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

        validate_rate = Validator.validate(rate, (Validator.rate_validator,))
        if isinstance(validate_rate, bool):
            self.rate = validate_rate
        else:
            raise Exception(validate_rate)

        self.user_id = user_id

    def __str__(self):
        return f'Film Id: {self.film_id} | Rate: {self.rate} | User Id: {self.user_id}'

<<<<<<< HEAD

    def create(**kwargs):
=======
    def create(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Create New Row Of Film Rate in Film Rate Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('film_rate', kwargs.get(
            'columns', None), kwargs.get('values', None))

<<<<<<< HEAD

    def read(**kwargs):
=======
    def read(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
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

<<<<<<< HEAD

    def update(**kwargs):
=======
    def update(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Update An Existing Film Rate In Film Rate Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('film_rate', kwargs.get(
            'columns', None), kwargs.get('condition', None))

<<<<<<< HEAD

    def delete(**kwargs):
=======
    def delete(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Delete An Existing Film Rate From Film Rate Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('film_rate', kwargs.get('condition', None))
