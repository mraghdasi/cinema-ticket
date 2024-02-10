from datetime import datetime

from src.db.db_operations import Manager


class Comment:
    description: str
    film_id: int
    user_id: int
    reply_to: int
    objects: Manager

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'comment')

    def __init__(self, description, film_id, user_id, reply_to=None, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """

        self.description = description
        self.film_id = film_id
        self.user_id = user_id
        self.reply_to = reply_to

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'User : {self.user_id} Description : {self.description} Film id : {self.film_id}'


Comment.set_manager()
