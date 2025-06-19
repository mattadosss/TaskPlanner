import flask
from flask import request, jsonify, session, redirect, url_for
from db_handler import db_handler, crud_db, filter_db, user_db
from datetime import datetime
import json
import delete_after


def is_logged_in1():
    return 1
def create_flask():
    app = flask.Flask(__name__)
    app.secret_key = "Task Planner"

    def is_logged_in():
        id = session.get("user_id")
        print(id)
        if id is not None:
            return id
        else:
            print("no user id in session storage")
            return redirect(url_for("on_login"))


    @app.route("/")
    def on_home():
        auth = is_logged_in()
        if isinstance(auth, flask.Response):  # redirect object
            return auth
        print(id)
        delete_after.clean_old_tasks()
        return flask.render_template("index.html")

    @app.route("/get_task")
    def on_get_task():
        return flask.render_template("get_task.html")

    @app.route("/create_task")
    def on_create_task():
        return flask.render_template("create_task.html")

    @app.route("/update_task")
    def on_update_task():
        return flask.render_template("update_task.html")

    @app.route("/login")
    def on_login():
        return flask.render_template("login.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template('404.html'), 404

    @app.route("/api_get_tasks")
    def api_get_tasks():
        user_id = is_logged_in()
        return crud_db.get_tasks(user_id)

    @app.route("/api_get_tasks_by_date")
    def api_get_tasks_by_date():
        user_id = is_logged_in()
        return filter_db.get_tasks_order_by_date(user_id)

    @app.route("/api_get_undone_tasks")
    def api_get_erledigt():
        user_id = is_logged_in()
        return filter_db.get_undone_tasks(user_id)

    @app.route("/api_get_task_by_title", methods=['GET'])
    def api_get_task_by_title():
        user_id = is_logged_in()
        args = request.args
        title = args.get("title")
        return filter_db.get_task_by_title(title, user_id)

    @app.route("/api_get_task_by_id", methods=['GET'])
    def api_get_task_by_id():
        user_id = is_logged_in()
        args = request.args
        id = args.get("id")
        return filter_db.get_task_by_id(id, user_id)

    @app.route("/api_create_task", methods=['POST'])
    def api_create_task():
        erledigt = request.form.get("erledigt")
        titel = request.form.get("Titel")
        beschreibung = request.form.get("beschreibung")
        datumUhrzeit = request.form.get("DatumUhrzeit")

        user_id = is_logged_in()
        result = crud_db.create_task(erledigt, titel, beschreibung, datumUhrzeit, user_id)
        return jsonify(result)

    @app.route("/api_delete_task",  methods=['DELETE'])
    def api_delete_task():
        args = request.args
        id = args.get("id")
        user_id = is_logged_in()
        result = crud_db.delete_task(id, user_id)
        return jsonify(result)

    @app.route("/api_delete_done_task")
    def api_delete_done_task():
        user_id = is_logged_in()
        result = db_handler.delete_done_tasks(user_id)
        return jsonify(result)

    @app.route("/api_update_task", methods=['PUT'])
    def api_update_task():
        id = request.form.get("id")
        erledigt = request.form.get("erledigt")
        titel = request.form.get("Titel")
        beschreibung = request.form.get("beschreibung")
        datumUhrzeit = request.form.get("DatumUhrzeit")
        user_id = is_logged_in()
        print(id)
        print(erledigt)
        print(titel)
        result = crud_db.update_task(id, erledigt, titel, beschreibung, datumUhrzeit, user_id)
        return jsonify(result)

    @app.route("/api_done_task")
    def api_done_task():
        args = request.args
        id = args.get("id")
        erledigt = args.get("erledigt")
        user_id = is_logged_in()
        #print(id, erledigt)
        result = filter_db.done_task(id, erledigt, user_id)
        delete_after.parse(id, erledigt)
        return jsonify(result)

    @app.route("/api_upcoming_tasks", methods=["GET"])
    def upcoming_tasks():
        now = datetime.now()
        user_id = is_logged_in()
        raw_tasks = crud_db.get_tasks(user_id)
        tasks = json.loads(raw_tasks) if isinstance(raw_tasks, str) else raw_tasks

        #print(tasks)

        upcoming = [
            task for task in tasks
            if datetime.strptime(task["DatumUhrzeit"], "%Y-%m-%d %H:%M:%S") > now
        ]
        return jsonify(upcoming)

    @app.route("/api_today_tasks", methods=["GET"])
    def today_tasks():
        user_id = is_logged_in()
        today = datetime.today().date()
        tasks = crud_db.get_tasks(user_id)

        tasks = json.loads(tasks)

        today_tasks = []
        for task in tasks:
            task_date = datetime.strptime(task["DatumUhrzeit"], "%Y-%m-%d %H:%M:%S").date()
            if task_date == today:
                today_tasks.append(task)

        return jsonify(today_tasks)

    @app.route("/api_login", methods=["POST"])
    def on_api_login():
        username = request.form.get("username")
        password = request.form.get("password")
        user_id = user_db.auth_user(username, password)

        if user_id == 0:
            return jsonify({"success": False, "message": "User not found"}), 401
        else:
            session["user_id"] = user_id
            return jsonify({"success": True, "user_id": user_id})

    @app.route("/logout")
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('on_login'))

    return app