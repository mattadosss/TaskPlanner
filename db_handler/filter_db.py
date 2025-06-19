from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import json

engine = create_engine("mysql+pymysql://root:hello1234@localhost/task_planner")


metadata = MetaData()
metadata.reflect(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()

def get_task_by_title(id, user_id):
    # Use parameterized LIKE query to prevent SQL injection
    query = sa.text('SELECT * FROM task WHERE task.Titel LIKE :pattern AND User_ID = :user_id')
    result = session.execute(query, {'pattern': f"%{id}%", 'user_id': {user_id}})
    rows = result.fetchall()

    # If no results found
    if not rows:
        return {
            "Titel": f'Task with Title: "{id}" not found',
            "erledigt": "",
            "Beschreibung": "",
            "DatumUhrzeit": ""
        }

    # Convert rows to JSON
    if len(rows) > 1:
        json_data = [dict(row._mapping) for row in rows]
    else:
        json_data = dict(rows[0]._mapping)

    return json.dumps(json_data, indent=2, default=str)


def get_task_by_id(id, user_id):
    # Use parameterized LIKE query to prevent SQL injection
    query = sa.text('SELECT * FROM task WHERE task.Task_ID LIKE :pattern AND User_ID = :user_id')
    result = session.execute(query, {'pattern': f"%{id}%", 'user_id': f'{user_id}'})
    rows = result.fetchall()

    # If no results found
    if not rows:
        return {
            "Titel": f'Task with ID "{id}" not found',
            "erledigt": "",
            "Beschreibung": "",
            "DatumUhrzeit": ""
        }

    # Convert rows to JSON
    if len(rows) > 1:
        json_data = [dict(row._mapping) for row in rows]
    else:
        json_data = dict(rows[0]._mapping)

    return json.dumps(json_data, indent=2, default=str)

def get_task_by_date(date_string, user_id):
    query = sa.text('''
        SELECT * FROM task
        WHERE DATE(task.DatumUhrzeit) = :date
        AND User_ID = :user_id
        ORDER BY task.DatumUhrzeit ASC
    ''')
    result = session.execute(query, {'date': date_string, 'user_id': user_id})
    rows = result.fetchall()

    if not rows:
        return {
            "message": f'No tasks found for date "{date_string}".',
            "tasks": []
        }

    json_data = [dict(row._mapping) for row in rows]
    return json.dumps(json_data, indent=2, default=str)


def get_undone_tasks(user_id):
    query = sa.text('''
        SELECT * FROM task
        WHERE erledigt = 0
        AND User_ID = :user_id;
    ''')
    result = session.execute(query, {'user_id': user_id})
    rows = result.fetchall()

    if not rows:
        return {
            "message": f'All tasks done.',
            "tasks": []
        }

    json_data = [dict(row._mapping) for row in rows]
    return json.dumps(json_data, indent=2, default=str)


def get_tasks_order_by_date(user_id):
    query = sa.text('''
        SELECT * FROM task
        WHERE User_ID = :user_id
        ORDER BY task.DatumUhrzeit ASC
    ''')
    result = session.execute(query, {'user_id': user_id})
    rows = result.fetchall()


    json_data = [dict(row._mapping) for row in rows]
    return json.dumps(json_data, indent=2, default=str)


def done_task(id, erledigt, user_id):
    query = sa.text("""
                UPDATE task
                SET 
                erledigt = :erledigt
                WHERE Task_ID = :id
                AND User_ID = :user_id;

            """)

    sess = session.execute(query, {'erledigt': erledigt, 'id': id, 'user_id': user_id})

    # print(sess)

    session.commit()

    answer = {
        "Titel": f'{id}'
    }
    return answer