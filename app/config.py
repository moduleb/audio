import os


class ConfigDevelopment():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
    SQLALCHEMY_TRACK_NOTIFICATION = False
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = 'app/data'
    SECRET_KEY = os.urandom(24)
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB


class ConfigProduction:
    SQLALCHEMY_DATABASE_URI = 'postgresql://audio:audio@pg:5433/audio'
    SQLALCHEMY_TRACK_NOTIFICATION = False
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False
    UPLOAD_FOLDER = '/app/data'
    SECRET_KEY = os.urandom(24)
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB


# Загружаем конфигурацию, указанную в переменной окружения FLASK_ENV
if os.environ.get("FLASK_ENV") == "production":
    config = ConfigProduction()
else:
    config = ConfigDevelopment()