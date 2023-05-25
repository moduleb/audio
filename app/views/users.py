from flask import request
from flask_restx import Namespace, Resource
import re

from app.container import user_service
from app.utils.token import generate_token

users_ns = Namespace('/users')


@users_ns.route("/")
class UsersView(Resource):
    def post(self):
        # Получаем данные запроса
        data = request.json

        if 'name' not in data:
            return "В запросе отсутствует обязательный параметр 'name'", 400

        # Получаем username из запроса
        username = data.get('name')

        if not username:
            return "Поле 'name' пустое", 400

        if not re.match(r'^[\w\s-]+$', username):
            return "Параметр 'name' содержит недопустимые символы"

        if user_service.is_exist(username):
            return "Пользователь с таким именем уже существует", 400

        # Создаем пользователя
        new_user = user_service.create_user(username)

        return {
            "uuid": new_user.uuid,
            "token": generate_token({"name": username})
        }
