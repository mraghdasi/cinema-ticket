from src.db.db_operations import DBOperation


class Hall:
    """
            Class To Make Hall Instances.
    """
    title: str
    capacity: int

    def __init__(self, title, capacity, **kwargs):
        """
                Initialize Instance (Constructor Method)
        """
        self.title = title
        self.capacity = capacity

    def __str__(self):
        return f'Title:{self.title} | Capacity:{self.capacity}'
