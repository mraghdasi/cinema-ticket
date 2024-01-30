import src.db.db_main as db


def create_user_table():
    db.db_runner.execute('create table if not exists user (id int unsigned auto_increment primary key not null,'
'username varchar(100) not null)')
