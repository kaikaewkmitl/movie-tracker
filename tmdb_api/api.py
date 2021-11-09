import configparser
from typing import Any, Dict, List
import requests
import os

from utils.const import *

config = configparser.ConfigParser()
config.read("./tmdb_api/config.ini")

API_KEY = config[BASE_URL]["API_KEY"]


def get_trending() -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/trending/all/day?api_key={API_KEY}"
    with requests.get(url) as response:
        return response.json()["results"]


def get_config() -> Dict[str, Any]:
    url = f"{BASE_URL_WITH_HTTPS}/configuration?api_key={API_KEY}"
    with requests.get(url) as response:
        return response.json()


def get_poster(poster_path: str) -> None:
    poster_config = get_config()
    poster_base_url = poster_config["images"]["base_url"]
    poster_size = poster_config["images"]["poster_sizes"][1]
    url = f"{poster_base_url}{poster_size}{poster_path}"
    with requests.get(url, stream=True) as response:
        if not os.path.exists(POSTERS_DIR):
            os.makedirs(POSTERS_DIR)

        with open(os.path.join(POSTERS_DIR, poster_path[1:]), "wb") as f:
            for chunk in response:
                f.write(chunk)
