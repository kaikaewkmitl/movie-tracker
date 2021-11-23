from tkinter import Label, Misc, Frame, Entry, Scrollbar
from tkinter.constants import BOTH, LEFT, END, RIGHT
from typing import Callable, Dict, Any, Optional

from tmdb_api.api import get_movie_by_name
from .abc_page import Page
from utils.my_widgets import MyHeading, MyListbox, MyMediumFont
from utils.globals import *

SEARCH_BAR_DEFAULT = "Search for movies"


class MainPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        super().__init__(parent, change_page_callback)

    def display(self) -> None:
        super().display()

        appName = MyHeading(self._page, text="Movie Tracker")
        appName.pack()

        searchbar = Entry(self._page,
                          bg="white",
                          fg="black",
                          width=30,
                          font=MyMediumFont(),
                          insertbackground="black",
                          )
        searchbar.insert(0, SEARCH_BAR_DEFAULT)
        searchbar.bind("<FocusIn>",
                       lambda _: searchbar.get() == SEARCH_BAR_DEFAULT and searchbar.delete(0, END)
                       )
        searchbar.bind("<FocusOut>",
                       lambda _:  len(searchbar.get()) == 0 and searchbar.insert(
                           0, SEARCH_BAR_DEFAULT)
                       )
        searchbar.bind("<Return>",
                       lambda _: self.search_movie(searchbar.get())
                       )
        searchbar.pack(pady=20)

        search_result = store.search_history[-1][0]
        text = "Trending Movies"
        if search_result != "":
            text = f"Search Result: {search_result}"
        movie_list_heading = MyHeading(self._page, text=text)
        movie_list_heading.pack()

        movie_list_container = Frame(self._page)
        movie_list_container.pack(pady=20)

        movies = store.search_history[-1][1]
        if len(movies) == 0:
            no_result = Label(movie_list_container,
                              text="No Movie Found...\nPlease try some other keywords",
                              font=MyMediumFont()
                              )
            no_result.pack()
        else:
            movie_list = MyListbox(movie_list_container,
                                   width=30,
                                   height=15,
                                   )
            # movie_list.bind("<<ListboxSelect>>", lambda e: print(
            #     movie_list.curselection()[0])
            # )
            movie_list.bind("<Double-Button-1>",
                            lambda _: self._change_page_cb(
                                MOVIE_INFO_PAGE,
                                movies[movie_list.curselection()[0]]
                            ))
            movie_list.pack(side=LEFT)

            for movie in movies:
                movie_list.insert(
                    END, movie[MOVIE_TITLE]
                )

            scrollbar = Scrollbar(movie_list_container)
            scrollbar.pack(side=RIGHT, fill=BOTH)

            movie_list.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=movie_list.yview)

    def search_movie(self, movie_name: str) -> None:
        if movie_name == "" or movie_name == SEARCH_BAR_DEFAULT:
            return

        # encode the movie_name
        movie_name_encoded = "%20".join(movie_name.split())
        searched_movies = get_movie_by_name(movie_name_encoded)
        store.search_history.append((movie_name, searched_movies))
        self._change_page_cb(MAIN_PAGE)
