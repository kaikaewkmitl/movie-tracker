import configparser
from typing import Any, Dict, List
import requests
import os

from utils.const import *


class TheMovieDBAPI:
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read("./tmdb_api/config.ini")

        self.__api_key = config[BASE_URL]["API_KEY"]

    def get_trending(self) -> List[Dict[str, Any]]:
        url = f"{BASE_URL_WITH_HTTPS}/trending/all/day?api_key={self.__api_key}"
        with requests.get(url) as response:
            return response.json()["results"]

    def get_config(self) -> Dict[str, Any]:
        url = f"{BASE_URL_WITH_HTTPS}/configuration?api_key={self.__api_key}"
        with requests.get(url) as response:
            return response.json()

    def get_poster(self, poster_path: str) -> None:
        poster_config = self.get_config()
        poster_base_url = poster_config["images"]["base_url"]
        poster_size = poster_config["images"]["poster_sizes"][1]
        url = f"{poster_base_url}{poster_size}{poster_path}"
        with requests.get(url, stream=True) as response:
            if not os.path.exists("posters"):
                os.makedirs("posters")

            with open(os.path.join("posters", poster_path[1:]), "wb") as f:
                for chunk in response:
                    f.write(chunk)
