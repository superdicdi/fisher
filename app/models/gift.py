from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, desc, func, distinct
from sqlalchemy.orm import relationship
from app import db
from app.models.base import Base
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_wish_counts(cls, gift_isbns):
        count_list = db.session.query(
            func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(gift_isbns),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{"count": count, "isbn": isbn} for count, isbn in count_list]
        return count_list

    @property
    def book(self):
        books = YuShuBook()
        books.search_by_isbn(self.isbn)
        return books.first

    @classmethod
    def recent(cls):
        return cls.query.filter_by(
            launched=False
        ).distinct(cls.isbn).all()
        # return cls.query.filter_by(launched=False).group_by(Gift.isbn).limit(30).all()

        # a = db.session.query(distinct(cls.isbn)).all()
        # return
        # pass
    def is_yourself_gift(self, user_id):
        if self.uid == user_id:
            return True
        return False

    def delete(self):
        self.status = 0
