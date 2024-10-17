import asyncio
from movie_api.async_requests import make_many_requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

urls = [
    "https://api.themoviedb.org/3/movie/550",
    "https://api.themoviedb.org/3/movie/500",
    "https://api.themoviedb.org/3/movie/200"
] * 100  # Pour tester la charge

# Ajout d'URLs répétées pour tester l'effet du cache
urls.extend([
    "https://api.themoviedb.org/3/movie/550",
    "https://api.themoviedb.org/3/movie/500",
    "https://api.themoviedb.org/3/movie/200"
] * 10)

async def run_simulation():
    params = {
        "api_key": os.getenv("TMDB_API_KEY"),
        "language": "en-US"
    }

    print("Début de la simulation sans cache")
    start_time = time.time()
    results = await make_many_requests(urls, params=params, max_concurrent_requests=50)
    end_time = time.time()
    print(f"Temps total sans cache : {end_time - start_time:.2f} secondes")

    print("\n--- Simulation de cache activée ---")
    start_time = time.time()
    results = await make_many_requests(urls, params=params, max_concurrent_requests=50)
    end_time = time.time()
    print(f"Temps total avec cache : {end_time - start_time:.2f} secondes")

if __name__ == "__main__":
    asyncio.run(run_simulation())
