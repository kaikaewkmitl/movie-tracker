import os
from tkinter import Label, Misc, Frame, Text
from tkinter.constants import DISABLED, END, LEFT, N, W, RIGHT
from PIL import ImageTk, Image
from typing import Any, Callable, Dict, Optional

from tmdb_api.api import get_poster
from .abc_page import Page
from utils.my_widgets import MyHeading, MyMediumFont, MySmallFont
from utils.const import *


class MovieInfoPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str, Optional[int]], None]) -> None:
        super().__init__(parent, change_page_callback)
        self.__movie: Dict[str, Any] = {}
        self.__movie[MOVIE_POSTER_IMG] = None
        self.__movie[MOVIE_TITLE] = ""
        self.__movie[MOVIE_OVERVIEW] = ""
        self.display()

    def display(self) -> None:
        movie_title = MyHeading(
            self._page, text=f"{self.__movie[MOVIE_TITLE]}"
        )
        movie_title.pack()

        overview_container = Frame(self._page)
        overview_container.pack(side=RIGHT)

        overview_heading = MyHeading(
            overview_container, font=MyMediumFont(), text="Overview"
        )
        overview_heading.pack(padx=20, anchor=W)

        overview = Text(overview_container,
                        width=50,
                        height=10,
                        font=MySmallFont(),
                        wrap="word"
                        )
        overview.insert(END, f"\t{self.__movie[MOVIE_OVERVIEW]}")
        overview.config(state=DISABLED)
        overview.pack(padx=20)

        poster_container = Frame(self._page)
        poster_container.pack(side=LEFT, padx=20, pady=15, anchor=N)

        poster = Label(poster_container,
                       image=self.__movie[MOVIE_POSTER_IMG], borderwidth=0)
        poster.pack(padx=20, pady=20)

    def set_movie_and_display(self, movie: Dict[str, Any]) -> None:
        for widget in self._page.winfo_children():
            widget.destroy()

        self.__movie = movie
        get_poster(movie[MOVIE_POSTER_PATH])
        path = os.path.join(POSTERS_DIR, self.__movie[MOVIE_POSTER_PATH][1:])
        self.__movie[MOVIE_POSTER_IMG] = ImageTk.PhotoImage(Image.open(path))
        self.display()
        self.set_on_display(True)
