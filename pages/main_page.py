from tkinter import Misc, Frame, Entry, Listbox, Scrollbar
from tkinter.constants import BOTH, LEFT, END, RIGHT
from typing import Callable, List, Dict, Any, Optional

from tmdb_api.api import get_movie_by_name
from utils.my_widgets import MyHeading, MyMediumFont
from utils.const import *
from .abc_page import Page


class MainPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str, Optional[int]], None],
                 trending_movies: List[Dict[str, Any]]) -> None:
        super().__init__(parent, change_page_callback)
        self.__trending_movies = trending_movies
        self.display()

    def display(self) -> None:
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
                       lambda _: self.search(searchbar.get())
                       )
        searchbar.pack(pady=20)

        trending_list_heading = MyHeading(self._page, text="Trending Movies")
        trending_list_heading.pack()

        trending_list_container = Frame(self._page)
        trending_list_container.pack(pady=20)

        trending_list = Listbox(trending_list_container,
                                font=MyMediumFont(),
                                width=30,
                                height=15,
                                bg="white",
                                fg="blue",
                                bd=0,
                                highlightthickness=0,
                                selectbackground="gray",
                                selectforeground="orange",
                                activestyle="dotbox"
                                )
        # trending_list.bind("<<ListboxSelect>>", lambda e: print(
        #     trending_list.curselection()[0])
        # )
        trending_list.bind("<Double-Button-1>",
                           lambda _: self._change_page_cb(
                               MOVIE_INFO_PAGE, trending_list.curselection()[0]
                           ))
        trending_list.pack(side=LEFT)

        for movie in self.__trending_movies:
            trending_list.insert(
                END, movie[MOVIE_TITLE]
            )

        scrollbar = Scrollbar(trending_list_container)
        scrollbar.pack(side=RIGHT, fill=BOTH)

        trending_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=trending_list.yview)

    def search(self, movie_name: str) -> None:
        if movie_name == "" or movie_name == SEARCH_BAR_DEFAULT:
            return

        movie_name = "%20".join(movie_name.split())
        searched_movies = get_movie_by_name(movie_name)
        for movie in searched_movies:
            movie[MOVIE_TITLE] = movie["title"] if "title" in movie else movie["name"]
            print(movie[MOVIE_TITLE])
