"""Flask app initialization via factory pattern."""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import create_engine
from metis_ai_services.config import get_config

from metis_ai_services.utils.dynamodb_util import init_dynamo_db

# cors = CORS()
# db = SQLAlchemy()
# migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask("Metis AI Services")
    app.debug = True
    app.config.from_object(get_config(config_name))

    from metis_ai_services.api import api_bp

    app.register_blueprint(api_bp)
    # cors.init_app(app, resources={r"/*": {"origins": "*"}})
    CORS(app, resources=r"/*")
    bcrypt.init_app(app)

    # db.init_app(app)
    # migrate.init_app(app, db)
    # init_sqlite_db(app.config)
    print("init dynamodb ...")
    init_dynamo_db()
    print("init dynamodb Done.")
    return app


def init_sqlite_db(conf):
    # engine = create_engine(conf.get("SQLALCHEMY_DATABASE_URI"), echo=True)
    # from metis_ai_services.models.dataset import DataSet
    # from metis_ai_services.models.dataframe import DataFrame
    # from metis_ai_services.models.user import User
    # from metis_ai_services.models.token_blacklist import BlacklistedToken

    # DataSet.__table__.create(bind=engine, checkfirst=True)
    # User.__table__.create(bind=engine, checkfirst=True)
    # BlacklistedToken.__table__.create(bind=engine, checkfirst=True)
    # DataFrame.__table__.create(bind=engine, checkfirst=True)
    pass
