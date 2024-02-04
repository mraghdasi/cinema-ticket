from src.db.db_operations import Manager


class Hall:
    """
            Class To Make Hall Instances.
    """
    title: str
    capacity: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'hall')

    def __init__(self, title, capacity, **kwargs):
        """
                Initialize Instance (Constructor Method)
        """
        self.title = title
        self.capacity = capacity

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Title:{self.title} | Capacity:{self.capacity}'


Hall.set_manager()
