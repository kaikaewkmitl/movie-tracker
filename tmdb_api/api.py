import configparser
import requests

BASE_URL = "api.themoviedb.org"

config = configparser.ConfigParser()
config.read("./tmdb_api/config.ini")

API_KEY = config[BASE_URL]["API_KEY"]


def getTrending():
    res = requests.get(
        f"https://{BASE_URL}/3/trending/all/day?api_key={API_KEY}")
    return res.json()["results"]
