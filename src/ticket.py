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

    @staticmethod
    def __str__(self):
        return f': Cinema Sans ID: {self.cinema_sans_id} | User ID: {self.user_id} | Sit Number: {self.sit_number}'

    @staticmethod
    def create(**kwargs):
        """
        Create New Row Of Ticket in ticket Table in Database
        """
        super().create('ticket', kwargs.get(
            'columns', None), kwargs.get('values', None))

    @staticmethod
    def read(**kwargs):
        """
        Get An Existing ticket From ticket Table in Database

        """
        super().read(kwargs.get('columns', None), 'ticket', kwargs.get(
            'condition', None), kwargs.get('order', None))

    @staticmethod
    def update(**kwargs):
        """
        Update An Existing ticket In ticket Table in Database

        """
        super().update('ticket', kwargs.get(
            'columns', None), kwargs.get('condition', None))

    @staticmethod
    def delete(**kwargs):
        """
        Delete An Existing ticket  From ticket Table in Database

        """
        super().delete('ticket', kwargs.get('condition', None))

