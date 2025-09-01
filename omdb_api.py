import httpx
from config import settings

BASE_URL = "http://www.omdbapi.com/"

async def fetch_movie_from_omdb(title: str):
    if not settings.omdb_api_key:
        return None
    params = {"t": title, "apikey": settings.omdb_api_key}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(BASE_URL, params=params)
        data = r.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "description": data.get("Plot")
            }
        return None

async def fetch_monitor_movies(limit: int = 10):
    if not settings.omdb_api_key:
        return []
    params = {"s": "monitor", "type": "movie", "apikey": settings.omdb_api_key}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(BASE_URL, params=params)
        data = r.json()
        if data.get("Response") == "True":
            results = data.get("Search", [])[:limit]
            return [item.get("Title") for item in results if item.get("Title")]
        return []
