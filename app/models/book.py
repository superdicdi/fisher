from sqlalchemy import Column, Integer, String
from app import db

__author__ = "TuDi"
__date__ = "2018/12/18 下午2:08"


class Book7(db.Model):

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    _author = Column('author', String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))


if __name__ == '__main__':
    db.create_all()