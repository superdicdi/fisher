from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from app import db
from app.models.base import Base
from app.spider.yushu_book import YuShuBook


class Wish(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_gift_counts(cls, wish_isbns):
        from app.models.gift import Gift
        count_list = db.session.query(
            func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(wish_isbns),
            Gift.status == 1).group_by(Gift.isbn).all()
        count_list = [{"count": count, "isbn": isbn} for count, isbn in count_list]
        return count_list

    @property
    def book(self):
        books = YuShuBook()
        books.search_by_isbn(self.isbn)
        return books.first

