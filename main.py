from tkinter import Label, Tk
from PIL import ImageTk, Image
import os
import shutil
import signal
from typing import Any, Dict, cast

from tmdb_api.api import get_genre_list, get_trending, init_api
from db.db import init_db
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
        self.root = Tk()
        self.root.title("Movie Tracker")
        self.root.geometry("800x700")
        self.root.configure(bg=LIGHT_THEME_BG)
        self.root.focus()

        signal.signal(signal.SIGINT, lambda x, y: self.interrupt())

        self.root.after(50, self.check)

        self.navbar = MyNavbar(
            self.root, self.change_page_callback
        )
        self.navbar.pack()
        self.navbar.remove_btn(BACK_BTN)

        self.pages: Dict[str, Page] = {
            MAIN_PAGE: MainPage(
                self.root, self.change_page_callback
            ),
            MOVIE_INFO_PAGE: MovieInfoPage(
                self.root, self.change_page_callback
            ),
            SIGNUP_PAGE: SignupPage(
                self.root, self.change_page_callback
            ),
            LOGIN_PAGE: LoginPage(
                self.root, self.change_page_callback
            ),
            USER_LIST_PAGE: UserListPage(
                self.root, self.change_page_callback
            )
        }

        self.dark_img = ImageTk.PhotoImage(
            Image.open(
                os.path.join("images", "dark_theme.png")
            ).resize((75, 40), Image.ANTIALIAS)
        )
        self.light_img = ImageTk.PhotoImage(
            Image.open(
                os.path.join("images", "light_theme.png")
            ).resize((75, 40), Image.ANTIALIAS)
        )

        self.theme_btn = Label(
            self.root,
            image=self.light_img,
            bg=LIGHT_THEME_BG,
            cursor="hand2"
        )
        self.theme_btn.place(x=10, y=650)
        self.theme_btn.bind("<Button-1>", lambda _: self.toggle_theme())

        self.pages[store.curpage].set_on_display(True)

        self.root.mainloop()

        if os.path.exists(POSTERS_DIR):
            shutil.rmtree(POSTERS_DIR)

    def interrupt(self) -> None:
        print("terminate by ctrl c")
        self.root.destroy()

    def check(self) -> None:
        self.root.after(50, self.check)

    def change_page_callback(self, page_name: str, movie: Dict[str, Any] = None) -> None:
        self.theme_btn.place_forget()
        self.pages[store.curpage].set_on_display(False)
        store.curpage = page_name

        if page_name == MOVIE_INFO_PAGE:
            page = cast(MovieInfoPage, self.pages[MOVIE_INFO_PAGE])
            page.set_movie_and_display(movie)
        else:
            self.pages[page_name].set_on_display(True)

        self.navbar.display()
        self.theme_btn.place(x=10, y=650)

    def toggle_theme(self) -> None:
        if store.theme[FG] == LIGHT_THEME_FG:
            store.theme[FG] = DARK_THEME_FG
            store.theme[BG] = DARK_THEME_BG
            self.theme_btn.config(image=self.dark_img)
        else:
            store.theme[FG] = LIGHT_THEME_FG
            store.theme[BG] = LIGHT_THEME_BG
            self.theme_btn.config(image=self.light_img)

        self.root.config(bg=store.theme[BG])
        self.theme_btn.config(bg=store.theme[BG])
        if store.curpage == MOVIE_INFO_PAGE:
            page = cast(MovieInfoPage, self.pages[MOVIE_INFO_PAGE])
            self.change_page_callback(
                store.curpage, page.get_movie()
            )
        else:
            self.change_page_callback(store.curpage)


if __name__ == "__main__":
    store.init_store(get_trending(), get_genre_list())
    print("fetched trending movies")

    init_api()
    print("initialised API")

    init_db()
    print("initialised DB")

    App()
