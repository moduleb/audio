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
            "access_token": generate_token({"name": username}),
            "type_token": "Bearer"
        }


def get_username_from_post_request(request):
    # Получаем данные запроса
    username = request.form.get('username')

    if not username:
        abort(400, "В запросе отсутствует обязательный параметр 'username'")

    if not re.match(r'^[\w\s-]+$', username):
        abort(400, "Параметр 'username' содержит недопустимые символы")

    return username
