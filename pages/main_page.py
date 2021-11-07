import tkinter as tk

from utils.utils import *


class MainPage(tk.Frame):
    def __init__(self, master, trending_movies, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        bigFont = get_big_font()
        mediumFont = get_medium_font()
        smallFont = get_small_font()

        navbar = tk.Frame(self)
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

        appName = MyHeading(self,
                            text="Movie Tracker"
                            )
        appName.pack(pady=10)

        searchbar = tk.Entry(self,
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

        trending_list_heading = MyHeading(self,
                                          text="Trending Movies"
                                          )
        trending_list_heading.pack(pady=10)

        trending_list_container = tk.Frame(self)
        trending_list_container.pack(pady=20)

        trending_list = tk.Listbox(trending_list_container,
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
        trending_list.pack(side=tk.LEFT)

        for movie in trending_movies:
            trending_list.insert(tk.END, movie)

        scrollbar = tk.Scrollbar(trending_list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        trending_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=trending_list.yview)
