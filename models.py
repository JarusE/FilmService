from sqlalchemy import Column, Integer, String, Text, UniqueConstraint
from database import Base

class Movie(Base):
    """
    Represents a movie entry in the database.

    This class is used to define the structure of the `movies` table in the database.
    It includes details such as the movie's title, year of release, and an optional
    description. The combination of `title` and `year` is uniquely constrained to
    ensure that no two movies with the same title and year exist in the database.

    :ivar id: A unique identifier for each movie entry.
    :type id: int
    :ivar title: The title of the movie.
    :type title: str
    :ivar year: The year the movie was released. This attribute is optional.
    :type year: str
    :ivar description: A brief description or synopsis of the movie. This attribute is optional.
    :type description: str
    """
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    year = Column(String(10), index=True, nullable=True)
    description = Column(Text, nullable=True)
    __table_args__ = (UniqueConstraint("title", "year", name="uq_title_year"),)
