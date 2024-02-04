from src.db.db_operations import Manager


class Package:
    """
        Class To Make Package Instances. 
    """
    id: int
    title: str
    cash_back: int
    price: int
    objects: object

    @classmethod
    def set_manager(cls):
        setattr(cls, 'objects', Manager(cls))
        setattr(cls, 'db_table_name', 'package')

    def __init__(self, title, cash_back, price, **kwargs):
        """
        Initialize Instance (Constructor Method)
        """
        self.title = title
        self.cash_back = cash_back
        self.price = price

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return f'Title : {self.title} | Cash Back: {self.cash_back} | Price: {self.price}'


Package.set_manager()
