from flask import request, abort
from flask_restx import Namespace, Resource
import re

from app.container import user_service
from app.utils.token import generate_token

users_ns = Namespace('/users')


@users_ns.route("/")
class UsersView(Resource):
    def post(self):
        # Получаем username из запроса
        username = get_username_from_post_request(request)

        # Создаем пользователя
        new_user = user_service.create_user(username)

        # Возвращаем uuid и token
        return {
            "uuid": new_user.uuid,
            "token": generate_token({"name": username})
        }


def get_username_from_post_request(request):
    # Получаем данные запроса
    data = request.json

    if 'name' not in data:
        abort(400, "В запросе отсутствует обязательный параметр 'name'")

    # Получаем username из запроса
    username = data.get('name')

    if not username:
        abort(400, "Поле 'name' пустое")

    if not re.match(r'^[\w\s-]+$', username):
        abort(400, "Параметр 'name' содержит недопустимые символы")

    return username
