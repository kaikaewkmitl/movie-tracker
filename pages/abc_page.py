from abc import ABC, abstractmethod
from tkinter import Frame, Misc
from tkinter.constants import BOTH
from typing import Callable, Optional


class Page(ABC):
    def __init__(self, parent: Misc,
                 change_page_callback: Callable[[str, str, Optional[int]], None]) -> None:
        self._on_display = False
        self._change_page_cb = change_page_callback
        self._page = Frame(parent)

    @abstractmethod
    def display(self) -> None:
        pass

    def set_on_display(self, on_display: bool) -> None:
        self._on_display = on_display
        if self._on_display:
            self._page.pack(fill=BOTH)
        else:
            self._page.pack_forget()
