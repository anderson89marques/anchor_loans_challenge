from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Boolean,
)

from .meta import Base


class Photo(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    uuid = Column(Text)
    name = Column(Text)
    description = Column(Text)
    is_aproved = Column(Boolean(create_constraint=False), default=False)
    likes = Column(Integer)
