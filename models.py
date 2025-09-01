from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from database import Base

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    year = Column(String(10), index=True, nullable=True)
    description = Column(Text, nullable=True)
    __table_args__ = (UniqueConstraint("title", "year", name="uq_title_year"),)
