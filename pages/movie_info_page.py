from tkinter import Misc, Frame
from typing import Callable

from .abc_page import Page
from utils.my_widgets import MyHeading


class MovieInfoPage(Page):
    def __init__(self, parent: Misc, callback: Callable[[str], None],
                 on_display: bool = False, *args, **kwargs) -> None:
        page = Frame(parent, *args, **kwargs)
        super().__init__(on_display, page)

        test = MyHeading(page, text="TESTING")
        test.pack()

    def set_on_display(self, on_display: bool) -> None:
        return super().set_on_display(on_display)

    def is_on_display(self) -> bool:
        return super().is_on_display()
