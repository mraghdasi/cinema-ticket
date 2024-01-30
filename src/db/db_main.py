import src.db.db_user as db_user
import mysql.connector as mySql_db

db_connector = mySql_db.connect(
    host='localhost',
    user='root',
    password='123@abc',
    database='cinema_ticket'
)
db_runner = db_connector.cursor()
db_user.create_user_table()
