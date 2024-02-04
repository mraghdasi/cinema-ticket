import re

from src.db.db_main import db_connector
from src.db.db_main import db_manager
from src.utils.custom_exceptions import ReadFromDataBaseError


class DBOperation:

    @staticmethod
    def create(entity: object, *args):
        """
        Inserts a new record into the specified entity.
        """
        table_name = entity.__name__.lower()
        obj = entity(*args)
        columns = tuple(vars(obj).keys())
        values = tuple(vars(obj).values())
        query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(values))})'
        exe = db_manager.execute_commit_query_with_value(query, values)

        if exe:
            query = f"SELECT * FROM {table_name} WHERE {' AND '.join([f'{c}={repr(v)}' for c, v in zip(columns, values)])}"
            db_connector.cursor.execute(query)
            created_row = db_connector.cursor.fetchone()

            def convert_datetime_to_str(dt):
                if type(dt) == 'str':
                    if re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$', dt):
                        return dt.split()[0]
                return dt

            entity_db_data = dict(
                zip([desc[0] for desc in db_connector.cursor.description], map(convert_datetime_to_str, created_row)))
            entity_db_data = dict([(key, value) for key, value in entity_db_data.items() if key not in vars(obj)])
            for key, value in entity_db_data.items():
                setattr(obj, key, value)
            return obj
        else:
            raise ReadFromDataBaseError()

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

        table_name = entity.__name__.lower()

        query = f"SELECT * FROM {table_name}"

        if condition is not None:
            query += f' WHERE {condition}'

        if order is not None:
            query += f' ORDER BY {order[0]} {order[1]}'

        exe = db_manager.execute_commit_query(query)

        if exe:
            objs_data = [dict(zip([desc[0] for desc in db_connector.cursor.description], data)) for data in
                    db_connector.cursor.fetchall()]
            return [entity(**obj) for obj in objs_data]
        else:
            return exe

    @staticmethod
    def update(entity: object, columns_values: dict, condition: str = None):
        """
        Updates records in the specified entity based on the provided column-value pairs and condition.

        Args:
            entity (str): The name of the table/entity to update records in.
            columns_values (dict): A dictionary containing key-value pairs for the update.
            condition (str, optional): The condition to filter records (default is None).

        Returns:
            True if everything is done OK

            False if something goes wrong
        """
        table_name = entity.__name__.lower()

        query = f'UPDATE {table_name} SET '

        query += ', '.join([f"{column} = {columns_values[column]}" for column in columns_values])

        if condition is not None:
            query += f' WHERE {condition}'

        return db_manager.execute_commit_query(query)
    #
    # @staticmethod
    # def delete(entity: str, condition: str = None):
    #     """
    #     Deletes records from the specified entity based on the provided condition.
    #
    #     Args:
    #         entity (str): The name of the table/entity to delete records from.
    #         condition (str, optional): The condition to filter records (default is None).
    #
    #     Returns:
    #         True if everything is done OK
    #
    #         False if something goes wrong
    # """
    #
    #     query = f'DELETE FROM {entity}'
    #     if condition is not None:
    #         query += f' WHERE {condition}'
    #
    #     return db_manager.execute_commit_query(query)
    #
    # def __str__(self) -> str:
    #     """
    #         A class for managing database operations.
    #
    #         Methods:
    #             create(entity: str, columns: tuple, values: tuple)
    #                 Inserts a new record into the specified entity.
    #
    #             read(columns: tuple, table_name: str, condition: str = None, order: list = None)
    #                 Retrieves records from the specified table based on the provided columns, condition, and order.
    #
    #             update(entity: str, columns_values: dict, condition: str = None)
    #                 Updates records in the specified entity based on the provided column-value pairs and condition.
    #
    #             delete(entity: str, condition: str = None)
    #                 Deletes records from the specified entity based on the provided condition.
    #     """
    #     return f'A class for managing database operations.'
    #
