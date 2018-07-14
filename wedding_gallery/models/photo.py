from sqlalchemy import Boolean, Column, Integer, Text

from .meta import Base


class Photo(Base):
    """ The SQLAlchemy declarative model class for a Photo object. """
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    uuid = Column(Text)
    name = Column(Text)
    description = Column(Text)
    is_aproved = Column(Boolean(create_constraint=False), default=False)
    likes = Column(Integer)
