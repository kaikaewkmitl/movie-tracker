from tkinter import Tk
import shutil
import signal
from typing import Dict, cast

from tmdb_api.api import TheMovieDBAPI
from pages.abc_page import Page
from pages.main_page import MainPage
from pages.movie_info_page import MovieInfoPage
from utils.const import *

tmdb_api = TheMovieDBAPI()

print("getting treding movies...")
trending_movies = tmdb_api.get_trending()
for movie in trending_movies:
    movie[MOVIE_TITLE] = movie["title"] if "title" in movie else movie["name"]


# test downloading image from internet
# print("downloading poster...")
# tmdb_api.get_poster(movies[0]["poster_path"])


class App:
    def __init__(self) -> None:
        print("creating an app...")

        self.__root = Tk()
        self.__root.title("movie tracker")
        self.__root.geometry("800x800")

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.__root.after(50, self.check)

        self.__pages: Dict[str, Page] = {
            MAIN_PAGE: MainPage(
                self.__root, trending_movies, self.change_page_callback
            ),
            MOVIE_INFO_PAGE: MovieInfoPage(
                self.__root, self.change_page_callback
            )
        }

        self.__pages[MAIN_PAGE].set_on_display(True)

        self.__root.mainloop()

        shutil.rmtree("posters")

    def interrupt(self) -> None:
        print("terminate by ctrl c")
        self.__root.destroy()

    def check(self) -> None:
        self.__root.after(50, self.check)

    def change_page_callback(self, page_name: str, i: int = -1):
        for k, v in self.__pages.items():
            if k == page_name:
                if k == MOVIE_INFO_PAGE:
                    v = cast(MovieInfoPage, v)
                    v.set_movie_and_display(trending_movies[i])
                else:
                    v.set_on_display(True)
            else:
                v.set_on_display(False)


App()
