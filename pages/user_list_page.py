from tkinter import Frame, Misc, Listbox, Scrollbar, messagebox
from tkinter.constants import LEFT, RIGHT, BOTH, END
from typing import Callable, Optional

from pages.abc_page import Page
from utils.my_widgets import MyHeading, MyMediumFont
from utils.globals import *


class UserListPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str, Optional[int]], None]) -> None:
        super().__init__(parent, change_page_callback)

    def display(self) -> None:
        super().display()

        if len(store.user) > 0:
            username = store.user["username"]
            user_heading = MyHeading(
                self._page, text=f"{username}'s Movie List"
            )
            user_heading.pack()

            print(store.user[USER_MOVIE_LIST])
            movies = store.user[USER_MOVIE_LIST]

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
        else:
            messagebox.showerror(
                "Unauthenticated", "You are unauthenticated, please log in first"
            )

            self._change_page_cb(LOGIN_PAGE)
