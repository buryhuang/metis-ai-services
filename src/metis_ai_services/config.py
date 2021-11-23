"""Config settings for for development, testing and production environments."""
import os

# from pathlib import Path
# HERE = Path(__file__).parent
# SQLITE_DEV = "sqlite:///" + str(HERE / "metisai_ai_services_dev.db")
# SQLITE_TEST = "sqlite:///" + str(HERE / "metisai_ai_services_test.db")
# SQLITE_PROD = "sqlite:///" + str(HERE / "metisai_ai_services_prod.db")

DB_TN_DataSet_DEVP = "DEVP_DataSet"
DB_TN_DataFrame_DEVP = "DEVP_DataFrame"
DB_TN_User_DEVP = "DEVP_User"
DB_TN_UserSession_DEVP = "DEVP_UserSession"

DB_TN_DataSet_TEST = "TEST_DataSet"
DB_TN_DataFrame_TEST = "TEST_DataFrame"
DB_TN_User_TEST = "TEST_User"
DB_TN_UserSession_TEST = "TEST_UserSession"

DB_TN_DataSet_PROD = "DataSet"
DB_TN_DataFrame_PROD = "DataFrame"
DB_TN_User_PROD = "User"
DB_TN_UserSession_PROD = "UserSession"


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "metisaisk")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    # SQLALCHEMY_DATABASE_URI = SQLITE_TEST

    # DynamoDB Config
    DataSet_TN = "DataSet_TEST"
    DataFrame_TN = "DataFrame_TEST"
    User_TN = "User_TEST"
    UserSession_TN = "UserSession_TEST"


class DevelopmentConfig(Config):
    """Development configuration."""

    TOKEN_EXPIRE_MINUTES = 15
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)

    # DynamoDB Config
    DataSet_TN = "DataSet_DEV"
    DataFrame_TN = "DataFrame_DEV"
    User_TN = "User_DEV"
    UserSession_TN = "UserSession_DEV"


class ProductionConfig(Config):
    """Production configuration."""

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True

    # DynamoDB Config
    DataSet_TN = "DataSet"
    DataFrame_TN = "DataFrame"
    User_TN = "User"
    UserSession_TN = "UserSession"


ENV_CONFIG_DICT = dict(devp=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    print(f"{config_name} config loaded.")
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)


class DBTestingConfig:
    DataSet_TN = DB_TN_DataSet_TEST
    DataFrame_TN = DB_TN_DataFrame_TEST
    User_TN = DB_TN_User_TEST
    UserSession_TN = DB_TN_UserSession_TEST


class DBDevelopmentConfig:
    DataSet_TN = DB_TN_DataSet_DEVP
    DataFrame_TN = DB_TN_DataFrame_DEVP
    User_TN = DB_TN_User_DEVP
    UserSession_TN = DB_TN_UserSession_DEVP


class DBProductionConfig:
    DataSet_TN = DB_TN_DataSet_PROD
    DataFrame_TN = DB_TN_DataFrame_PROD
    User_TN = DB_TN_User_PROD
    UserSession_TN = DB_TN_UserSession_PROD


DB_CONFIG_DICT = dict(devp=DBDevelopmentConfig, test=DBTestingConfig, prod=DBProductionConfig)


def init_db_config(config_name):
    return DB_CONFIG_DICT.get(config_name, DBProductionConfig)
