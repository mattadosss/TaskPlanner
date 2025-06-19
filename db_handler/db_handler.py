from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import json

engine = create_engine("mysql+pymysql://root:hello1234@localhost/task_planner")


metadata = MetaData()
metadata.reflect(bind=engine)


Session = sessionmaker(bind=engine)
session = Session()




def delete_done_tasks(user_id):

    try:
        # Use a raw SQL DELETE statement
        session.execute(sa.text("DELETE FROM task WHERE erledigt = 1 AND User_ID = :user_id"), {'user_id': user_id})
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
            "message": f"All done Tasks deleted"
        }

