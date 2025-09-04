from pydantic import BaseModel, Field
from typing import Optional

class MovieBase(BaseModel):
    """
    Represents the base model for a movie entity.

    This class serves as a foundational model for movies, encapsulating
    details such as the title, year, and description. It is intended to
    enable structured and consistent usage of movie-related data within
    an application.

    :ivar title: The title of the movie. It must be a string with a minimum
        length of 1 and a maximum length of 255.
    :type title: str
    :ivar year: Optional release year of the movie.
    :type year: Optional[str]
    :ivar description: Optional description or summary of the movie's content.
    :type description: Optional[str]
    """
    title: str = Field(..., min_length=1, max_length=255)
    year: Optional[str] = None
    description: Optional[str] = None

class MovieCreate(MovieBase):
    """
    Represents the creation of a movie entry with specific attributes.

    This class is intended to be used for defining the fields required
    to create a new movie object. It inherits from `MovieBase`, which
    contains shared attributes for movie instances. The class does not
    introduce any additional attributes or methods beyond its base class.
    """
    pass

class MovieUpdate(BaseModel):
    """
    Representation of an update to a movie's details.

    This class is used to update information about a movie, such as its title,
    release year, and description. It defines optional fields, which allow partial
    updates to a movie's details without requiring all information to be provided.

    :ivar title: Title of the movie. Optional. If `None`, the title will not be
                 updated.
    :type title: Optional[str]
    :ivar year: Release year of the movie. Optional. If `None`, the release year
                will not be updated.
    :type year: Optional[str]
    :ivar description: Description or synopsis of the movie. Optional. If `None`,
                       the description will not be updated.
    :type description: Optional[str]
    """
    title: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None

class MovieOut(MovieBase):
    """
    Represents the output model for a movie.

    This class is designed to store information about a movie while inheriting
    base properties from the MovieBase class. It also supports configuration
    to allow attribute mapping using external sources.

    :ivar id: Unique identifier for the movie.
    :type id: int
    """
    id: int
    class Config:
        from_attributes = True
