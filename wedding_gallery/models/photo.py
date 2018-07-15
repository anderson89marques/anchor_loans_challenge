from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from .meta import Base


class Photo(Base):
    """ The SQLAlchemy declarative model class for a Photo object. """
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    uuid = Column(Text)
    name = Column(Text)
    description = Column(Text)
    is_approved = Column(Boolean(create_constraint=False), default=False)
    likes = Column(Integer)

    creator_id = Column(ForeignKey('users.id'), nullable=False)
    creator = relationship('User', backref='photos')
