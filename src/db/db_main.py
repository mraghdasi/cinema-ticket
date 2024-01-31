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
        '''
            CREATE TABLE IF NOT EXISTS  user(
                id INT NOT NULL PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE CHECK(username REGEXP '^[A-Za-z0-9]+$'),
                email VARCHAR(100) NOT NULL UNIQUE CHECK (email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
                phone_number VARCHAR(20) DEFAULT NULL CHECK (phone_number REGEXP '^\\+?[0-9]+$'),
                password VARCHAR(100) NOT NULL CHECK (password REGEXP '^[A-Za-z0-9]+$'),
                birthday DATE NOT NULL,
                last_login DEFAULT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                subscription_id INT DEFAULT NULL,
                wallet_id INT DEFAULT NULL,
                balance INT DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS user_bank_account (
                user_id INTEGER NOT NULL,
                title VARCHAR(100) NOT NULL,
                card_number VARCHAR(20) NOT NULL,
                cvv2 VARCHAR(4) NOT NULL,
                password VARCHAR(100) NOT NULL,
                amount BIGINT,
                minimum_amount BIGINT,
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
            CREATE TABLE IF NOT EXISTS transaction (
                user_bank_account_id INTEGER NOT NULL,
                transaction_type INTEGER NOT NULL,
                amount BIGINT ,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_bank_account_id) REFERENCES user_bank_account(user_id)
            );
            CREATE TABLE IF NOT EXISTS package (
                id INTEGER,
                title VARCHAR(255),
                cash_back INTEGER DEFAULT 0,
                price INTEGER
            );
            CREATE TABLE IF NOT EXISTS subscription (
                id INTEGER,
                user_id INTEGER,
                package_id INTEGER,
                expire_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (package_id) REFERENCES package(id)
            );
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER,
                title VARCHAR(255),
                min_age INTEGER
            );
            CREATE TABLE IF NOT EXISTS hall (
                id INTEGER ,
                title VARCHAR(255),
                capacity INTEGER
            );
            CREATE TABLE IF NOT EXISTS cinema_sans (
                id INTEGER,
                start_time TIME,
                end_time TIME,
                film_id INTEGER,
                hall_id INTEGER,
                price INTEGER,
                FOREIGN KEY (film_id) REFERENCES films(id),
                FOREIGN KEY (hall_id) REFERENCES hall(id)
            );
            CREATE TABLE IF NOT EXISTS ticket (
                id INTEGER ,
                cinema_sans_id INTEGER,
                user_id INTEGER,
                sit_number INTEGER,
                FOREIGN KEY (cinema_sans_id) REFERENCES cinema_sans(id),
                FOREIGN KEY (user_id) REFERENCES user(id)            
            );
            CREATE TABLE IF NOT EXISTS film_rate (
                id INTEGER,
                film_id INTEGER,
                rate INTEGER,
                user_id INTEGER,
                FOREIGN KEY (film_id) REFERENCES films(id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
            CREATE TABLE IF NOT EXISTS comment (
                id INTEGER,
                description TEXT,
                film_id INTEGER,
                user_id INTEGER,
                reply_to INTEGER NULL,
                created_at DATETIME,
                FOREIGN KEY (film_id) REFERENCES films(id),
                FOREIGN KEY (user_id) REFERENCES user(id)            
            
            );
        '''





db_connector = DatabaseConnector(host='localhost', user='root', password='root', database='cinema_ticket')
db_manager = DatabaseManager(db_connector)
# db_connector.initialize_database()
