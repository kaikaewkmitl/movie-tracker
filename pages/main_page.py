from tkinter import Label, Misc, Frame, Entry, Listbox, Scrollbar
from tkinter.constants import BOTH, LEFT, END, RIGHT
from typing import Callable, List, Dict, Any, Optional

from tmdb_api.api import get_movie_by_name
from utils.my_widgets import MyHeading, MyMediumFont
from utils.const import *
from .abc_page import Page


class MainPage(Page):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, str, Optional[int]], None]) -> None:
        super().__init__(parent, change_page_callback)
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
                       lambda _: self.search_movie(searchbar.get())
                       )
        searchbar.pack(pady=20)

        text = "Trending Movies"
        if STORE[SEARCH_HISTORY][-1][0] != "":
            text = f"Search Result: {STORE[SEARCH_HISTORY][-1][0]}"
        movie_list_heading = MyHeading(self._page, text=text)
        movie_list_heading.pack()

        movie_list_container = Frame(self._page)
        movie_list_container.pack(pady=20)

        if len(STORE[SEARCH_HISTORY][-1][1]) == 0:
            no_result = Label(movie_list_container,
                              text="No Movie Found...\nPlease try some other keywords",
                              font=MyMediumFont()
                              )
            no_result.pack()
        else:
            movie_list = Listbox(movie_list_container,
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
            # movie_list.bind("<<ListboxSelect>>", lambda e: print(
            #     movie_list.curselection()[0])
            # )
            movie_list.bind("<Double-Button-1>",
                            lambda _: self._change_page_cb(
                                MAIN_MOVIE_LIST,
                                MOVIE_INFO_PAGE,
                                STORE[SEARCH_HISTORY][-1][1]
                                [movie_list.curselection()[0]]
                            ))
            movie_list.pack(side=LEFT)

            for movie in STORE[SEARCH_HISTORY][-1][1]:
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
        movie_name = "%20".join(movie_name.split())
        searched_movies = get_movie_by_name(movie_name)
        for movie in searched_movies:
            movie[MOVIE_TITLE] = movie["title"] if "title" in movie else movie["name"]

        STORE[SEARCH_HISTORY].append((movie_name, searched_movies))
        for widget in self._page.winfo_children():
            widget.destroy()

        self._change_page_cb(SEARCH_BAR, MAIN_PAGE)
