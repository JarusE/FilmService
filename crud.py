from sqlalchemy.orm import Session
from typing import List, Optional
from models import Movie
from schemas import MovieCreate, MovieUpdate

def create_movie(db: Session, data: MovieCreate) -> Movie:
    movie = Movie(**data.model_dump())
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
    return db.query(Movie).filter(Movie.id == movie_id).first()

def get_movies(db: Session, skip: int = 0, limit: int = 50) -> List[Movie]:
    return db.query(Movie).offset(skip).limit(limit).all()

def update_movie(db: Session, movie_id: int, data: MovieUpdate) -> Optional[Movie]:
    movie = get_movie(db, movie_id)
    if not movie:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(movie, k, v)
    db.commit()
    db.refresh(movie)
    return movie

def delete_movie(db: Session, movie_id: int) -> bool:
    movie = get_movie(db, movie_id)
    if not movie:
        return False
    db.delete(movie)
    db.commit()
    return True

def get_by_title_year(db: Session, title: str, year: Optional[str]) -> Optional[Movie]:
    q = db.query(Movie).filter(Movie.title == title)
    if year:
        q = q.filter(Movie.year == year)
    return q.first()

def count_movies(db: Session) -> int:
    return db.query(Movie).count()

def ensure_movie(
        db: Session,
        title: str,
        year: Optional[str],
        description: Optional[str],
) -> Movie:
    existing = get_by_title_year(db, title, year)
    if existing:
        return existing
    return create_movie(db, MovieCreate(title=title, year=year, description=description))
