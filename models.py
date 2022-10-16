from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Class(Base):
    """The Class corresponds to the "class" database table."""
    __tablename__ = 'class'
    id = Column(UUID(as_uuid=True), primary_key=True)
    course = Column(String)
    descrip = Column(String)
    discord = Column(String)
