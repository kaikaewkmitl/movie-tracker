from tkinter import Tk
import shutil
import signal
from typing import List

from tmdb_api.api import TheMovieDBAPI
from pages.abc_page import Page
from pages.main_page import MainPage
from pages.movie_info_page import MovieInfoPage

tmdb_api = TheMovieDBAPI()

print("getting treding movies...")
movies = tmdb_api.get_trending()

trending_movies: List[str] = [movie['title'] if 'title' in movie else movie['name']
                              for movie in movies]

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

        self.__pages: List[Page] = [
            MainPage(self.__root, trending_movies),
            MovieInfoPage(self.__root)
        ]

        self.__pages[0].set_on_display(True)

        self.__root.mainloop()

        shutil.rmtree("posters")

    def interrupt(self) -> None:
        print("terminate by ctrl c")
        self.__root.destroy()

    def check(self) -> None:
        self.__root.after(50, self.check)


App()
