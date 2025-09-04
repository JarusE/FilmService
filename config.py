from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    """
    Settings class for application configuration.

    This class is responsible for storing configuration parameters such as
    API keys, database URLs, and any other settings required by the application.
    The values are populated by reading environment variables.

    :ivar omdb_api_key: The API key required to interact with the OMDB API.
    :type omdb_api_key: str
    :ivar db_url: The database connection URL. Defaults to a local SQLite database
        if the environment variable is not set.
    :type db_url: str
    """
    omdb_api_key: str = os.getenv("OMDB_API_KEY", "")
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./movies.db")

settings = Settings()
