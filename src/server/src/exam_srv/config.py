"""Настройки конфигурации для сред разработки, тестирования и продуктива."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

HERE = Path(__file__).parent
SQLITE_DEV = "sqlite:///" + str(HERE / "exam_srv_dev.db")
SQLITE_TEST = "sqlite:///" + str(HERE / "exam_srv_test.db")
SQLITE_PROD = "sqlite:///" + str(HERE / "exam_srv_prod.db")


class Config:
    """Базовая конфигурация."""

    SECRET_KEY = os.getenv("SECRET_KEY", "open sesame")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    """Тестовая конфигурация."""

    TESTING = True
    TOKEN_EXPIRE_MINUTES = 30
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST


class DevelopmentConfig(Config):
    """Конфигурация для разработки."""

    TOKEN_EXPIRE_MINUTES = 15
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)


class ProductionConfig(Config):
    """Конфигурация для продуктива."""

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Извлечь параметры конфигурации среды."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
