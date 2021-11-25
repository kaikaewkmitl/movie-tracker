from tkinter import Frame, Label, Misc, OptionMenu, Scrollbar, StringVar, messagebox
from tkinter.constants import LEFT, RIGHT, BOTH, END, X
from copy import deepcopy
from typing import Callable, Optional

from pages.abc_page import Page
from utils.my_widgets import MyButton, MyHeading, MyListbox, MyMediumFont, MySmallFont
from utils.globals import *

LAST_ADDED = "Last Added"
ALPHABETICAL = "Alphabetical"
RATING = "Rating"

ALL_MOVIE = "All Movie"


class UserListPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str, Optional[Dict[str, Any]]], None]) -> None:
        super().__init__(parent, change_page_callback)

        self.__cur_sort_option = LAST_ADDED
        self.__cur_status = ALL_MOVIE
        self.__movies: List[Dict[str, Any]] = []

    def display(self) -> None:
        super().display()

        if len(store.user) > 0:
            if len(self.__movies) == 0:
                self.__movies = deepcopy(store.user[USER_MOVIE_LIST])

            if len(self.__movies) == 0:
                padder = Label(
                    self._page
                )
                padder.pack(pady=100)

                empty_list_heading = MyHeading(
                    self._page, text="Your list is empty..."
                )
                empty_list_heading.pack()

                message = MyHeading(
                    self._page, text="Come back again later",
                    font=MyMediumFont()
                )
                message.pack()
            else:
                username = store.user[USER_USERNAME]
                user_heading = MyHeading(
                    self._page, text=f"{username}'s Movie List"
                )
                user_heading.pack()

                movie_status_btn_container = Frame(self._page)
                movie_status_btn_container.pack()

                self.__btns: Dict[str, MyButton] = {
                    ALL_MOVIE: MyButton(
                        movie_status_btn_container, text=ALL_MOVIE,
                        command=lambda: self.set_cur_status(ALL_MOVIE)
                    ),
                    STATUS_WATCHED: MyButton(
                        movie_status_btn_container, text="Watched",
                        command=lambda: self.set_cur_status(STATUS_WATCHED)
                    ),
                    STATUS_WILL_WATCH: MyButton(
                        movie_status_btn_container, text="Will Watch",
                        command=lambda: self.set_cur_status(STATUS_WILL_WATCH)
                    )
                }
                self.focus_btn()

                for btn in self.__btns.values():
                    btn.pack(side=LEFT)

                sort_option_container = Frame(self._page)
                sort_option_container.pack(pady=10, padx=200, fill=X)

                sort_option = StringVar(
                    sort_option_container, self.__cur_sort_option
                )

                sort_option_dropdown = OptionMenu(
                    sort_option_container, sort_option,
                    LAST_ADDED, ALPHABETICAL, RATING,
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

                movie_list = MyListbox(movie_list_container,
                                       width=30,
                                       height=15,
                                       )

                movie_list.bind("<Double-Button-1>",
                                lambda _: self._change_page_cb(
                                    MOVIE_INFO_PAGE,
                                    self.__movies[movie_list.curselection()[0]]
                                ))
                movie_list.pack(side=LEFT)

                for movie in self.__movies:
                    if self.__cur_status == ALL_MOVIE:
                        movie_list.insert(
                            END, movie[MOVIE_TITLE]
                        )
                    elif self.__cur_status == STATUS_WATCHED and movie[MOVIE_STATUS] == STATUS_WATCHED:
                        movie_list.insert(
                            END, movie[MOVIE_TITLE]
                        )
                    elif self.__cur_status == STATUS_WILL_WATCH and movie[MOVIE_STATUS] == STATUS_WILL_WATCH:
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

    def dropdown_handler(self, option: str) -> None:
        if option == LAST_ADDED and self.__cur_sort_option != LAST_ADDED:
            self.__movies = deepcopy(
                store.user[USER_MOVIE_LIST]
            )
            self.__cur_sort_option = LAST_ADDED
        elif option == ALPHABETICAL and self.__cur_sort_option != ALPHABETICAL:
            self.__movies.sort(key=lambda m: m[MOVIE_TITLE])
            self.__cur_sort_option = ALPHABETICAL
        elif option == RATING and self.__cur_sort_option != RATING:
            self.__movies.sort(
                key=lambda m: m[MOVIE_RATING], reverse=True
            )
            self.__cur_sort_option = RATING

        self._change_page_cb(USER_LIST_PAGE)

    def focus_btn(self) -> None:
        for k, v in self.__btns.items():
            if self.__cur_status == k:
                v.config(fg="orange")
            else:
                v.config(fg="black")

    def set_cur_status(self, status: str) -> None:
        self.__cur_status = status
        self._change_page_cb(USER_LIST_PAGE)
