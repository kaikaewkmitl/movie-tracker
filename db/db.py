import configparser
from copy import deepcopy
from psycopg2 import Error, connect
from psycopg2._psycopg import connection
from typing import Dict
import bcrypt
from tmdb_api.api import get_movie_by_id

from utils.globals import *

config = configparser.ConfigParser()
config.read("config.ini")

HEROKU_POSTGRES = "heroku postgres"
HOST = config[HEROKU_POSTGRES]["HOST"]
DATABASE = config[HEROKU_POSTGRES]["DATABASE"]
USER = config[HEROKU_POSTGRES]["USER"]
PORT = config[HEROKU_POSTGRES]["PORT"]
PASSWORD = config[HEROKU_POSTGRES]["PASSWORD"]


def open_db_connection() -> connection:
    try:
        return connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            port=PORT,
            password=PASSWORD,
            sslmode="require"
        )
    except (Exception, Error) as err:
        print("DB Error:", err)


def create_user_table() -> None:
    conn = open_db_connection()
    cur = conn.cursor()

    query = f"""CREATE TABLE IF NOT EXISTS users(
        {USER_ID} SERIAL PRIMARY KEY,
        {USER_USERNAME} VARCHAR NOT NULL,
        {USER_PASSWORD} VARCHAR NOT NULL,
        {USER_MOVIE_LIST} INTEGER[] DEFAULT """ + "'{}');"
    cur.execute(query)
    conn.commit()
    conn.close()


def init_db() -> None:
    create_user_table()


def get_user(username: str) -> Dict[str, Any]:
    conn = open_db_connection()
    cur = conn.cursor()

    query = f"SELECT * FROM users WHERE {USER_USERNAME} = %s LIMIT 1;"
    cur.execute(query, (username,))
    result = cur.fetchone()
    if result == None:
        return {}

    conn.commit()
    conn.close()

    movie_list: List[Dict[str, Any]] = []
    for id in result[3]:
        movie_list.append(get_movie_by_id(id))

    user = {
        USER_ID: result[0],
        USER_USERNAME: result[1],
        USER_PASSWORD: result[2],
        USER_MOVIE_LIST: movie_list,
        USER_MOVIE_LIST_ORIGINAL: deepcopy(movie_list)
    }
    return user


def insert_new_user(username: str, password: str) -> None:
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = open_db_connection()
    cur = conn.cursor()

    query = f"INSERT INTO users ({USER_USERNAME}, {USER_PASSWORD}) VALUES (%s, %s);"
    cur.execute(query, (username, hashed_password.decode("utf-8")))
    conn.commit()
    conn.close()


def authenticate_user(username: str, password: str) -> Dict[str, None]:
    user = get_user(username)
    if len(user) == 0:
        return {}

    if not bcrypt.checkpw(password.encode("utf-8"), user[USER_PASSWORD].encode("utf-8")):
        return {}

    user.pop(USER_PASSWORD, None)
    return user


def add_movie_to_user_list(movie: Dict[str, Any]) -> Dict[str, Any]:
    conn = open_db_connection()
    cur = conn.cursor()

    query = f"UPDATE users SET {USER_MOVIE_LIST} = {USER_MOVIE_LIST} || %s WHERE {USER_ID} = %s"

    cur.execute(query, (movie[MOVIE_ID], store.user[USER_ID]))
    conn.commit()
    conn.close()

    user = get_user(store.user[USER_USERNAME])
    user.pop(USER_PASSWORD, None)
    return user
