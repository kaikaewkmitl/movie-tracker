import configparser
import os
import requests
from requests.models import Response
from requests.adapters import HTTPAdapter, Retry
from typing import Any, Dict, List

from utils.globals import *

config = configparser.ConfigParser()
config.read("config.ini")

BASE_URL = "api.themoviedb.org"
BASE_URL_WITH_HTTPS = f"https://{BASE_URL}/3"
API_KEY = config[BASE_URL]["API_KEY"]

session = requests.session()
retry = Retry(
    total=3,
    read=3,
    connect=3,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def handle_request(url: str, stream: bool = False) -> Response:
    try:
        response = session.get(url, timeout=3, stream=stream)
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)


def get_trending() -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/trending/all/day?api_key={API_KEY}"
    response = handle_request(url)
    return response.json()["results"]


def get_movie_by_name(movie_name: str) -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/search/movie?api_key={API_KEY}&query={movie_name}&page=1"
    response = handle_request(url)
    return response.json()["results"]


def get_config() -> Dict[str, Any]:
    url = f"{BASE_URL_WITH_HTTPS}/configuration?api_key={API_KEY}"
    response = handle_request(url)
    return response.json()


def get_poster(poster_path: str) -> None:
    poster_config = get_config()
    poster_base_url = poster_config["images"]["base_url"]
    poster_size = poster_config["images"]["poster_sizes"][2]
    url = f"{poster_base_url}{poster_size}{poster_path}"
    response = handle_request(url, stream=True)
    if not os.path.exists(POSTERS_DIR):
        os.makedirs(POSTERS_DIR)

    with open(os.path.join(POSTERS_DIR, poster_path[1:]), "wb") as f:
        for chunk in response:
            f.write(chunk)
