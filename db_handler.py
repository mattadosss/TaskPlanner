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




