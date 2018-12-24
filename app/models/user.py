from sqlalchemy import Column, String, Boolean, Integer, Float
from app.models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column("password", String(128))
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # def get_password(self):
    #     return self._password
    #
    # def set_password(self, value):
    #     self._password = generate_password_hash(value)
    #
    # password = property(get_password, set_password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self._password, value)


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
