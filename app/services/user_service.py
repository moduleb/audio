import uuid

from app.dao.models import User
from app.dao.user_dao import UserDAO


class UserService:
    def __init__(self, dao:UserDAO):
        self.dao = dao

    def get_one(self, name):
        return self.dao.get_one(name)

    def get_one_by_uuid(self, uuid):
        return self.dao.get_one_by_uuid(uuid)

    def create_user(self, data: dict):
        new_user = User(
            name=data.get("name"),
            uuid=uuid.uuid4()
        )
        self.dao.save_user(new_user)
        return new_user

    def is_exist(self, name):
        user = self.dao.get_one(name)
        print(user)
        if user is not None:
            return True
        else:
            return False
