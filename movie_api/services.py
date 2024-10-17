import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def make_request_with_retry(url, params=None, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                print(f"Requête réussie pour {url}")
                return response.json()
            elif response.status_code == 429:
                print("Trop de requêtes. Attente...")
                time.sleep(2 ** attempt)
            elif response.status_code in {500, 503}:
                print("Erreur serveur. Nouvelle tentative...")
                time.sleep(2 ** attempt)
            else:
                return f"Erreur : {response.status_code}"
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion : {e}")
            time.sleep(2 ** attempt)
    return "Échec après plusieurs tentatives."
