import tkinter as tk

from utils.utils import *
from .abc_page import Page


class MainPage(Page):
    def __init__(self, parent, trending_movies, on_display=False, *args, **kwargs):
        page = tk.Frame(parent, *args, **kwargs)
        page.pack(fill=tk.BOTH)
        super().__init__(on_display, page)

        bigFont = get_big_font()
        mediumFont = get_medium_font()
        smallFont = get_small_font()

        navbar = tk.Frame(page)
        navbar.pack(fill=tk.X)

        my_list_btn = MyButton(navbar, text="My List")
        my_list_btn.pack(side=tk.LEFT, padx=10)

        signup_btn = MyButton(navbar, text="Signup")
        signup_btn.pack(side=tk.RIGHT, padx=10)

        login_btn = MyButton(navbar, text="Login")
        login_btn.pack(side=tk.RIGHT)

        appName = MyHeading(page, text="Movie Tracker")
        appName.pack()

        searchbar = tk.Entry(page,
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

        trending_list_heading = MyHeading(page, text="Trending Movies")
        trending_list_heading.pack()

        trending_list_container = tk.Frame(page)
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

    def is_on_display(self):
        return super().is_on_display()

    def set_on_display(self, on_display: bool):
        super().set_on_display(on_display)
