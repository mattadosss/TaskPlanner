import flask
import db_handler

def create_flask():
    app = flask.Flask(__name__)


    @app.route("/")
    def on_home():
        return flask.send_file("html/index.html")

    @app.route("/api_get_tasks")
    def api_get_tasks():
        return db_handler.get_tasks()


    return app