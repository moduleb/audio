from app.dao.models import User

class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one_by_name(self, name: str) -> User:
        return self.session.query(User).filter(User.name == name).first()

    def get_one_by_uuid(self, uuid: str) -> User:
        return self.session.query(User).filter(User.uuid == uuid).first()

    def save_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()