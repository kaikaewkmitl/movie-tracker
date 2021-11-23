import os
from tkinter import Label, Misc, Frame, Text, messagebox
from tkinter.constants import DISABLED, END, LEFT, N, NW, W, RIGHT
from PIL import ImageTk, Image
from typing import Any, Callable, Dict, Optional
from db.db import add_movie_to_user_list

from tmdb_api.api import get_poster
from .abc_page import Page
from utils.my_widgets import MyBigFont, MyButton, MyHeading, MyListbox, MyMediumFont, MySmallFont
from utils.globals import *


class MovieInfoPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        super().__init__(parent, change_page_callback)
        self.__movie: Dict[str, Any] = {}
        self.__movie[MOVIE_POSTER_IMG] = None
        self.__movie[MOVIE_TITLE] = ""
        self.__movie[MOVIE_OVERVIEW] = ""

    def display(self) -> None:
        super().display()

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
                        wrap="word",
                        fg="black",
                        bg="white"
                        )
        overview.insert(END, f"\t{self.__movie[MOVIE_OVERVIEW]}")
        overview.config(state=DISABLED)
        overview.pack(padx=20)

        others_container = Frame(overview_container)
        others_container.pack(padx=20, side=LEFT)

        movie_genres_id = self.__movie[MOVIE_GENRE_IDS]
        # if MOVIE_GENRES in self.__movie:
        #     movie_genres = self.__movie[MOVIE_GENRES]

        genre_heading = MyHeading(
            others_container, font=MyMediumFont(), text="Genres"
        )
        genre_heading.grid(row=0, column=0, sticky=W)

        genres = MyListbox(
            others_container,
            font=MySmallFont(),
            height=len(movie_genres_id),
            width=19
        )
        genres.grid(row=1, column=0, sticky=NW)

        for genre in movie_genres_id:
            genres.insert(END, store.genre_dict[genre])

        others_heading = MyHeading(
            others_container, font=MyMediumFont(), text="Other Info"
        )
        others_heading.grid(row=0, column=1, padx=10, sticky=W)

        others = MyListbox(
            others_container,
            font=MySmallFont(),
            height=6,
            width=30
        )
        others.grid(row=1, column=1, padx=10, sticky=NW)
        others.insert(END,
                      f"Original Language: {self.__movie[MOVIE_LANGUAGE]}",
                      "",
                      f"Release Date: {self.__movie[MOVIE_RELEASE_DATE]}",
                      "",
                      f"Rating: {self.__movie[MOVIE_RATING]}"
                      )

        poster_container = Frame(self._page)
        poster_container.pack(side=LEFT, padx=20, pady=15, anchor=N)

        poster: Label
        if self.__movie[MOVIE_POSTER_IMG] != None:
            poster = Label(poster_container,
                           image=self.__movie[MOVIE_POSTER_IMG], borderwidth=0
                           )
        else:
            poster = Label(poster_container,
                           text="No Poster",
                           font=MyBigFont(),
                           fg="orange",
                           height=6
                           )
        poster.pack(padx=20, pady=20)

        if not self.is_in_user_list():
            add_to_list_btn = MyButton(
                poster_container,
                text="Add To My List",
                font=MyMediumFont(),
                command=self.add_to_list
            )
            add_to_list_btn.pack()

    def set_movie_and_display(self, movie: Dict[str, Any]) -> None:
        self.__movie = movie
        if MOVIE_POSTER_PATH in self.__movie and self.__movie[MOVIE_POSTER_PATH] != None:
            path = os.path.join(
                POSTERS_DIR, self.__movie[MOVIE_POSTER_PATH][1:]
            )
            if not os.path.exists(path):
                get_poster(movie[MOVIE_POSTER_PATH])

            self.__movie[MOVIE_POSTER_IMG] = ImageTk.PhotoImage(
                Image.open(path)
            )
        else:
            self.__movie[MOVIE_POSTER_IMG] = None

        self.set_on_display(True)

    def add_to_list(self) -> None:
        if len(store.user) > 0:
            user = add_movie_to_user_list(self.__movie)
            store.user = user
            messagebox.showinfo(
                "Updated User List", f"You've added {self.__movie[MOVIE_TITLE]} to your list"
            )
            self._page.focus()
            self._change_page_cb(MOVIE_INFO_PAGE, self.__movie)
        else:
            messagebox.showerror(
                "Unauthenticated", "You are unauthenticated, please log in first"
            )
            self._page.focus()
            self._change_page_cb(LOGIN_PAGE)

    def is_in_user_list(self):
        if len(store.user) == 0:
            return False

        for m in store.user[USER_MOVIE_LIST]:
            if self.__movie[MOVIE_ID] == m[MOVIE_ID]:
                return True

        return False
