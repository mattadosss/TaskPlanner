# TaskPlanner

A Flask-based web application for managing personal tasks with user authentication and automatic cleanup of old tasks.

---

## Features

- User login and registration
- Create, complete, and delete tasks
- Tasks older than 24h are automatically removed
- Session-based user tracking
- REST API endpoints for frontend interaction
- Stores old task logs in `tasks_to_delete.csv`

---

##  Tech Stack

- Python 3 (Flask, SQLAlchemy)
- HTML + JavaScript
- MySql (or any SQL-compatible DB)

---

## Main Files

- `main.py` – App entry point
- `webapi.py` – Flask app factory
- `db_handler.py` – Task database logic
- `user_db.py` – User database logic
- `delete_after.py` – Removes old tasks (24h rule)
- `tasks_to_delete.csv` – Log of removed task IDs

---

## How to Run

#### 1. Clone the Repository

```bash
git clone https://github.com/mattadosss/TaskPlanner.git
cd TaskPlanner
```

---

#### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

---

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

#### 4. Configure Database Credentials

Edit the file:

```text
/db_handler/config.ini
```

Update it with your own credentials:

```ini
[database]
username = your_username
password = your_password
host = localhost
database = task_planner
```

---

#### 5. Set Up the MySQL Database

1. **Login to MySQL:**

```bash
mysql -u your_username -p
```

2. **Run the SQL schema:**

```sql
source path/to/your/project/db/Task_Planner.sql;
```

> Replace `path/to/your/project` with the full path to your local clone.

---

#### 6. Run the Application

```bash
python main.py
```

Then open your browser and go to:

```text
http://localhost:5000
```

##  API Overview

- `POST /api_login` – Logs in user
- `POST /api_create_user` – Registers user
- `GET /api_get_tasks` – Gets user’s tasks
- `PUT /api_done_task?id=1&erledigt=1` – Mark task done/undone
- `GET /api_delete_done_task` – Delete all completed tasks

