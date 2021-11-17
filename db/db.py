import configparser
from psycopg2 import Error, connect
from psycopg2._psycopg import connection
from typing import Dict
import bcrypt

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


def create_movie_type() -> None:
    conn = open_db_connection()
    cur = conn.cursor()

    # have to use try except because
    # TYPE doesn't support IF NOT EXISTS
    try:
        query = f"""CREATE TYPE movie AS(
            {MOVIE_ID} INTEGER,
            {MOVIE_TITLE} VARCHAR
        );"""
        cur.execute(query)
        conn.commit()
        conn.close()
    except:
        print("movie type already exist")


def create_user_table() -> None:
    conn = open_db_connection()
    cur = conn.cursor()

    query = f"""CREATE TABLE IF NOT EXISTS users(
        {USER_ID} SERIAL PRIMARY KEY,
        {USER_USERNAME} VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        {USER_MOVIE_LIST} movie[] DEFAULT """ + "'{}');"
    cur.execute(query)
    conn.commit()
    conn.close()


def init_db() -> None:
    create_movie_type()
    create_user_table()


def insert_new_user(username: str, password: str) -> None:
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = open_db_connection()
    cur = conn.cursor()

    query = "INSERT INTO users (username, password) VALUES (%s, %s);"
    cur.execute(query, (username, hashed_password.decode("utf-8")))
    conn.commit()
    conn.close()


def find_one_user(username: str, password: str) -> Dict[str, None]:
    conn = open_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM users WHERE username= %s LIMIT 1;"
    cur.execute(query, (username,))
    result = cur.fetchone()
    if result == None:
        return {}

    conn.commit()
    conn.close()

    if not bcrypt.checkpw(password.encode("utf-8"), result[2].encode("utf-8")):
        return {}

    user = {
        USER_ID: result[0],
        USER_USERNAME: result[1],
        USER_MOVIE_LIST: result[3]
    }
    return user


def update_movie_list(user_id: int, movie_id: int, movie_title: str):
    conn = open_db_connection()
    cur = conn.cursor()

    query = "UPDATE users SET movie_list = movie_list || %s::movie WHERE id = %s"

    cur.execute(cur.mogrify(query, ((movie_id, movie_title), user_id)))
    conn.commit()
    conn.close()
