from src.db.db_operations import DBOperation
from src.utils.custom_validators import Validator


class Film(DBOperation):
    """
        Class To Make Film Instances. 
    """
    title: str
    min_age: int

    def __init__(self, title, min_age):
        """
        Initialize Instance (Constructor Method)
        """
        self.title = title

        validate_min_age = Validator.validate(
            min_age, (Validator.min_age_validator,))
        if isinstance(validate_min_age, bool):
            self.min_age = validate_min_age
        else:
            raise Exception(validate_min_age)

    def __str__(self):
        return f'Title : {self.title} | Min Age: {self.min_age}'

<<<<<<< HEAD

    def create(**kwargs):
=======
    def create(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Create New Row Of Film in Film Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            values: string of columns values, comma separated (val1, val2, val3)
        :return:
        """
        super().create('film', kwargs.get(
            'columns', None), kwargs.get('values', None))

<<<<<<< HEAD

    def read(**kwargs):
=======
    def read(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Get An Existing Film From Film Table in Database
        :param kwargs:
            columns: string of columns names, comma separated (col1, col2, col3)
            condition: string of conditions (col1 = 'val1'), Default Value None
            order: tuple of two value (col_name, ASC|DESC) (col1, ASC), Default Value None
        :return:
        """
        super().read(kwargs.get('columns', None), 'film', kwargs.get(
            'condition', None), kwargs.get('order', None))

<<<<<<< HEAD

    def update(**kwargs):
=======
    def update(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Update An Existing Film In Film Table in Database
        :param kwargs:
            columns: string of columns names and values, comma separated "col1 = val1, col2 = val2, col3 = val3"
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().update('film', kwargs.get(
            'columns', None), kwargs.get('condition', None))

<<<<<<< HEAD

    def delete(**kwargs):
=======
    def delete(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Delete An Existing Film From Film Table in Database
        :param kwargs:
            condition: string of conditions (col1 = 'val1'), Default Value None
        :return:
        """
        super().delete('film', kwargs.get('condition', None))
