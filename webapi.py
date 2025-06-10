import flask
from flask import request, jsonify
import db_handler
from datetime import datetime
import json
import delete_after


def create_flask():
    app = flask.Flask(__name__)
    app.secret_key = "Task Planner"

    test_user_id = 1

    @app.route("/")
    def on_home():
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

    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template('404.html'), 404

    @app.route("/api_get_tasks")
    def api_get_tasks():
        return db_handler.get_tasks(test_user_id)

    @app.route("/api_get_tasks_by_date")
    def api_get_tasks_by_date():
        return db_handler.get_tasks_order_by_date(test_user_id)

    @app.route("/api_get_undone_tasks")
    def api_get_erledigt():
        return db_handler.get_undone_tasks(test_user_id)

    @app.route("/api_get_task_by_title", methods=['GET'])
    def api_get_task_by_title():
        args = request.args
        title = args.get("title")
        return db_handler.get_task_by_title(title, test_user_id)

    @app.route("/api_get_task_by_id", methods=['GET'])
    def api_get_task_by_id():
        args = request.args
        id = args.get("id")
        return db_handler.get_task_by_id(id, test_user_id)

    @app.route("/api_create_task", methods=['POST'])
    def api_create_task():
        erledigt = request.form.get("erledigt")
        titel = request.form.get("Titel")
        beschreibung = request.form.get("beschreibung")
        datumUhrzeit = request.form.get("DatumUhrzeit")

        result = db_handler.create_task(erledigt, titel, beschreibung, datumUhrzeit, test_user_id)
        return jsonify(result)

    @app.route("/api_delete_task",  methods=['DELETE'])
    def api_delete_task():
        args = request.args
        id = args.get("id")
        result = db_handler.delete_task(id, test_user_id)
        return jsonify(result)

    @app.route("/api_delete_done_task")
    def api_delete_done_task():
        result = db_handler.delete_done_tasks(test_user_id)
        return jsonify(result)

    @app.route("/api_update_task", methods=['PUT'])
    def api_update_task():
        id = request.form.get("id")
        erledigt = request.form.get("erledigt")
        titel = request.form.get("Titel")
        beschreibung = request.form.get("beschreibung")
        datumUhrzeit = request.form.get("DatumUhrzeit")
        print(id)
        print(erledigt)
        print(titel)
        result = db_handler.update_task(id, erledigt, titel, beschreibung, datumUhrzeit, test_user_id)
        return jsonify(result)

    @app.route("/api_done_task")
    def api_done_task():
        args = request.args
        id = args.get("id")
        erledigt = args.get("erledigt")
        #print(id, erledigt)
        result = db_handler.done_task(id, erledigt, test_user_id)
        delete_after.parse(id, erledigt)
        return jsonify(result)

    @app.route("/api_upcoming_tasks", methods=["GET"])
    def upcoming_tasks():
        now = datetime.now()

        raw_tasks = db_handler.get_tasks(test_user_id)
        tasks = json.loads(raw_tasks) if isinstance(raw_tasks, str) else raw_tasks

        #print(tasks)

        upcoming = [
            task for task in tasks
            if datetime.strptime(task["DatumUhrzeit"], "%Y-%m-%d %H:%M:%S") > now
        ]
        return jsonify(upcoming)

    @app.route("/api_today_tasks", methods=["GET"])
    def today_tasks():
        today = datetime.today().date()
        tasks = db_handler.get_tasks(test_user_id)

        tasks = json.loads(tasks)

        today_tasks = []
        for task in tasks:
            task_date = datetime.strptime(task["DatumUhrzeit"], "%Y-%m-%d %H:%M:%S").date()
            if task_date == today:
                today_tasks.append(task)

        return jsonify(today_tasks)



    return app