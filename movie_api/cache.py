from cachetools import TTLCache, cached
from .services import make_request_with_retry
import os

cache = TTLCache(maxsize=100, ttl=3600)  # Cache avec expiration de 1 heure

@cached(cache)
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": os.getenv("TMDB_API_KEY")}
    return make_request_with_retry(url, params)