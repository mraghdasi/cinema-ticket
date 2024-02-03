from src.db.db_operations import DBOperation


class Ticket(DBOperation):
    """
            Class To Make Subscription Instances.
    """
    cinema_sans_id: int
    user_id: int
    sit_number: int

    def __init__(self, cinema_sans_id, user_id, sit_number):
        """
        Initialize Instance (Constructor Method)
        """
        self.cinema_sans_id = cinema_sans_id
        self.user_id = user_id
        self.sit_number = sit_number

<<<<<<< HEAD

    def __str__(self):
        return f': Cinema Sans ID: {self.cinema_sans_id} | User ID: {self.user_id} | Sit Number: {self.sit_number}'


    def create(**kwargs):
=======
    def __str__(self):
        return f': Cinema Sans ID: {self.cinema_sans_id} | User ID: {self.user_id} | Sit Number: {self.sit_number}'

    def create(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Create New Row Of Ticket in ticket Table in Database
        """
        super().create('ticket', kwargs.get(
            'columns', None), kwargs.get('values', None))

<<<<<<< HEAD

    def read(**kwargs):
=======
    def read(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Get An Existing ticket From ticket Table in Database

        """
        super().read(kwargs.get('columns', None), 'ticket', kwargs.get(
            'condition', None), kwargs.get('order', None))

<<<<<<< HEAD

    def update(**kwargs):
=======
    def update(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Update An Existing ticket In ticket Table in Database

        """
        super().update('ticket', kwargs.get(
            'columns', None), kwargs.get('condition', None))

<<<<<<< HEAD

    def delete(**kwargs):
=======
    def delete(self, **kwargs):
>>>>>>> 922f00e871ae084fcc4542cdec9f2e889dc9e009
        """
        Delete An Existing ticket  From ticket Table in Database

        """
        super().delete('ticket', kwargs.get('condition', None))
