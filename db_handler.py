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
    result = session.execute(sa.text("SElECT * FROM task WHERE task.Task_ID =" + id))
    row = result.fetchone()
    if row is None:
        no_entry_json = {
            "Titel": f'Task with ID {id} not found',
            "erledigt": "",
            "Beschreibung": "",
            "DatumUhrzeit": ""
        }
        return no_entry_json

    json_data = dict(row._mapping)

    # Convert to JSON string (if needed)
    json_string = json.dumps(json_data, indent=2, default=str)
    return json_string

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


