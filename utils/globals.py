from typing import Any, Dict, List, Tuple

# theme
FG = "fg"
BG = "bg"
WHITE = "#FFF"
BLACK = "#000"
LIGHT_THEME_BG = WHITE
LIGHT_THEME_FG = BLACK
DARK_THEME_BG = "#2D1530"
DARK_THEME_FG = WHITE
ORANGE = "#F8795D"

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
MOVIE_GENRE_IDS = "genre_ids"
MOVIE_GENRES = "genres"
MOVIE_LANGUAGE = "original_language"
MOVIE_RELEASE_DATE = "release_date"
MOVIE_STATUS = "movie_status"

# user's movie status
STATUS_WATCHED = "watched"
STATUS_WILL_WATCH = "will_watch"

# directories
POSTERS_DIR = "posters"
IMAGES_DIR = "images"

# navbar widget's names
USER_LIST_BTN = "user_list_btn"
SIGNUP_BTN = "signup_btn"
LOGIN_BTN = "login_btn"
LOGOUT_BTN = "logout_btn"
BACK_BTN = "back_btn"
WELCOME_USER = "welcome_user"

# user authentication validations
WITHIN_MIN_LEN = "min_len"
WITHIN_MAX_LEN = "max_len"
IS_ALNUM = "is_alnum"

# store.user keys
USER_ID = "id"
USER_USERNAME = "username"
USER_PASSWORD = "password"
USER_MOVIE_LIST = "movie_list"


class Store:
    def __init__(self) -> None:
        self.user: Dict[str, Any] = {}
        self.curpage: str = ""
        self.search_history: List[Tuple[str, List[Dict[str, Any]]]] = []
        self.genre_dict: Dict[int, str] = {}
        self.theme: Dict[str, str] = {}

    def init_store(self, trending_movies: List[Dict[str, Any]],
                   genre_dict: List[Dict[str, Any]]) -> None:
        self.curpage = MAIN_PAGE
        self.theme = {
            FG: LIGHT_THEME_FG,
            BG: LIGHT_THEME_BG
        }
        self.search_history.append(("", trending_movies))
        for genre in genre_dict:
            self.genre_dict[genre["id"]] = genre["name"]


store = Store()
