import flask
from flask import request
from backend import db_handler


def create_flask():
    app = flask.Flask(__name__)


    @app.route("/")
    def on_home():
        return flask.send_file("../templates/index.html")

    @app.route("/get_task")
    def on_get_task():
        return flask.send_file("../templates/get_task.html")

    @app.route("/api_get_tasks")
    def api_get_tasks():
        return db_handler.get_tasks()

    @app.route("/api_get_task", methods=['GET'])
    def api_get_task():
        args = request.args
        id = args.get("id")
        return db_handler.get_task(id)


    return app