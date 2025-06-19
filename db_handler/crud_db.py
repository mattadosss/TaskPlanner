from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import json

engine = create_engine("mysql+pymysql://root:hello1234@localhost/task_planner")


metadata = MetaData()
metadata.reflect(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()


def get_tasks(user_id):
    query = sa.text("SELECT * FROM task WHERE User_ID = :user_id")
    result = session.execute(query, {'user_id': {user_id}})
    rows = result.fetchall()
    json_data = [dict(row._mapping) for row in rows]

    # Convert to JSON string (if needed)
    json_string = json.dumps(json_data, indent=2, default=str)

    return json_string





def create_task(erledigt, titel, beschreibung, datumUhrzeit, user_id):
    query = sa.text("""
        INSERT INTO Task (erledigt, Titel, Beschreibung, DatumUhrzeit, User_ID)
        VALUES (
            :erledigt,
            :titel,
            :beschreibung,
            :datumUhrzeit,
            :user_id
        )
    """)

    session.execute(query, {
        'erledigt': erledigt,
        'titel': titel,
        'beschreibung': beschreibung,
        'datumUhrzeit': datumUhrzeit,
        'user_id': user_id
    })

    session.commit()

    return {
        "Titel": titel,
        "erledigt": erledigt,
        "Beschreibung": beschreibung,
        "DatumUhrzeit": datumUhrzeit,
        "User_ID": user_id
    }


def update_task(id, erledigt, titel, beschreibung, datumUhrzeit, user_id):
    query = sa.text("""
            UPDATE task
            SET 
            erledigt = :erledigt,
            Titel = :titel,
            Beschreibung = :beschreibung,
            DatumUhrzeit = :datumUhrzeit
            WHERE Task_ID = :id
            AND User_ID = :user_id;

        """)

    sess = session.execute(query, {
        'erledigt': erledigt,
        'titel': titel,
        'beschreibung': beschreibung,
        'datumUhrzeit': datumUhrzeit,
        'id': id,
        'user_id': user_id
    })

    # print(sess)

    session.commit()

    answer = {
        "Titel": f'{titel}',
        "erledigt": f'{erledigt}',
        "Beschreibung": f'{beschreibung}',
        "DatumUhrzeit": f'{datumUhrzeit}',
        "user_id": f'{user_id}'
    }
    return answer


def delete_task(id, user_id):
    print(id)

    try:
        # Use a raw SQL DELETE statement
        session.execute(sa.text("DELETE FROM task WHERE Task_ID = :task_id AND User_ID = :user_id"),
                        {'task_id': id, 'user_id': user_id})
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