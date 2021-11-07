import tkinter as tk
import shutil
import signal

from tmdb_api.api import TheMovieDBAPI
from pages.main_page import MainPage

tmdb_api = TheMovieDBAPI()

print("getting treding movies...")
movies = tmdb_api.get_trending()

trending_movies = [movie['title'] if 'title' in movie else movie['name']
                   for movie in movies]

# test downloading image from internet
# print("downloading poster...")
# tmdb_api.get_poster(movies[0]["poster_path"])


class App:
    def __init__(self):
        print("creating an app...")

        self.__root = tk.Tk()
        self.__root.title("movie tracker")
        self.__root.geometry("800x800")

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.__root.after(50, self.check)

        current_page = MainPage(self.__root, trending_movies)
        # current_page.pack(fill=tk.BOTH)
        # current_page.tkraise()

        self.__root.mainloop()

        shutil.rmtree("posters")

    def interrupt(self):
        print("terminate by ctrl c")
        self.__root.destroy()

    def check(self):
        self.__root.after(50, self.check)


App()
