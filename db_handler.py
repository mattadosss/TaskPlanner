from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import json

engine = create_engine("mysql+pymysql://root:hello1234@localhost/task_planner")


metadata = MetaData()
metadata.reflect(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()


def get_tasks():
    result = session.execute(sa.text("SELECT * FROM task"))
    rows = result.fetchall()
    json_data = [dict(row._mapping) for row in rows]

    # Convert to JSON string (if needed)
    json_string = json.dumps(json_data, indent=2, default=str)

    return json_string
def get_task(id):
    # Use parameterized LIKE query to prevent SQL injection
    query = sa.text('SELECT * FROM task WHERE task.Titel LIKE :pattern')
    result = session.execute(query, {'pattern': f"%{id}%"})
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


def create_task(erledigt, titel, beschreibung, datumUhrzeit):
    query = sa.text("""
            INSERT INTO Task (erledigt, Titel, Beschreibung, DatumUhrzeit)
            values (
                :erledigt,
                :titel,
                :beschreibung,
                :datumUhrzeit
           )
        """)

    sess = session.execute(query, {
        'erledigt': erledigt,
        'titel': titel,
        'beschreibung': beschreibung,
        'datumUhrzeit': datumUhrzeit
    })

    session.commit()

    answer = {
            "Titel": f'{titel}',
            "erledigt": f'{erledigt}',
            "Beschreibung": f'{beschreibung}',
            "DatumUhrzeit": f'{datumUhrzeit}'
        }
    return answer

def delete_task(id):
    print(id)

    try:
        # Use a raw SQL DELETE statement
        session.execute(sa.text("DELETE FROM task WHERE Task_ID = :task_id"), {'task_id': id})
        session.commit()  # Commit the transaction
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error deleting task: {e}")

    if id is None:
        no_entry_json = {
            "Titel": f'Task with ID {id} not found',
            "erledigt": "",
            "Beschreibung": "",
            "DatumUhrzeit": ""
        }
        return no_entry_json
    else:
        return {
            "success": True,
            "message": f"Task with ID {id} was deleted."
        }


def get_task_by_date(date_string):
    query = sa.text('''
        SELECT * FROM task
        WHERE DATE(task.DatumUhrzeit) = :date
        ORDER BY task.DatumUhrzeit ASC
    ''')
    result = session.execute(query, {'date': date_string})
    rows = result.fetchall()

    if not rows:
        return {
            "message": f'No tasks found for date "{date_string}".',
            "tasks": []
        }

    json_data = [dict(row._mapping) for row in rows]
    return json.dumps(json_data, indent=2, default=str)


def get_tasks_order_by_date():
    query = sa.text('''
        SELECT * FROM task
        ORDER BY task.DatumUhrzeit ASC
    ''')
    result = session.execute(query)
    rows = result.fetchall()


    json_data = [dict(row._mapping) for row in rows]
    return json.dumps(json_data, indent=2, default=str)



