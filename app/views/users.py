from flask import request
from flask_restx import Namespace, Resource

from app.container import user_service
from app.utils.token import generate_token

users_ns = Namespace('/users')


@users_ns.route("/")
class UsersView(Resource):
    def post(self):
        # Получаем данные запроса
        data = request.json

        if not 'name' in data:
            return "Неверный формат запроса", 400

        if not data.get('name'):
            return "Поле 'name' пустое", 400

        elif user_service.is_exist(data.get('name')):
            return "Пользователь с таким именем уже существует", 400

        else:
            new_user = user_service.create_user(data)
            return {
                "uuid": new_user.uuid,
                "token": generate_token({"name": new_user.name})
            }
