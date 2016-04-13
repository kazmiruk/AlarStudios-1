import hashlib

from sqlalchemy import Boolean, Column, Integer, String

from app import config
from app.db import db_session, Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(32))
    full_rights = Column(Boolean, default=False)

    def __init__(self, username, password, full_rights=False):
        self.username = username
        self.password = self._get_password_hash(password)
        self.full_rights = full_rights

    def create(self):
        db_session.add(self)
        db_session.commit()

    def remove(self):
        db_session.delete(self)
        db_session.commit()

    def save(self):
        db_session.commit()

    @classmethod
    def get(cls, pk):
        return cls.query.filter(User.id == pk).first()

    @classmethod
    def _get_password_hash(cls, password):
        return hashlib.sha256("{}|{}".format(password, config.SECRET_KEY)).hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        return cls.query.filter(
            User.username == username and User.password == User._get_password_hash(password)).first()
