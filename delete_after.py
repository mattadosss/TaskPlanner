import csv
from datetime import datetime, timedelta
import db_handler
import webapi

CSV = 'tasks_to_delete.csv'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
EXPECTED_FIELDS = ["id", "DatumUhrzeit"]

def is_older_than_24_hours(date_str):
    task_time = datetime.strptime(date_str, DATE_FORMAT)
    return datetime.now() - task_time > timedelta(hours=24)

def clean_old_tasks():
    try:
        with open(CSV, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            tasks = list(reader)
    except FileNotFoundError:
        #print("CSV file not found. Nothing to clean.")
        return

    if not tasks:
        #print("CSV file is empty. Nothing to clean.")
        return

    remaining_tasks = []

    for task in tasks:
        if is_older_than_24_hours(task['DatumUhrzeit']):
            result = db_handler.delete_task(task["id"], webapi.is_logged_in1())
            print(result)
        else:
            remaining_tasks.append(task)

    with open(CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=EXPECTED_FIELDS)
        writer.writeheader()
        writer.writerows(remaining_tasks)

    print("Deleted old tasks.")

def add_task_log(task_id):
    now = datetime.now().strftime(DATE_FORMAT)
    with open(CSV, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=EXPECTED_FIELDS)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({'id': task_id, 'DatumUhrzeit': now})

def delete_task_by_id(task_id):

    try:
        with open(CSV, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            rows = [row for row in reader if row["id"] != str(task_id)]
    except FileNotFoundError:
        print("CSV file not found.")
        return

    with open(CSV, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=EXPECTED_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse(id, erledigt):
    if erledigt == "1":
        add_task_log(id)
    else:
        delete_task_by_id(id)

if __name__ == "__main__":
    clean_old_tasks()
