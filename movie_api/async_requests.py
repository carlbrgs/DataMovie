import asyncio
import aiohttp
from cachetools import TTLCache, cached

cache = TTLCache(maxsize=1000, ttl=3600)

@cached(cache)
async def fetch(session, url, params):
    try:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.text()
            else:
                return f"Erreur : {response.status} pour l'URL {url}"
    except aiohttp.ClientError as e:
        return f"Erreur de connexion pour {url}: {e}"

async def make_many_requests(urls, max_concurrent_requests=100, params=None):
    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async def bound_fetch(url):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                return await fetch(session, url, params)

    tasks = [bound_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
