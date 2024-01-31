from src.db.db_main import db_manager


class DBOperation:

    # @staticmethod
    # def create(query):
    #     db_manager.execute_commit_query(query)
    #
    # @staticmethod
    # def read(query):
    #     db_manager.execute_commit_query(query)
    #
    # @staticmethod
    # def update(query):
    #     db_manager.execute_commit_query(query)
    #
    # @staticmethod
    # def delete(query):
    #     db_manager.execute_commit_query(query)

    @staticmethod
    def create(entity: str, columns: tuple, values: tuple):
        query = f'INSERT INTO {entity} {columns} VALUES {values}'
        db_manager.execute_commit_query(query)

    @staticmethod
    def read(columns: tuple, table_name: str, condition: str = None, order: list = None):
        query = f'SELECT {columns} FROM {table_name}'

        if condition is not None:
            query += f' WHERE {condition}'

        if order is not None:
            query += f' ORDER BY {order[0]} {order[1]}'

        db_manager.execute_commit_query(query)

    @staticmethod
    def update(mode: str, entity: str, column: str, condition: str = None, alter_mode: str = None):
        if mode == 'ALTER':
            query = f'ALTER TABLE {entity} {alter_mode} COLUMN {column} {condition}'
        else:
            query = f'UPDATE {entity} SET {column}'
            if condition is not None:
                query += f' WHERE {condition}'
        db_manager.execute_commit_query(query)

    @staticmethod
    def delete(mode: str, entity: str, condition: str = None):
        if mode == 'DELETE':
            query = f'DELETE FROM {entity}'
            if condition is not None:
                query += f' WHERE {condition}'
        elif mode == 'DROP':
            query = f'DROP TABLE {entity}'
        else:
            query = f'TRUNCATE TABLE {entity}'

        db_manager.execute_commit_query(query)
