from sqlalchemy.orm import Session
from typing import List, Optional
from models import Movie
from schemas import MovieCreate, MovieUpdate

def create_movie(db: Session, data: MovieCreate) -> Movie:
    """
    Creates and persists a new movie record in the database. This function uses
    the given `db` session to add a new movie based on the provided data, then
    commits the transaction and refreshes the state to retrieve the latest
    information of the new movie entry.

    :param db: Database session used to interact with the database.
    :type db: Session
    :param data: Data required to create a new movie record.
    :type data: MovieCreate
    :return: The newly created movie record.
    :rtype: Movie
    """
    movie = Movie(**data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
    """
    Fetch a movie from the database by its unique identifier.

    This function retrieves a single movie record from the database using the
    provided movie ID. If no matching record is found, it will return None.

    :param db: Database session object used for querying the data
    :type db: Session
    :param movie_id: Identifier of the movie to fetch
    :type movie_id: int
    :return: Movie object if found, otherwise None
    :rtype: Optional[Movie]
    """
    return db.query(Movie).filter(Movie.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 50) -> List[Movie]:
    """
    Fetches a paginated list of movies from the database.

    This function retrieves movies starting at the specified offset and limits the
    number of results returned. The results are sourced directly from the database
    session provided, enabling controlled access to data.

    :param db: The database session used to query the Movie data.
    :type db: Session
    :param skip: The number of records to skip from the start.
    :type skip: int
    :param limit: The maximum number of records to return.
    :type limit: int
    :return: A list of Movie objects retrieved from the database based on the
             specified parameters.
    :rtype: List[Movie]
    """
    return db.query(Movie).offset(skip).limit(limit).all()

def update_movie(db: Session, movie_id: int, data: MovieUpdate) -> Optional[Movie]:
    """
    Updates an existing movie in the database with the provided data. If the movie
    with the given ID does not exist, the function returns None. The function
    commits the changes to the database and refreshes the movie instance before
    returning it.

    :param db: A database session instance.
    :param movie_id: ID of the movie to be updated.
    :param data: An instance of MovieUpdate containing updated movie data.
    :return: The updated Movie instance if found, otherwise None.
    """
    movie = get_movie(db, movie_id)
    if not movie:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(movie, k, v)
    db.commit()
    db.refresh(movie)
    return movie

def delete_movie(db: Session, movie_id: int) -> bool:
    """
    Deletes a movie from the database based on the provided movie ID.

    This function searches for a movie in the database using the given movie ID. If the movie
    exists, it deletes the movie from the database and commits the transaction. If the movie
    does not exist, the function returns False.

    :param db: The database session used to access and modify the database.
    :type db: Session
    :param movie_id: The unique identifier of the movie to be deleted.
    :type movie_id: int
    :return: True if the movie was successfully deleted, False otherwise.
    :rtype: bool
    """
    movie = get_movie(db, movie_id)
    if not movie:
        return False
    db.delete(movie)
    db.commit()
    return True

def get_by_title_year(db: Session, title: str, year: Optional[str]) -> Optional[Movie]:
    """
    Fetch a movie record from the database based on its title and optionally its year.

    This function queries the database to find a movie matching the provided title.
    If a year is also specified, it filters the results further to match the given year.
    Returns the first matching record or None if no match is found.

    :param db: Database session used to query the movie record
    :type db: Session
    :param title: Title of the movie to search for
    :type title: str
    :param year: (Optional) Year of release to filter the results
    :type year: Optional[str]
    :return: The first `Movie` object that matches the criteria or None if no match is found
    :rtype: Optional[Movie]
    """
    q = db.query(Movie).filter(Movie.title == title)
    if year:
        q = q.filter(Movie.year == year)
    return q.first()

def count_movies(db: Session) -> int:
    """
    Counts the total number of movies in the database.

    This function queries the database to retrieve the total count of movie
    records. It ensures that the count of all the movies is returned as an
    integer value.

    :param db: Session
        The database session used to query the Movie records.
    :return: int
        The total count of movies in the database.
    """
    return db.query(Movie).count()

def ensure_movie(
        db: Session,
        title: str,
        year: Optional[str],
        description: Optional[str],
) -> Movie:
    """
    Ensures a movie record exists in the database with the given title, year, and description. If a
    movie with the specified title and year is already present in the database, it will return the
    existing record. Otherwise, it will create a new movie record with the provided details and return it.

    :param db: Database session to interact with the database.
    :type db: Session
    :param title: The title of the movie to be ensured in the database.
    :type title: str
    :param year: The year the movie was released. Can be None if not provided.
    :type year: Optional[str]
    :param description: A brief description of the movie. Can be None if not provided.
    :type description: Optional[str]
    :return: The movie record that matches the provided title and year, or the newly created movie
        record if it does not already exist.
    :rtype: Movie
    """
    existing = get_by_title_year(db, title, year)
    if existing:
        return existing
    return create_movie(db, MovieCreate(title=title, year=year, description=description))
