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

session = requests.Session()


def init_api() -> None:
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


def add_movie_title(movie: Dict[str, Any]) -> None:
    movie[MOVIE_TITLE] = movie["title"] if "title" in movie else movie["name"]


def add_genre_ids(movie: Dict[str, Any]) -> None:
    movie[MOVIE_GENRE_IDS] = []
    for genre in movie[MOVIE_GENRES]:
        movie[MOVIE_GENRE_IDS].append(genre["id"])


def get_trending() -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/trending/movie/day?api_key={API_KEY}"
    response = handle_request(url)
    movies = response.json()["results"]
    for movie in movies:
        add_movie_title(movie)

    return movies


def get_movie_by_name(movie_name: str) -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/search/movie?api_key={API_KEY}&query={movie_name}&page=1"
    response = handle_request(url)
    movies = response.json()["results"]
    for movie in movies:
        add_movie_title(movie)
        add_genre_ids(movie)

    return movies


def get_config() -> Dict[str, Any]:
    url = f"{BASE_URL_WITH_HTTPS}/configuration?api_key={API_KEY}"
    response = handle_request(url)
    return response.json()


def get_genre_list() -> List[Dict[str, Any]]:
    url = f"{BASE_URL_WITH_HTTPS}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = handle_request(url)
    return response.json()["genres"]


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


def get_movie_by_id(movie_id: int) -> Dict[str, Any]:
    url = f"{BASE_URL_WITH_HTTPS}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = handle_request(url)
    movie = response.json()
    add_movie_title(movie)
    add_genre_ids(movie)
    return movie
