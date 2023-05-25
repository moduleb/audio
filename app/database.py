from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import config

db = declarative_base()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SwssionClass = sessionmaker(bind=engine)
db_session = SwssionClass()