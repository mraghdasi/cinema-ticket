from src.db.db_operations import DBOperation, Manager


class Ticket(DBOperation):
    """
            Class To Make Subscription Instances.
    """
    cinema_sans_id: int
    user_id: int
    sit_number: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'ticket')

    def __init__(self, cinema_sans_id, user_id, sit_number, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        self.cinema_sans_id = cinema_sans_id
        self.user_id = user_id
        self.sit_number = sit_number

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f': Cinema Sans ID: {self.cinema_sans_id} | User ID: {self.user_id} | Sit Number: {self.sit_number}'


Ticket.set_manager()
