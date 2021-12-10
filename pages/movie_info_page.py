import os
from tkinter import Label, Misc, Frame, OptionMenu, StringVar, Text, messagebox
from tkinter.constants import DISABLED, END, LEFT, N, NW, W, RIGHT
from PIL import ImageTk, Image
from typing import Any, Callable, Dict, Optional
from db.db import add_movie_to_user_list, update_movie_status

from tmdb_api.api import get_poster
from .abc_page import Page
from utils.my_widgets import MyBigFont, MyButton, MyHeading, MyListbox, MyMediumFont, MySmallFont
from utils.globals import *


class MovieInfoPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        super().__init__(parent, change_page_callback)
        self.movie: Dict[str, Any] = {}
        self.movie[MOVIE_POSTER_IMG] = None
        self.movie[MOVIE_TITLE] = ""
        self.movie[MOVIE_OVERVIEW] = ""

    def display(self) -> None:
        super().display()

        movie_title = MyHeading(
            self.page, text=f"{self.movie[MOVIE_TITLE]}"
        )
        movie_title.pack()

        overview_container = Frame(self.page, bg=store.theme[BG])
        overview_container.pack(side=RIGHT)

        overview_heading = MyHeading(
            overview_container, font=MyMediumFont(), text="Overview"
        )
        overview_heading.pack(padx=20, anchor=W)

        overview = Text(
            overview_container,
            width=50,
            height=10,
            font=MySmallFont(),
            wrap="word",
            fg=store.theme[FG],
            bg=store.theme[BG],
            highlightthickness=1,
            borderwidth=1,
            highlightbackground=store.theme[FG],
            highlightcolor=store.theme[FG]
        )
        overview.insert(END, f"\t{self.movie[MOVIE_OVERVIEW]}")
        overview.config(state=DISABLED)
        overview.pack(padx=20)

        others_container = Frame(overview_container, bg=store.theme[BG])
        others_container.pack(padx=20, side=LEFT)

        movie_genres_id = self.movie[MOVIE_GENRE_IDS]

        genre_heading = MyHeading(
            others_container, font=MyMediumFont(), text="Genres"
        )
        genre_heading.grid(row=0, column=0, sticky=W)

        genres = MyListbox(
            others_container,
            font=MySmallFont(),
            height=6,
            width=19
        )
        genres.grid(row=1, column=0, sticky=NW)

        for genre in movie_genres_id:
            genres.insert(END, store.genre_dict[genre])

        others_heading = MyHeading(
            others_container,
            font=MyMediumFont(),
            text="Other Info"
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
                      f"Original Language: {self.movie[MOVIE_LANGUAGE]}",
                      "",
                      f"Release Date: {self.movie[MOVIE_RELEASE_DATE]}",
                      "",
                      f"Rating: {self.movie[MOVIE_RATING]}"
                      )

        poster_container = Frame(self.page, bg=store.theme[BG])
        poster_container.pack(side=LEFT, padx=20, pady=15, anchor=N)

        poster: Label
        if self.movie[MOVIE_POSTER_IMG] != None:
            poster = Label(
                poster_container,
                image=self.movie[MOVIE_POSTER_IMG], borderwidth=0
            )
        else:
            poster = Label(
                poster_container,
                text="No Poster",
                font=MyBigFont(),
                fg=ORANGE,
                bg=store.theme[BG],
                height=6
            )
        poster.pack(padx=20, pady=20)

        add_to_list_container = Frame(poster_container, bg=store.theme[BG])
        add_to_list_container.pack()

        movie = self.find_in_user_list()

        if len(movie) == 0:
            add_to_list_heading = MyHeading(
                add_to_list_container,
                font=MyMediumFont(),
                text="Add To My List"
            )
            add_to_list_heading.pack(pady=5)

            watched_btn = MyButton(
                add_to_list_container,
                text="Watched",
                command=lambda: self.add_to_list(STATUS_WATCHED)
            )
            watched_btn.pack(pady=5)

            will_watch_btn = MyButton(
                add_to_list_container,
                text="Will Watch",
                command=lambda: self.add_to_list(STATUS_WILL_WATCH)
            )
            will_watch_btn.pack(pady=0)
        else:
            self.movie[MOVIE_STATUS] = movie[MOVIE_STATUS]

            status = StringVar(
                add_to_list_container,
                "Watched" if movie[MOVIE_STATUS] == STATUS_WATCHED else "Will Watch"
            )

            watch_status = MyHeading(
                add_to_list_container,
                font=MyMediumFont(),
                text="Status: "
            )
            watch_status.pack(pady=5, side=LEFT)

            watch_status_option = OptionMenu(
                add_to_list_container,
                status,
                "Watched",
                "Will Watch",
                command=self.dropdown_handler,
            )
            watch_status_option.pack(pady=5, side=LEFT)
            watch_status_option.config(
                font=MySmallFont(), background=store.theme[BG],
                fg=store.theme[FG], activeforeground=store.theme[FG]
            )

    def set_movie_and_display(self, movie: Dict[str, Any]) -> None:
        self.movie = movie
        if MOVIE_POSTER_PATH in self.movie and self.movie[MOVIE_POSTER_PATH] != None:
            path = os.path.join(
                POSTERS_DIR, self.movie[MOVIE_POSTER_PATH][1:]
            )
            if not os.path.exists(path):
                get_poster(movie[MOVIE_POSTER_PATH])

            self.movie[MOVIE_POSTER_IMG] = ImageTk.PhotoImage(
                Image.open(path)
            )
        else:
            self.movie[MOVIE_POSTER_IMG] = None

        self.set_on_display(True)

    def add_to_list(self, status: str) -> None:
        if len(store.user) > 0:
            user = add_movie_to_user_list(self.movie, status)
            store.user = user
            messagebox.showinfo(
                "Updated User List", f"You've added {self.movie[MOVIE_TITLE]} to your list"
            )
            self.page.focus()
            self.change_page_cb(MOVIE_INFO_PAGE, self.movie)
        else:
            messagebox.showerror(
                "Unauthenticated", "You are unauthenticated, please log in first"
            )
            self.page.focus()
            self.change_page_cb(LOGIN_PAGE)

    def find_in_user_list(self) -> Dict[str, Any]:
        if len(store.user) == 0:
            return {}

        for m in store.user[USER_MOVIE_LIST]:
            if self.movie[MOVIE_ID] == m[MOVIE_ID]:
                return m

        return {}

    def dropdown_handler(self, status: str):
        status_dict: Dict[str, str] = {
            "Watched": STATUS_WATCHED,
            "Will Watch":  STATUS_WILL_WATCH
        }

        if status_dict[status] != self.movie[MOVIE_STATUS]:
            user = update_movie_status(
                self.movie, status_dict[status]
            )
            store.user = user
            messagebox.showinfo(
                "Updated User List", f"You've updated {self.movie[MOVIE_TITLE]}'s watch status"
            )
            self.page.focus()
            self.change_page_cb(MOVIE_INFO_PAGE, self.movie)

    def get_movie(self):
        return self.movie
