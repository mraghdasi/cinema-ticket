from src.db.db_operations import DBOperation


class Hall(DBOperation):
    """
            Class To Make Hall Instances.
    """
    title: str
    capacity: int

    def __init__(self, title, capacity):
        """
                Initialize Instance (Constructor Method)
        """
        self.title = title
        self.capacity = capacity

    def __str__(self):
        return f'Title:{self.title} | Capacity:{self.capacity}'

    def create(**kwargs):
        """
            Create New Row Of Hall info in Hall Table in Database

        """
        super().create('hall', kwargs.get(
            'columns', None), kwargs.get('values', None))

    def read(**kwargs):
        """
        Get An Existing Hall info From Hall Table in Database

        """
        super().read(kwargs.get('columns', None), 'hall', kwargs.get(
            'condition', None), kwargs.get('order', None))

    def update(**kwargs):
        """
        Update An Existing آHall info In Hall Table in Database
        """
        super().update('subscription', kwargs.get(
            'columns', None), kwargs.get('condition', None))

    def delete(**kwargs):
        """
        Delete An Existing Hall info From Hall Table in Database

        """
        super().delete('hall', kwargs.get('condition', None))
