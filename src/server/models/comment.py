from datetime import datetime

from src.db.db_operations import DBOperation, Manager


class Comment(DBOperation):
    description: str
    film_id: int
    user_id: int
    created_at: datetime
    reply_to: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'comment')

    def __init__(self, description, film_id, user_id, created_at, reply_to=None):
        """
        Initialize Instance (Constructor Method)
        """

        self.description = description
        self.film_id = film_id
        self.user_id = user_id
        self.created_at = created_at
        self.reply_to = reply_to

    def __str__(self):
        return f'User : {self.user_id} Description : {self.description} Film id : {self.film_id} Created at : {self.created_at}'


Comment.set_manager()
