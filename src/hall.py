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

    def create(self, **kwargs):
        """
            Create New Row Of Hall info in Hall Table in Database

        """
        super().create('hall', kwargs.get(
            'columns', None), kwargs.get('values', None))

<<<<<<< HEAD

    def read(**kwargs):
=======
    def read(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Get An Existing Hall info From Hall Table in Database

        """
        super().read(kwargs.get('columns', None), 'hall', kwargs.get(
            'condition', None), kwargs.get('order', None))

<<<<<<< HEAD

    def update(**kwargs):
=======
    def update(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Update An Existing آHall info In Hall Table in Database
        """
        super().update('hall', kwargs.get(
            'columns', None), kwargs.get('condition', None))

<<<<<<< HEAD

    def delete(**kwargs):
=======
    def delete(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Delete An Existing Hall info From Hall Table in Database

        """
        super().delete('hall', kwargs.get('condition', None))
