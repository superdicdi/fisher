from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.user import User
# from app import db
from app.models.base import Base


class Gift(Base):
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)


# if __name__ == '__main__':
#     db.create_all()