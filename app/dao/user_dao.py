from flask import abort

from app.dao.models import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one_by_name(self, name: str) -> User:
        try:
            return self.session.query(User).filter(User.name == name).first()
        except Exception:
            abort(500, "Ошибка базы данных")

    def get_one_by_uuid(self, uuid: str) -> User:
        try:
            return self.session.query(User).filter(User.uuid == uuid).first()
        except Exception:
            abort(500, "Ошибка базы данных")

    def save_user(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.commit()
        except Exception:
            abort(500, "Ошибка базы данных")
