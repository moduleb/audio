from flask import Flask
from flask_restx import Api
from waitress import serve

from app.config import config
from app.views.record import record_ns
from app.views.users import users_ns

# Создание приложения
app = Flask("__name__")

# Загрузка конфигурации
app.config.from_object(config)
app.app_context().push()

# Регистрация restx и неймспейсов
api = Api(app)
api.add_namespace(users_ns)
api.add_namespace(record_ns)


if __name__ == "__main__":
    # Запуск
    if app.config.get("FLASK_ENV") == "production":
        serve(app, host="0.0.0.0", port=80)
    else:
        app.run(host="0.0.0.0", port=80)
