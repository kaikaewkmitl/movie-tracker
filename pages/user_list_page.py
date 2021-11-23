from tkinter import Frame, Misc, Listbox, OptionMenu, Scrollbar, StringVar, messagebox
from tkinter.constants import LEFT, RIGHT, BOTH, END, X
from copy import deepcopy
from typing import Callable, Optional

from pages.abc_page import Page
from tmdb_api.api import get_movie_by_id
from utils.my_widgets import MyHeading, MyMediumFont, MySmallFont
from utils.globals import *

LAST_ADDED = "Last Added"
ALPHABETICAL = "Alphabetical"

cur_sort_option = LAST_ADDED


class UserListPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        super().__init__(parent, change_page_callback)

    def display(self) -> None:
        super().display()

        if len(store.user) > 0:
            username = store.user[USER_USERNAME]
            user_heading = MyHeading(
                self._page, text=f"{username}'s Movie List"
            )
            user_heading.pack()

            sort_option_container = Frame(self._page)
            sort_option_container.pack(pady=10, padx=200, fill=X)

            sort_option = StringVar(sort_option_container, cur_sort_option)

            sort_option_dropdown = OptionMenu(
                sort_option_container, sort_option,
                LAST_ADDED, ALPHABETICAL,
                command=self.dropdown_handler
            )
            sort_option_dropdown.pack(side=RIGHT)
            sort_option_dropdown.config(font=MySmallFont())

            sort_option_heading = MyHeading(
                sort_option_container,
                text="Sort By: ", font=MySmallFont()
            )
            sort_option_heading.pack(side=RIGHT, padx=10)

            movie_list_container = Frame(self._page)
            movie_list_container.pack(pady=20)

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
            # movie_list.bind("<Double-Button-1>",
            #                 lambda _: self._change_page_cb(
            #                     MOVIE_INFO_PAGE,
            #                     movies[movie_list.curselection()[0]]
            #                 ))
            movie_list.bind("<Double-Button-1>",
                            lambda _: self._change_page_cb(
                                MOVIE_INFO_PAGE,
                                store.user[USER_MOVIE_LIST]
                                [movie_list.curselection()[0]]
                            ))
            movie_list.pack(side=LEFT)

            for movie in store.user[USER_MOVIE_LIST]:
                movie_list.insert(
                    END, movie[MOVIE_TITLE]
                )

            scrollbar = Scrollbar(movie_list_container)
            scrollbar.pack(side=RIGHT, fill=BOTH)

            movie_list.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=movie_list.yview)
        else:
            messagebox.showerror(
                "Unauthenticated", "You are unauthenticated, please log in first"
            )
            self._page.focus()
            self._change_page_cb(LOGIN_PAGE)

    def dropdown_handler(self, option):
        global cur_sort_option
        if option == LAST_ADDED and cur_sort_option != LAST_ADDED:
            store.user[USER_MOVIE_LIST] = deepcopy(
                store.user[USER_MOVIE_LIST_ORIGINAL]
            )
            cur_sort_option = LAST_ADDED
            self._change_page_cb(USER_LIST_PAGE)
        elif option == ALPHABETICAL and cur_sort_option != ALPHABETICAL:
            store.user[USER_MOVIE_LIST].sort(key=lambda m: m[MOVIE_TITLE])
            cur_sort_option = ALPHABETICAL
            self._change_page_cb(USER_LIST_PAGE)
