import os
import flask


def create_app():
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flask_db.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import flaskdb
    flaskdb.init_app(app)
    app.register_blueprint(flaskdb.bp)

    print("app configured.")
    return app
