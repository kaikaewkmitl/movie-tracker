from typing import Any, Dict, List

# pages
MAIN_PAGE = "main_page"
MOVIE_INFO_PAGE = "movie_info_page"
SIGNUP_PAGE = "signup_page"
LOGIN_PAGE = "login_page"
USER_LIST_PAGE = "user_list_page"

# tmdb api urls
BASE_URL = "api.themoviedb.org"
BASE_URL_WITH_HTTPS = f"https://{BASE_URL}/3"

# movie keys
MOVIE_TITLE = "movie_title"
MOVIE_OVERVIEW = "overview"
MOVIE_POSTER_PATH = "poster_path"
MOVIE_POSTER_IMG = "poster_img"

POSTERS_DIR = "posters"

# widget names
MY_LIST_BTN = "my_list_btn"
SIGNUP_BTN = "signup_btn"
LOGIN_BTN = "login_btn"
BACK_BTN = "back_btn"
MAIN_MOVIE_LIST = "main_movie_list"
SEARCH_BAR = "search_bar"

SEARCH_BAR_DEFAULT = "Search for movies"

USER = "user"
CURPAGE = "curpage"
TRENDING_MOVIES = "trending_movies"
SEARCH_HISTORY = "search_history"
STORE = {
    USER: {},
    CURPAGE: "",
    TRENDING_MOVIES: [],
    SEARCH_HISTORY: []
}
