import configparser

BASE_URL = "api.themoviedb.org"

config = configparser.ConfigParser()
config.read("./tmdb_api/config.ini")


def p():
    print(config[BASE_URL]["API_KEY"])
