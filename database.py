from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    Creates and manages a database session.

    This function is a generator that initializes a new database session, yields
    it for use, and ensures the session is properly closed after its usage.

    Yields:
        Session: A database session instance.

    :return: Yields a database session for performing operations. Closes the
        session after usage.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
