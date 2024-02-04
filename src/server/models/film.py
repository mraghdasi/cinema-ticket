from src.db.db_operations import Manager


class Film:
    """
        Class To Make Film Instances. 
    """
    title: str
    min_age: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'film')

    def __init__(self, title, min_age, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """

        # validate_min_age = Validator.validate(
        #     min_age, (Validator.min_age_validator,))
        # if isinstance(validate_min_age, bool):
        #     self.min_age = validate_min_age
        # else:
        #     raise Exception(validate_min_age)

        self.title = title
        self.min_age = min_age

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Title : {self.title} | Min Age: {self.min_age}'


Film.set_manager()
