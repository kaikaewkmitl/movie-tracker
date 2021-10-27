import configparser
import requests
import shutil
import os

BASE_URL = "api.themoviedb.org"
BASE_URL_WITH_HTTPS = f"https://{BASE_URL}/3"

config = configparser.ConfigParser()
config.read("./tmdb_api/config.ini")

API_KEY = config[BASE_URL]["API_KEY"]


def get_trending():
    url = f"{BASE_URL_WITH_HTTPS}/trending/all/day?api_key={API_KEY}"
    with requests.get(url) as response:
        return response.json()["results"]


def get_config():
    url = f"{BASE_URL_WITH_HTTPS}/configuration?api_key={API_KEY}"
    with requests.get(url) as response:
        return response.json()


def get_poster(poster_path: str, i: int):
    poster_config = get_config()
    poster_base_url = poster_config["images"]["base_url"]
    poster_size = poster_config["images"]["poster_sizes"][1]
    url = f"{poster_base_url}{poster_size}{poster_path}"
    with requests.get(url, stream=True) as response:
        if not os.path.exists("posters"):
            os.makedirs("posters")

        with open(os.path.join("posters", poster_path[1:]), "wb") as f:
            shutil.copyfileobj(response.raw, f)
