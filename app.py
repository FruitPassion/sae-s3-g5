import os
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, url_for

from controller.admin import admin
from controller.api import api
from controller.apprentis import apprenti
from controller.personnel import personnel
from model_db.shared_model import db

from controller.auth import auth


def create_app():
    app = Flask(__name__, template_folder="view")
    app.config.from_object("config.DevConfig")
    toolbar = DebugToolbarExtension(app)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    app.register_blueprint(personnel)
    app.register_blueprint(apprenti)
    app.register_blueprint(admin)
    db.init_app(app)

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == "static":
            filename = values.get("filename", None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values["q"] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    app.run()


if __name__ == "__main__":
    create_app()
