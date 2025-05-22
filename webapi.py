import flask
from flask import request, jsonify
import db_handler


def create_flask():
    app = flask.Flask(__name__)


    @app.route("/")
    def on_home():
        return flask.render_template("index.html")

    @app.route("/get_task")
    def on_get_task():
        return flask.render_template("get_task.html")

    @app.route("/create_task")
    def on_create_task():
        return flask.render_template("create_task.html")

    @app.route("/api_get_tasks")
    def api_get_tasks():
        return db_handler.get_tasks()

    @app.route("/api_get_task", methods=['GET'])
    def api_get_task():
        args = request.args
        id = args.get("id")
        return db_handler.get_task(id)

    @app.route("/api_create_task", methods=['POST'])
    def api_create_task():
        erledigt = request.form.get("erledigt")
        titel = request.form.get("Titel")
        beschreibung = request.form.get("beschreibung")
        datumUhrzeit = request.form.get("DatumUhrzeit")

        result = db_handler.create_task(erledigt, titel, beschreibung, datumUhrzeit)
        return jsonify(result)


    return app