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
    return get_movies(db, skip=skip, limit=limit)

@app.put("/movies/{movie_id}", response_model=MovieOut)
def update_movie_endpoint(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    movie = update_movie(db, movie_id, payload)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie_endpoint(movie_id: int, db: Session = Depends(get_db)):
    ok = delete_movie(db, movie_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Movie not found")
    return None

@app.on_event("startup")
async def seed_movies_if_less_than_10():
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

