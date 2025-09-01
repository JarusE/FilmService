from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    omdb_api_key: str = os.getenv("OMDB_API_KEY", "")
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./movies.db")

settings = Settings()
