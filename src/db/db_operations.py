from src.db.db_main import db_manager
from src.db.db_main import db_connector


class DBOperation:

    @staticmethod
    def create(entity: str, columns: tuple, values: tuple):
        """
        Inserts a new record into the specified entity.

        Args:
            entity (str): The name of the table/entity to insert into.
            columns (tuple): A tuple containing the column names to insert data into.
            values (tuple): A tuple containing the corresponding values to be inserted.

        Returns:
            The row that was inserted
        """

        query = f'INSERT INTO {entity} {columns} VALUES {values}'
        exe = db_manager.execute_commit_query(query)

        if exe:
            db_connector.cursor.execute(
                f"SELECT * FROM {entity} WHERE id = {db_connector.cursor.lastrowid}")
            created_row = db_connector.cursor.fetchone()

            return dict(zip(columns, created_row))
        else:
            return exe

    @staticmethod
    def read(columns: tuple, table_name: str, condition: str = None, order: list = None):
        """
        Retrieves records from the specified table based on the provided columns, condition, and order.

        Args:
            columns (tuple): A tuple containing the column names to retrieve.
            table_name (str): The name of the table to retrieve records from.
            condition (str, optional): The condition to filter records (default is None).
            order (list, optional): A list specifying the order of results [column to order by, sorting (ASC or DESC)] (default is None).

        Returns:
            The row(s) that was suppused to be read
        """

        query = f'SELECT {columns} FROM {table_name}'

        if condition is not None:
            query += f' WHERE {condition}'

        if order is not None:
            query += f' ORDER BY {order[0]} {order[1]}'

        exe = db_manager.execute_commit_query(query)

        if exe:
            return db_connector.cursor.fetchall()
        else:
            return exe

    @staticmethod
    def update(entity: str, columns_values: dict, condition: str = None):
        """
        Updates records in the specified entity based on the provided column-value pairs and condition.

        Args:
            entity (str): The name of the table/entity to update records in.
            columns_values (dict): A dictionary containing column-value pairs for the update.
            condition (str, optional): The condition to filter records (default is None).

        Returns:
            True if everything is done OK

            False if something goes wrong
        """

        query = f'UPDATE {entity} SET '

        # query += ', '.join([f"{column} = {columns_values[column]
        # }" for column in columns_values])

        if condition is not None:
            query += f' WHERE {condition}'

        return db_manager.execute_commit_query(query)


@staticmethod
def delete(entity: str, condition: str = None):
    """
    Deletes records from the specified entity based on the provided condition.

    Args:
        entity (str): The name of the table/entity to delete records from.
        condition (str, optional): The condition to filter records (default is None).

    Returns:
        True if everything is done OK

        False if something goes wrong
    """

    query = f'DELETE FROM {entity}'
    if condition is not None:
        query += f' WHERE {condition}'

    return db_manager.execute_commit_query(query)


def __str__(self) -> str:
    details = """
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
    return details