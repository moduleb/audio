import uuid

from app.dao.models import User
from app.dao.user_dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one_by_name(self, name: str) -> User:
        return self.dao.get_one_by_name(name)

    def get_one_by_uuid(self, uuid: str) -> User:
        return self.dao.get_one_by_uuid(uuid)

    def create_user(self, username: str) -> User:
        new_user = User(
            name=username,
            uuid=uuid.uuid4()
        )
        self.dao.save_user(new_user)
        return new_user

    def is_exist(self, name: str) -> bool:
        user = self.dao.get_one_by_name(name)
        if user:
            return True
        else:
            return False
