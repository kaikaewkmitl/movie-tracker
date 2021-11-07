import tkinter as tk
from tkinter.font import Font
import shutil
import signal

from tmdb_api.api import TheMovieDBAPI
from pages.main_page import MainPage

tmdb_api = TheMovieDBAPI()

print("getting treding movies...")
movies = tmdb_api.get_trending()

trendingMovies = [movie['title'] if 'title' in movie else movie['name']
                  for movie in movies]

# test downloading image from internet
# print("downloading poster...")
# tmdb_api.get_poster(movies[0]["poster_path"])


class App:
    def __init__(self):
        print("creating an app...")

        self.root = tk.Tk()
        self.root.title("movie tracker")
        self.root.geometry("800x800")

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.root.after(50, self.check)

        current_page = MainPage(self.root, trendingMovies)
        current_page.pack(fill=tk.BOTH)
        current_page.tkraise()

        self.root.mainloop()

        shutil.rmtree("posters")

    def interrupt(self):
        print("terminate by ctrl c")
        self.root.destroy()

    def check(self):
        self.root.after(50, self.check)


App()
