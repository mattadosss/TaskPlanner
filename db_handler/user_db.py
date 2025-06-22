from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import json

engine = create_engine("mysql+pymysql://root:hello1234@localhost/task_planner")


metadata = MetaData()
metadata.reflect(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()

def auth_user(username, password):
    query = sa.text('''
            SELECT user.User_ID FROM user
            WHERE username = :username
            AND password = :password
        ''')

    result = session.execute(query, {'username': username, 'password': password}).fetchone()

    if result:
        user_id = result._mapping['User_ID']
        print(f"User found: {user_id}")
        return user_id
    else:
        print("No user found.")
        return 0


def create_user(username, password):
    check_query = sa.text("SELECT User_ID FROM user WHERE username = :username")
    result = session.execute(check_query, {'username': username}).fetchone()

    if result:
        return {
            'success': False,
            'message': 'Username already exists'
        }

    insert_query = sa.text("""
        INSERT INTO user (username, password)
        VALUES (:username, :password)
    """)

    session.execute(insert_query, {
        'username': username,
        'password': password
    })
    session.commit()


    return {
        'success': True,
        'password': password,
        'username': username
    }

