import uuid

from flask import abort

from app.dao.models import User
from app.dao.user_dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one_by_name(self, username: str) -> User:
        user = self.dao.get_one_by_name(username)
        if user:
            return user
        else:
            abort(404, "Пользователя с таким username не существует")

    def get_one_by_uuid(self, uuid: str) -> User:
        user = self.dao.get_one_by_uuid(uuid)
        if user:
            return user
        else:
            abort(404, "Пользователя с таким uuid не существует")

    def create_user(self, username: str) -> User:

        if self.dao.get_one_by_name(username):
            abort(400, "Пользователь с таким именем уже существует")
        else:
            new_user = User(
                name=username,
                uuid=uuid.uuid4()
            )
            self.dao.save_user(new_user)
            return new_user

