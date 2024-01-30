import mysql.connector as mysql_db


class DatabaseConnector:
    """
    A class responsible for connecting to the MySQL database.

    Attributes:
        host (str): The database host.
        user (str): The database user.
        password (str): The database password.
        database (str): The name of the database.

    Methods:
        __init__(self, host, user, password, database):
            Initializes the DatabaseConnector with the provided connection details.

    """

    def __init__(self, host, user, password, database):
        """
        Initializes the DatabaseConnector with the provided connection details.

        Parameters:
            host (str): The database host.
            user (str): The database user.
            password (str): The database password.
            database (str): The name of the database.
        """
        self.connection = mysql_db.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()


class DatabaseManager:
    """
    A class responsible for managing database operations.

    Attributes:
        db_connector (DatabaseConnector): An instance of DatabaseConnector for database connection.

    Methods:
        __init__(self, db_connector):
            Initializes the DatabaseManager with a DatabaseConnector instance.

    """

    def __init__(self, db_connector):
        """
        Initializes the DatabaseManager with a DatabaseConnector instance.

        Parameters:
            db_connector (DatabaseConnector): An instance of DatabaseConnector for database connection.
        """
        self.db_connector = db_connector

    def execute_commit_query(self, query):
        """
        Execute a SQL query on the connected database.

        Parameters:
            query (str): The SQL query to be executed.
        """
        try:
            self.db_connector.cursor.execute(query)
            self.db_connector.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def initialize_database(self):
        """
        Initialize the database by creating necessary tables.
        Call this method once during the application setup.
        """
        # Add code here to create other tables if needed

        # # Add User Table to Database
        # query = '''
        #     CREATE TABLE IF NOT EXISTS user (id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT NOT NULL,
        #     username VARCHAR(100) UNIQUE NOT NULL)
        # '''
        # self.execute_commit_query(query)


db_connector = DatabaseConnector(host='localhost', user='root', password='root', database='cinema_ticket')
db_manager = DatabaseManager(db_connector)
# db_connector.initialize_database()
