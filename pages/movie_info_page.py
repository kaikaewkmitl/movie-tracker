from tkinter import Misc, Frame
from typing import Any, Callable, Dict

from .abc_page import Page
from utils.my_widgets import MyHeading
from utils.const import *


class MovieInfoPage(Page):
    def __init__(self, parent: Misc, change_page_callback: Callable[[str], None],
                 on_display: bool = False) -> None:
        self.__movie: Dict[str, Any] = {}
        super().__init__(on_display, parent, change_page_callback)

    def display(self) -> None:
        page = self.get_page()
        movie_title = MyHeading(page, text=f"{self.__movie[MOVIE_TITLE]}")
        movie_title.pack()

    def set_movie_and_display(self, movie: Dict[str, Any]) -> None:
        self.__movie = movie
        self.set_on_display(True)
