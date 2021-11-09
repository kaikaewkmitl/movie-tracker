from tkinter import Tk, Frame, LEFT, RIGHT, X
import shutil
import signal
from typing import Dict, cast

from tmdb_api.api import get_trending
from utils.my_widgets import MyButton, MyNavbar
from pages.abc_page import Page
from pages.main_page import MainPage
from pages.movie_info_page import MovieInfoPage
from utils.const import *


class App:
    def __init__(self) -> None:
        print("creating an app...")
        self.__root = Tk()
        self.__root.title("movie tracker")
        self.__root.geometry("800x650")

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.__root.after(50, self.check)

        self.__navbar = MyNavbar(self.__root, self.change_page_callback)
        self.__navbar.pack()

        self.__pages: Dict[str, Page] = {
            MAIN_PAGE: MainPage(
                self.__root, self.change_page_callback, trending_movies
            ),
            MOVIE_INFO_PAGE: MovieInfoPage(
                self.__root, self.change_page_callback
            )
        }

        self.__pages[MAIN_PAGE].set_on_display(True)

        self.__curpage = MAIN_PAGE

        self.__root.mainloop()

        shutil.rmtree(POSTERS_DIR)

    def interrupt(self) -> None:
        print("terminate by ctrl c")
        self.__root.destroy()

    def check(self) -> None:
        self.__root.after(50, self.check)

    # def change_page_callback(self, page_name: str, i: int = -1) -> None:
    #     for k, v in self.__pages.items():
    #         if k == page_name:
    #             if k == MOVIE_INFO_PAGE:
    #                 v = cast(MovieInfoPage, v)
    #                 v.set_movie_and_display(trending_movies[i])
    #             else:
    #                 v.set_on_display(True)

    #             if k == MAIN_PAGE:
    #                 self.__navbar.remove_back_btn()
    #             else:
    #                 self.__navbar.display_back_btn()
    #         else:
    #             v.set_on_display(False)

    def change_page_callback(self, page_name: str, i: int = -1) -> None:
        self.__pages[self.__curpage].set_on_display(False)
        if page_name == MOVIE_INFO_PAGE:
            page = cast(MovieInfoPage, self.__pages[MOVIE_INFO_PAGE])
            page.set_movie_and_display(trending_movies[i])
        else:
            self.__pages[page_name].set_on_display(True)

        self.__curpage = page_name


if __name__ == "__main__":
    print("getting treding movies...")
    trending_movies = get_trending()
    for movie in trending_movies:
        movie[MOVIE_TITLE] = movie["title"] if "title" in movie else movie["name"]

    App()
