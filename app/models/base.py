from sqlalchemy import Column, SmallInteger, Integer

from app import db

__author__ = "TuDi"
__date__ = "2018/12/21 下午1:50"


class Base(db.Model):
    __abstract__ = True
    # create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)