from flask_login import current_user
from sqlalchemy import Column, String, Integer, SmallInteger

from app import db
from app.models.base import Base


class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'
    id = Column(Integer, primary_key=True)
    # 邮件信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return self._pending

    @pending.setter
    def pending(self, raw):
        self._pending = raw.value

    def save_drift(self, drift_form, current_gift):
        with db.auto_commit():
            # 将表单数据一一对应赋值，表单名称和模型名称必须一致
            drift_form.populate_obj(self)

            self.gift_id = current_gift.id
            self.requester_id = current_user.id
            self.requester_nickname = current_user.nickname
            self.gifter_nickname = current_gift.user.nickname
            self.gifter_id = current_gift.user.id
            self.book_title = current_gift.book["title"]
            self.book_author = current_gift.book["author"]
            self.book_img = current_gift.book["image"]
            self.isbn = current_gift.book["isbn"]

            current_user.beans -= 1
            db.session.add(self)



