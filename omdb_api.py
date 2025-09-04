import httpx
from config import settings

BASE_URL = "http://www.omdbapi.com/"

async def fetch_movie_from_omdb(title: str):
    """
    Fetch movie details from the OMDB API asynchronously.

    This function fetches data about a movie from the OMDB API using the
    provided movie title. If the OMDB API key is not set in the settings,
    it will return None. If the API response indicates success, a
    dictionary containing the movie's title, year, and description will be
    returned. Otherwise, None will be returned.

    :param title: The title of the movie to fetch.
    :type title: str
    :return: A dictionary with "title", "year", and "description" keys if
             the movie is found, or None if not found or if the API key
             is missing/invalid.
    :rtype: dict or None
    """
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
    """
    Fetches a list of movie titles related to the keyword "monitor" using the OMDB API.

    This is an asynchronous function that communicates with the OMDB API to fetch
    movie titles. The function uses a query parameter-based approach with a specific
    timeout for the HTTP request.

    :param limit: The maximum number of movie titles to fetch. Defaults to 10.
    :type limit: int
    :return: A list of movie titles related to the keyword "monitor". If no titles are found
             or if the API key is not configured, an empty list is returned.
    :rtype: List[str]
    """
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
