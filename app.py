# ----------------------------------------------------------- #
# -- This file is responsible for running the microservice -- #
# ----------------------------------------------------------- #
from flask import Flask
from config import Config
from routes import blueprints
from models import db
from flask_migrate import Migrate
from scheduler import init_scheduler


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.secret_key = app.config["SECRET_KEY"] # Fetch secret key from Config.py
    db.init_app(app)
    migrate = Migrate(app, db)

    scheduler = init_scheduler(app)
    scheduler.start()

    # Register routes
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run(debug=False, port=8000)
