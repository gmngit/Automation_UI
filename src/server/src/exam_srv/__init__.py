"""Инициализация приложения Flask через шаблон проектирования factory."""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

from exam_srv.config import get_config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask("exam_srv", static_folder="pages/static", static_url_path="/assets")
    app.config.from_object(get_config(config_name))

    from .api import api_bp

    with app.app_context():
        from .pages import main

    app.register_blueprint(api_bp)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    bootstrap = Bootstrap5(app)
    return app
