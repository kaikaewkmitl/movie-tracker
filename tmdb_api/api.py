import configparser
import os
import requests
from typing import Any, Dict, List

from utils.const import *

config = configparser.ConfigParser()
config.read("./tmdb_api/config.ini")

API_KEY = config[BASE_URL]["API_KEY"]


def get_trending() -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/trending/all/day?api_key={API_KEY}"
    with requests.get(url) as response:
        return response.json()["results"]


def get_movie_by_name(movie_name: str) -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/search/movie?api_key={API_KEY}&query={movie_name}&page=1"
    with requests.get(url) as response:
        return response.json()["results"]


def get_config() -> Dict[str, Any]:
    url = f"{BASE_URL_WITH_HTTPS}/configuration?api_key={API_KEY}"
    with requests.get(url) as response:
        return response.json()


def get_poster(poster_path: str) -> None:
    poster_config = get_config()
    poster_base_url = poster_config["images"]["base_url"]
    poster_size = poster_config["images"]["poster_sizes"][2]
    url = f"{poster_base_url}{poster_size}{poster_path}"
    with requests.get(url, stream=True) as response:
        if not os.path.exists(POSTERS_DIR):
            os.makedirs(POSTERS_DIR)

        with open(os.path.join(POSTERS_DIR, poster_path[1:]), "wb") as f:
            for chunk in response:
                f.write(chunk)
