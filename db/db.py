import configparser
from psycopg2 import Error, connect
from psycopg2._psycopg import connection
from typing import Tuple, Union

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
        print("connecting to db...")
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

    query = """CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        movie_list INTEGER[] DEFAULT '{}'
    );"""

    cur.execute(query)

    conn.commit()
    conn.close()


def insert_new_user(username: str, password: str) -> None:
    conn = open_db_connection()
    cur = conn.cursor()

    query = "INSERT INTO users (username, password) VALUES (%s, %s);"
    cur.execute(query, (username, password))

    conn.commit()
    conn.close()


def find_one_user(username: str) -> Union[Tuple, None]:
    conn = open_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM users WHERE username=%s LIMIT 1;"
    cur.execute(query, (username,))
    user = cur.fetchone()

    conn.commit()
    conn.close()
    return user
