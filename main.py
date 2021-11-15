from tkinter import Tk
import os
import shutil
import signal
from typing import Any, Dict, cast

from tmdb_api.api import get_trending
from pages.abc_page import Page
from pages.main_page import MainPage
from pages.movie_info_page import MovieInfoPage
from pages.signup_page import SignupPage
from pages.login_page import LoginPage
from pages.user_list_page import UserListPage
from utils.my_widgets import MyNavbar
from utils.globals import *


class App:
    def __init__(self) -> None:
        print("creating an app...")
        self.__root = Tk()
        self.__root.title("Movie Tracker")
        self.__root.geometry("800x700")

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.__root.after(50, self.check)

        self.__navbar = MyNavbar(self.__root, self.change_page_callback)
        self.__navbar.pack()
        self.__navbar.remove_btn(BACK_BTN)

        self.__pages: Dict[str, Page] = {
            MAIN_PAGE: MainPage(
                self.__root, self.change_page_callback
            ),
            MOVIE_INFO_PAGE: MovieInfoPage(
                self.__root, self.change_page_callback
            ),
            SIGNUP_PAGE: SignupPage(
                self.__root, self.change_page_callback
            ),
            LOGIN_PAGE: LoginPage(
                self.__root, self.change_page_callback
            ),
            USER_LIST_PAGE: UserListPage(
                self.__root, self.change_page_callback
            )
        }

        self.__pages[MAIN_PAGE].display()
        self.__pages[MAIN_PAGE].set_on_display(True)

        self.__root.mainloop()

        if os.path.exists(POSTERS_DIR):
            shutil.rmtree(POSTERS_DIR)

    def interrupt(self) -> None:
        print("terminate by ctrl c")
        self.__root.destroy()

    def check(self) -> None:
        self.__root.after(50, self.check)

    def change_page_callback(self, page_name: str, movie: Dict[str, Any] = None) -> None:
        self.__pages[store.curpage].set_on_display(False)

        if page_name == MOVIE_INFO_PAGE:
            page = cast(MovieInfoPage, self.__pages[MOVIE_INFO_PAGE])
            page.set_movie_and_display(movie)
        else:
            self.__pages[page_name].set_on_display(True)

        store.curpage = page_name

        for widget in self.__pages[page_name].get_page().winfo_children():
            widget.destroy()

        self.__pages[page_name].display()

        self.__navbar.display()


if __name__ == "__main__":
    print("getting trending movies")
    trending_movies = get_trending()
    for movie in trending_movies:
        movie[MOVIE_TITLE] = movie["title"] if "title" in movie else movie["name"]

    store.trending_movies = trending_movies
    store.curpage = MAIN_PAGE
    store.search_history.append(("", trending_movies))

    App()
