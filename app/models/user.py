from flask import current_app
from sqlalchemy import Column, String, Boolean, Integer, Float

from app.libs.enums import PendingStatus
from app.models.base import Base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    def can_save_to_list(self, isbn):
        gift = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wish = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gift and not wish:
            return True
        return False

    def generate_token(self, expire_time=600):
        s = Serializer(current_app.config["SECRET_KEY"], expire_time)
        temp = s.dumps({"id": self.id}).decode("utf-8")
        return temp

    def can_send_gift(self):
        if self.beans < 1:
            return False
        success_send_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()

        if int(success_receive_count) / 2 <= int(success_send_count):
            return True
        return False

    @staticmethod
    def reset_password(token, new_password):

        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except Exception as e:
            return False

        uid = data.get("id")
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
            db.session.add(user)
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + "/" + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
