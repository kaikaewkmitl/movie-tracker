import tkinter as tk
from tkinter.font import Font
import shutil
import signal

from tmdb_api.api import TheMovieDBAPI

tmdb_api = TheMovieDBAPI()
movies = tmdb_api.get_trending()

# test downloading image from internet
tmdb_api.get_poster(movies[0]["poster_path"])


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("movie tracker")
        self.root.geometry("800x800")

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.root.after(50, self.check)

        myFont = Font(
            family="Helvetica",
            size=25,
            weight="bold"
        )

        appName = tk.Label(self.root,
                           text="Movie Tracker",
                           font=myFont
                           )
        appName.pack(pady=10)

        searchbar = tk.Entry(self.root,
                             bg="white",
                             width=30,
                             fg="black",
                             font=myFont,
                             insertbackground="gray"
                             )
        searchbar.insert(0, "Search for movies")
        searchbar.bind("<FocusIn>",
                       lambda _: searchbar.get() == "Search for movies" and searchbar.delete(0, tk.END)
                       )
        searchbar.bind("<FocusOut>",
                       lambda _:  len(searchbar.get()) == 0 and searchbar.insert(
                           0, "Search for movies")
                       )
        searchbar.pack()

        frame1 = tk.Frame(self.root)
        frame1.pack(pady=10)

        myList = tk.Listbox(frame1,
                            font=myFont,
                            width=30,
                            height=5,
                            bg="white",
                            bd=0,
                            fg="blue",
                            highlightthickness=0,
                            selectbackground="black",
                            activestyle="none"
                            )
        myList.pack(side=tk.LEFT)

        trendingList = [movie['title'] if 'title' in movie else movie['name']
                        for movie in movies]
        for movie in trendingList:
            myList.insert(tk.END, movie)

        scrollbar = tk.Scrollbar(frame1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        myList.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=myList.yview)

        self.root.mainloop()
        shutil.rmtree("posters")

    def interrupt(self):
        print("terminate by ctrl c")
        self.root.destroy()

    def check(self):
        self.root.after(50, self.check)


App()
