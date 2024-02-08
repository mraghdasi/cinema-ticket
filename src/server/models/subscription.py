from datetime import datetime

from src.db.db_operations import Manager


class Subscription:
    """
        Class To Make Subscription Instances. 
    """
    user_id: int
    package_id: int
    expire_at: datetime
    objects: Manager

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'subscription')

    def __init__(self, user_id, package_id, expire_at, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        self.user_id = user_id
        self.package_id = package_id
        self.expire_at = expire_at

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'User Id: {self.user_id} | Package Id: {self.package_id} | Expire At: {self.expire_at}'


Subscription.set_manager()
