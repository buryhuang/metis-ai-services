"""Flask app initialization via factory pattern."""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from metis_ai_services.config import get_config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask("Metis AI Services")
    app.debug = True
    app.config.from_object(get_config(config_name))
    # print(config_name)
    # print(app.config)

    # Base = declarative_base()
    # engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"), echo=True)
    # Base.metadata.create_all(engine)
    init_db(app.config)

    from metis_ai_services.api import api_bp

    app.register_blueprint(api_bp)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    return app


def init_db(conf):
    engine = create_engine(conf.get("SQLALCHEMY_DATABASE_URI"), echo=True)
    from metis_ai_services.models.dataset import DataSet

    DataSet.__table__.create(bind=engine, checkfirst=True)
