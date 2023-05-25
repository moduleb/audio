from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import db, engine, db_session


class User (db):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    audio = relationship("Audio", backref='users', primaryjoin="User.id==Audio.user_id")


class Audio (db):
    __tablename__= "audio"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String, nullable=False, unique=True)
    path = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))




# db.metadata.drop_all(engine)
# db.metadata.create_all(engine)
# db_session.commit()