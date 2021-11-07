import tkinter as tk
from tkinter.font import Font
import shutil
import signal

from tmdb_api.api import TheMovieDBAPI
from my_utils import *

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

        bigFont = get_big_font()
        mediumFont = get_medium_font()
        smallFont = get_small_font()

        navbar = tk.Frame(self.root)
        navbar.pack(fill=tk.X)

        myListBtn = tk.Button(navbar,
                              text="My List",
                              font=smallFont
                              )
        myListBtn.pack(side=tk.LEFT, padx=10)

        signupBtn = tk.Button(navbar,
                              text="Signup",
                              font=smallFont,
                              )
        signupBtn.pack(side=tk.RIGHT, pady=10, padx=10)

        loginBtn = tk.Button(navbar,
                             text="Login",
                             font=smallFont
                             )
        loginBtn.pack(side=tk.RIGHT, pady=10)

        appName = MyHeading(self.root,
                            text="Movie Tracker"
                            )
        appName.pack(pady=10)

        searchbar = tk.Entry(self.root,
                             bg="white",
                             fg="black",
                             width=30,
                             font=mediumFont,
                             insertbackground="gray",
                             )
        searchbar.insert(0, "Search for movies")
        searchbar.bind("<FocusIn>",
                       lambda _: searchbar.get() == "Search for movies" and searchbar.delete(0, tk.END)
                       )
        searchbar.bind("<FocusOut>",
                       lambda _:  len(searchbar.get()) == 0 and searchbar.insert(
                           0, "Search for movies")
                       )
        searchbar.pack(pady=20)

        trendingListHeading = MyHeading(self.root,
                                        text="Trending Movies"
                                        )
        trendingListHeading.pack(pady=10)

        trendingListContainer = tk.Frame(self.root)
        trendingListContainer.pack(pady=20)

        trendingList = tk.Listbox(trendingListContainer,
                                  font=mediumFont,
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
        trendingList.pack(side=tk.LEFT)

        for movie in trendingMovies:
            trendingList.insert(tk.END, movie)

        scrollbar = tk.Scrollbar(trendingListContainer)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        trendingList.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=trendingList.yview)

        self.root.mainloop()

        shutil.rmtree("posters")

    def interrupt(self):
        print("terminate by ctrl c")
        self.root.destroy()

    def check(self):
        self.root.after(50, self.check)


App()
