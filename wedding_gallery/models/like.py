from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .meta import Base


class Like(Base):
    """ The SQLAlchemy declarative model class for a Like object. """
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    photo_id = Column(ForeignKey('photos.id'), nullable=False)
    photo = relationship('Photo', back_populates='likes')

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='likes')
