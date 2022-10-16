from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Course(Base):
    """The Course corresponds to the "course" database table."""
    __tablename__ = 'course'
    id = Column(UUID(as_uuid=True), primary_key=True)
    course = Column(String)
    title = Column(String)
    subjectArea = Column(String)
    discord = Column(String)
