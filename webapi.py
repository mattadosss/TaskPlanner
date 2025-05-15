import flask

def create_flask():
    app = flask.Flask(__name__)


    @app.route("/")
    def on_home():
        return flask.send_file("html/index.html")


    return app