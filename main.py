from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import Base, engine, get_db
from schemas import MovieCreate, MovieUpdate, MovieOut
from crud import (
    create_movie, get_movie, get_movies, update_movie, delete_movie,
    get_by_title_year, count_movies, ensure_movie
)
from omdb_api import fetch_movie_from_omdb, fetch_monitor_movies

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Movie Service", version="1.0.0")

@app.post("/movies/", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
async def create_movie_endpoint(payload: MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie entry in the database.

    The endpoint receives incoming movie data, optionally fetches additional
    information from an external OMDB service if some fields are missing, and
    creates a new movie entry in the database if no conflicts exist with pre-existing
    entries based on title and year. If the movie with the same title and year already
    exists, raises a conflict error. The operation returns the newly created movie data.

    :param payload: The payload containing the movie details to be created.
    :param db: The database session for performing operations.
    :return: The newly created movie representation.
    """
    incoming = payload.model_dump()
    if not incoming.get("year") or not incoming.get("description"):
        omdb = await fetch_movie_from_omdb(incoming["title"])
        if omdb:
            incoming["year"] = incoming.get("year") or omdb.get("year")
            incoming["description"] = incoming.get("description") or omdb.get("description")
    if get_by_title_year(db, incoming["title"], incoming.get("year")):
        raise HTTPException(status_code=409, detail="Такой фильм уже есть")
    return create_movie(db, MovieCreate(**incoming))

@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    """
    Fetches movie data associated with a given movie identifier from the database.

    :param movie_id: The identifier of the movie to be retrieved.
    :type movie_id: int
    :param db: The database session dependency used to interact with the database.
    :type db: Session
    :return: The movie object retrieved from the database.
    :rtype: MovieOut
    :raises HTTPException: If the movie is not found, raises an exception with a
        status code 404 and a message indicating that the movie was not found.
    """
    movie = get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="ФИльм не найден")
    return movie

@app.get("/movies/", response_model=List[MovieOut])
def list_movies_endpoint(
        skip: int = 0,
        limit: int = Query(50, le=100),
        q: Optional[str] = Query(None, description="Поиск по названию"),
        db: Session = Depends(get_db),
):
    """
    Handles the retrieval of movies from the database.

    This endpoint allows users to fetch a list of movies with optional
    filters, limits, and pagination. It supports search functionality
    based on movie titles. The response will be a paginated list of
    movies, adhering to the provided limits or defaults.

    :param skip: The number of records to skip for pagination.
    :type skip: int
    :param limit: The maximum number of records to return. Defaults to 50
        with a maximum allowed value of 100.
    :type limit: int
    :param q: An optional string used to search for movies by their title.
        The search is case-insensitive and can match partial titles.
    :type q: Optional[str]
    :param db: A dependency-injected database session to interact with the
        data layer.
    :type db: Session
    :return: A list of movies according to the applied filters and
        pagination.
    :rtype: List[MovieOut]
    """
    return get_movies(db, skip=skip, limit=limit)

@app.put("/movies/{movie_id}", response_model=MovieOut)
def update_movie_endpoint(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    """
    Updates an existing movie record in the database. If the movie is not found, raises
    a 404 HTTP exception.

    :param movie_id: The ID of the movie to be updated
    :type movie_id: int
    :param payload: The data to update for the movie
    :type payload: MovieUpdate
    :param db: The database session dependency
    :type db: Session
    :return: The updated movie record
    :rtype: MovieOut

    :raises HTTPException: If the movie with the given ID is not found
    """
    movie = update_movie(db, movie_id, payload)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    """
    Deletes a movie from the database identified by the given movie ID.

    This endpoint allows the deletion of a specified movie by its unique movie ID.
    The deletion process uses the given database session to locate and remove the
    movie. If the movie ID does not exist in the database, a 404 HTTP exception
    is raised.

    :param movie_id: The unique identifier of the movie to be deleted.
    :param db: The database session dependency for interacting with the database.
    :return: None
    """
    ok = delete_movie(db, movie_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None

@app.on_event("startup")
async def seed_movies_if_less_than_10():
    """
    This function is an asynchronous handler that seeds movies if the current count of
    movies in the database is less than 10. It fetches movies from external resources
    and stores them in the database. The function relies on utility functions for
    fetching and ensuring movies exist in the database.

    :return: None
    :rtype: None
    :raises Exception: If an error occurs during the operation
    """
    logging.info("less_than_10 проверка")
    db = next(get_db())
    try:
        current_count = count_movies(db)
        if current_count >= 10:
            logging.info("less_than_10 пропуск проверки")
            return

        logging.info("less_than_10")
        titles = await fetch_monitor_movies(limit=10)

        for title in titles:
            data = await fetch_movie_from_omdb(title)
            if data:
                ensure_movie(db, data["title"], data.get("year"), data.get("description"))

        db.commit()
    except Exception as e:
        logging.exception(f"less_than_10 ошибка: {e}")

