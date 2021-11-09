from tkinter import Label, Misc, Frame, Text
from tkinter.constants import BOTH, END, LEFT, N, RIGHT
from PIL import ImageTk, Image
from typing import Any, Callable, Dict

from tmdb_api.api import get_poster
from .abc_page import Page
from utils.my_widgets import MyHeading, MyMediumFont, MySmallFont
from utils.const import *


class MovieInfoPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str], None]) -> None:
        super().__init__(False, parent, change_page_callback)
        self.__movie: Dict[str, Any] = {}

    def display(self) -> None:
        page = self.get_page()

        movie_title = MyHeading(page, text=f"{self.__movie[MOVIE_TITLE]}")
        movie_title.pack()

        overview_container = Frame(page)
        overview_container.pack(side=RIGHT)

        overview_heading = MyHeading(
            overview_container, font=MyMediumFont(), text="Overview"
        )
        overview_heading.pack()

        overview = Text(overview_container,
                        width=50,
                        font=MySmallFont(),
                        wrap="word"
                        )
        overview.insert(END, self.__movie[MOVIE_OVERVIEW])
        overview.pack(padx=20)

        poster_container = Frame(page)
        poster_container.pack(side=LEFT, padx=20, pady=15, anchor=N)

        poster = Label(poster_container,
                       image=self.__movie[MOVIE_POSTER_IMG], borderwidth=0)
        poster.pack(padx=20, pady=20)

    def set_movie_and_display(self, movie: Dict[str, Any]) -> None:
        self.__movie = movie
        get_poster(movie[MOVIE_POSTER_PATH])
        path = os.path.join(POSTERS_DIR, self.__movie[MOVIE_POSTER_PATH][1:])
        self.__movie[MOVIE_POSTER_IMG] = ImageTk.PhotoImage(Image.open(path))
        self.set_on_display(True)
