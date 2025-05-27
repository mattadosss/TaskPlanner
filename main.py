import webapi
import pymysql
import db_handler
import datetime
app = webapi.create_flask()


try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='hello1234',
        database='task_planner'
    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"Database version: {version}")
finally:
    connection.close()


#db_handler.create_task(0, "besen", "yesen", "2024-05-08 01:28:54")
#db_handler.delete_task(34)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
