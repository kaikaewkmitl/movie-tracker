import tkinter as tk

from .abc_page import Page
from utils.utils import MyHeading


class MovieInfoPage(Page):
    def __init__(self, parent: tk.Misc, on_display: bool = False,
                 *args, **kwargs) -> None:
        page = tk.Frame(parent, *args, **kwargs)
        super().__init__(on_display, page)

        test = MyHeading(page, text="TESTING")
        test.pack()

    def set_on_display(self, on_display: bool) -> None:
        return super().set_on_display(on_display)

    def is_on_display(self) -> bool:
        return super().is_on_display()
