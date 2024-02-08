import os

import mysql.connector as mysql_db
from dotenv import load_dotenv

# Load the .env file
from src.utils.custom_exceptions import DBError

load_dotenv()


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
        self.cursor = self.connection.cursor(buffered=True)


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

    def execute_commit_query(self, query: str):
        """
        Execute a SQL query on the connected database.

        Parameters:
            query (str): The SQL query to be executed.
        """
        try:
            self.db_connector.cursor.execute(query)
            self.db_connector.connection.commit()
        except Exception as e:
            raise DBError()

    def execute_commit_query_with_value(self, query: str, values: tuple):
        """
        Execute a SQL query on the connected database.

        Params:
            query (str): The SQL query to be executed.
            value (tuple): The SQL values to be executed.

        """
        try:
            self.db_connector.cursor.execute(query, values)
            self.db_connector.connection.commit()
        except Exception as e:
            raise DBError()

    def initialize_database(self):
        """
        Initialize the database by creating necessary tables.
        Call this method once during the application setup.
        """

        # # Add User Table to Database
        query = '''
            CREATE TABLE IF NOT EXISTS  user(
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE ,
                phone_number VARCHAR(255) DEFAULT NULL ,
                password VARCHAR(255) NOT NULL ,
                birthday DATE NOT NULL,
                last_login DATETIME DEFAULT CURRENT_TIMESTAMP ,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                subscription_id INT DEFAULT 1,
                balance INT DEFAULT 0,
                role INT DEFAULT 1,
                is_logged_in INT DEFAULT 0
            );
        '''
        self.execute_commit_query(query)

        # Add Film Table to Database
        query = '''
                    CREATE TABLE IF NOT EXISTS film (
                        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                        title VARCHAR(255),
                        min_age INT
                    );
                '''
        self.execute_commit_query(query)

        # Add Hall Table to Database
        query = '''
                    CREATE TABLE IF NOT EXISTS hall (
                        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                        title VARCHAR(255),
                        capacity INT
                    );
                '''
        self.execute_commit_query(query)

        # Add User Bank Account Table to Database
        query = '''
            CREATE TABLE IF NOT EXISTS user_bank_account (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                card_number VARCHAR(255) NOT NULL,
                cvv2 VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                amount INT NOT NULL,
                minimum_amount INT NOT NULL,
                expire_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
        '''
        self.execute_commit_query(query)

        # Add Package Table to Database
        query = '''
        CREATE TABLE IF NOT EXISTS package (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                title VARCHAR(255),
                cash_back INTEGER DEFAULT 0,
                price INT
            );
        '''
        self.execute_commit_query(query)

        # Add Subscription Table to Database
        query = '''
            CREATE TABLE IF NOT EXISTS subscription (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                user_id INT,
                package_id INT,
                expire_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (package_id) REFERENCES package(id)
            );
         '''
        self.execute_commit_query(query)

        # Add Cinema Sans Table to Database
        query = '''
                    CREATE TABLE IF NOT EXISTS cinema_sans (
                        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                        premiere_date DATE,
                        start_time TIME,
                        end_time TIME,
                        film_id INT,
                        hall_id INT,
                        price INT,
                        FOREIGN KEY (film_id) REFERENCES film(id),
                        FOREIGN KEY (hall_id) REFERENCES hall(id)
                    );
                '''
        self.execute_commit_query(query)

        # Add Ticket Table to Database
        query = '''
            CREATE TABLE IF NOT EXISTS ticket (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                cinema_sans_id INT,
                user_id INT,
                sit_number INT,
                FOREIGN KEY (cinema_sans_id) REFERENCES cinema_sans(id),
                FOREIGN KEY (user_id) REFERENCES user(id)            
            );
        '''
        self.execute_commit_query(query)

        # Add Film Rate Table to Database
        query = '''
            CREATE TABLE IF NOT EXISTS film_rate (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                film_id INT,
                rate INT,
                user_id INT,
                FOREIGN KEY (film_id) REFERENCES film(id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
        '''
        self.execute_commit_query(query)

        # Add Comment Table to Database
        query = '''
            CREATE TABLE IF NOT EXISTS comment (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                description TEXT,
                film_id INT,
                user_id INT,
                reply_to INT NULL,
                created_at DATETIME,
                FOREIGN KEY (film_id) REFERENCES film(id),
                FOREIGN KEY (user_id) REFERENCES user(id),            
                FOREIGN KEY (reply_to) REFERENCES comment(id)            
            );
        '''
        self.execute_commit_query(query)


db_connector = DatabaseConnector(
    host=os.getenv('DB_HOST'), user=os.getenv('DB_USERNAME'), password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_SCHEMA_DATABASE'))
db_manager = DatabaseManager(db_connector)
db_manager.initialize_database()
