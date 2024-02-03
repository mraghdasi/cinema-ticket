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
        query ='''
            CREATE TABLE IF NOT EXISTS  user(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE ,
                phone_number VARCHAR(255) DEFAULT NULL ,
                password VARCHAR(255) NOT NULL ,
                birthday DATE NOT NULL,
                last_login DATETIME DEFAULT NULL ,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                subscription_id INT DEFAULT NULL,                
                balance INT DEFAULT 0
            );
        '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS user_bank_account (
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                card_number VARCHAR(255) NOT NULL,
                cvv2 VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                amount INT NOT NULL,
                minimum_amount INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
        '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS transaction (
                user_bank_account_id INT NOT NULL,
                transaction_type INTEGER NOT NULL,
                amount INT NOT NULL ,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_bank_account_id) REFERENCES user_bank_account(user_id)
            );
         '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS package (
                id INT,
                title VARCHAR(255),
                cash_back INTEGER DEFAULT 0,
                price INT
            );
        '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS subscription (
                id INT,
                user_id INT,
                package_id INT,
                expire_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (package_id) REFERENCES package(id)
            );
         '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS ticket (
                id INT ,
                cinema_sans_id INT,
                user_id INT,
                sit_number INT,
                FOREIGN KEY (cinema_sans_id) REFERENCES cinema_sans(id),
                FOREIGN KEY (user_id) REFERENCES user(id)            
            );
        '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS cinema_sans (
                id INT,
                start_time TIME,
                end_time TIME,
                film_id INT,
                hall_id INT,
                price INT,
                FOREIGN KEY (film_id) REFERENCES films(id),
                FOREIGN KEY (hall_id) REFERENCES hall(id)
            );
        '''
        self.execute_commit_query(query)




        query ='''
            CREATE TABLE IF NOT EXISTS films (
                id INT,
                title VARCHAR(255),
                min_age INT
            );
        '''
        self.execute_commit_query(query)



        query ='''
            CREATE TABLE IF NOT EXISTS hall (
                id INT ,
                title VARCHAR(255),
                capacity INT
            );
        '''
        self.execute_commit_query(query)



        query = '''
            CREATE TABLE IF NOT EXISTS film_rate (
                id INT,
                film_id INT,
                rate INT,
                user_id INT,
                FOREIGN KEY (film_id) REFERENCES films(id),
                FOREIGN KEY (user_id) REFERENCES user(id)
            );
        '''
        self.execute_commit_query(query)



        query ='''
            CREATE TABLE IF NOT EXISTS comment (
                id INT,
                description TEXT,
                film_id INT,
                user_id INT,
                reply_to INT NULL,
                created_at DATETIME,
                FOREIGN KEY (film_id) REFERENCES films(id),
                FOREIGN KEY (user_id) REFERENCES user(id),            
                FOREIGN KEY (reply_to) REFERENCES comment(id)            
            );
        '''
        self.execute_commit_query(query)

            # CREATE TABLE IF NOT EXISTS package (
            #     id INT,
            #     user_id,
            #     title VARCHAR(255),
            #     cash_back INTEGER DEFAULT 0,
            #     price INT,
            #     FOREIGN KEY (user_id) REFERENCES user(id)
            # );
            # CREATE TABLE IF NOT EXISTS subscription (
            #     id INT,
            #     user_id INT,
            #     package_id INT,
            #     expire_at TIMESTAMP,
            #     FOREIGN KEY (user_id) REFERENCES user(id),
            #     FOREIGN KEY (package_id) REFERENCES package(id)
            # );


db_connector = DatabaseConnector(
    host='localhost', user='root', password='root', database='cinema_ticket')
db_manager = DatabaseManager(db_connector)
# db_connector.initialize_database()
