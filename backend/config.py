import os


class Config:
    _db_url = os.environ.get("DATABASE_URL", "sqlite:///notes.db")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}

    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32).hex())
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
    MAX_NOTE_LENGTH = int(os.environ.get("MAX_NOTE_LENGTH", 100_000))
    MAX_QUESTION_LENGTH = int(os.environ.get("MAX_QUESTION_LENGTH", 1_000))
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))
    RATELIMIT_STORAGE_URL = os.environ.get("RATELIMIT_STORAGE_URL", "memory://")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


def get_config():
    env = os.environ.get("FLASK_ENV", "development")
    return ProductionConfig() if env == "production" else DevelopmentConfig()
