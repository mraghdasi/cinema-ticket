from src.db.db_main import db_connector
from src.db.db_main import db_manager


class Manager:
    """
        A Class To Manage DB Operations For Specific Class
    """

    def __init__(self, entity: object):
        self.entity = entity

    def create(self, *args, **kwargs):
        return DBOperation.create(self.entity, *args, **kwargs)

    def read(self, *args):
        return DBOperation.read(self.entity, *args)

    def update(self, *args):
        return DBOperation.update(self.entity, *args)

    def delete(self, *args):
        return DBOperation.delete(self.entity, *args)

    def query(self, *args, **kwargs):
        return DBOperation.query(self.entity, *args, **kwargs)


class DBOperation:

    @staticmethod
    def create(entity: object, *args, **kwargs):
        """
        Inserts a new record into the specified entity.
        """
        table_name = entity.db_table_name
        obj = entity(*args, **kwargs)
        columns = tuple(vars(obj).keys())
        values = tuple(vars(obj).values())
        query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(values))})'
        db_manager.execute_commit_query_with_value(query, values)

        return DBOperation.read(entity, ' AND '.join([f'{c}={repr(v)}' for c, v in zip(columns, values) if v]))[0]

    @staticmethod
    def read(entity: object, condition: str = None, order: list = None):
        """
        Retrieves records from the specified table based on the provided columns, condition, and order.

        Args:
            entity (object): A Class to Find Which Table We Are Going To Read From
            condition (str, optional): The condition to filter records (default is None).
            order (list, optional): A list specifying the order of results [column to order by, sorting (ASC or DESC)] (default is None).

        Returns:
            The Instance of Entity Based On row(s) that was supposed to be read
        """

        table_name = entity.db_table_name

        query = f"SELECT * FROM {table_name}"

        if condition is not None:
            query += f' WHERE {condition}'

        if order is not None:
            query += f' ORDER BY {order[0]} {order[1]}'

        db_manager.execute_commit_query(query)

        objs_data = [dict(zip([desc[0] for desc in db_connector.cursor.description], data)) for data in
                     db_connector.cursor.fetchall()]
        return [entity(**obj) for obj in objs_data]

    @staticmethod
    def update(entity: object, columns_values: dict, condition: str = None):
        """
        Updates records in the specified entity based on the provided column-value pairs and condition.

        Args:
            entity (object): The name of the table/entity to update records in.
            columns_values (dict): A dictionary containing key-value pairs for the update.
            condition (str, optional): The condition to filter records (default is None).

        Returns:
            True if everything is done OK

            False if something goes wrong
        """
        table_name = entity.db_table_name
        sub_query = ', '.join([f'{column} = "{columns_values[column]}"' for column in columns_values])
        query = f"UPDATE {table_name} SET {sub_query}"
        if condition is not None:
            query += f' WHERE {condition}'
        db_manager.execute_commit_query(query)
        return DBOperation.read(entity, condition)

    @staticmethod
    def delete(entity: object, condition: str = None):
        """
        Deletes records from the specified entity based on the provided condition.

        Args:
            entity (object): The name of the table/entity to delete records from.
            condition (str, optional): The condition to filter records (default is None).

        Returns:
            True if everything is done OK

            False if something goes wrong
    """
        table_name = entity.db_table_name
        query = f'DELETE FROM {table_name}'
        if condition is not None:
            query += f' WHERE {condition}'
        db_manager.execute_commit_query(query)

    @staticmethod
    def query(entity: object, queries: str, fetch=False):
        """
        :param entity: (object) The name of the table/entity to Run Query on It.
        :param fetch: (bool) Return Data
        :param queries: (str)String Of Custom Query
        :return:
            True Or False
        """
        db_manager.execute_commit_query(queries)
        if fetch:
            objs_data = [dict(zip([desc[0] for desc in db_connector.cursor.description], data)) for data in
                         db_connector.cursor.fetchall()]
            return [entity(**obj) for obj in objs_data]
        else:
            return True

    def __str__(self) -> str:
        """
            A class for managing database operations.

            Methods:
                create(entity: str, columns: tuple, values: tuple)
                    Inserts a new record into the specified entity.

                read(columns: tuple, table_name: str, condition: str = None, order: list = None)
                    Retrieves records from the specified table based on the provided columns, condition, and order.

                update(entity: str, columns_values: dict, condition: str = None)
                    Updates records in the specified entity based on the provided column-value pairs and condition.

                delete(entity: str, condition: str = None)
                    Deletes records from the specified entity based on the provided condition.
        """
        return f'A class for managing database operations.'
