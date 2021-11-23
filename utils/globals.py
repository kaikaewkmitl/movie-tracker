from typing import Any, Dict, List, Tuple

# pages
MAIN_PAGE = "main_page"
MOVIE_INFO_PAGE = "movie_info_page"
SIGNUP_PAGE = "signup_page"
LOGIN_PAGE = "login_page"
USER_LIST_PAGE = "user_list_page"

# movie keys
MOVIE_ID = "id"
MOVIE_TITLE = "movie_title"
MOVIE_OVERVIEW = "overview"
MOVIE_POSTER_PATH = "poster_path"
MOVIE_POSTER_IMG = "poster_img"
MOVIE_RATING = "vote_average"

POSTERS_DIR = "posters"

# widget names
USER_LIST_BTN = "user_list_btn"
SIGNUP_BTN = "signup_btn"
LOGIN_BTN = "login_btn"
BACK_BTN = "back_btn"
WELCOME_USER = "welcome_user"

# validations
WITHIN_MIN_LEN = "min_len"
WITHIN_MAX_LEN = "max_len"
IS_ALNUM = "is_alnum"
IS_FOUND = "is_found"
IS_MATCH = "is_match"

# store.user keys
USER_ID = "id"
USER_USERNAME = "username"
USER_PASSWORD = "password"
USER_MOVIE_LIST = "movie_list"
USER_MOVIE_LIST_ORIGINAL = "user_movie_list_original"


class Store:
    def __init__(self) -> None:
        self.user: Dict[str, Any] = {}
        self.curpage: str = ""
        self.trending_movies: List[Dict[str, Any]] = []
        self.search_history: List[Tuple[str, List[Dict[str, Any]]]] = []

    def init_store(self, trending_movies: List[Dict[str, Any]]) -> None:
        self.curpage = MAIN_PAGE
        self.trending_movies = trending_movies
        self.search_history.append(("", trending_movies))


store = Store()
